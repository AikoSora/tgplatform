<h1 align="center">
VKdeo
</h1>
<p align="center">
Бот для скачивания видео с ВК
<br /><br />
<img alt="Python3.8" src="https://img.shields.io/badge/Python-3.8-blue">
<img alt="Django4.1.1" src="https://img.shields.io/badge/Django-4.1.1-brightgreen">
<img alt="Uvloop0.17.0" src="https://img.shields.io/badge/uvloop-0.17.0-blue">
<img alt="Aiogram2.22.1" src="https://img.shields.io/badge/Aiogram-2.22.1-blue">
</p>

## Взаимодействие с ботом
Сам [бот](http://t.me/vkdeo_bot)
<br />

## Установка и запуск
Сначала создадим виртуальное окружение и установим зависимости
```shell
python3 -m venv env
source env/bin/activate
python -m pip install requirements.txt
```
После нужно провести миграцию моделей для создания базы данных
```shell
python manage.py migrate
```
Теперь в файле [settings](tgbot/settings.py) в самом низу укажем токен который можно получить [здесь](https://t.me/BotFather)
<br />
После можно запустить бота
```shell
python manage.py startbot
```

## Команды
Все команды можно создавать в папке [commands](app/bot/commands), примеры вы можете осмотреть там-же