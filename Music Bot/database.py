import sqlite3

def create_database():
    connection = sqlite3.connect("music.db")
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS songs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            file_id TEXT NOT NULL,
            title TEXT NOT NULL,
            duration INTEGER
        )
    """)

    connection.commit()
    connection.close()

def add_song(user_id, file_id, title, duration):
    connection = sqlite3.connect("music.db")
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO songs (user_id, file_id, title, duration)
        VALUES (?, ?, ?, ?)
    """, (user_id, file_id, title, duration))

    connection.commit()
    connection.close()

def get_songs(user_id):
    connection = sqlite3.connect("music.db")
    cursor = connection.cursor()

    cursor.execute("""
        SELECT id, file_id, title, duration
        FROM songs
        WHERE user_id = ?
    """, (user_id,))

    songs = cursor.fetchall()
    connection.close()

    return songs


def get_song_titles(user_id):
    connection = sqlite3.connect("music.db")
    cursor = connection.cursor()

    cursor.execute("""
        SELECT title
        FROM songs
        WHERE user_id = ?
    """, (user_id,))

    songs = cursor.fetchall()
    connection.close()

    return songs

def clear_songs():
    connection = sqlite3.connect("music.db")
    cursor = connection.cursor()

    cursor.execute("DELETE FROM songs")

    connection.commit()
    connection.close()

def get_song_by_id(user_id, song_id):
    connection = sqlite3.connect("music.db")
    cursor = connection.cursor()

    cursor.execute("""
        SELECT id, file_id, title, duration
        FROM songs
        WHERE user_id = ? AND id = ?
    """, (user_id, song_id))

    song = cursor.fetchone()
    connection.close()

    return song
