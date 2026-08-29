import sqlite3
from datetime import datetime

def init_db():
    conn = sqlite3.connect("storage.db")
    cursor = conn.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS notes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        text TEXT,
        created_at TEXT)""")

    cursor.execute("""CREATE TABLE IF NOT EXISTS files (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        file_id TEXT,
        file_type TEXT,
        description TEXT,
        unique_code TEXT UNIQUE,
        created_at TEXT)""")

    conn.commit()
    conn.close()

# ====== NOTES FUNCTION =====
def add_note(user_id, text):
    conn = sqlite3.connect("storage.db")
    cursor = conn.cursor()
    
    cursor.execute("INSERT INTO notes (user_id, text, created_at) VALUES (?,?,?)", (user_id, text, datetime.now().strftime("%Y-%m-%d %H:%M")))
    conn.commit()
    cursor.execute("SELECT * FROM notes WHERE user_id = ?", (user_id,))
    rows = cursor.fetchall()
    print("📝 Сохранено:", rows)  # ← смотри консоль
    conn.close()
    
def get_note(user_id):
    conn = sqlite3.connect("storage.db")
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM notes WHERE user_id = ? ORDER BY created_at", (user_id,))
    rows = cursor.fetchall()
    conn.close()
    return rows

def search_note(user_id, search_text):
    conn = sqlite3.connect("storage.db")
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM notes WHERE user_id = ? AND text LIKE ?", (user_id, f"%{search_text}%"))
    rows = cursor.fetchall()
    conn.close()
    return rows

def delete_note(user_id, note_id):
    conn = sqlite3.connect("storage.db")
    cursor = conn.cursor()
    
    cursor.execute("DELETE FROM notes WHERE id = ? AND user_id = ?", (note_id, user_id))
    conn.commit()
    conn.close()
    

# =====FILE FUNCTION =====
def save_file(user_id, file_id, file_type, description, unique_code):
    conn = sqlite3.connect("storage.db")
    cursor = conn.cursor()
    
    cursor.execute("INSERT INTO files (user_id, file_id, file_type, description, unique_code, created_at) VALUES (?,?,?,?,?,?)", (user_id, file_id, file_type, description, unique_code, datetime.now().strftime("%Y-%m-%d %H:%M")))
    conn.commit()
    conn.close()
    
def get_file_unique(unique_code):
    conn = sqlite3.connect("storage.db")
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM files WHERE unique_code = ?", (unique_code,))
    rows = cursor.fetchall()
    print(f"🔍 Ищем код: '{unique_code}' → Найдено: {rows}")  # ← добавь
    conn.close()
    return rows

def get_file_user_id(user_id):
    conn = sqlite3.connect("storage.db")
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM files WHERE user_id = ? ORDER BY created_at", (user_id,))
    rows = cursor.fetchall()
    conn.close()
    return rows

def search_file(user_id, search_text):
    conn = sqlite3.connect("storage.db")
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM files WHERE user_id = ? AND description LIKE ?", (user_id, f"%{search_text}%"))
    rows = cursor.fetchall()
    conn.close()
    return rows

    
def delete_file_by_code(unique_code, user_id):
    conn = sqlite3.connect("storage.db")
    c = conn.cursor()
    c.execute("DELETE FROM files WHERE unique_code = ? AND user_id = ?", (unique_code, user_id))
    deleted = c.rowcount > 0
    conn.commit()
    conn.close()
    return deleted

# ===== GLOBAL DELETE =====
def delete_all_user_data(user_id):
    conn = sqlite3.connect("storage.db")
    c = conn.cursor()
    c.execute("DELETE FROM notes WHERE user_id = ?", (user_id,))
    c.execute("DELETE FROM files WHERE user_id = ?", (user_id,))
    conn.commit()
    conn.close()
    
    
# ===== GLOBAL SEARCH =====
def all_search(user_id, search_text):
    notes = search_note(user_id, search_text)    
    files = search_file(user_id, search_text)
    return notes, files