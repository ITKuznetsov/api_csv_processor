# API CSV Processor
Форматирует файл CSV формата через API endpoint
## Технологии
* Python
* Django
* Django REST Framework
* Python-dotenv
## Локальный запуск (Windows)
1. Перейдите в локальную директорию проекта, затем создайте и активируйте виртуальное окружение
   ```cmd
   python -m venv venv
   venv\Scripts\Activate
   ```

2. Установите зависимости
   ```cmd
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

3. Создайте файл .env и установите необходимый ключ для settings.py (SECRET_KEY)
   ```cmd
   New-Item -Path . -Name ".env" -ItemType "File"
   ```

4. Выполните миграции
   ```cmd
   python manage.py migrate
   ```

5. Создайте суперпользователя
   ```cmd
   python manage.py createsuperuser
   ```
## Как пользоваться?
1. Запустите локальный сервер
  ```cmd
   python manage.py runserver
   ```
2. Перейдите по url: http://127.0.0.1:8000/admin/ и авторизируйтесь под аккаунтом суперпользователя
3. Добавте в корневую директорию проекта ваш файл (test.csv)
4. Перейдите по url: http://127.0.0.1:8000/api/process-csv/, если запрос был выполнен удачно, отформатированный файл сохранится в директории проекта (formated_test.csv)
