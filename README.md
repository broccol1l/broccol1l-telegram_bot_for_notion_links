(Используйте main ветку)

Функционал

1. Добавление ссылок в базу данных Notion
      
        -Пользователь отправляет ссылку боту в Telegram.
        -Бот анализирует ссылку и добавляет её в указанную базу данных Notion.
2. Удаление ссылок
                  
       -Возможность удалять сохранённые ссылки через команды бота.
3. Получение всех сохранённых ссылок

        -Бот может отправить пользователю список всех ссылок, хранящихся в базе данных Notion.
4. Интеграция с Telegram API и Notion API

        -Подключение к Notion через специальную базу данных.
        -Работа с кнопками и меню в Telegram для удобства взаимодействия.
5. Управление состояниями

        -Используется состояние для отслеживания текущих действий пользователя.
6. Валидация ссылок

        -Бот проверяет, является ли отправленное сообщение корректной ссылкой.

Инструкция по запуску

Шаг 1: Клонирование репозитория

Клонируйте проект на ваш локальный компьютер:

    git clone <ссылка на репозиторий>
    cd <название папки>

Шаг 2: Установка зависимостей

Создайте виртуальное окружение и установите зависимости:

    python -m venv venv
    source venv/bin/activate  # Windows: venv\Scripts\activate
    pip install -r requirements.txt

Шаг 3: Интеграция с Notion

    Подключите ваш бот к моей базе данных Notion через ссылку-приглашение. Убедитесь, что у токена есть доступ к вашей базе данных. https://www.notion.so/invite/05e2be1eaaa2ce0f06890cd623e6d1548463ff68

Шаг 4: Настройка переменных окружения

    Переименуйте .env.example в .env
    Можете вставить свой Notion API Token и DataBase ID

Шаг 5: Запуск бота

Запустите бота:

    python __main__.py


Использование:

    /start: начало работы с ботом.
    Остальное управление по кнопкам!

Требования:

    Python 3.8+
    Установленные зависимости из requirements.txt
    Активированный API для Telegram и Notion
