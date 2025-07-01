# Telegram Project

Телеграм-бот для работы с банковскими картами.

## Описание проекта

Данное приложение представляет собой телеграм-бота для работы с банковскими картами. Он интегрируется с Telegram API, обеспечивает автоматическую отправку сообщений и уведомлений, а также предоставляет настраиваемый функционал для пользователей. Интерфейс бота интуитивно понятен и удобен для взаимодействия.

## Getting Started

Refer to the documentation for setup instructions and usage examples.

## Установка

### .env

```env
BOT_TOKEN=токен_телеграм_бота
WEBAPP_URL=адрес_хоста
POSTGRES_DB=название_базы_данных
POSTGRES_USER=юзер_базы_данных
POSTGRES_PASSWORD=пароль_базы_данных
PGADMIN_DEFAULT_EMAIL=логин_админки
PGADMIN_DEFAULT_PASSWORD=пароль_админки
POSTGRES_HOST=хост_базы_данных
POSTGRES_PORT=порт_базы_данных
```

### Зависимости Backend (Python)

1. Убедитесь, что у вас установлен Python версии 3.8 или выше.
2. Установите зависимости с помощью pip:

```bash
pip install -r requirements.txt
```

### Установка Frontend

1. Установите зависимости фронтенда (используя yarn):

```bash
yarn install
```

2. Запустите сервер разработки фронтенда:

```bash
yarn start
```

### Запуск Backend

```bash
python backend/app.py
# или
uvicorn backend.app:app --port 8000
```

### Использование Docker Compose

Для запуска проекта с помощью Docker выполните:

```bash
docker-compose up --build
```

Фронтенд будет доступен на [http://localhost:3000](http://localhost:3000), а бекенд на [http://localhost:8000](http://localhost:8000).
