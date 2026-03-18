# --- Stage 1: Сборка зависимостей ---
FROM python:3.11-slim as builder

WORKDIR /app

# Копируем файл зависимостей
COPY requirements.txt .

# Устанавливаем зависимости в папку пользователя
RUN pip install --user --no-cache-dir -r requirements.txt

# --- Stage 2: Финальный образ ---
FROM python:3.11-slim as runtime

WORKDIR /app

# Аргументы и переменные для порта (по умолчанию 8000)
ENV APP_PORT=8000

# Копируем установленные библиотеки
COPY --from=builder /root/.local /root/.local
# Копируем код приложения
COPY . .

# Добавляем путь к пакетам
ENV PATH=/root/.local/bin:$PATH

# Используем переменную окружения для порта
EXPOSE ${APP_PORT}

# Запуск через переменную, чтобы была гибкость в docker-compose
CMD uvicorn main:app --host 0.0.0.0 --port ${APP_PORT}