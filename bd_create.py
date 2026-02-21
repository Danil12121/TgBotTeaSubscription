import psycopg2
from psycopg2 import sql

DB_NAME = "tgbotteadb"
DB_USER = "nastya"
DB_PASSWORD = "password"
DB_HOST = "localhost"
DB_PORT = "5432"
SCHEMA_NAME = "bot_schema"  # твоя отдельная схема

def reset_database():
    # Подключаемся к служебной базе postgres
    conn = psycopg2.connect(
        dbname="postgres",
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT
    )
    conn.autocommit = True
    cursor = conn.cursor()

    # Удаляем старую базу
    cursor.execute(f"DROP DATABASE IF EXISTS {DB_NAME}")
    print(f"База {DB_NAME} удалена")

    # Создаем новую базу
    cursor.execute(f"CREATE DATABASE {DB_NAME}")
    print(f"База {DB_NAME} создана заново")

    cursor.close()
    conn.close()


def create_schema_and_tables():
    conn = psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT
    )
    cursor = conn.cursor()

    # Создаем схему
    cursor.execute(sql.SQL("CREATE SCHEMA IF NOT EXISTS {}").format(
        sql.Identifier(SCHEMA_NAME)
    ))

    # Создаем таблицу пользователей
    cursor.execute(sql.SQL("""
        CREATE TABLE IF NOT EXISTS {}.user_table(
            id SERIAL PRIMARY KEY,
            tg_id BIGINT UNIQUE,
            last_notification_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            is_admin BOOLEAN DEFAULT FALSE,
            is_approve BOOLEAN DEFAULT FALSE
        )
    """).format(sql.Identifier(SCHEMA_NAME)))

    # Создаем таблицу транзакций
    cursor.execute(sql.SQL("""
        CREATE TABLE IF NOT EXISTS {}.transaction_table(
            id SERIAL PRIMARY KEY,
            user_id INTEGER REFERENCES {}.user_table(id),
            number VARCHAR(255) NOT NULL,
            date_of_approve TIMESTAMP,
            admin_id INTEGER REFERENCES {}.user_table(id)
        )
    """).format(sql.Identifier(SCHEMA_NAME),
                sql.Identifier(SCHEMA_NAME),
                sql.Identifier(SCHEMA_NAME)))

    # Добавляем одного администратора в user_table
    cursor.execute(sql.SQL("""
        INSERT INTO {}.user_table (tg_id, is_admin, is_approve)
        VALUES (%s, %s, %s)
        ON CONFLICT (tg_id) DO NOTHING
    """).format(sql.Identifier(SCHEMA_NAME)), (
        123456789,  # Telegram ID админа
        True,
        True
    ))

    conn.commit()
    cursor.close()
    conn.close()
    print("Схема и таблицы созданы, админ добавлен")


if __name__ == "__main__":
    reset_database()
    create_schema_and_tables()
    print("База, схема и таблицы созданы заново")