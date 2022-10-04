# Проект "Хабр"
## Командная разработка команды №1 по методологии Agile
Веб-сайт в формате системы тематических коллективных блогов (именуемых хабами) с элементами новостного сайта, созданный для публикации новостей, аналитических статей, мыслей, связанных с направлениями обучения в образовательной компании.

## Основные системные требования:
* Ubuntu 20.04 LTS
* Python 3.9
* PostgreSQL 13
* Зависимости из файла requirements.txt

## Запуск проекта
### Установка Docker
#### Обновление информации о репозиториях
```angular2html
 $ sudo apt-get update
 $ sudo apt-get install \
    ca-certificates \
    curl \
    gnupg \
    lsb-releas
```
#### Добавление официального GPG ключа Docker
```angular2html
$ sudo mkdir -p /etc/apt/keyrings
$ curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
```
#### Добавление репозитория Docker
```angular2html
$ echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
```
#### Установка Docker
```angular2html
$ sudo apt-get update
$ sudo apt-get install docker-ce docker-ce-cli containerd.io docker-compose-plugin
```
### Установка Git
#### Обновление информации о репозиториях
```angular2html
$ sudo apt-get update
```
#### Установка Git
```angular2html
$ sudo apt get install git
```
### Клонируем репозиторий с проектом
```angular2html
$ git clone https://github.com/GB-Team-1/Habr-proj.git
```
### Запускаем проект в Docker
```angular2html
$ cd Habr-proj/
$ chmod +x habr_proj/entrypoint.sh
$ sudo docker-compose up --build
```
### Вводим в браузере адрес сервера и веб-сайт открывается.