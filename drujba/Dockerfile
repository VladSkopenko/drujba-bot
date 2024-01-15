FROM python:3.11

# Устанавливаем Poetry
RUN pip install poetry

# Создаем рабочий каталог
WORKDIR /app

# Копируем все файлы из текущего каталога в контейнер
COPY . /app/

# Устанавливаем зависимости с помощью Poetry
RUN pip intall -r ruquirements.txt

# Команда для запуска приложения
CMD ["python", "app.py"]
