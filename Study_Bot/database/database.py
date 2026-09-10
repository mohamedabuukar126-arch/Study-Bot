import sqlite3
import random
import string

def get_db():
  conn = sqlite3.connect("users.db")
  return conn, conn.cursor()


# user functions
def add_user(user_id):
   conn, cursor = get_db()
   cursor.execute("INSERT INTO users (user_id, coins, last_claim) VALUES (?, ?, ?)", (user_id, 1000, 0))
   conn.commit()
   conn.close()

def add_study(user_id, study_time):
  conn, cursor = get_db()
  cursor.execute("UPDATE study SET study_time = ? WHERE user_id = ?", (study_time, user_id))
  conn.commit()
  conn.close()
  
def get_user(user_id):
  conn, cursor = get_db()
  cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id))
  user = cursor.fetchone()
  conn.close()
  return user

def get_coins(user_id):
  conn, cursor = get_db()
  cursor.execute("SELECT coins FROM users WHERE user_id = ?", (user_id,))
  result = cursor.fetchone()
  conn.close()
  

def user_exists(user_id):
  conn, cursor = get_db()
  cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id))
  user = cursor.fetchone()
  conn.close()
  return user is not None


# study function
def save_study(user_id, study_time):
  conn, cursor = get_db()
  cursor.execute("INSERT OR REPLACE INTO study (user_id, study_time) VALUES (?, ?)", (user_id, study_time))
  conn.commit()
  conn.close()
  

def get_studytime(user_id):
  conn, cursor = get_db()
  cursor.execute("SELECT study_time FROM study WHERE user_id = ?", (user_id,))
  result = cursor.fetchone()
  conn.close()
  return result[0] if result else None

def updatetotalstudytime(user_id, study_time):
  conn, cursor = get_db()
  cursor.execute("UPDATE study SET study_time = ? WHERE user_id = ?", (study_time, user_id))
  conn.commit()
  conn.close()

def end_studytime(user_id):
  conn, cursor = get_db()
  cursor.execute("DELETE FROM study WHERE user_id = ?", (user_id,))
  conn.commit()
  conn.close()


def todolist(user_id, task):
  conn, cursor = get_db()
  cursor.execute("INSERT INTO users (user_id, task) VALUES (?, ?)", (user_id), (task))
  conn.commit()
  conn.close()

def get_todolist(user_id, task):
  conn, cursor = get_db()
  cursor.exeucte("SELECT * FROM users WHERE user_id = ? AND task = ?", (user_id), (task))
  conn.commit()
  conn.close()

def study_running(user_id):
  conn, cursor = get_db()
  cursor.execute("SELECT 1 FROM study WHERE user_id = ?", (user_id,))
  result = cursor.fetchone()
  conn.close()
  return result is not None
  

# fun functions
def get_quote():
   conn, cursor = get_db()
   cursor.execute("SELECT * FROM quotes")
   quote = cursor.fetchone()
   conn.close()
   return quote

def get_roast():
   conn, cursor = get_db()
   cursor.execute("SELECT * FROM roasts")
   roast = cursor.fetchone()
   conn.close()

def profile(user_id):
  conn, cursor = get_db()
  cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id))
  conn.commit()
  conn.close()
                 



# callback functions
def show_todolist(user_id, task):
   conn, cursor = get_db()
   cursor.execute("SELECT * FROM users WHERE user_id = ? AND task = ?", (user_id, task))
   conn.commit()
   conn.close()
  


   


# save data
def save_data(user_id, task):
   conn, cursor = get_db()
   cursor.execute("INSERT INTO users (user_id, task) VALUES (?, ?)", (user_id, task))
   conn.commit()
   conn.close()

def save_study(user_id, study_time):
   conn, cursor = get_db()
   cursor.execute("INSERT OR REPLACE INTO study (user_id, study_time) VALUES (?, ?)", (user_id, study_time))
   conn.commit()
   conn.close()

def save_notes(user_id, notes, category):
  conn, cursor = get_db()
  cursor.execute("INSERT INTO notes (user_id, notes, category ) VALUES (?, ?, ?)", (user_id, notes, category))
  conn.commit()
  conn.close()

def save_message(user_id, message, role):
  conn, cursor = get_db()
  cursor.execute("INSERT INTO aihistory (user_id, role, message) VALUES (?, ?, ?)", (user_id, role, message))
  conn.commit()
  conn.close()
  

def get_message(user_id):
  conn, cursor = get_db()
  # this is the message that the user sent to the AI model
  cursor.execute("SELECT role, message FROM aihistory WHERE user_id = (?) ORDER BY Timestamp DESC LIMIT 5", (user_id,))
  rows = cursor.fetchall()
  messages = []
  for role, mesages in rows:
    messages.append({
      "role": role,
      "content": mesages})
  conn.close()
  return messages

def get_assitantreply(assitantreply):
  conn, cursor = get_db()
  cursor.execute("SELECT message FROM aihistory WHERE role = ?", (assitantreply,))
  conn.commit()
  conn.close()
  


