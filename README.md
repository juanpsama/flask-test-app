# Flask App Deployment on Ubuntu Server with Apache
[![es](https://img.shields.io/badge/lang-es-yellow.svg)](https://github.com/juanpsama/flask-test-app/blob/master/README.es.md)

This document describes the steps to deploy this Flask application on Ubuntu server 22.04 LTS with Apache.

## Prerequisites

- Ubuntu Server 22.04
- Flask application

## Step 1: Installing and Configuring Apache
- (Optional) First we need to install a ssh and ftp package to connect us to the server
- Install Apache and wsgi package 
	- `sudo apt-get install apache2 libapache2-mod-wsgi-py3`
- Create a new apache config file
	- `sudo nano /etc/apache2/sites-available/flaskapp.conf `  
	-  Paste the following code into the file: 
	- ```` 
		<VirtualHost *:80>
        ServerAdmin webmaster@localhost
        DocumentRoot /var/www/flask-test-app

        WSGIDaemonProcess flask-app user=www-data group=www-data threads=1
        WSGIScriptAlias / /var/www/flask-test-app/app.wsgi

        <Directory /var/www/flask-test-app>
             WSGIProcessGroup flask-app
             WSGIApplicationGroup %{GLOBAL}
             Order deny,allow
             Allow from all
        </Directory>

        ErrorLog /var/www/flask-test-app/logs/error.log
        CustomLog /var/www/flask-test-app/logs/access.log combined
		</VirtualHost>
- Enable the new Apache configuration:
	- `sudo a2ensite flaskapp` 
- Disable default Apache home configuration:
	- `sudo a2dissite 000-default`

## Step 2: Setting up MySQL for the database
Install MySQL and pymysql connector to use it with Flask:
- Install MySQL server on ubuntu 
	- ` sudo apt install mysql-server`
	- 	`sudo apt install mysql-client`
- Setup MySQL 
	- `sudo mysql_secure_instalation` 
- Change mysql root password
	- `sudo mysql -u root`
	- `AlTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY '<your_password>'` 
- Create database for the flask project
	- `sudo mysql -u root -p`
	- `CREATE DATABASE <database_name>;`
- Install pymysql connector to connect to the flask app
	- `pip install pymysql`
	- `pip install cryptography`
## Step 3: Setting Up the Flask Application
- Install Python 3 and pip:
	-`sudo apt-get install python3 python3-pip python3-venv` 
- Clone this repo into /var/www/
	- `cd /var/www/`
	- `git clone https://github.com/juanpsama/flask-test-app.git`
- Create a python venv 
	-  `python3 -m venv venv`
- Activate the python venv
	- `source venv/bin/activate` 
- Install all the packages
	- `pip install -r requirements.txt`
- Change the permission on project folder to allow it to write files in the files directory
	- `sudo chmod -R a+rw /var/www/flask-test-app/files/`
- Set up env variables 
	- `export FLASK_KEY='<your_secret_key>'`
	-  `export DB_URL='mysql+pymysql://root:<db_password>@localhost/<db_name>'`
**Note:** You should add a .env file to secure your env variables or hardcoding this variables into main.py file

**Finally** restart Apache to deploy your flask app
`sudo systemctl reload apache2`	

Access typing server ip into the browser
## Troubleshooting
If you see some "Internal Server Error" you can see error messages at the end of the file  
`/var/www/flask-test-app/logs/error.log`
Open this file using nano editor:
`sudo nano /var/www/flask-test-app/logs/error.log`

---
**Sources:** 
- [How to Deploy a Flask App to Linux ](https://www.youtube.com/watch?v=w0QDAg85Oow)
- [How To Use MySQL Database With Flask](https://www.youtube.com/watch?v=w0QDAg85Oow)
- [Deploying Flask Application on Ubuntu](https://tecadmin.net/deploying-flask-application-on-ubuntu-apache-wsgi/)
- [INSTALAR MYSQL SERVER](https://www.youtube.com/watch?v=ACM8UvZqFOY)

