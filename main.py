import sqlite3
import pandas as pd
from fpdf import FPDF
from tkinter import *
from tkinter import messagebox, ttk, simpledialog, filedialog
from datetime import datetime

# Создание базы данных и таблиц
def create_database():
    conn = sqlite3.connect('auto_parts.db')
    cursor = conn.cursor()

    # Таблица автозапчастей
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS parts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            category TEXT NOT NULL,
            manufacturer TEXT NOT NULL,
            supplier TEXT NOT NULL,
            price REAL NOT NULL,
            quantity INTEGER NOT NULL
        )
    ''')

    # Таблица клиентов
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS clients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            full_name TEXT NOT NULL,
            phone TEXT NOT NULL
        )
    ''')

    # Таблица заказов
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            client_id INTEGER NOT NULL,
            part_id INTEGER NOT NULL,
            quantity INTEGER NOT NULL,
            order_date TEXT NOT NULL,
            status TEXT DEFAULT 'Новый',
            FOREIGN KEY (client_id) REFERENCES clients(id),
            FOREIGN KEY (part_id) REFERENCES parts(id)
        )
    ''')

    conn.commit()
    conn.close()


# Функции для работы с таблицами
def add_part(name, category, manufacturer, supplier, price, quantity):
    conn = sqlite3.connect('auto_parts.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO parts (name, category, manufacturer, supplier, price, quantity)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (name, category, manufacturer, supplier, price, quantity))
    conn.commit()
    conn.close()


def view_parts():
    conn = sqlite3.connect('auto_parts.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM parts')
    rows = cursor.fetchall()
    conn.close()
    return rows


def add_client(full_name, phone):
    conn = sqlite3.connect('auto_parts.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO clients (full_name, phone)
        VALUES (?, ?)
    ''', (full_name, phone))
    conn.commit()
    conn.close()


def view_clients():
    conn = sqlite3.connect('auto_parts.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM clients')
    rows = cursor.fetchall()
    conn.close()
    return rows

def view_suppliers():
    conn = sqlite3.connect('auto_parts.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM suppliers')
    rows = cursor.fetchall()
    conn.close()
    return rows

def add_order(client_id, part_id, quantity, order_date, status="Новый"):
    conn = sqlite3.connect('auto_parts.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO orders (client_id, part_id, quantity, order_date, status)
        VALUES (?, ?, ?, ?, ?)
    ''', (client_id, part_id, quantity, order_date, status))
    conn.commit()
    conn.close()


def get_order_details():
    conn = sqlite3.connect('auto_parts.db')
    cursor = conn.cursor()

    cursor.execute('''
        SELECT 
            orders.id,
            clients.full_name AS client_name,
            parts.name AS part_name,
            orders.quantity,
            orders.order_date,
            orders.status
        FROM orders
        JOIN clients ON orders.client_id = clients.id
        JOIN parts ON orders.part_id = parts.id
    ''')
    rows = cursor.fetchall()
    conn.close()

    # Отладочный вывод
    print("Данные из get_order_details:", rows)

    # Форматируем дату
    formatted_rows = []
    for row in rows:
        formatted_date = format_order_date(row[4])
        formatted_rows.append((row[0], row[1], row[2], row[3], formatted_date, row[5]))

    return formatted_rows

def update_order_status(order_id, new_status):
    conn = sqlite3.connect('auto_parts.db')
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE orders SET status = ? WHERE id = ?
    ''', (new_status, order_id))
    conn.commit()
    conn.close()

def format_order_date(order_date):
    try:
        return datetime.strptime(order_date, "%Y-%m-%d %H:%M:%S").strftime("%d.%m.%Y %H:%M")
    except ValueError:
        return order_date


def select_client():
    clients = view_clients()
    if not clients:
        messagebox.showwarning("Ошибка", "Список клиентов пуст!")
        return None

    top = Toplevel()
    top.title("Выбор клиента")

    tree = ttk.Treeview(top, columns=("ID", "ФИО", "Телефон"), show="headings")
    tree.heading("ID", text="ID")
    tree.heading("ФИО", text="ФИО")
    tree.heading("Телефон", text="Телефон")
    tree.pack(pady=10)

    for client in clients:
        tree.insert("", END, values=client)

    selected_client_id = None  # Переменная для хранения выбранного ID клиента

    def on_select():
        nonlocal selected_client_id
        selected_item = tree.selection()
        if not selected_item:
            messagebox.showwarning("Ошибка", "Клиент не выбран!")
            return
        selected_client_id = tree.item(selected_item[0])['values'][0]
        top.destroy()

    Button(top, text="Выбрать", command=on_select).pack(pady=5)

    top.wait_window()  # Ожидаем закрытия окна
    return selected_client_id

