FROM node:20

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем зависимости
COPY package.json yarn.lock ./

# Включаем corepack и устанавливаем зависимости
RUN corepack enable && yarn install

# Копируем исходный код
COPY . .

# Пробрасываем порт Vite
EXPOSE 5173

# Запускаем Vite dev-сервер
CMD ["yarn", "dev"]