def check_datasaving(user_id):
  conn, cursor = get_db()
  cursor.execute("SELECT(COUNT(*)) FROM aihistory WHERE user_id = ?", (user_id,))
  result = cursor.fetchone()
  conn.close()
  return result[0] if result else None
  


def delete_notes(user_id):
  conn, cursor = get_db()
  cursor.execute("DELETE FROM notes WHERE user_id = ?", (user_id,))
  conn.commit()
  conn.close()

def delete_note(user_id, note_id):
  conn, cursor = get_db()
  cursor.execute("DELETE FROM notes WHERE user_id = ? AND id = ?", (user_id, note_id))
  conn.commit()
  conn.close()


def get_notes(user_id):
  conn, cursor = get_db()
  # calls the data from save_notes()
  cursor.execute("SELECT * FROM notes WHERE user_id = ?", (user_id,))
  return cursor.fetchall()

def idnotes(user_id):
  conn, cursor = get_db()
  cursor.execute("SELECT id FROM notes WHERE id = ? and user_id = ?", (user_id,))
  conn.commit()
  conn.close()

def update_note(user_id, note_id, new_note):
  conn, cursor = get_db()
  cursor.execute("UPDATE notes SET notes = ? WHERE user_id = ? AND id = ?", (new_note, user_id, note_id))
  conn.commit()
  conn.close()


  

  

def save_coins(user_id, coins):
   conn, cursor = get_db()
   cursor.execute("INSERT INTO users (user_id, coins) VALUES (?, ?)", (user_id, coins))
   conn.commit()
   conn.close()

def save_last_claim(user_id, last_claim):
  conn, cursor = get_db()
  cursor.execute("INSERT INTO users (user_id, last_claim) VALUES (?, ?)", (user_id, last_claim))
  conn.commit()
  conn.close()


def save_flashcards(user_id, flashcards):
  conn, cursor = get_db()
  cursor.execute("INSERT INTO users (user_id, flashcards) VALUES (?, ?)", (user_id, flashcards))
  conn.commit()
  conn.close()


def show_flashcards(user_id, flashcards):
  conn, cursor = get_db()
  cursor.execute("SELECT * FROM users WHERE user_id = ? AND flashcards = ?", (user_id, flashcards))
  conn.commit()
  conn.close()



# delete stuff
def delete_flashcards(user_id, flashcards):
  conn, cursor = get_db()
  cursor.execute("DELETE FROM users WHERE user_id = ? AND flashcards = ?", (user_id, flashcards))
  conn.commit()
  conn.close()

def delete_coins(user_id, coins):
  conn, cursor = get_db()
  cursor.execute("DELETE FROM users WHERE user_id = ? AND coins = ?", (user_id, coins))
  conn.commit()
  conn.close()

def delete_user(user_id):
  conn, cursor = get_db()
  cursor.execute("DELETE FROM users WHERE user_id = ?,", (user_id))
  conn.commit()
  conn.close()

def delete_study(user_id):
  conn, cursor = get_db()
  cursor.execute("DELETE FROM study WHERE user_id = ?", (user_id,))
  conn.commit()
  conn.close()

def delete_task(user_id, task):
  conn, cursor = get_db()
  conn.execute("DELETE FROM users, WHERE user_id = ? and task = ?", (user_id, task))
  conn.commit()
  conn.close()

def delete_todolist(user_id, task):
   conn, cursor = get_db()
   cursor.execute("DELETE FROM users WHERE user_id = ? AND task = ?", (user_id, task))
   conn.commit()
   conn.close()

# ban people from my bot
def ban_user(user_id):
  conn, cursor = get_db()
  cursor.execute("INSERT INTO banlist (user_id) VALUES (?)", (user_id,))
  conn.commit()
  conn.close()

def saveaiquiz_attempts(user_id):
  conn, cursor = get_db()
  cursor.execute("""INSERT INTO aiquizcount (user_id, attempts) VALUES(?, 1) ON CONFLICT(user_id) DO UPDATE SET attempts = attempts + 1""", (user_id,))            
  conn.commit()
  conn.close()



