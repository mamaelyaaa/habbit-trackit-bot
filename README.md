# Habbit TrackIt Bot

## Установка и запуск

1. Перейти в нужную папку: `backend` или `bot`
2. Создать в ней виртуальное окружение

    ```shell
    # pip
    python -m venv .venv
    .venv/Scripts/activate
    pip install -r requirements.txt
   
    # uv
    uv venv
    .venv/Scripts/activate
    uv sync
    ```

3. Пометить папку `src` как Root
4. Создать файл переменных окружения для DEV и TEST среды:

   ```shell
   cp .env.example .env
   cp .env.test.example .env.test
   ```

5. Запустить `src/main.py`

## Конфигурация

Чтобы запустить базу данных, необходимо поднять соотвествующий контейнер с помощью docker-compose

   ```shell
   # Для DEV среды:
   docker compose up -d db
   python src/main.py
   
   # Для TEST среды:
   docker compose up -d test_db
   pytest -v 
   ```

> Запустить сразу _две_ базы данных нельзя
 
> Чтобы сменить среду разработки в `.env` файле нужно заменить `RUN__MODE` на необходимый