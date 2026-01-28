# Используем официальный образ Python 3.10
FROM python:3.10-slim

# Устанавливаем системные зависимости
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Устанавливаем рабочую директорию внутри контейнера
WORKDIR /app

# Копируем файл с зависимостями
COPY api/requirements.txt .

# Устанавливаем Python зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем код API в контейнер
COPY api/ .

# Открываем порт 8000 для доступа к API
EXPOSE 8000

# Команда для запуска сервера при старте контейнера
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