# create tables
def create_tables():
   conn, cursor = get_db()
   cursor.execute("""CREATE TABLE IF NOT EXISTS users (user_id TEXT PRIMARY KEY, coins INTEGER, last_claim INTEGER)""")
   cursor.execute("""CREATE TABLE IF NOT EXISTS study (user_id TEXT PRIMARY KEY, study_time INTEGER)""")
   cursor.execute("""CREATE TABLE IF NOT EXISTS quotes (quote TEXT)""")
   cursor.execute("""CREATE TABLE IF NOT EXISTS roasts (roast TEXT)""")
   cursor.execute("""CREATE TABLE IF NOT EXISTS flashcards (user_id TEXT PRIMARY KEY, flashcards TEXT)""")
   cursor.execute("""CREATE TABLE IF NOT EXISTS todolist (user_id TEXT PRIMARY KEY, task TEXT)""")
   cursor.execute("""CREATE TABLE IF NOT EXISTS studystats (user_id TEXT PRIMARY KEY, task TEXT)""")
   cursor.execute("""CREATE TABLE IF NOT EXISTS notes (id INTEGER PRIMARY KEY AUTOINCREMENT, user_id TEXT, notes TEXT, category TEXT)""")
   cursor.execute("""CREATE TABLE IF NOT EXISTS keys (key TEXT PRIMARY KEY, plan TEXT NOT NULL, redeemed INTEGER DEFAULT 0, redeemed_by INTEGER, created_at DATETIME DEFAULT CURRENT_TIMESTAMP, expires_at DATETIME)""")
   cursor.execute("""CREATE TABLE IF NOT EXISTS aihistory (user_id INTEGER, role TEXT, message TEXT, Timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)""")
   cursor.execute("""CREATE TABLE IF NOT EXISTS aiquizcount(user_id INTEGER PRIMARY KEY, attempts INTEGER DEFAULT 0)""")
   cursor.execute("""CREATE TABLE IF NOT EXISTS categories(id INTEGER PRIMARY KEY AUTOINCREMENT, user_id TEXT NOT NULL, category TEXT NOT NULL, UNIQUE(user_id, category))""")
   conn.close()
   

# check if there are any tables
def check_tables():
  conn, cursor = get_db()
  cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
  print(cursor.fetchall())
  conn.close()


# close the database
def close_db():
   conn, cursor = get_db()
   conn.close()
   print("Database closed successfully")

# validation
def check_study(user_id):
  conn, cursor = get_db()
  cursor.execute("SELECT 1 FROM study WHERE user_id = ?", (user_id,))
  result = cursor.fetchone()
  conn.close()
  return result is not None

def check_notes(user_id):
  conn, cursor = get_db()
  cursor.execute("SELECT COUNT(*) FROM notes WHERE user_id = ?", (user_id,))
  count = cursor.fetchone()[0]
  conn.close()
  return count

def aiquiz_attempts(user_id):
  conn, cursor = get_db()
  cursor.execute("SELECT COUNT(*) FROM aiquizcount WHERE user_id = ?", (user_id,))
  count = cursor.fetchone()[0]
  conn.close()
  return count
    



# debug
def checkstudytable(user_id):
  conn, cursor = get_db()
  cursor.execute("SELECT * FROM study WHERE user_id = ?", (user_id,))
  print(cursor.fetchall())

def debug():
  conn, cursor = get_db()
  cursor.execute("DROP TABLE notes")
  conn.commit()
  conn.close()

#search function
def search_notes(user_id, search_term):
  conn, cursor = get_db()
  cursor.execute("SELECT* FROM notes WHERE user_id = ? AND notes LIKE ?", (user_id, f"%{search_term}%"))
  result = cursor.fetchall()
  conn.close()
  return result

def latest_notes(user_id):
  conn, cursor = get_db()
  cursor.execute("SELECT* FROM notes WHERE user_id = ? ORDER BY id DESC LIMIT 5", (user_id,))
  result = cursor.fetchall()
  conn.close()
  return result



# ai functions
def clear_memory(user_id):
  conn, cursor = get_db()
  cursor.execute("DELETE FROM aihistory WHERE user_id = ?", (user_id,))
  conn.commit()
  conn.close()

def get_user_mode(user_id):
  conn, cursor = get_db()
  cursor.execute("SELECT mode FROM users WHERE user_id = ?", (user_id,))
  result = cursor.fetchone()
  conn.close()
  return result[0] if result else None
  

# announcement function
def get_all_users():
  conn, cursor = get_db()
  cursor.execute("SELECT user_id FROM users")
  result = cursor.fetchall()
  conn.close()
  return [row[0] for row in result]

def get_user(user_id):
  conn, cursor = get_db()
  cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
  result = cursor.fetchone()
  conn.close()
  return result

# export function
def export_notes(user_id):
  conn, cursor = get_db()
  cursor.execute("SELECT* FROM notes WHERE user_id = ? ORDER BY id ASC", (user_id,))
  result = cursor.fetchall()
  conn.close()
  return [row[2] for row in result]


# recall category
def call_category(user_id):
  conn, cursor = get_db()
  # calls the data from save_notes()
  cursor.execute("SELECT DISTINCT category FROM categories WHERE user_id = ?", (user_id,))
  return cursor.fetchall()

def add_category(user_id, category):
  conn, cursor = get_db()
  try:
    cursor.execute("INSERT INTO categories (user_id, category) VALUES (?,?)", (user_id, category))
    conn.commit()
    conn.close()
    return True
  except sqlite3.IntegrityError:
    return False
  
def showcase_notes(user_id, category):
  conn, cursor = get_db()
  cursor.execute("SELECT* FROM notes WHERE user_id = ? and category = ?", (user_id, category))
  result = cursor.fetchall()
  conn.close()
  return [row[2] for row in result]






  


  
  
  
  
  
  
  
  




   


   




  
  
  

