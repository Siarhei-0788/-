import sqlite3
from pathlib import Path
from datetime import datetime

DB_PATH = Path("hotel.db")

def get_conn():
    return sqlite3.connect(DB_PATH)

def init_db():
    with get_conn() as conn:
        conn.executescript("""
        CREATE TABLE IF NOT EXISTS guests(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name  TEXT NOT NULL,
            phone TEXT NOT NULL,
            email TEXT NOT NULL
        );
        CREATE TABLE IF NOT EXISTS rooms(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            number INTEGER NOT NULL UNIQUE,
            type TEXT NOT NULL,
            price INTEGER NOT NULL,
            status TEXT NOT NULL DEFAULT 'available'
        );
        CREATE TABLE IF NOT EXISTS services(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name  TEXT NOT NULL,
            price INTEGER NOT NULL
        );
        CREATE TABLE IF NOT EXISTS bookings(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            guest_id INTEGER,
            room_id INTEGER,
            check_in TEXT,
            check_out TEXT,
            FOREIGN KEY(guest_id) REFERENCES guests(id),
            FOREIGN KEY(room_id) REFERENCES rooms(id)
        );
        CREATE TABLE IF NOT EXISTS booking_services(
            booking_id INTEGER,
            service_id INTEGER,
            PRIMARY KEY (booking_id, service_id),
            FOREIGN KEY(booking_id) REFERENCES bookings(id),
            FOREIGN KEY(service_id) REFERENCES services(id)
        );
        CREATE TABLE IF NOT EXISTS reports(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            created_at TEXT NOT NULL,
            content TEXT NOT NULL
        );
        """)
        conn.commit()

def add_guest(name, phone, email):
    with get_conn() as conn:
        conn.execute("INSERT INTO guests(name, phone, email) VALUES(?,?,?)",
                     (name, phone, email))
        conn.commit()
def get_room_numbers():
    """Получить список доступных номеров"""
    with get_conn() as conn:
        return conn.execute("SELECT id, number FROM rooms WHERE status = 'available'").fetchall()

def list_guests():
    """Получить список гостей"""
    with get_conn() as conn:
        return conn.execute("SELECT id, name FROM guests").fetchall()

def add_room(number, room_type, price):
    with get_conn() as conn:
        conn.execute("INSERT INTO rooms(number, type, price, status) VALUES(?,?,?,?)",
                    (number, room_type, price, 'available'))
        conn.commit()

def list_rooms():
    with get_conn() as conn:
        return conn.execute("SELECT id, number, type, price, status FROM rooms").fetchall()

def add_service(name, price):
    with get_conn() as conn:
        conn.execute("INSERT INTO services(name, price) VALUES(?,?)", (name, price))
        conn.commit()

def list_services():
    """Получить список услуг"""
    with get_conn() as conn:
        return conn.execute("SELECT id, name, price FROM services").fetchall()

def add_booking(guest_id, room_id, service_ids, check_in, check_out):
    with get_conn() as conn:
        # Создаем основную запись бронирования
        cur = conn.execute("""
            INSERT INTO bookings(guest_id, room_id, check_in, check_out)
            VALUES(?,?,?,?)
        """, (guest_id, room_id, check_in, check_out))
        booking_id = cur.lastrowid
        
        # Добавляем выбранные услуги
        for service_id in service_ids:
            conn.execute("""
                INSERT INTO booking_services(booking_id, service_id)
                VALUES(?,?)
            """, (booking_id, service_id))
        
        conn.commit()
        return booking_id

def report_bookings():
    with get_conn() as conn:
        # Получаем основную информацию о бронированиях
        bookings = conn.execute("""
            SELECT b.id, g.name, r.number, r.type, b.check_in, b.check_out
            FROM bookings b
            JOIN guests g ON g.id = b.guest_id
            JOIN rooms r ON r.id = b.room_id
            ORDER BY b.id
        """).fetchall()
        
        results = []
        for booking in bookings:
            booking_id = booking[0]
            # Получаем все услуги для этого бронирования
            services = conn.execute("""
                SELECT s.name, s.price 
                FROM booking_services bs
                JOIN services s ON s.id = bs.service_id
                WHERE bs.booking_id = ?
            """, (booking_id,)).fetchall()
            
            # Формируем строку с перечислением услуг
            service_list = ", ".join([f"{s[0]} ({s[1]} руб.)" for s in services])
            total_service_price = sum(s[1] for s in services)
            
            results.append((
                booking[0],  # ID бронирования
                booking[1],  # Имя гостя
                booking[2],  # Номер комнаты
                booking[3],  # Тип комнаты
                service_list,  # Список услуг
                total_service_price,  # Общая стоимость услуг
                booking[4],  # Дата заезда
                booking[5]   # Дата выезда
            ))
        
        return results


def add_report(content):
    with get_conn() as conn:
        cur = conn.execute(
            "INSERT INTO reports(created_at, content) VALUES(?,?)",
            (datetime.now().strftime('%Y-%m-%d %H:%M:%S'), content)
        )
        conn.commit()
        return cur.lastrowid

def list_reports():
    with get_conn() as conn:
        return conn.execute(
            "SELECT id, created_at FROM reports ORDER BY id DESC"
        ).fetchall()

def generate(self):
    bookings = report_bookings()
    lines = []
    
    for oid, guest, room, room_type, svc, price, check_in, check_out in bookings:
        lines.append(
            f"#{oid} | Гость: {guest} | Номер: {room} ({room_type}) | "
            f"Услуги: {svc} | Общая стоимость услуг: {price} руб. | "
            f"Въезд: {check_in} | Выезд: {check_out}"
        )
    
    content = "\n".join(lines) or "Бронирования отсутствуют"
    rep_id = add_report(content)
    self.refresh_history(select_id=rep_id)
    self.out.delete("1.0", tk.END)
    self.out.insert(tk.END, content)
    messagebox.showinfo("OK", f"Отчёт №{rep_id} сохранён")

def get_report(report_id):
    with get_conn() as conn:
        row = conn.execute(
            "SELECT content FROM reports WHERE id = ?", (report_id,)
        ).fetchone()
        return row[0] if row else ""