def select_parts():
    parts = view_parts()
    if not parts:
        messagebox.showwarning("Ошибка", "Список автозапчастей пуст!")
        return None

    top = Toplevel()
    top.title("Выбор автозапчастей")

    tree = ttk.Treeview(top, columns=("ID", "Название", "Цена", "Количество"), show="headings")
    tree.heading("ID", text="ID")
    tree.heading("Название", text="Название")
    tree.heading("Цена", text="Цена")
    tree.heading("Количество", text="Количество")
    tree.pack(pady=10)

    for part in parts:
        tree.insert("", END, values=(part[0], part[1], part[5], part[6]))

    selected_parts = []

    def add_part():
        selected_item = tree.selection()
        if not selected_item:
            messagebox.showwarning("Ошибка", "Автозапчасть не выбрана!")
            return
        part_id = tree.item(selected_item[0])['values'][0]
        part_name = tree.item(selected_item[0])['values'][1]
        part_price = float(tree.item(selected_item[0])['values'][2])  # Преобразование строки в число
        part_quantity = int(tree.item(selected_item[0])['values'][3])  # Преобразование строки в число

        quantity = simpledialog.askinteger("Количество", f"Введите количество для {part_name}:")
        if not quantity or quantity > part_quantity:
            messagebox.showwarning("Ошибка", f"Недостаточно запчастей ({part_quantity} доступно)!")
            return

        selected_parts.append((part_id, part_name, part_price, quantity))
        update_cart()

    cart_tree = ttk.Treeview(top, columns=("ID", "Название", "Цена", "Количество"), show="headings")
    cart_tree.heading("ID", text="ID")
    cart_tree.heading("Название", text="Название")
    cart_tree.heading("Цена", text="Цена")
    cart_tree.heading("Количество", text="Количество")
    cart_tree.pack(pady=10)

    def update_cart():
        for i in cart_tree.get_children():
            cart_tree.delete(i)
        for part in selected_parts:
            cart_tree.insert("", END, values=part)

    Button(top, text="Добавить в заказ", command=add_part).pack(side=LEFT, padx=5)

    def confirm_order():
        if not selected_parts:
            messagebox.showwarning("Ошибка", "Заказ пуст!")
            return
        top.destroy()
        return selected_parts

    Button(top, text="Подтвердить заказ", command=lambda: confirm_order()).pack(side=LEFT, padx=5)

    top.wait_window()  # Ожидаем закрытия окна
    return selected_parts
def create_order():
    client_id = select_client()
    if not client_id:
        return

    selected_parts = select_parts()
    if not selected_parts:
        return

    order_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    conn = sqlite3.connect('auto_parts.db')
    cursor = conn.cursor()

    total_price = 0.0  # Инициализация с плавающей точкой

    try:
        for part in selected_parts:
            part_id, _, price_str, quantity_str = part  # Предполагаем, что price и quantity могут быть строками

            # Преобразование строк в числа
            price = float(price_str)
            quantity = int(quantity_str)

            # Добавление заказа в базу данных
            cursor.execute('''
                INSERT INTO orders (client_id, part_id, quantity, order_date, status)
                VALUES (?, ?, ?, ?, ?)
            ''', (client_id, part_id, quantity, order_date, "Новый"))

            # Уменьшение количества запчастей на складе
            cursor.execute('''
                UPDATE parts SET quantity = quantity - ? WHERE id = ?
            ''', (quantity, part_id))

            total_price += price * quantity

        conn.commit()
        messagebox.showinfo("Успешно", f"Заказ создан! Общая стоимость: {total_price:.2f}")

    except Exception as e:
        conn.rollback()
        messagebox.showerror("Ошибка", f"Не удалось создать заказ: {e}")
    finally:
        conn.close()

    app.update_orders_table()

