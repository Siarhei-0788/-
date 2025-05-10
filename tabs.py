from db import (
    add_guest, add_room, add_service, add_booking,
    list_guests, get_room_numbers, list_rooms,  # Добавьте эту строку
    list_services, report_bookings,
    add_report, list_reports, get_report
)
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from db import (add_guest, add_room, add_service, add_booking, 
                list_guests, list_rooms, list_services, report_bookings,
                add_report, list_reports, get_report)
from models import POPULARS, AUTHOR

# Гости 
class GuestsTab(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        ttk.Label(self, text="ФИО").pack()
        self.name_e = ttk.Entry(self); self.name_e.pack()
        ttk.Label(self, text="Телефон").pack()
        self.phone_e = ttk.Entry(self); self.phone_e.pack()
        ttk.Label(self, text="Email").pack()
        self.email_e = ttk.Entry(self); self.email_e.pack()
        ttk.Button(self, text="Сохранить гостя", command=self.save).pack()
        ttk.Label(self, text=AUTHOR).pack(side="bottom", pady=5)

    def save(self):
        add_guest(self.name_e.get(), self.phone_e.get(), self.email_e.get())
        messagebox.showinfo("OK", "Гость добавлен")

# Номера 
class RoomsTab(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.number_var = tk.StringVar()
        self.type_var   = tk.StringVar()
        self.price_var  = tk.StringVar()

        ttk.Label(self, text="Номер").pack()
        self.number_e = ttk.Entry(self, textvariable=self.number_var); self.number_e.pack()

        ttk.Label(self, text="Тип").pack()
        self.type_cb = ttk.Combobox(self, textvariable=self.type_var,
                                     values=POPULARS["room_types"])
        self.type_cb.pack()

        ttk.Label(self, text="Цена (руб/ночь)").pack()
        self.price_e = ttk.Entry(self); self.price_e.pack()

        ttk.Button(self, text="Сохранить номер", command=self.save).pack()
        ttk.Label(self, text=AUTHOR).pack(side="bottom", pady=5)

    def save(self):
        add_room(self.number_var.get(), self.type_var.get(), int(self.price_var.get()))
        messagebox.showinfo("OK", "Номер добавлен")

# Услуги
class ServicesTab(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.service_var = tk.StringVar()
        self.price_e     = ttk.Entry(self)

        ttk.Label(self, text="Услуга").pack()
        ttk.Combobox(self, textvariable=self.service_var,
                     values=POPULARS["hotel_services"]).pack()

        ttk.Label(self, text="Цена (руб)").pack()
        self.price_e.pack()

        ttk.Button(self, text="Сохранить услугу", command=self.save).pack()
        ttk.Label(self, text=AUTHOR).pack(side="bottom", pady=5)

    def save(self):
        add_service(self.service_var.get(), int(self.price_e.get()))
        messagebox.showinfo("OK", "Услуга добавлена")

# Бронирование 
class BookingTab(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        
        # Основной фрейм для всех элементов
        main_frame = ttk.Frame(self)
        main_frame.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)
        
        # Фрейм для кнопок
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=0, column=0, columnspan=2, pady=5, sticky=tk.EW)
        
        # Кнопка обновления
        refresh_btn = ttk.Button(button_frame, text="Обновить информацию", command=self.refresh_all)
        refresh_btn.pack(side=tk.LEFT, padx=5)
        
        # Гость
        ttk.Label(main_frame, text="Гость:").grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        self.guest_var = tk.StringVar()
        self.guest_cb = ttk.Combobox(main_frame, textvariable=self.guest_var)
        self.guest_cb.grid(row=1, column=1, padx=5, pady=5, sticky=tk.EW)
        
        # Номер
        ttk.Label(main_frame, text="Номер:").grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)
        self.room_var = tk.StringVar()
        self.room_cb = ttk.Combobox(main_frame, textvariable=self.room_var)
        self.room_cb.grid(row=2, column=1, padx=5, pady=5, sticky=tk.EW)
        
        # Даты
        ttk.Label(main_frame, text="Дата заезда:").grid(row=3, column=0, padx=5, pady=5, sticky=tk.W)
        self.check_in_var = tk.StringVar()
        ttk.Entry(main_frame, textvariable=self.check_in_var).grid(row=3, column=1, padx=5, pady=5, sticky=tk.EW)
        
        ttk.Label(main_frame, text="Дата выезда:").grid(row=4, column=0, padx=5, pady=5, sticky=tk.W)
        self.check_out_var = tk.StringVar()
        ttk.Entry(main_frame, textvariable=self.check_out_var).grid(row=4, column=1, padx=5, pady=5, sticky=tk.EW)
        
        # Услуги (множественный выбор)
        ttk.Label(main_frame, text="Услуги:").grid(row=5, column=0, padx=5, pady=5, sticky=tk.NW)
        self.services_listbox = tk.Listbox(main_frame, selectmode=tk.MULTIPLE, height=4)
        self.services_listbox.grid(row=5, column=1, padx=5, pady=5, sticky=tk.EW)
        
        # Кнопка сохранения
        self.save_btn = ttk.Button(main_frame, text="Забронировать", command=self.save_booking)
        self.save_btn.grid(row=6, column=0, columnspan=2, pady=10)
        
        # Заполнение данных
        self.refresh_all()
        
        # Настройка растягивания колонок
        main_frame.columnconfigure(1, weight=1)
    
    def refresh_all(self):
        """Обновить все данные из базы"""
        self.refresh_guests()
        self.refresh_rooms()
        self.refresh_services()
        messagebox.showinfo("Обновлено", "Данные успешно обновлены")
        
    def refresh_guests(self):
        guests = list_guests()
        self.guest_cb['values'] = [f"{g[0]}: {g[1]}" for g in guests]
        
    def refresh_rooms(self):
        rooms = get_room_numbers()
        self.room_cb['values'] = [f"{r[0]}: {r[1]}" for r in rooms]
        
    def refresh_services(self):
        services = list_services()
        self.services_listbox.delete(0, tk.END)
        for service in services:
            self.services_listbox.insert(tk.END, f"{service[0]}: {service[1]} ({service[2]} руб.)")
    
    def save_booking(self):
        try:
            guest_id = int(self.guest_var.get().split(":")[0])
            room_id = int(self.room_var.get().split(":")[0])
            check_in = self.check_in_var.get()
            check_out = self.check_out_var.get()
            
            # Получаем выбранные услуги
            selected_indices = self.services_listbox.curselection()
            service_ids = [int(self.services_listbox.get(i).split(":")[0]) for i in selected_indices]
            
            if not service_ids:
                messagebox.showwarning("Предупреждение", "Выберите хотя бы одну услугу")
                return
            
            # Проверка дат
            if not check_in or not check_out:
                messagebox.showwarning("Предупреждение", "Заполните даты заезда и выезда")
                return
            
            # Создаем бронирование
            booking_id = add_booking(guest_id, room_id, service_ids, check_in, check_out)
            messagebox.showinfo("Успех", f"Бронирование #{booking_id} создано!")
            
            # Очищаем поля и обновляем данные
            self.guest_var.set("")
            self.room_var.set("")
            self.check_in_var.set("")
            self.check_out_var.set("")
            self.services_listbox.selection_clear(0, tk.END)
            self.refresh_all()
            
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка при создании бронирования: {str(e)}")
   
    def refresh(self):
        self.guest_cb["values"]  = [f"{c[0]} - {c[1]}" for c in list_guests()]
        self.room_cb["values"]   = [f"{r[0]} - {r[1]}" for r in list_rooms()]
        self.service_cb["values"] = [f"{s[0]} - {s[1]}" for s in list_services()]

    def create_booking(self):
        if not (self.guest_cb.get() and self.room_cb.get() and self.service_cb.get() and 
                self.check_in_e.get() and self.check_out_e.get()):
            messagebox.showwarning("Ошибка", "Заполните все поля")
            return

        guest_id  = int(self.guest_cb.get().split(" - ")[0])
        room_id   = int(self.room_cb.get().split(" - ")[0])
        service_id = int(self.service_cb.get().split(" - ")[0])
        booking_id = add_booking(guest_id, room_id, service_id, 
                                 self.check_in_e.get(), self.check_out_e.get())

        messagebox.showinfo("OK", f"Бронирование №{booking_id} создано")

# Отчёты 
class ReportsTab(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.history = ttk.Treeview(self, columns=("date",), show="headings", height=6)
        self.history.heading("date", text="Создан")
        self.history.pack(side="left", fill="y")
        self.history.bind("<<TreeviewSelect>>", self.load_selected)

        right = ttk.Frame(self); right.pack(expand=True, fill="both", side="left")
        ttk.Button(right, text="Сформировать новый отчёт", command=self.generate).pack()
        self.out = tk.Text(right); self.out.pack(expand=True, fill="both")
        self.refresh_history()

    def generate(self):
        bookings = report_bookings()
        print("Найдено бронирований:", len(bookings))  # Проверка

        lines = []
        for oid, guest, room, room_type, svc, price, check_in, check_out in bookings:
            lines.append(f"#{oid} | Гость: {guest} | Номер: {room} | Услуга: {svc} | Цена: {price} руб. | Въезд: {check_in} | Выезд: {check_out}")

        content = "\n".join(lines) or "Бронирования отсутствуют"
        rep_id = add_report(content)  
        self.refresh_history(select_id=rep_id)
        self.out.delete("1.0", tk.END)
        self.out.insert(tk.END, content)
        messagebox.showinfo("OK", f"Отчёт №{rep_id} сохранён")


    def refresh_history(self, select_id=None):
        for i in self.history.get_children():
            self.history.delete(i)
        for rid, dt in list_reports():
            self.history.insert("", "end", iid=str(rid), values=(dt,))
        if select_id:
            self.history.selection_set(str(select_id))

    def load_selected(self, _):
        sel = self.history.selection()
        if sel:
            rid = int(sel[0])
            content = get_report(rid)
            self.out.delete("1.0", tk.END)
            self.out.insert(tk.END, content)
