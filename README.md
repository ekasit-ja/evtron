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
8. create service file at `/etc/systemd/system/uwsgi.service` to enable us to use command `service uwsgi restart`. This service file will run uWSGI in emperor mode. (Emperor mode means uWSGI will restart automatically when initial file is modified.). Paste below code into the file.
```
[Unit]
Description=uWSGI service (in emporer mode) for www.pcjindustries.co.th run by Django

[Service]
ExecStartPre=/bin/bash -c 'mkdir -p /run/uwsgi; chown root:root /run/uwsgi'
ExecStart=/usr/local/bin/uwsgi --emperor /home/ekasit/pcj-django/site/pcj.ini
Restart=always
KillSignal=SIGQUIT
Type=notify
NotifyAccess=all

[Install]
WantedBy=multi-user.target
```
9. execute `systemctl daemon-reload` to inform system there is change from service files
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
    server_name    pcjindustries.co.th www.pcjindustries.co.th server.pcjindustries.co.th;

    access_log     /home/ekasit/pcj-django/site/access.log;
    error_log      /home/ekasit/pcj-django/site/error.log;

    location = favicon.ico { access_log off; log_not_found off; }
    location /static/ {
        alias /home/ekasit/pcj-django/static/;
    }

    location /media/ {
        alias /home/ekasit/pcj-django/upload/;
    }

    location / {
        include uwsgi_params;
        uwsgi_pass unix:/home/ekasit/pcj-django/site/tutorial.sock;
    }
}
```
13. check syntax with `nginx -t`
14. restart service to apply changes by `service nginx restart && service uwsgi restart`
15. browse to website to check if it is working

at this point, we can use `service [nginx, uwsgi] [start, stop, restart]`

---
