import tkinter as tk
from tkinter import messagebox, ttk
import sqlite3
from datetime import datetime

# Подключение к базе данных SQLite
conn = sqlite3.connect('auto_parts.db')
cursor = conn.cursor()

# Создание таблицы cars (марки и модели авто)
cursor.execute('''
    CREATE TABLE IF NOT EXISTS cars (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        brand TEXT NOT NULL,
        model TEXT NOT NULL
    )
''')

# Создание или обновление таблицы parts (запчасти с количеством)
cursor.execute('''
    CREATE TABLE IF NOT EXISTS parts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        articul TEXT NOT NULL,
        price REAL NOT NULL,
        category TEXT NOT NULL,
        car_id INTEGER,
        quantity INTEGER NOT NULL DEFAULT 0,
        FOREIGN KEY(car_id) REFERENCES cars(id)
    )
''')

# Проверка наличия столбца quantity и его добавление, если его нет
cursor.execute("PRAGMA table_info(parts)")
columns = [column[1] for column in cursor.fetchall()]
if "quantity" not in columns:
    cursor.execute('ALTER TABLE parts ADD COLUMN quantity INTEGER NOT NULL DEFAULT 0')
    conn.commit()

# Создание таблицы clients (клиенты)
cursor.execute('''
    CREATE TABLE IF NOT EXISTS clients (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        phone TEXT NOT NULL
    )
''')

# Создание таблицы orders (заказы)
cursor.execute('''
    CREATE TABLE IF NOT EXISTS orders (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        client_id INTEGER NOT NULL,
        order_date TEXT NOT NULL,
        FOREIGN KEY(client_id) REFERENCES clients(id)
    )
''')

# Создание таблицы order_parts (связь заказов и запчастей)
cursor.execute('''
    CREATE TABLE IF NOT EXISTS order_parts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        order_id INTEGER NOT NULL,
        part_id INTEGER NOT NULL,
        quantity INTEGER NOT NULL,
        FOREIGN KEY(order_id) REFERENCES orders(id),
        FOREIGN KEY(part_id) REFERENCES parts(id)
    )
''')

# Глобальные переменные
selected_order_id = None


# Функция для получения списка автомобилей
def get_cars():
    cursor.execute('SELECT id, brand, model FROM cars')
    return cursor.fetchall()


# Функция для добавления новой машины
def add_car():
    brand = entry_brand.get()
    model = entry_model.get()

    if brand and model:
        cursor.execute('INSERT INTO cars (brand, model) VALUES (?, ?)', (brand, model))
        conn.commit()
        messagebox.showinfo("Успех", "Машина успешно добавлена!")
        clear_car_entries()
        view_cars()
    else:
        messagebox.showerror("Ошибка", "Все поля должны быть заполнены.")


# Функция для просмотра всех машин
def view_cars():
    tree_cars.delete(*tree_cars.get_children())
    cursor.execute('SELECT * FROM cars')
    rows = cursor.fetchall()
    for row in rows:
        tree_cars.insert("", "end", values=row)


# Функция для удаления машины
def delete_car():
    selected_item = tree_cars.selection()
    if not selected_item:
        messagebox.showerror("Ошибка", "Выберите машину для удаления.")
        return

    car_id = tree_cars.item(selected_item)['values'][0]
    cursor.execute('DELETE FROM cars WHERE id = ?', (car_id,))
    conn.commit()
    tree_cars.delete(selected_item)
    messagebox.showinfo("Успех", "Машина успешно удалена!")


# Функция для редактирования машины
def edit_car():
    selected_item = tree_cars.selection()
    if not selected_item:
        messagebox.showerror("Ошибка", "Выберите машину для редактирования.")
        return

    car_id = tree_cars.item(selected_item)['values'][0]
    brand = entry_brand.get()
    model = entry_model.get()

    if brand and model:
        cursor.execute('UPDATE cars SET brand = ?, model = ? WHERE id = ?', (brand, model, car_id))
        conn.commit()
        messagebox.showinfo("Успех", "Машина успешно обновлена!")
        clear_car_entries()
        view_cars()
    else:
        messagebox.showerror("Ошибка", "Все поля должны быть заполнены.")


# Функция для очистки полей ввода машин
def clear_car_entries():
    entry_brand.delete(0, tk.END)
    entry_model.delete(0, tk.END)


