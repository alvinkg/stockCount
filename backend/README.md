# VIRTUAL ENVIRONMENT

The virtual environment for this python app is using a directory 'react-flask-jwt' in the main folder REACT-FLASK-JWT

The command is: $ source react-flask-jwt/bin/activate

## Flask Migrate

## Install python-dotenv

alvinlim@coolhandsg-iMac backend % pip install python-dotenv

## Need to focus effort on SQLAlchemy ORM

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    content = db.Column(db.Text)
    comments = db.relationship('Comment', backref='post')

    def __repr__(self):
        return f'<Post "{self.title}">'


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))

    def __repr__(self):
        return f'<Comment "{self.content[:20]}...">'

## for the dotenv variables

added a new file .env-localDO

## 23 Oct 2023 install in konvergentgroup

alvin@konvergent01:~$ git clone https://github.com/alvinkg/stockCount.git
Resolving deltas: 100% (179/179), done.

[How To Serve Flask Applications with Gunicorn and Nginx on Ubuntu 20.04](https://www.digitalocean.com/community/tutorials/how-to-serve-flask-applications-with-gunicorn-and-nginx-on-ubuntu-20-04)

## update and install python packages

alvin@konvergent01:~$ sudo apt update
Reading state information... Done
1 package can be upgraded. Run 'apt list --upgradable' to see it.
alvin@konvergent01:~$ sudo apt install python3-pip python3-dev build-essential libssl-dev libffi-dev python3-setuptools
0 upgraded, 0 newly installed, 0 to remove and 1 not upgraded.

## cd to stockCount

alvin@konvergent01:~$ ls
myproject  om_account_accountant-15.0.6.3.0.zip  stockCount  website1
alvin@konvergent01:~$ cd stockCount

## make venv

alvin@konvergent01:~/stockCount$ sudo apt install python3-venv
python3-venv is already the newest version (3.8.2-0ubuntu2).

## create venv
alvin@konvergent01:~/stockCount/backend$ python3 -m venv venv --prompt="stockCount"
Error: [Errno 2] No such file or directory: '/home/alvin/stockCount/backend/venv/bin/python3'
=> alvin@konvergent01:~/stockCount/backend$ rm -rf venv

alvin@konvergent01:~/stockCount/backend$ python3 -m venv venv --prompt="stockCount"
alvin@konvergent01:~/stockCount/backend$ ls
 README.md  'app copy.py'   app_Mac2DO.py   app_Mac2Mac.py   app_localDO.py   app_remote.py   models.py   models_DO.py   requirements.txt   venv   wsgi.py

alvin@konvergent01:~/stockCount/backend$ source venv/bin/activate
(stockCount) alvin@konvergent01:~/stockCount/backend$

## install wheel

(stockCount) alvin@konvergent01:~/stockCount/backend$ pip install wheel
Collecting wheel
  Using cached wheel-0.41.2-py3-none-any.whl (64 kB)
Installing collected packages: wheel
Successfully installed wheel-0.41.2

## install gunicorn & flask
(stockCount) alvin@konvergent01:~/stockCount/backend$ pip install gunicorn flask

## install python-dotenv
(stockCount) alvin@konvergent01:~/stockCount/backend$ pip install python-dotenv

## create a local var file
(stockCount) alvin@konvergent01:~/stockCount/backend$ touch .env-localDO

## install python packages in requirements.txt
(stockCount) alvin@konvergent01:~/stockCount/backend$ pip install -r requirements.txt

## setup postgresql
### setup dB alvin
using Note 7 Oct 2023 (2)

(stockCount) alvin@konvergent01:~/stockCount/backend$ \psql
psql: error: FATAL:  role "alvin" does not exist

## change user to default super user postgres
(stockCount) alvin@konvergent01:~/stockCount/backend$ sudo -i -u postgres

## login to postgresql as postgres 
postgres@konvergent01:~$ \psql
psql (12.16 (Ubuntu 12.16-0ubuntu0.20.04.1))
Type "help" for help.

postgres=# 

## list dB and owners
postgres=# \l
                              List of databases
   Name    |  Owner   | Encoding | Collate |  Ctype  |   Access privileges   
-----------+----------+----------+---------+---------+-----------------------
 odoo15    | odoo15   | UTF8     | C       | C.UTF-8 | 
 postgres  | postgres | UTF8     | C.UTF-8 | C.UTF-8 | 
 template0 | postgres | UTF8     | C.UTF-8 | C.UTF-8 | =c/postgres          +
           |          |          |         |         | postgres=CTc/postgres
 template1 | postgres | UTF8     | C.UTF-8 | C.UTF-8 | =c/postgres          +
           |          |          |         |         | postgres=CTc/postgres

## list users / roles
postgres=# \du
                                   List of roles
 Role name |                         Attributes                         | Member of 
-----------+------------------------------------------------------------+-----------
 odoo15    | Superuser, Create role, Create DB                          | {}
 postgres  | Superuser, Create role, Create DB, Replication, Bypass RLS | {}

# create new SUPER USER alvin
postgres=# CREATE USER alvin SUPERUSER;
CREATE ROLE

# Add password to USER alvin for login purposes
postgres=# \password alvin
Enter new password for user "alvin": 
Enter it again: 
postgres=# 
password = 'alvin'

# CREATE DATABASE 'alvin'
postgres=# CREATE DATABASE alvin OWNER alvin;
CREATE DATABASE

postgres=# \l

                              List of databases
   Name    |  Owner   | Encoding | Collate |  Ctype  |   Access privileges   
-----------+----------+----------+---------+---------+-----------------------
 alvin     | alvin    | UTF8     | C.UTF-8 | C.UTF-8 | 
 odoo15    | odoo15   | UTF8     | C       | C.UTF-8 | 
 postgres  | postgres | UTF8     | C.UTF-8 | C.UTF-8 | 
 template0 | postgres | UTF8     | C.UTF-8 | C.UTF-8 | =c/postgres          +
           |          |          |         |         | postgres=CTc/postgres
 template1 | postgres | UTF8     | C.UTF-8 | C.UTF-8 | =c/postgres          +

## login as user alvin
unable to logout in the ubuntu env as postgres
not needed just => postgres@konvergent01:~$ exit
before logout create db 'alvin'

(stockCount) alvin@konvergent01:~/stockCount/backend$ \psql
psql: error: FATAL:  database "alvin" does not exist

(stockCount) alvin@konvergent01:~/stockCount/backend$ \psql
psql (12.16 (Ubuntu 12.16-0ubuntu0.20.04.1))
Type "help" for help.

alvin=# 

## setup a port 

(stockCount) alvin@konvergent01:~/stockCount/backend$ python app_localDO.py
True
url: postgresql://alvin:alvin@localhost/alvin
 * Serving Flask app 'app_localDO'
 * Debug mode: on
Address already in use
Port 5000 is in use by another program. Either identify and stop that program, or start the server with a different port.

### change the port of myproject.py
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000)
    
    may want to remove the debug=True and
    make the production app
    
