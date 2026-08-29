# 📦 Universal Storage Bot

Telegram bot for storing notes and files with unique codes.  
A personal cloud storage inside Telegram.

---

## ✨ Features

- 📝 **Add notes** — save any text notes
- 📎 **Upload files** — photos, documents, videos (with description)
- 🔍 **Search** — find notes and files by keywords
- 📋 **View all records** — notes and files in one list
- 🗑️ **Delete** — remove notes, files, or all data at once
- 📊 **Statistics** — count of notes and files
- 🆔 **Unique codes** — each file gets a unique 8-character code
- 📥 **Get file by code** — via `/get CODE` or inline button
- 🤖 **HTML formatting** — beautiful and readable messages
- 🧠 **FSM (Finite State Machine)** — smooth user interaction

---

## 🛠️ Tech Stack

- **Python 3.11+**
- **Aiogram 3.x** — asynchronous Telegram Bot API framework
- **SQLite** — lightweight local database
- **FSM** — finite state machine for step-by-step dialogs

---

## 📁 Project Structure
storage_bot/
├── main.py # Bot entry point
├── message.py # All command and callback handlers
├── keyboards.py # Inline keyboards
├── states.py # FSM states
├── basedatastorage.py # SQLite database operations
├── utils.py # Helper functions (code generator)
├── configdatastorage.py # Bot token
├── requirements.txt # Dependencies
└── storage.db # SQLite database (auto-created)
text

---

## 📦 Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/DansDUSK/storage-bot.git
   cd storage-bot
   ```
2. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```
3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create configdatastorage.py with your bot token:
```python
token = "YOUR_BOT_TOKEN_HERE"
```

5. Run the bot:
```bash
python main.py
```
🚀 Deployment

Easily deploy on:

Railway (recommended)

Render.com

PythonAnywhere

📄 License
MIT © DansDUSK

📩 Contact
GitHub: DansDUSK

Telegram: @daggerka

⭐ If you like this project, give it a star!
text

---

## 🇷🇺 README.ru.md (Русский)

# 📦 Универсальный бот-хранилище

Telegram-бот для хранения заметок и файлов с уникальными кодами.  
Личное облачное хранилище внутри Telegram.

---

## ✨ Возможности

- 📝 **Добавление заметок** — сохраняй любые текстовые заметки
- 📎 **Загрузка файлов** — фото, документы, видео (с описанием)
- 🔍 **Поиск** — находи заметки и файлы по ключевым словам
- 📋 **Просмотр всех записей** — заметки и файлы в одном списке
- 🗑️ **Удаление** — удаляй заметки, файлы или все данные сразу
- 📊 **Статистика** — количество заметок и файлов
- 🆔 **Уникальные коды** — каждый файл получает уникальный 8-символьный код
- 📥 **Получение файла по коду** — через `/get КОД` или кнопку
- 🤖 **HTML-форматирование** — красивые и понятные сообщения
- 🧠 **FSM (машина состояний)** — плавное взаимодействие с пользователем

---

## 🛠️ Технологии

- **Python 3.11+**
- **Aiogram 3.x** — асинхронный фреймворк для Telegram Bot API
- **SQLite** — лёгкая локальная база данных
- **FSM** — машина состояний для пошаговых диалогов

---

## 📁 Структура проекта
storage_bot/
├── main.py # Точка входа
├── message.py # Обработчики команд и callback'ов
├── keyboards.py # Инлайн-клавиатуры
├── states.py # Состояния FSM
├── basedatastorage.py # Работа с SQLite
├── utils.py # Вспомогательные функции (генератор кодов)
├── configdatastorage.py # Токен бота
├── requirements.txt # Зависимости
└── storage.db # База данных SQLite (создаётся автоматически)

text

---

## 📦 Установка

1. Клонируй репозиторий:
   ```bash
   git clone https://github.com/DansDUSK/storage-bot.git
   cd storage-bot
   ```
   
2. Создай виртуальное окружение:
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

3. Установи зависимости:
```bash
pip install -r requirements.txt
```

4. Создай файл configdatastorage.py с токеном бота:
```python
token = "ТВОЙ_ТОКЕН_БОТА"
```

5. Запусти бота:
```bash
python main.py
```

🚀 Деплой
Бота можно развернуть на любой платформе, поддерживающей Python:

Railway (рекомендуется)

Render.com

PythonAnywhere

📄 Лицензия
MIT © DansDUSK

📩 Контакты
GitHub: DansDUSK

Telegram: @daggerka

⭐ Если понравился проект — поставь звёздочку!
text

---

## 📦 `requirements.txt`
aiogram>=3.0.0
