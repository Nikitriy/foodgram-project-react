# Foodgram

### Описание проекта

Сервис Foodgram предназначен для поиска и выкладывания собственных рецептов.

Функция список покупок также поможет быстро получить перечень всего необходимого для готовки.

### Как запустить проект:

Клонировать репозиторий и перейти в него в командной строке:

```
git clone https://github.com/Nikitriy/foodgram-project-react.git
```

```
cd foodgram-project-react
```

Cоздать и активировать виртуальное окружение:

```
python -m venv venv
```

* Если у вас Linux/macOS

    ```
    source venv/bin/activate
    ```

* Если у вас windows

    ```
    source venv/scripts/activate
    ```

Установить зависимости из файла requirements.txt:

```
pip install -r requirements.txt
```

Выполнить миграции:

```
python manage.py makemigrations
```

```
python manage.py migrate
```

Запустить проект:

```
python manage.py runserver
```

### URL-адрес

https://useful-foodgram.bounceme.net

### Используемые технологии

- Django
- Docker
- Python

### Автор

Проект разработан [Nikitriy](https://github.com/Nikitriy)
