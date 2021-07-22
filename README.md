### Описание:

api_final_yatube позволит Вам работать с базой проекта Yatube: 
получать, добавлять, корректировать и удалять информацию о публикациях, пользователях, комментариях, подписках пользователей. 

Подробную документацию о всех доступных действиях Вы можете получить здесь http://127.0.0.1:8000/redoc/


### Как запустить проект:

Клонировать репозиторий и перейти в него в командной строке:

```bash
git clone https://github.com/feyaschuk/api_final_yatube.git
```

Cоздать и активировать виртуальное окружение:

```bash
python3 -m venv env
```

```bash
source env/bin/activate (MAC OC, Linux) // source venv/Scripts/activate (Windows)
```

```bash
python3 -m pip install --upgrade pip
```

Установить зависимости из файла requirements.txt:

```bash
pip install -r requirements.txt
```

Выполнить миграции:

```bash
python3 manage.py migrate
```

Запустить проект:

```bash
python3 manage.py runserver
```


### Примеры обращений к API:

Получение списка публикаций: 


Тип запроса GET. 


Адрес запроса: 
```bash
http://127.0.0.1:8000/api/v1/posts/
```

Результат

```
  [{
        "id": 1,
        "author": "user",
        "text": "First time hear today about this app. Gonna try it - then will back with feedback.",
        "created": "2021-07-20T11:45:48.406342Z",
        "post": 1
    },
    {
        "id": 3,
        "author": "user",
        "text": "First time hear today about this app. Gonna try it - then will back with feedback.",
        "created": "2021-07-20T11:48:22.596287Z",
        "post": 1   }]
```
Создание новой публикации: 


Тип запроса POST. 


Адрес запроса: http://127.0.0.1:8000/api/v1/posts/

Тело запроса

```
 "text": "First time hear today about this app. Gonna try it - then will back with feedback."
```

Результат

```
 {
    "id": 16,
    "author": "user",
    "text": "First time hear today about this app. Gonna try it - then will back with feedback.",
    "pub_date": "2021-07-21T10:33:59.481821Z",
    "image": null,
    "group": null
}
```
