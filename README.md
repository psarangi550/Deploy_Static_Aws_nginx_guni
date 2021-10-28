# Deploy_Static_Aws_nginx_guni

## Deployement Help for Aws_Using nginx webserver , gunicorn wsgi file , supervisor bash to run gunicorn on background over IAM AWS EC2 instance using AWS ubuntu AMI Image

> first thing first remember that all need to be done in side your django_project folder and make sure All actvity need to be done unde the virtual enviroment on 
>
> ####  Step:1-Update the package index
> sudo apt update
> #### Step:2:- first install nginx
> sudo apt-get install nginx -->it will be downloaded where home parent folder present etc/nginx 
> By default nginx uses port 80 you can see that by going /etc/nginx/sites-enable/default and running "cat" command on the Same 
>so on you ec2 instance make sure to open port number 80 by going to security group and edit the inbound rules as suctom tcp port 80 and source anywhere ip4
>#### step:-3:-you can start,reload and stop the nginx by using 
>sudo systemctl start nginx
>sudo systemctl stop nginx
>sudo systemctl reload nginx
>now you can check nginx homepage been coming up or not by opening ip public dns of EC2 instance
>##### step:-4-You can then clone your repo 
>for that you have to use git clone < your .git github remote repo ** go to the folder ** 
>#### step:-5 go to the clonefolder (if not)where manage.py present and install the python3-pip,python3-virtualenv or python3-venv module
>sudo apt install python3-pip
>sudo apt install python3-virtualenv
>sudo apt install python3-venv if not using virtualenv
>#### step:-6 to create a vitual env inside the git clone folder and make it on all the time as it will redirect to gunicorn location and then  install  requirements.txt which will be inside the virtual environment so that  gunicorn django must be present in virtual env 
>in order to activate you can either use virtualenv env(folder)
>or python3 -m venv env
>to activate both  source env/bin/activate
>once activated install the requirement.txt by pip3 install -r requirements.txt
>#### Step:-7 Now we have to install the supervisor to run the gunicorn wsgi on the backgroud
>sudo apt-get install supervisor 
>it will be installed it will be downloaded where home parent folder present etc/supervisor
>#### step:-8 now on the while on virtualenv on run the gunicorn using on port 9090(or any port) but make sure to open the port as custom tcp and source as anywhere from EC2 Security group
>for running the gunicorn on a port use 
>gunicorn --bind 0.0.0.0:9090 App_name.wsgi:application #to check if there is any problem
>check by goint to EC2 instance ip4 dns with port number on your browser
>here gunicorn running on a port but we want to run gunicorn on a unix socket to which nginx webserver cqan send the request 
>stop once validate
>#### step-9:-now go to /etc/supervisor/conf.d/ and create a gunicorn configuration file which will be run by supervisor bash
>/etc/supervisor/conf.d/ -->here create a gunicorn.cong file as sudo touch gunicorn.conf
>open that with nano editor as sudo nano  gunicorn.conf
>now edit it as below : -make the virtual env on
>here repo name means where manage.py present

-----------------------------
[program:gunicorn]
directory=/home/ubuntu/Repository_name
command=/home/ubuntu/Repository_name/env/bin/gunicorn --workers 3 --bind unix:/home/ubuntu/Repository_name/app.sock App_name.wsgi:application
autostart=true
autorestart=true
stderr_logfile=/var/log/gunicorn/gunicorn.err.log
stdout_logfile=/var/log/gunicorn/gunicorn.out.log

[group:guni]
programs:gunicorn

-----------------------------

>#### step:-10:- now check whether superbisor can read,update and whats the status , the status must be running but you must be on /etc/supervisor/conf.d/ 

>sudo supervisorctl reread
>sudo supervisorctl update
>sudo supervisorctl status
>if need you can also reload by using sudo supervisorctl reload

> #### step:-11:-now you can go to /etc/nginx/sites-available to tell nginx to sent request to unix socket which gunicorn can read and provide response from django wsgi file 
>for that go to  /etc/nginx/sites-available
>sudo touch django.conf:-to create the config file
>sudo nano django.conf :-to open the configuration file

-----------------------------
server {
	listen 80;
	server_name your_ip your_url/ec2 instance name;
	
	location / {
		include proxy_params;
		proxy_pass http://unix:/home/ubuntu/Repository_name/app.sock;
	}
	location /static {
		autoindex on;
		alias /home/ubuntu/Repository_name/static/; #where your static folder  
	}
	}

--------------

> #### in case you are getting server_bucketsize issue then:-

>cd /etc/nginx
>sudo nano nginx.conf #change the "server_names_hash_bucket_size 64;" to "server_names_hash_bucket_size 128;"

>sudo ln django.conf /etc/nginx/sites-enabled/ :-to tell sites enable about the new django configuration 

>To restart the ngin please use below commnd

>sudo nginx -t
>sudo service nginx restart
>deactivate:-this is optional
>sudo supervisorctl reload
>sudo systemctl reload nginx
>sudo systemctl start nginx
>sudo nginx -t
