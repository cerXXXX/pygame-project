import sqlite3


def create_database():
    """Создаёт базу данных и таблицы, если их ещё нет"""

    conn = sqlite3.connect("data.db")
    cursor = conn.cursor()

    cursor.execute("""CREATE TABLE IF NOT EXISTS completed_levels (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            level INTEGER UNIQUE
        )""")

    cursor.execute("""CREATE TABLE IF NOT EXISTS level_results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            level INTEGER,
            score INTEGER,
            time REAL,
            win BOOLEAN
        )""")

    conn.commit()
    conn.close()


def save_completed_level(level):
    """Сохраняет номер пройденного уровня в базу данных"""

    conn = sqlite3.connect("data.db")
    cursor = conn.cursor()

    cursor.execute("INSERT OR IGNORE INTO completed_levels (level) VALUES (?)", (level,))
    conn.commit()
    conn.close()


def get_completed_levels():
    """Возвращает список всех пройденных уровней"""

    conn = sqlite3.connect("data.db")
    cursor = conn.cursor()

    cursor.execute("SELECT level FROM completed_levels")
    levels = {row[0] for row in cursor.fetchall()}

    conn.close()
    return levels


def save_level_result(level, score, time, win):
    """Сохраняет результат уровня (номер, счёт, время, победа/поражение) в базу"""

    conn = sqlite3.connect("data.db")
    cursor = conn.cursor()

    cursor.execute("INSERT INTO level_results (level, score, time, win) VALUES (?, ?, ?, ?)",
                   (level, score, time, win))

    conn.commit()
    conn.close()


def get_level_results():
    """Возвращает список всех результатов уровней"""

    conn = sqlite3.connect("data.db")
    cursor = conn.cursor()

    cursor.execute("SELECT level, score, time, win FROM level_results")
    results = cursor.fetchall()

    conn.close()
    return results


def get_best_result(level):
    """Возвращает лучший результат прохождения уровня (score и time) для выигранных попыток,
    или None, если результатов нет"""

    conn = sqlite3.connect("data.db")
    cursor = conn.cursor()
    cursor.execute(
        "SELECT score, time FROM level_results WHERE level = ? AND win = 1 ORDER BY score DESC LIMIT 1",
        (level,))
    result = cursor.fetchone()
    conn.close()
    return result


# автоматически создаём базу при первом запуске
create_database()
