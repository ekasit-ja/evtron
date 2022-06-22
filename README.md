### test evtron

for development on Windows environments, **Git Bash** originally does not reply verbose feedback text. We need to use `vim .bahsrc` and add code `alias python='winpty python.exe'` then save it and restart **Git Bash** 2 times.

### Development
for this development, we cannot use command `source bin/activate` for virtual environment.  Instead, command `source venv/Scripts/activate` has to be executed. (not sure why this change. but on CestOS server, command `source venv/bin/activate` is still valid though.)

---

### Preparation for deployment
**Create project folder in `/home/ekasit` (same folder as main pcj website).
1. First of all, create project folder with `mkdir pcjevtron && cd pcjevtron`
2. execute `mkdir source static upload site`
   - if this is first run, install python virtual environment executing `pip3 install virtualenv`
   - also copy everything into `upload` folder.  We use SQLite database so the data is already in repository.
3. execute `virtualenv -p python3 venv` to create python virtual environment
4. then `source venv/bin/activate`
5. then `cd source`
   - if this is first run, execute `git clone https://github.com/ekasit-ja/evtron.git .` to clone source code first
   - then execute `pip3 install -r pip_packages.txt` to install all required packages
   - follow this [website](`https://sourceexample.com/en/1c4153d4c3d4e65dac45/`) to install newer version of SQLite and let uWSGI links with SQLite newer version.
   - then execute `python3 manage.py collectstatic` to gather all static files and put them into `static` folder
6. then `python3 manage.py runserver 0.0.0.0:8000`. Access website with ip address directly to check everything.  Note that this is remotely access to server.  127.0.0.1:8000 is **NOT** remotely accessible.

**Note that video elements are all non-seekable on Django development environment**

### Working with CLI
Note that Django is **NOT** working when we put the process into background.

---

## Deployment
1. `deactivate` virtual environment first
2. We install uWSGI globally with `pip3 install uwsgi`
3. create file `pcjevtron.ini` (uWSGI initial file) in folder `site`
4. paste below configuration in the file
```
[uwsgi]
home = /home/ekasit/pcjevtron/venv
chdir = /home/ekasit/pcjevtron/source
wsgi-file = /home/ekasit/pcjevtron/source/evtron/wsgi.py

http = 0.0.0.0:8000
#socket = /home/ekasit/pcjevtron/site/tutorial.sock
#vacuum = true
#chown-socket = root:root
#chmod-socket = 666
#listen = 512
```
5. execute `sysctl -w net.core.somaxconn=512` to increase system request size (this is a test to fix 502 error when server is on for a long period of time) and add `net.core.somaxconn=512` to file `/etc/sysctl.conf` for permanent change the request size
6. execute `uwsgi pcjevtron.ini` and browse website to check if it is working or not. (static files will not be served at this point)
7. if everything is fine, comment line `http = 0.0.0.0:8000` and remove comment from the rest




8. create service file at `/etc/systemd/system/uwsgi2.service` to enable us to use command `service uwsgi2 restart`. This service file will run uWSGI in emperor mode. (Emperor mode means uWSGI will restart automatically when initial file is modified.). Paste below code into the file.
```
[Unit]
Description=uWSGI service (in emporer mode) for www.pcjevtron.com run by Django

[Service]
ExecStartPre=/bin/bash -c 'mkdir -p /run/uwsgi; chown root:root /run/uwsgi'
ExecStart=/usr/local/bin/uwsgi --emperor /home/ekasit/pcjevtron/site/pcjevtron.ini
Restart=always
KillSignal=SIGQUIT
Type=notify
NotifyAccess=all

[Install]
WantedBy=multi-user.target
```
9. execute `systemctl daemon-reload` to inform system there is change from service files

---
### Noted that if we already deployed PCJ INDUSTRIES website before, skip step 10-11 and add directive `server {...}` from step 12 instead of editing existing one.
---

10. install NGINX with `yum install nginx`
11. configure NGINX at `/etc/nginx/nginx.conf` by comment server directive (see below)
```
...
    include /etc/nginx/conf.d/*.conf;

#    server {
#        listen       80 default_server;
#        listen       [::]:80 default_server;
#        ...
#    }
...
```
12. then add below code instead
```
server {
    # allow upload file as large up to 10M #
    client_max_body_size 10M;
    listen 80;

    server_name    pcjevtron.com www.pcjevtron.com;

    access_log     /home/ekasit/pcjevtron/site/access.log;
    error_log      /home/ekasit/pcjevtron/site/error.log;

    location = favicon.ico { access_log off; log_not_found off; }
    location /static/ {
        alias /home/ekasit/pcjevtron/static/;
    }

    location /media/ {
        alias /home/ekasit/pcjevtron/upload/;
    }

    location /.well-known/ {
        alias /home/ekasit/pcjevtron/.well-known/;
    }

    location / {
        include uwsgi_params;
        uwsgi_pass unix:/home/ekasit/pcjevtron/site/tutorial.sock;
    }
}
```
13. check syntax with `nginx -t`
14. restart service to apply changes by `service nginx restart && service uwsgi2 restart`
15. browse to website to check if it is working