# Функция для создания окна добавления новой запчасти
def open_add_part_window():
    def add_part():
        name = entry_name.get()
        articul = entry_articul.get()
        price = entry_price.get()
        category = entry_category.get()
        selected_car = combo_car.get()
        quantity = entry_quantity.get()  # Новое поле: Количество

        if name and articul and price and category and selected_car and quantity.isdigit():
            try:
                price = float(price)
                quantity = int(quantity)  # Преобразуем количество в целое число
                car_id = None
                cars = get_cars()
                for car in cars:
                    if f"{car[1]} {car[2]}" == selected_car:
                        car_id = car[0]
                        break

                if car_id is None:
                    messagebox.showerror("Ошибка", "Автомобиль не найден.")
                    return

                cursor.execute(
                    'INSERT INTO parts (name, articul, price, category, car_id, quantity) VALUES (?, ?, ?, ?, ?, ?)',
                    (name, articul, price, category, car_id, quantity))  # Добавляем поле quantity
                conn.commit()
                messagebox.showinfo("Успех", "Запчасть успешно добавлена!")
                add_part_window.destroy()
                view_parts()
            except ValueError:
                messagebox.showerror("Ошибка", "Цена должна быть числом, а количество — целым числом.")
        else:
            messagebox.showerror("Ошибка", "Все поля должны быть заполнены корректно.")

    add_part_window = tk.Toplevel(root)
    add_part_window.title("Добавление запчасти")

    label_name = tk.Label(add_part_window, text="Название:")
    label_name.grid(row=0, column=0, padx=5, pady=5)
    entry_name = tk.Entry(add_part_window)
    entry_name.grid(row=0, column=1, padx=5, pady=5)

    label_articul = tk.Label(add_part_window, text="Артикул:")
    label_articul.grid(row=1, column=0, padx=5, pady=5)
    entry_articul = tk.Entry(add_part_window)
    entry_articul.grid(row=1, column=1, padx=5, pady=5)

    label_price = tk.Label(add_part_window, text="Цена:")
    label_price.grid(row=2, column=0, padx=5, pady=5)
    entry_price = tk.Entry(add_part_window)
    entry_price.grid(row=2, column=1, padx=5, pady=5)

    label_category = tk.Label(add_part_window, text="Категория:")
    label_category.grid(row=3, column=0, padx=5, pady=5)
    entry_category = tk.Entry(add_part_window)
    entry_category.grid(row=3, column=1, padx=5, pady=5)

    label_car = tk.Label(add_part_window, text="Автомобиль:")
    label_car.grid(row=4, column=0, padx=5, pady=5)
    combo_car = ttk.Combobox(add_part_window, state="readonly")
    combo_car['values'] = [f"{car[1]} {car[2]}" for car in get_cars()]
    combo_car.grid(row=4, column=1, padx=5, pady=5)

    # Новое поле: Количество
    label_quantity = tk.Label(add_part_window, text="Количество:")
    label_quantity.grid(row=5, column=0, padx=5, pady=5)
    entry_quantity = tk.Entry(add_part_window)
    entry_quantity.grid(row=5, column=1, padx=5, pady=5)

    button_add = tk.Button(add_part_window, text="Добавить", command=add_part)
    button_add.grid(row=6, column=0, columnspan=2, pady=10)


# Функция для просмотра всех запчастей
def view_parts():
    tree_parts.delete(*tree_parts.get_children())
    cursor.execute('''
        SELECT parts.id, parts.name, parts.articul, parts.price, parts.category, cars.brand, cars.model, parts.quantity
        FROM parts
        LEFT JOIN cars ON parts.car_id = cars.id
    ''')
    rows = cursor.fetchall()
    for row in rows:
        tree_parts.insert("", "end", values=row)


# Функция для добавления клиента
def add_client():
    name = entry_client_name.get()
    phone = entry_client_phone.get()

    if name and phone:
        cursor.execute('INSERT INTO clients (name, phone) VALUES (?, ?)', (name, phone))
        conn.commit()
        messagebox.showinfo("Успех", "Клиент успешно добавлен!")
        clear_client_entries()
        view_clients()
    else:
        messagebox.showerror("Ошибка", "Все поля должны быть заполнены.")


