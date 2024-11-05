import psycopg2
from decouple import config

# Чтение параметров подключения из переменных окружения
DATABASE_NAME = config("DATABASE_NAME")
DATABASE_USER = config("DATABASE_USER")
DATABASE_PASSWORD = config("DATABASE_PASSWORD")
DATABASE_HOST = config("DATABASE_HOST")
DATABASE_PORT = config("DATABASE_PORT")

# Проверка подключения
try:
    # Установка подключения к PostgreSQL
    connection = psycopg2.connect(
        dbname=DATABASE_NAME,
        user=DATABASE_USER,
        password=DATABASE_PASSWORD,
        host=DATABASE_HOST,
        port=DATABASE_PORT,
    )
    print("Подключение к базе данных успешно установлено!")
except psycopg2.OperationalError as e:
    print("Ошибка подключения к базе данных:", e)
finally:
    # Закрываем подключение, если оно было установлено
    if 'connection' in locals() and connection:
        connection.close()
        print("Подключение к базе данных закрыто.")