at this point, we can use `service [nginx, uwsgi2] [start, stop, restart]`

---

### Set up auto-start at boot
1. execute `systemctl enable uwsgi2.service nginx`
2. then `reboot` to restart server
3. then `service nginx status` and `service uwsgi2 status` and browse to the website to check if everything is working.

---





















### SSL for https
We will use **certbot** software to handle **Let’s Encrypt** certificate automatically.
1. install certbot by executing `yum install certbot python2-certbot-nginx`
2. then `certbot --nginx` to let certbot configure NGINX automatically
3. certbot will put check key on `/root/static` by default (called webroot-path). However, we do not let nginx have root access.  So we have to change webroot-path by `certbot certonly --webroot -w /home/ekasit/pcjevtron -d www.pcjevtron.com,pcjevtron.com` then choose option 2 (renew and replace cert) (use only 1 -d to create just 1 domain for all 3 addresses. There should be only 1 certificate folder which is `www.pcjevtron.com`)
4. we have to force all `non-www` to `www` as well as provide `.well-known` path by changing below
```
location / {
    include uwsgi_params;
    uwsgi_pass unix:/home/ekasit/pcjevtron/site/tutorial.sock;
}
```
to
```
location / {
    include uwsgi_params;
    uwsgi_pass unix:/home/ekasit/pcjevtron/site/tutorial.sock;
}

if ($host = server.pcjevtron.com) {
    return 301 https://www.pcjevtron.com$request_uri;
} # managed by Certbot

if ($host = pcjevtron.com) {
    return 301 https://www.pcjevtron.com$request_uri;
} # managed by Certbot

listen 443 ssl; # managed by Certbot
ssl_certificate /etc/letsencrypt/live/www.pcjevtron.com/fullchain.pem; # managed by Certbot
ssl_certificate_key /etc/letsencrypt/live/www.pcjevtron.com/privkey.pem; # managed by Certbot
include /etc/letsencrypt/options-ssl-nginx.conf; # managed by Certbot
ssl_dhparam /etc/letsencrypt/ssl-dhparams.pem; # managed by Certbot
```
5. comment out line `listen 80;` in main `server` directive
6. in server directive which listen to port 80, change
```
server {
if ($host = www.pcjindustries.co.th) {
    return 301 https://$host$request_uri;
} # managed by Certbot


if ($host = server.pcjindustries.co.th) {
    return 301 https://$host$request_uri;
} # managed by Certbot


if ($host = pcjindustries.co.th) {
    return 301 https://$host$request_uri;
} # managed by Certbot
```
to
```
if ($host = www.pcjevtron.com) {
    return 301 https://www.pcjevtron.com$request_uri;
} # managed by Certbot


if ($host = server.pcjevtron.com) {
    return 301 https://www.pcjevtron.com$request_uri;
} # managed by Certbot


if ($host = pcjevtron.com) {
    return 301 https://www.pcjevtron.com$request_uri;
} # managed by Certbot
```
7. restart NGINX with `service nginx restart` and execute `certbot renew --dry-run` to check if renewal succeed or not.
8. set job to auto-renew certificate by executing `crontab -e`. cronjob file will be opened
9. then put `0 4 2 * * /usr/bin/certbot renew >> /home/ekasit/pcj-django/site/renew_cert.log 2>&1` on the last line. (it means every month, on 2nd day at 04.00, execute `certbot renew` and log it in that file either output is normal or error)

---

### Auto restart service
After long period of deployment time, service alawys crashes for unknown reason.  Therefore, we need to restart service automatically by `crontab`.  Thus set up to restart the service daily.
1. Open file `/var/spool/cron/root`
2. add `0 4 * * * /home/ekasit/pcj-django/source/daily_restart.sh >> /home/ekasit/pcj-django/site/daily_restart.log 2>&1` on the last line
3. save the file
4. change permission of `daily_restart.sh` file in source code folder to 744 (executable by owner)

---

### Before signing off & Every later update
1. Do not forget to change `DEBUG=False` in `settings.py`
2. execute `python3 manange.py collectstatic` (under virtual environment) to collect all updated static files
3. and restart both services with `service nginx restart && service uwsgi restart`
