Инструкция по развёртыванию приложения:
---
1) Необходимо проверить наличие питона, для этого в терминале ввести команду:
```
python3 --version
```
2) Если python3 не установлен, то установим его:
```
sudo apt-get update
sudo apt-get install python3.9.5
```
3) Развернём виртуальное окружение. Для этого перейдём в директорию с проектом и последовательно выполним команды:
```
python3 -m venv myvenv
source myvenv/bin/activate
pip install -U -r requirements.txt
```
4) Введём в терминал:
```
mysql
```
5) Создадим пользователя и базу данных в терминале:
```
CREATE DATABASE shortened_url
USE shortened_url
CREATE USER 'alexey'@'localhost' IDENTIFIED BY '476198898'
GRANT ALL ON shortened_url.* TO 'alexey'@'localhost'
FLUSH PRIVILEGES
exit
```
6) Выполним миграции:
```
python manage.py migrate
```
7) Запустим проект:
```
python manage.py runserver
```