# GUI для управления программой
class AutoPartsApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Автоматизированное рабочее место продавца автозапчастей")

        # Меню
        menu = Menu(root)
        root.config(menu=menu)

        reference_menu = Menu(menu, tearoff=0)
        menu.add_cascade(label="Справочники", menu=reference_menu)
        reference_menu.add_command(label="Клиенты", command=lambda: self.show_reference("clients"))
        reference_menu.add_command(label="Заказы", command=self.show_orders)

        file_menu = Menu(menu, tearoff=0)
        menu.add_cascade(label="Файл", menu=file_menu)
        file_menu.add_command(label="Выход", command=root.quit)

        report_menu = Menu(menu, tearoff=0)
        menu.add_cascade(label="Отчеты", menu=report_menu)
        report_menu.add_command(label="Создать PDF отчет", command=self.generate_pdf_report)

        file_menu.add_command(label="Экспорт в Excel", command=self.export_to_excel)
        file_menu.add_command(label="Импорт из Excel", command=self.import_from_excel)

        help_menu = Menu(menu, tearoff=0)
        menu.add_cascade(label="Помощь", menu=help_menu)
        help_menu.add_command(label="Руководство", command=self.show_guide)

        # Главный фрейм для таблицы автозапчастей
        main_frame = Frame(root)
        main_frame.pack(pady=10)

        Label(main_frame, text="Таблица автозапчастей").pack()

        # Список автозапчастей
        self.parts_tree = ttk.Treeview(main_frame, columns=("ID", "Name", "Category", "Manufacturer", "Supplier", "Price", "Quantity"), show="headings")
        self.parts_tree.pack(pady=10)
        self.parts_tree.heading("ID", text="ID")
        self.parts_tree.heading("Name", text="Название")
        self.parts_tree.heading("Category", text="Категория")
        self.parts_tree.heading("Manufacturer", text="Производитель")
        self.parts_tree.heading("Supplier", text="Поставщик")
        self.parts_tree.heading("Price", text="Цена")
        self.parts_tree.heading("Quantity", text="Количество")
        self.update_parts_list()

        Button(main_frame, text="Добавить", command=self.add_part_form).pack(side=LEFT, padx=5)
        Button(main_frame, text="Редактировать", command=self.edit_part).pack(side=LEFT, padx=5)
        Button(main_frame, text="Удалить", command=self.delete_part).pack(side=LEFT, padx=5)
        Button(main_frame, text="Создать заказ", command=create_order).pack(side=LEFT, padx=5)

        # Таблица заказов
        self.orders_tree = None

    def update_parts_list(self):
        for i in self.parts_tree.get_children():
            self.parts_tree.delete(i)
        parts = view_parts()
        for part in parts:
            self.parts_tree.insert("", END, values=part)

    def add_part_form(self):
        top = Toplevel(self.root)
        top.title("Добавить автозапчасть")

        Label(top, text="Название:").grid(row=0, column=0)
        name_entry = Entry(top)
        name_entry.grid(row=0, column=1)

        Label(top, text="Категория:").grid(row=1, column=0)
        category_entry = Entry(top)
        category_entry.grid(row=1, column=1)

        Label(top, text="Производитель:").grid(row=2, column=0)
        manufacturer_entry = Entry(top)
        manufacturer_entry.grid(row=2, column=1)

        Label(top, text="Поставщик:").grid(row=3, column=0)
        supplier_entry = Entry(top)
        supplier_entry.grid(row=3, column=1)

        Label(top, text="Цена:").grid(row=4, column=0)
        price_entry = Entry(top)
        price_entry.grid(row=4, column=1)

        Label(top, text="Количество:").grid(row=5, column=0)
        quantity_entry = Entry(top)
        quantity_entry.grid(row=5, column=1)

        Button(top, text="Сохранить", command=lambda: self.save_part(name_entry.get(), category_entry.get(), manufacturer_entry.get(), supplier_entry.get(), price_entry.get(), quantity_entry.get(), top)).grid(row=6, column=0, columnspan=2)

    def save_part(self, name, category, manufacturer, supplier, price, quantity, window):
        add_part(name, category, manufacturer, supplier, float(price), int(quantity))
        messagebox.showinfo("Успешно", "Автозапчасть добавлена!")
        window.destroy()
        self.update_parts_list()

    def edit_part(self):
        selected_item = self.parts_tree.selection()[0]
        part_id = self.parts_tree.item(selected_item)['values'][0]

        self.edit_part_form(part_id)

    def edit_part_form(self, part_id):
        top = Toplevel(self.root)
        top.title("Редактировать автозапчасть")

        part = [p for p in view_parts() if p[0] == part_id][0]

        Label(top, text="Название:").grid(row=0, column=0)
        name_entry = Entry(top)
        name_entry.insert(0, part[1])
        name_entry.grid(row=0, column=1)

        Label(top, text="Категория:").grid(row=1, column=0)
        category_entry = Entry(top)
        category_entry.insert(0, part[2])
        category_entry.grid(row=1, column=1)

        Label(top, text="Производитель:").grid(row=2, column=0)
        manufacturer_entry = Entry(top)
        manufacturer_entry.insert(0, part[3])
        manufacturer_entry.grid(row=2, column=1)

        Label(top, text="Поставщик:").grid(row=3, column=0)
        supplier_entry = Entry(top)
        supplier_entry.insert(0, part[4])
        supplier_entry.grid(row=3, column=1)

        Label(top, text="Цена:").grid(row=4, column=0)
        price_entry = Entry(top)
        price_entry.insert(0, part[5])
        price_entry.grid(row=4, column=1)

        Label(top, text="Количество:").grid(row=5, column=0)
        quantity_entry = Entry(top)
        quantity_entry.insert(0, part[6])
        quantity_entry.grid(row=5, column=1)

        Button(top, text="Сохранить",
               command=lambda: self.update_part(part_id, name_entry.get(), category_entry.get(),
                                                manufacturer_entry.get(), supplier_entry.get(), price_entry.get(),
                                                quantity_entry.get(), top)).grid(row=6, column=0, columnspan=2)

    def update_part(self, part_id, name, category, manufacturer, supplier, price, quantity, window):
        conn = sqlite3.connect('auto_parts.db')
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE parts SET name = ?, category = ?, manufacturer = ?, supplier = ?, price = ?, quantity = ? WHERE id = ?
        ''', (name, category, manufacturer, supplier, float(price), int(quantity), part_id))
        conn.commit()
        conn.close()

        messagebox.showinfo("Успешно", "Автозапчасть обновлена!")
        window.destroy()
        self.update_parts_list()

    def delete_part(self):
        selected_item = self.parts_tree.selection()[0]
        part_id = self.parts_tree.item(selected_item)['values'][0]

        conn = sqlite3.connect('auto_parts.db')
        cursor = conn.cursor()
        cursor.execute('DELETE FROM parts WHERE id = ?', (part_id,))
        conn.commit()
        conn.close()

        messagebox.showinfo("Успешно", f"Автозапчасть {part_id} удалена!")
        self.parts_tree.delete(selected_item)

    def add_client_form(self, parent):
        top = Toplevel(parent)
        top.title("Добавить клиента")

        Label(top, text="ФИО:").grid(row=0, column=0)
        full_name_entry = Entry(top)
        full_name_entry.grid(row=0, column=1)

        Label(top, text="Телефон:").grid(row=1, column=0)
        phone_entry = Entry(top)
        phone_entry.grid(row=1, column=1)

        def save_client():
            full_name = full_name_entry.get()
            phone = phone_entry.get()

            if not full_name or not phone:
                messagebox.showwarning("Ошибка", "Заполните все поля!")
                return

            add_client(full_name, phone)
            messagebox.showinfo("Успешно", "Клиент добавлен!")
            top.destroy()

        Button(top, text="Сохранить", command=save_client).grid(row=2, column=0, columnspan=2)

    def update_orders_table(self):
        if self.orders_tree:
            for i in self.orders_tree.get_children():
                self.orders_tree.delete(i)
            data = get_order_details()
            for row in data:
                self.orders_tree.insert("", END, values=row)

    def show_reference(self, reference_type):
        top = Toplevel(self.root)
        top.title(reference_type.capitalize())

        if reference_type == "clients":
            columns = ["ID", "ФИО", "Телефон"]
            data = view_clients()
            add_func = lambda: self.add_client_form(top)
        elif reference_type == "suppliers":
            columns = ["ID", "Название", "Телефон"]
            data = view_suppliers()
            add_func = lambda: self.add_supplier_form(top)

        tree = ttk.Treeview(top, columns=columns, show="headings")
        for col in columns:
            tree.heading(col, text=col)
        tree.pack(pady=10)

        for row in data:
            tree.insert("", END, values=row)

        Button(top, text="Добавить", command=add_func).pack(side=LEFT, padx=5)
        Button(top, text="Редактировать", command=lambda: self.edit_record(tree, reference_type)).pack(side=LEFT,
                                                                                                       padx=5)
        Button(top, text="Удалить", command=lambda: self.delete_record(tree, reference_type)).pack(side=LEFT, padx=5)

    def show_orders(self):
        top = Toplevel(self.root)
        top.title("Заказы")

        # Фильтр по статусу
        Label(top, text="Фильтр по статусу:").grid(row=0, column=0)
        status_var = StringVar(top)
        status_var.set("Все")  # Значение по умолчанию
        status_options = ["Все", "Новый", "В обработке", "Выполнен", "Отменён"]
        status_menu = OptionMenu(top, status_var, *status_options)
        status_menu.grid(row=0, column=1)

        def filter_orders():
            selected_status = status_var.get()
            if selected_status == "Все":
                data = get_order_details()
            else:
                data = [order for order in get_order_details() if order[5] == selected_status]
            self.update_orders_table_with_data(data)

        Button(top, text="Применить фильтр", command=filter_orders).grid(row=0, column=2, padx=5)

        # Таблица заказов
        columns = ["ID", "Клиент", "Запчасть", "Количество", "Дата заказа", "Статус"]
        self.orders_tree = ttk.Treeview(top, columns=columns, show="headings")
        for col in columns:
            self.orders_tree.heading(col, text=col)
        self.orders_tree.grid(row=1, column=0, columnspan=3, pady=10)

        # Инициализация таблицы
        self.update_orders_table()

        # Кнопки управления заказами
        Button(top, text="Изменить статус", command=lambda: self.change_order_status(self.orders_tree)).grid(row=2,
                                                                                                             column=0,
                                                                                                             pady=5)
        Button(top, text="Редактировать", command=lambda: self.edit_record(self.orders_tree, "orders")).grid(row=2,
                                                                                                             column=1,
                                                                                                             pady=5)
        Button(top, text="Удалить", command=lambda: self.delete_record(self.orders_tree, "orders")).grid(row=2,
                                                                                                         column=2,
                                                                                                         pady=5)

    def update_orders_table(self):
        if self.orders_tree:
            for i in self.orders_tree.get_children():
                self.orders_tree.delete(i)
            data = get_order_details()
            for row in data:
                self.orders_tree.insert("", END, values=row)

    def update_orders_table_with_data(self, data):
        if self.orders_tree:
            for i in self.orders_tree.get_children():
                self.orders_tree.delete(i)
            for row in data:
                self.orders_tree.insert("", END, values=row)

    def change_order_status(self, tree):
        selected_item = tree.selection()
        if not selected_item:
            messagebox.showwarning("Ошибка", "Заказ не выбран!")
            return
        order_id = tree.item(selected_item[0])['values'][0]
        current_status = tree.item(selected_item[0])['values'][5]

        top = Toplevel(self.root)
        top.title("Изменение статуса заказа")

        Label(top, text="Текущий статус:").grid(row=0, column=0)
        Label(top, text=current_status).grid(row=0, column=1)

        Label(top, text="Новый статус:").grid(row=1, column=0)
        status_var = StringVar(top)
        status_var.set(current_status)  # Установка текущего статуса как значения по умолчанию
        status_options = ["Новый", "В обработке", "Выполнен", "Отменён"]
        status_menu = OptionMenu(top, status_var, *status_options)
        status_menu.grid(row=1, column=1)

        def save_status():
            new_status = status_var.get()
            update_order_status(order_id, new_status)
            messagebox.showinfo("Успешно", f"Статус заказа {order_id} изменен на '{new_status}'!")
            top.destroy()
            self.update_orders_table()

        Button(top, text="Сохранить", command=save_status).grid(row=2, column=0, columnspan=2)

    def edit_record(self, tree, reference_type):
        selected_item = tree.selection()
        if not selected_item:
            messagebox.showwarning("Ошибка", "Запись не выбрана!")
            return
        record_id = tree.item(selected_item[0])['values'][0]

        if reference_type == "clients":
            self.edit_client_form(record_id)
        elif reference_type == "orders":
            self.edit_order_form(record_id)

    def edit_order_form(self, order_id):
        top = Toplevel(self.root)
        top.title("Редактировать заказ")

        order = [o for o in get_order_details() if o[0] == order_id][0]

        Label(top, text="Клиент:").grid(row=0, column=0)
        client_name_label = Label(top, text=order[1])
        client_name_label.grid(row=0, column=1)

        Label(top, text="Запчасть:").grid(row=1, column=0)
        part_name_label = Label(top, text=order[2])
        part_name_label.grid(row=1, column=1)

        Label(top, text="Количество:").grid(row=2, column=0)
        quantity_entry = Entry(top)
        quantity_entry.insert(0, order[3])
        quantity_entry.grid(row=2, column=1)

        Label(top, text="Дата заказа:").grid(row=3, column=0)
        date_label = Label(top, text=order[4])
        date_label.grid(row=3, column=1)

        Label(top, text="Статус:").grid(row=4, column=0)
        status_var = StringVar(top)
        status_var.set(order[5])  # Установка текущего статуса как значения по умолчанию
        status_options = ["Новый", "В обработке", "Выполнен", "Отменён"]
        status_menu = OptionMenu(top, status_var, *status_options)
        status_menu.grid(row=4, column=1)

        def save_order():
            new_quantity = quantity_entry.get()
            new_status = status_var.get()
            conn = sqlite3.connect('auto_parts.db')
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE orders SET quantity = ?, status = ? WHERE id = ?
            ''', (int(new_quantity), new_status, order_id))
            conn.commit()
            conn.close()

            messagebox.showinfo("Успешно", "Заказ обновлен!")
            top.destroy()
            self.update_orders_table()

        Button(top, text="Сохранить", command=save_order).grid(row=5, column=0, columnspan=2)

    def delete_record(self, tree, reference_type):
        selected_item = tree.selection()
        if not selected_item:
            messagebox.showwarning("Ошибка", "Запись не выбрана!")
            return
        record_id = tree.item(selected_item[0])['values'][0]

        if reference_type == "orders":
            conn = sqlite3.connect('auto_parts.db')
            cursor = conn.cursor()
            cursor.execute('DELETE FROM orders WHERE id = ?', (record_id,))
            conn.commit()
            conn.close()

            messagebox.showinfo("Успешно", f"Заказ {record_id} удален!")
            tree.delete(selected_item)
            self.update_orders_table()

    def generate_pdf_report(self):
        data = get_order_details()
        if not data:
            messagebox.showwarning("Ошибка", "Нет данных для создания отчета!")
            return

        pdf = FPDF()
        pdf.add_page()
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.set_font("Arial", size=12)

        # Заголовок
        pdf.cell(200, 10, txt="Отчет по заказам", ln=True, align="C")
        pdf.ln(10)

        # Заголовки таблицы
        headers = ["ID", "Клиент", "Запчасть", "Количество", "Дата заказа", "Статус"]
        for header in headers:
            pdf.cell(33, 10, txt=header, border=1)

        pdf.ln()

        # Данные таблицы
        for row in data:
            for item in row:
                pdf.cell(33, 10, txt=str(item), border=1)
            pdf.ln()

        # Сохранение файла
        file_path = "order_report.pdf"
        pdf.output(file_path)
        messagebox.showinfo("Успешно", f"Отчет сохранен в файл: {file_path}")

    def export_to_excel(self):
        data = get_order_details()
        if not data:
            messagebox.showwarning("Ошибка", "Нет данных для экспорта!")
            return

        df = pd.DataFrame(data, columns=["ID", "Клиент", "Запчасть", "Количество", "Дата заказа", "Статус"])
        file_path = "orders_export.xlsx"
        df.to_excel(file_path, index=False)
        messagebox.showinfo("Успешно", f"Данные экспортированы в файл: {file_path}")

    def import_from_excel(self):
        file_path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx")])
        if not file_path:
            return

        try:
            df = pd.read_excel(file_path)
            conn = sqlite3.connect('auto_parts.db')
            cursor = conn.cursor()

            for _, row in df.iterrows():
                cursor.execute('''
                    INSERT INTO orders (client_id, part_id, quantity, order_date, status)
                    VALUES (?, ?, ?, ?, ?)
                ''', (row['client_id'], row['part_id'], row['quantity'], row['order_date'], row['status']))

            conn.commit()
            messagebox.showinfo("Успешно", "Данные импортированы!")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось импортировать данные: {e}")
        finally:
            conn.close()

    def show_guide(self):
        top = Toplevel(self.root)
        top.title("Руководство пользователя")

        guide_text = """
        Руководство по использованию программы:

        1. Добавление автозапчастей:
           - Перейдите в раздел "Автозапчасти".
           - Нажмите "Добавить" и заполните форму.

        2. Создание заказа:
           - Нажмите "Создать заказ".
           - Выберите клиента и необходимые запчасти.

        3. Управление заказами:
           - Просматривайте, редактируйте и удаляйте заказы в разделе "Заказы".

        4. Генерация отчетов:
           - Создайте PDF-отчет через меню "Отчеты".

        5. Импорт/Экспорт данных:
           - Используйте меню "Файл" для импорта и экспорта данных в Excel.
        """

        Label(top, text=guide_text, justify=LEFT).pack(padx=10, pady=10)

if __name__ == "__main__":
    create_database()
    root = Tk()
    app = AutoPartsApp(root)
    root.mainloop()
