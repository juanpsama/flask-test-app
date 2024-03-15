# Implementación de una aplicación Flask en un servidor Ubuntu con Apache

[![en](https://img.shields.io/badge/lang-en-red.svg)](https://github.com/juanpsama/flask-test-app/blob/master/README.md)

Este documento describe los pasos para implementar esta aplicación Flask en UbuntuServer 22.04 LTS con Apache.

## Prerrequisitos

- UbuntuServer 22.04
- Aplicación Flask

## Paso 1: Instalación y configuración de Apache
- (Opcional) Primero necesitamos instalar un paquete ssh y ftp para conectarnos al servidor
- Instalar Apache y wsgi 
	- `sudo apt-get install apache2 libapache2-mod-wsgi-py3`
- Crear un nuevo archivo de configuración de Apache
	- `sudo nano /etc/apache2/sites-available/flaskapp.conf `  
	-  Pega el siguiente código en el archivo: 
		````<VirtualHost *:80>
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
</VirtualHost>`
- Habilitar la nueva configuración de Apache:
	- `sudo a2ensite flaskapp` 
- Deshabilitar la configuración predeterminada de Apache:
	- `sudo a2dissite 000-default`

## Paso 2: Configuración de MySQL para la base de datos
Instalar MySQL y pymysql como conector para usarlo con Flask:
- Instalar el servidor MySQL en ubuntu 
	- ` sudo apt install mysql-server`
	- `sudo apt install mysql-client`
- Configurar MySQL 
	- `sudo mysql_secure_instalation` 
- Cambiar la contraseña de root de mysql
	- `sudo mysql -u root`
	- `AlTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY '<your_password>'` 
- Crear la base de datos para el proyecto flask
	- `sudo mysql -u root -p`
	- `CREATE DATABASE <database_name>;`
- Instalar el conector pymysql para conectar mysql a la aplicacion en flask
	- `pip install pymysql`
	- `pip install cryptography`
## Paso 3: Configuración de la aplicación Flask
- Instalar Python 3 y pip:
	-`sudo apt-get install python3 python3-pip python3-venv` 
- Clonar este repositorio en /var/www/
	- `cd /var/www/`
	- `git clone https://github.com/juanpsama/flask-test-app.git`
- Crear un entorno virtual de python 
	-  `python3 -m venv venv`
- Activar el entorno virtual de python
	- `source venv/bin/activate` 
- Instalar todos los paquetes
	- `pip install -r requirements.txt`
- Cambiar el permiso en la carpeta del proyecto para permitirle escribir archivos en el directorio 'files'
	- `sudo chmod -R a+rw /var/www/flask-test-app/files/`
- Configurar las variables de entorno 
	- `export FLASK_KEY='<your_secret_key>'`
	-  `export DB_URL='mysql+pymysql://root:<db_password>@localhost/<db_name>'`
**Nota:** Deberías agregar un archivo .env para asegurar tus variables de entorno o codificar estas variables en el archivo main.py

**Finalmente** reiniciar Apache para desplegar la aplicación en flask
`sudo systemctl reload apache2`	

Acceder escribiendo la ip del servidor en el navegador
## Solución de problemas
Si ves un mensaje que dice "Internal Server Error" puedes ver los mensajes de error al final del archivo  
`/var/www/flask-test-app/logs/error.log`
Abre este archivo usando el editor nano:
`sudo nano /var/www/flask-test-app/logs/error.log`

---
**Fuentes:** 
- [How to Deploy a Flask App to Linux ](https://www.youtube.com/watch?v=w0QDAg85Oow)
- [How To Use MySQL Database With Flask](https://www.youtube.com/watch?v=w0QDAg85Oow)
- [Deploying Flask Application on Ubuntu](https://tecadmin.net/deploying-flask-application-on-ubuntu-apache-wsgi/)
- [INSTALAR MYSQL SERVER](https://www.youtube.com/watch?v=ACM8UvZqFOY)
