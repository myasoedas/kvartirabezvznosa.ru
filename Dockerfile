# Используем официальный образ Python 3.9-slim
FROM python:3.9-slim

# Отключаем буферизацию вывода для корректного логирования
ENV PYTHONUNBUFFERED=1

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем файл зависимостей и устанавливаем пакеты
COPY requirements.txt /app/
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Копируем весь исходный код в контейнер
COPY . /app/

# Устанавливаем PYTHONPATH, чтобы можно было импортировать blogicum
ENV PYTHONPATH=/app/blogicum_project

# Запускаем Gunicorn с 3 воркерами
CMD ["gunicorn", "--workers", "3", "--bind", "0.0.0.0:8000", "blogicum_project.blogicum.wsgi:application"]