# create wsgi.py endpoint
from app_localDO import app

if __name__ == "__main__":
	app.run()

# test guicorn on wsgi.py
^X^C(stockCount) alvin@konvergent01:~/stockCount/backend$ gunicorn --bind 0.0.0.0:5000 wsgi:app
[2023-10-23 05:51:58 +0000] [133425] [INFO] Starting gunicorn 21.2.0
[2023-10-23 05:51:58 +0000] [133425] [INFO] Listening at: http://0.0.0.0:5000 (133425)
[2023-10-23 05:51:58 +0000] [133425] [INFO] Using worker: sync
[2023-10-23 05:51:59 +0000] [133427] [INFO] Booting worker with pid: 133427

{"message":"success"}

# make systemd service file'
alvin@konvergent01:~/stockCount/backend$ sudo nano /etc/systemd/system/app_localDO.service

[Unit]
Description=Gunicorn instance to serve stockCount/backend
After=network.target

[Service]
User=alvin
Group=www-data
WorkingDirectory=/home/alvin/stockCount/backend
Environment="PATH=/home/alvin/stockCount/backend/venv/bin"
ExecStart=/home/alvin/stockCount/backend/venv/bin/gunicorn --workers 3 --bind unix:app_localDO.sock -m 007 wsgi:app

[Install]
WantedBy=multi-user.target

alvin@konvergent01:~/stockCount/backend$ sudo systemctl start app_localDO
alvin@konvergent01:~/stockCount/backend$ sudo systemctl enable app_localDO
Created symlink /etc/systemd/system/multi-user.target.wants/app_localDO.service → /etc/systemd/system/app_localDO.service.

# status service
alvin@konvergent01:~/stockCount/backend$ sudo systemctl status app_localDO
● app_localDO.service - Gunicorn instance to serve stockCount/backend
     Loaded: loaded (/etc/systemd/system/app_localDO.service; enabled; vendor preset: enabled)
     Active: active (running) since Mon 2023-10-23 05:57:50 UTC; 1min 2s ago
   Main PID: 133585 (gunicorn)
      Tasks: 4 (limit: 2323)



alvin@konvergent01:/etc/nginx/sites-available$ sudo nano konvergentgroup.com
alvin@konvergent01:/etc/nginx/sites-available$ sudo nginx -t
nginx: the configuration file /etc/nginx/nginx.conf syntax is ok
nginx: configuration file /etc/nginx/nginx.conf test is successful
alvin@konvergent01:/etc/nginx/sites-available$ sudo systemctl restart nginx
    