# Функция для просмотра всех клиентов
def view_clients():
    tree_clients.delete(*tree_clients.get_children())
    cursor.execute('SELECT * FROM clients')
    rows = cursor.fetchall()
    for row in rows:
        tree_clients.insert("", "end", values=row)


# Функция для очистки полей ввода клиентов
def clear_client_entries():
    entry_client_name.delete(0, tk.END)
    entry_client_phone.delete(0, tk.END)


# Функция для создания нового заказа
def create_order():
    def confirm_order():
        global selected_order_id
        selected_client = combo_client.get()
        if not selected_client:
            messagebox.showerror("Ошибка", "Выберите клиента для создания заказа.")
            return

        # Получаем ID клиента
        client_id = None
        cursor.execute('SELECT id FROM clients WHERE name = ?', (selected_client,))
        result = cursor.fetchone()
        if result:
            client_id = result[0]
        else:
            messagebox.showerror("Ошибка", "Клиент не найден.")
            return

        # Создаем заказ
        order_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute('INSERT INTO orders (client_id, order_date) VALUES (?, ?)', (client_id, order_date))
        conn.commit()
        selected_order_id = cursor.lastrowid

        # Добавляем выбранные запчасти в заказ
        selected_parts = tree_selected_parts.get_children()
        if not selected_parts:
            messagebox.showwarning("Предупреждение", "Не добавлено ни одной запчасти.")
            return

        for item in selected_parts:
            part_id = tree_selected_parts.item(item)['values'][0]
            quantity = tree_selected_parts.item(item)['values'][3]

            # Проверяем, достаточно ли товара на складе
            cursor.execute('SELECT quantity FROM parts WHERE id = ?', (part_id,))
            current_quantity = cursor.fetchone()[0]
            if current_quantity < quantity:
                messagebox.showerror("Ошибка", f"Недостаточно запчастей в наличии для заказа (ID: {part_id}).")
                return

            # Уменьшаем количество на складе
            new_quantity = current_quantity - quantity
            cursor.execute('UPDATE parts SET quantity = ? WHERE id = ?', (new_quantity, part_id))

            # Добавляем запчасть в заказ
            cursor.execute('INSERT INTO order_parts (order_id, part_id, quantity) VALUES (?, ?, ?)',
                           (selected_order_id, part_id, quantity))
        conn.commit()

        messagebox.showinfo("Успех", "Заказ успешно создан!")
        order_window.destroy()
        view_parts()  # Обновляем список запчастей после изменения количества

    def add_part_to_order():
        selected_part = tree_parts.selection()
        if not selected_part:
            messagebox.showerror("Ошибка", "Выберите запчасть для добавления в заказ.")
            return

        part_id = tree_parts.item(selected_part)['values'][0]
        part_name = tree_parts.item(selected_part)['values'][1]
        part_price = tree_parts.item(selected_part)['values'][3]

        quantity = entry_quantity.get()
        if not quantity.isdigit() or int(quantity) <= 0:
            messagebox.showerror("Ошибка", "Количество должно быть положительным числом.")
            return

        # Проверяем, есть ли такая запчасть уже в заказе
        for item in tree_selected_parts.get_children():
            if tree_selected_parts.item(item)['values'][0] == part_id:
                current_quantity = tree_selected_parts.item(item)['values'][3]
                tree_selected_parts.item(item,
                                         values=(part_id, part_name, part_price, int(current_quantity) + int(quantity)))
                return

        # Если запчасти нет в заказе, добавляем её
        tree_selected_parts.insert("", "end", values=(part_id, part_name, part_price, quantity))

    order_window = tk.Toplevel(root)
    order_window.title("Создание заказа")

    # Выбор клиента
    label_client = tk.Label(order_window, text="Клиент:")
    label_client.grid(row=0, column=0, padx=5, pady=5)
    combo_client = ttk.Combobox(order_window, state="readonly")
    combo_client['values'] = [client[1] for client in view_clients_data()]
    combo_client.grid(row=0, column=1, padx=5, pady=5)

    # Таблица доступных запчастей
    columns_parts = ("ID", "Название", "Артикул", "Цена", "Категория", "Марка авто", "Модель авто", "Количество")
    tree_parts = ttk.Treeview(order_window, columns=columns_parts, show="headings", height=10)
    for col in columns_parts:
        tree_parts.heading(col, text=col)
        tree_parts.column(col, width=100)
    tree_parts.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

    view_parts_data(tree_parts)

    # Количество запчастей
    label_quantity = tk.Label(order_window, text="Количество:")
    label_quantity.grid(row=2, column=0, padx=5, pady=5)
    entry_quantity = tk.Entry(order_window)
    entry_quantity.grid(row=2, column=1, padx=5, pady=5)

    # Кнопка добавления запчасти в заказ
    button_add_part = tk.Button(order_window, text="Добавить в заказ", command=add_part_to_order)
    button_add_part.grid(row=3, column=0, columnspan=2, pady=10)

    # Таблица выбранных запчастей
    columns_selected_parts = ("ID", "Название", "Цена", "Количество")
    tree_selected_parts = ttk.Treeview(order_window, columns=columns_selected_parts, show="headings", height=5)
    for col in columns_selected_parts:
        tree_selected_parts.heading(col, text=col)
        tree_selected_parts.column(col, width=100)
    tree_selected_parts.grid(row=4, column=0, columnspan=2, padx=10, pady=10)

    # Кнопка подтверждения заказа
    button_confirm_order = tk.Button(order_window, text="Подтвердить заказ", command=confirm_order)
    button_confirm_order.grid(row=5, column=0, columnspan=2, pady=10)


