import sqlite3

conn = sqlite3.connect("database.db")
cursor = conn.cursor()

# Users table
cursor.execute("""
CREATE TABLE IF NOT EXISTS users(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
)
""")

# Bookings table
cursor.execute("""
CREATE TABLE IF NOT EXISTS bookings(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT NOT NULL,
    mobile TEXT NOT NULL,
    temple TEXT NOT NULL,
    booking_date TEXT NOT NULL,
    tickets INTEGER NOT NULL,
    payment_status TEXT NOT NULL         
)
""")
#temples table
cursor.execute("""
CREATE TABLE IF NOT EXISTS temples(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    temple_name TEXT NOT NULL,
    state TEXT NOT NULL,
    city TEXT NOT NULL,
    description TEXT,
    opening_time TEXT,
    closing_time TEXT,
    image TEXT,
    contact TEXT
)
""")
cursor.execute("""
CREATE TABLE IF NOT EXISTS partners(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    temple_name TEXT,
    person TEXT,
    email TEXT,
    mobile TEXT,
    state TEXT,
    city TEXT,
    address TEXT,
    description TEXT
)
""")
cursor.execute("""
CREATE TABLE IF NOT EXISTS feedback(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    temple_name TEXT,
    rating INTEGER,
    review TEXT
)
""")
conn.commit()
conn.close()

print("Database created successfully!")
