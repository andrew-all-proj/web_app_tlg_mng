1. Создаем папку и копируем файлы flask 
	sudo mkdir /opt/manage_site
	
2. Создаем виртуальное окружение:
	- скачаваем иустанавливаем: 
	   sudo apt-get install virtualenv
	- Переходим в папку с сайтом и создаем виртульное окружение командой:
	    virtualenv -p python3 venv

3. Создаем файл запуска Flask экземпляра wsgi.py
	
	from flsite import app

	if __name__ == '__main__':
    		app.run()

4. Активируем виртуальное окружение:
	   source venv/bin/activate 
    - Установка Flask устанавливаем командой:
	   sudo pip install flask

    - Установка wsgi 
	   pip install gunicorn
	- Если нужно устанавливаем:
	   pip install flask_login
	- Проверка:
	   python3 wsgi.py
	- deactivate

5. Настройка автозапуска systemd: 
	- Создаем файл в каталоге /etc/systemd/system/
	    sudo nano /etc/systemd/system/manage_site.service
	- Настройки файла:
		[Unit]
		Description=Start manage_site
		After=network.target

		[Service]
		User=pi
		Group=www-data
		WorkingDirectory=/opt/manage_site
		Enviroment="PATH=/opt/manage_site/venv/bin"
		ExecStart=/opt/manage_site/venv/bin/gunicorn  --workers 5 --bind unix:gunicorn.sock -m 007 wsgi:app
        Restart=always
		
		[Install]
		 WantedBy=multi-user.target
	
	- sudo systemctl enable manage_site.service
	- Запуск:
	   sudo systemctl start manage_site.service 
	- Проверка:
	   sudo systemctl status manage_site.service


5. Настройка NGINX
	- Установка
	    sudo apt-get install nginx
	- Запускаем NGINX
	    sudo service nginx start
	- Создаем файл конфигурации   
 	    sudo nano /etc/nginx/conf.d/manage_site.conf
	- Настройки файла в manage_site.conf
		
	
	server {
    listen 80 default_server;
    listen [::]:80 default_server;
    server_name web-server.com;
    client_max_body_size 100M;

    location / {
    include proxy_params;
    proxy_pass http://unix:/opt/manage_site/gunicorn.sock;
    }
   }
    
	- В папке /etc/nginx/ удаляем файл дефолтных настроек
	      sudo rm /etc/nginx/sites-enabled/default
	- Проверяем правильность настроек командой 
		sudo nginx -t
	- При правильных настройках будес сообщение: 
		nginx: the configuration file /etc/nginx/nginx.conf syntax is ok
		nginx: configuration file /etc/nginx/nginx.conf test is successful
	- Перезапускаем nginx командой 
		sudo nginx -s reload


	- Активируем автозагрузку:
                sudo systemctl enable  manage_site.service
	- Запускаем сервис:
                sudo systemctl start manage_site.service
	- Проверяем статус
				sudo systemctl status manage_site.service
				