# Функция для просмотра всех клиентов (для Combobox)
def view_clients_data():
    cursor.execute('SELECT * FROM clients')
    return cursor.fetchall()


# Функция для просмотра всех запчастей (для Treeview)
def view_parts_data(tree):
    tree.delete(*tree.get_children())
    cursor.execute('''
        SELECT parts.id, parts.name, parts.articul, parts.price, parts.category, cars.brand, cars.model, parts.quantity
        FROM parts
        LEFT JOIN cars ON parts.car_id = cars.id
    ''')
    rows = cursor.fetchall()
    for row in rows:
        tree.insert("", "end", values=row)


# Функция для просмотра всех заказов
def view_orders():
    tree_orders.delete(*tree_orders.get_children())
    cursor.execute('''
        SELECT orders.id, clients.name, clients.phone, orders.order_date
        FROM orders
        LEFT JOIN clients ON orders.client_id = clients.id
    ''')
    rows = cursor.fetchall()
    for row in rows:
        order_id = row[0]
        cursor.execute('''
            SELECT SUM(parts.price * order_parts.quantity)
            FROM order_parts
            LEFT JOIN parts ON order_parts.part_id = parts.id
            WHERE order_parts.order_id = ?
        ''', (order_id,))
        total = cursor.fetchone()[0] or 0  # Если нет запчастей, сумма равна 0
        tree_orders.insert("", "end", values=(order_id, row[1], row[2], row[3], total))


# Функция для просмотра деталей заказа
def view_order_details():
    selected_order = tree_orders.selection()
    if not selected_order:
        messagebox.showerror("Ошибка", "Выберите заказ для просмотра деталей.")
        return

    order_id = tree_orders.item(selected_order)['values'][0]

    details_window = tk.Toplevel(root)
    details_window.title(f"Детали заказа #{order_id}")

    cursor.execute('''
        SELECT order_parts.id, parts.name, parts.price, order_parts.quantity, parts.price * order_parts.quantity AS total
        FROM order_parts
        LEFT JOIN parts ON order_parts.part_id = parts.id
        WHERE order_parts.order_id = ?
    ''', (order_id,))
    rows = cursor.fetchall()

    columns_order_details = ("ID", "Название", "Цена", "Количество", "Сумма")
    tree_order_details = ttk.Treeview(details_window, columns=columns_order_details, show="headings")
    for col in columns_order_details:
        tree_order_details.heading(col, text=col)
        tree_order_details.column(col, width=100)
    tree_order_details.pack(padx=10, pady=10)

    for row in rows:
        tree_order_details.insert("", "end", values=row)


# Создание GUI
root = tk.Tk()
root.title("АРМ Продавца Автозапчастей")

