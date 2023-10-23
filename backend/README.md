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

