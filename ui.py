import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox
from pathlib import Path
from datetime import datetime
from tabs import GuestsTab, RoomsTab, ServicesTab, BookingTab, ReportsTab

DB_PATH = Path("hotel.db")

def get_conn():
    return sqlite3.connect(DB_PATH)

class RoomsTab(ttk.Frame):
    """Вкладка 'Номера' с черным текстом"""
    def __init__(self, parent):
        super().__init__(parent)

        # Настройка стилей
        style = ttk.Style()
        style.configure("Black.TLabel", foreground="black")
        style.configure("Black.TButton", foreground="black")
        style.configure("Black.TEntry", foreground="black")
        style.configure("Black.TCombobox", foreground="black")

        # Поле для номера комнаты
        ttk.Label(self, text="Номер комнаты:", style="Black.TLabel").grid(row=0, column=0, padx=5, pady=5)
        self.number_var = tk.StringVar()
        ttk.Entry(self, textvariable=self.number_var, style="Black.TEntry").grid(row=0, column=1, padx=5, pady=5)

        # Поле для типа комнаты
        ttk.Label(self, text="Тип комнаты:", style="Black.TLabel").grid(row=1, column=0, padx=5, pady=5)
        self.type_var = tk.StringVar()
        self.type_cb = ttk.Combobox(self, textvariable=self.type_var, 
                                  values=["Одноместный", "Двухместный", "Люкс", "Апартаменты"],
                                  style="Black.TCombobox")
        self.type_cb.grid(row=1, column=1, padx=5, pady=5)
        self.type_cb.set("Выберите тип")

        # Поле для цены
        ttk.Label(self, text="Цена:", style="Black.TLabel").grid(row=2, column=0, padx=5, pady=5)
        self.price_var = tk.StringVar()
        ttk.Entry(self, textvariable=self.price_var, style="Black.TEntry").grid(row=2, column=1, padx=5, pady=5)

        # Кнопка сохранения
        self.save_btn = ttk.Button(self, text="Добавить номер", command=self.save_room, style="Black.TButton")
        self.save_btn.grid(row=3, column=1, padx=5, pady=5)

    def save_room(self):
        """Сохранение номера в базу"""
        try:
            number = self.number_var.get().strip()
            room_type = self.type_var.get().strip()
            price = self.price_var.get().strip()

            # Проверка введенных данных
            if not number.isdigit():
                messagebox.showerror("Ошибка", "Номер комнаты должен быть числом!")
                return

            if room_type not in ["Одноместный", "Двухместный", "Люкс", "Апартаменты"]:
                messagebox.showerror("Ошибка", "Выберите корректный тип комнаты!")
                return

            if not price.isdigit():
                messagebox.showerror("Ошибка", "Введите корректную цену!")
                return

            # Добавление номера в базу
            add_room(int(number), room_type, int(price))
            messagebox.showinfo("Успех", "Номер успешно добавлен!")
            
            # Очистка полей после успешного добавления
            self.number_var.set("")
            self.type_cb.set("Выберите тип")
            self.price_var.set("")

        except Exception as e:
            messagebox.showerror("Ошибка", f"Произошла ошибка: {str(e)}")

class MainWindow(tk.Tk):
    """Главное окно приложения"""
    def __init__(self):
        super().__init__()
        self.title("АРМ администратора гостиницы")
        self.geometry("900x500")
        
        # Установка иконки окна
        try:
            
            self.iconbitmap('hotel.ico')  # Укажите имя вашего файла иконки
            
        except Exception as e:
            print(f"Не удалось загрузить иконку: {e}")
            # Приложение продолжит работу без иконки
                
        # Создаем стиль для меню
        style = ttk.Style()

        # Общий фон окна
        style.configure("TFrame", background="#D3D3D3")  # Темно-серый фон

        # Стиль вкладок (Notebooks)
        style.configure("TNotebook", background="#404040")
        style.configure("TNotebook.Tab", background="#505050", foreground="white", padding=[10, 5], font=('Arial', 10))
        style.map("TNotebook.Tab", background=[("selected", "#606060")], foreground=[("selected", "white")])

        # Стиль кнопок
        style.configure("TButton", background="#606060", foreground="white", font=('Arial', 10))

        # Стиль меток (Label)
        style.configure("TLabel", background="#D3D3D3", foreground="white", font=('Arial', 10))

        
        # Стиль для вкладок (синие с черным текстом)
        style.configure("TNotebook", background="#3498db")
        style.configure("TNotebook.Tab", 
                      background="#2980b9",
                      foreground="black",  # Черный текст для вкладок
                      padding=[10, 5],
                      font=('Arial', 10))
        
        # Стиль для активной вкладки
        style.map("TNotebook.Tab",
                background=[("selected", "#3498db")],
                foreground=[("selected", "black")],  # Черный текст для активной вкладки
                expand=[("selected", [1, 1, 1, 0])])
        
        # Общий стиль для черного текста
        style.configure("TLabel", foreground="black")
        style.configure("TButton", foreground="black")
        style.configure("TEntry", foreground="black")
        style.configure("TCombobox", foreground="black")

        nb = ttk.Notebook(self)
        nb.pack(expand=True, fill="both")

        # Добавление вкладок
        nb.add(GuestsTab(nb), text="Гости")
        nb.add(RoomsTab(nb), text="Номера")
        nb.add(ServicesTab(nb), text="Услуги")
        nb.add(BookingTab(nb), text="Бронирование")
        nb.add(ReportsTab(nb), text="Отчёты")

        # Настройка фона
        self.configure(background="white")  # Белый фон для лучшей читаемости черного текста

if __name__ == "__main__":
    app = MainWindow()
    app.mainloop()