# Вкладки
tab_control = ttk.Notebook(root)
tab_cars = ttk.Frame(tab_control)
tab_parts = ttk.Frame(tab_control)
tab_clients = ttk.Frame(tab_control)
tab_orders = ttk.Frame(tab_control)
tab_control.add(tab_cars, text="Автомобили")
tab_control.add(tab_parts, text="Запчасти")
tab_control.add(tab_clients, text="Клиенты")
tab_control.add(tab_orders, text="Заказы")
tab_control.pack(expand=1, fill="both")

# Вкладка "Автомобили"
label_brand = tk.Label(tab_cars, text="Марка:")
label_brand.grid(row=0, column=0, padx=5, pady=5)
entry_brand = tk.Entry(tab_cars)
entry_brand.grid(row=0, column=1, padx=5, pady=5)

label_model = tk.Label(tab_cars, text="Модель:")
label_model.grid(row=1, column=0, padx=5, pady=5)
entry_model = tk.Entry(tab_cars)
entry_model.grid(row=1, column=1, padx=5, pady=5)

button_add_car = tk.Button(tab_cars, text="Добавить машину", command=add_car)
button_add_car.grid(row=2, column=0, columnspan=2, pady=10)

button_edit_car = tk.Button(tab_cars, text="Редактировать", command=edit_car)
button_edit_car.grid(row=3, column=0, pady=5)

button_delete_car = tk.Button(tab_cars, text="Удалить", command=delete_car)
button_delete_car.grid(row=3, column=1, pady=5)

columns_cars = ("ID", "Марка", "Модель")
tree_cars = ttk.Treeview(tab_cars, columns=columns_cars, show="headings")
for col in columns_cars:
    tree_cars.heading(col, text=col)
    tree_cars.column(col, width=100)
tree_cars.grid(row=4, column=0, columnspan=2, padx=10, pady=10)

# Вкладка "Запчасти"
button_add_part = tk.Button(tab_parts, text="Добавить запчасть", command=open_add_part_window)
button_add_part.grid(row=0, column=0, pady=10)

columns_parts = ("ID", "Название", "Артикул", "Цена", "Категория", "Марка авто", "Модель авто", "Количество")
tree_parts = ttk.Treeview(tab_parts, columns=columns_parts, show="headings")
for col in columns_parts:
    tree_parts.heading(col, text=col)
    tree_parts.column(col, width=100)
tree_parts.grid(row=1, column=0, padx=10, pady=10)

# Вкладка "Клиенты"
label_client_name = tk.Label(tab_clients, text="Имя:")
label_client_name.grid(row=0, column=0, padx=5, pady=5)
entry_client_name = tk.Entry(tab_clients)
entry_client_name.grid(row=0, column=1, padx=5, pady=5)

label_client_phone = tk.Label(tab_clients, text="Телефон:")
label_client_phone.grid(row=1, column=0, padx=5, pady=5)
entry_client_phone = tk.Entry(tab_clients)
entry_client_phone.grid(row=1, column=1, padx=5, pady=5)

button_add_client = tk.Button(tab_clients, text="Добавить клиента", command=add_client)
button_add_client.grid(row=2, column=0, columnspan=2, pady=10)

columns_clients = ("ID", "Имя", "Телефон")
tree_clients = ttk.Treeview(tab_clients, columns=columns_clients, show="headings")
for col in columns_clients:
    tree_clients.heading(col, text=col)
    tree_clients.column(col, width=100)
tree_clients.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

# Вкладка "Заказы"
button_create_order = tk.Button(tab_orders, text="Создать заказ", command=create_order)
button_create_order.grid(row=0, column=0, pady=10)

button_view_orders = tk.Button(tab_orders, text="Просмотреть заказы", command=view_orders)
button_view_orders.grid(row=0, column=1, pady=10)

columns_orders = ("ID", "Клиент", "Телефон", "Дата", "Общая сумма")
tree_orders = ttk.Treeview(tab_orders, columns=columns_orders, show="headings")
for col in columns_orders:
    tree_orders.heading(col, text=col)
    tree_orders.column(col, width=150)
tree_orders.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

button_view_order_details = tk.Button(tab_orders, text="Посмотреть детали", command=view_order_details)
button_view_order_details.grid(row=2, column=0, columnspan=2, pady=10)

# Запуск приложения
view_cars()
view_parts()
view_clients()
root.mainloop()

# Закрытие соединения с базой данных при выходе
conn.close()