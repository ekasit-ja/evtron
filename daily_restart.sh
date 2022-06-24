/bin/systemctl restart nginx.service
/bin/systemctl restart uwsgi2.service
D=`date`
echo daily_restart from PCJ_EVTRON is executed at --- $D
