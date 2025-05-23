# Tasks API

Tasks API — это простой REST API для управления задачами. Проект построен с использованием Django и Django REST Framework.

## 🔧 Установка

1. Клонируйте репозиторий:

```bash
git clone https://github.com/your-username/tasks-api.git
cd tasks-api
```

2. Создайте `.env` файл или задайте переменные окружения (если вы не используете Docker Compose с `.env`).

3. Запустите проект с помощью Docker:

```bash
docker compose up --build
```

Приложение будет доступно на `http://localhost:8000`.

## 📦 Основные зависимости

- Python 3.11
- Django 5.2.1
- Django REST Framework
- PostgreSQL

## 🌐 Swagger-документация

Swagger автоматически генерирует документацию на основе вашего API. Она доступна по адресу:

```
http://localhost:8000/api/schema/swagger-ui/
```

Если вы используете `drf-spectacular`, убедитесь, что в `settings.py` подключено следующее:

```python
INSTALLED_APPS = [
    ...
    'drf_spectacular',
    ...
]

REST_FRAMEWORK = {
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
}
```

И добавлены маршруты в `urls.py`:

```python
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

urlpatterns = [
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
]
```

## 🗃 Структура проекта

```
tasks-api/
│
├── todolist/               # Основное Django приложение
│   ├── models.py
│   ├── views.py
│   ├── serializers.py
│   └── urls.py
│
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md
```

## ✅ Миграции и суперпользователь

Внутри контейнера:

```bash
docker compose exec backend python manage.py migrate
docker compose exec backend python manage.py createsuperuser
```

