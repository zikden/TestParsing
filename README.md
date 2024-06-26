## Тестовое задание в Тендерплан

### Описание:
Данный проект содержит код на Python для веб-скрапинга с использованием BeautifulSoup и Celery для асинхронной обработки задач.

### Установка:
1. Установите необходимые зависимости, запустив:
    ```bash
    pip install -r requirements.text
    ```
    или
    ```bash
    poetry install
    ```
2. Убедитесь, что у вас установлен и запущен Redis на `localhost:6379`.

### Использование:
1. Запустите рабочего Celery, используя следующую команду:
    ```bash
    celery -A tasks worker --loglevel=info
    ```
2. Запустите основной скрипт для запуска задачи парсинга.

### Структура кода:
- `constats.py`: Содержит постоянные значения, используемые в коде.
- `tasks.py`: Содержит задачи Celery для парсинга веб-страниц и XML-данных.
- `main.py`: Основной скрипт для запуска задачи парсинга.

### Пояснение к коду:
1. Класс `ParseTask`:
    - Задача для парсинга главной страницы.
    - Получает содержимое страницы, извлекает необходимые данные с помощью BeautifulSoup и запускает задачу `ParseXML` для каждого найденного заказа.

2. Класс `ParseXML`:
    - Задача для парсинга XML-данных конкретного заказа.
    - Получает XML-данные по указанному URL, извлекает время публикации и выводит данные на экран.
