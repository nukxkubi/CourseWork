import tkinter as tk
from tkinter import messagebox, ttk
import sqlite3
from datetime import datetime
import os

# Подключение к базе данных SQLite
conn = sqlite3.connect('auto_parts.db')
cursor = conn.cursor()

# Создание таблицы manufacturers (производители авто)
cursor.execute('''
    CREATE TABLE IF NOT EXISTS manufacturers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL
    )
''')

# Создание таблицы categories (категории запчастей)
cursor.execute('''
    CREATE TABLE IF NOT EXISTS categories (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL
    )
''')

# Создание таблицы cars (марки и модели авто)
cursor.execute('''
    CREATE TABLE IF NOT EXISTS cars (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        manufacturer_id INTEGER NOT NULL,
        brand TEXT NOT NULL,
        model TEXT NOT NULL,
        FOREIGN KEY(manufacturer_id) REFERENCES manufacturers(id)
    )
''')

# Создание или обновление таблицы parts (запчасти с количеством)
cursor.execute('''
    CREATE TABLE IF NOT EXISTS parts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        articul TEXT NOT NULL,
        price REAL NOT NULL,
        category_id INTEGER,
        car_id INTEGER,
        quantity INTEGER NOT NULL DEFAULT 0,
        FOREIGN KEY(category_id) REFERENCES categories(id),
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

# Создание таблицы orders (заказы с полем status)
cursor.execute('''
    CREATE TABLE IF NOT EXISTS orders (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        client_id INTEGER NOT NULL,
        order_date TEXT NOT NULL,
        status TEXT NOT NULL DEFAULT 'В обработке',
        FOREIGN KEY(client_id) REFERENCES clients(id)
    )
''')

# Проверка наличия столбца status и его добавление, если его нет
cursor.execute("PRAGMA table_info(orders)")
columns = [column[1] for column in cursor.fetchall()]
if "status" not in columns:
    cursor.execute('ALTER TABLE orders ADD COLUMN status TEXT NOT NULL DEFAULT "В обработке"')
    conn.commit()

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


# Функция для фильтрации записей в Treeview
def filter_tree(tree, query, table_name):
    tree.delete(*tree.get_children())
    if table_name == 'cars':
        cursor.execute('''
            SELECT cars.id, manufacturers.name, cars.brand, cars.model 
            FROM cars 
            LEFT JOIN manufacturers ON cars.manufacturer_id = manufacturers.id
            WHERE cars.brand LIKE ? OR cars.model LIKE ? OR manufacturers.name LIKE ?
        ''', ('%' + query + '%', '%' + query + '%', '%' + query + '%'))
    elif table_name == 'parts':
        cursor.execute('''
            SELECT parts.id, parts.name, parts.articul, parts.price, categories.name, cars.brand, cars.model, parts.quantity
            FROM parts
            LEFT JOIN categories ON parts.category_id = categories.id
            LEFT JOIN cars ON parts.car_id = cars.id
            WHERE parts.name LIKE ? OR parts.articul LIKE ? OR categories.name LIKE ? OR cars.brand LIKE ? OR cars.model LIKE ?
        ''', ('%' + query + '%', '%' + query + '%', '%' + query + '%', '%' + query + '%', '%' + query + '%'))
    elif table_name == 'clients':
        cursor.execute('SELECT * FROM clients WHERE name LIKE ? OR phone LIKE ?',
                       ('%' + query + '%', '%' + query + '%'))
    elif table_name == 'orders':
        cursor.execute('''
            SELECT orders.id, clients.name, clients.phone, orders.order_date, orders.status
            FROM orders
            LEFT JOIN clients ON orders.client_id = clients.id
            WHERE clients.name LIKE ? OR clients.phone LIKE ? OR orders.status LIKE ?
        ''', ('%' + query + '%', '%' + query + '%', '%' + query + '%'))
    elif table_name == 'categories':
        cursor.execute('SELECT * FROM categories WHERE name LIKE ?', ('%' + query + '%',))
    elif table_name == 'manufacturers':
        cursor.execute('SELECT * FROM manufacturers WHERE name LIKE ?', ('%' + query + '%',))

    rows = cursor.fetchall()
    for row in rows:
        tree.insert("", "end", values=row)


# Функция для получения списка производителей
def get_manufacturers():
    cursor.execute('SELECT id, name FROM manufacturers')
    return cursor.fetchall()


# Функция для получения списка категорий
def get_categories():
    cursor.execute('SELECT id, name FROM categories')
    return cursor.fetchall()


# Функция для получения списка автомобилей
def get_cars():
    cursor.execute('''
        SELECT cars.id, manufacturers.name, cars.brand, cars.model
        FROM cars
        LEFT JOIN manufacturers ON cars.manufacturer_id = manufacturers.id
    ''')
    return cursor.fetchall()


# Функция для просмотра всех заказов
def view_orders():
    tree_orders.delete(*tree_orders.get_children())
    cursor.execute('''
        SELECT orders.id, clients.name, clients.phone, orders.order_date, orders.status
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
        tree_orders.insert("", "end", values=(order_id, row[1], row[2], row[3], row[4], total))


# Функция для просмотра всех производителей
def view_manufacturers():
    filter_tree(tree_manufacturers, '', 'manufacturers')



# Функция для генерации отчета о заказе
def generate_order_report(order_id, client_name, order_date, total_price):
    # Получаем детали заказа
    cursor.execute('''
        SELECT parts.name, parts.price, order_parts.quantity, parts.price * order_parts.quantity AS total
        FROM order_parts
        LEFT JOIN parts ON order_parts.part_id = parts.id
        WHERE order_parts.order_id = ?
    ''', (order_id,))
    order_details = cursor.fetchall()

    # Создаем содержимое отчета
    report_content = f"Отчет о заказе #{order_id}\n\n"
    report_content += f"Дата: {order_date}\n"
    report_content += f"Клиент: {client_name}\n\n"
    report_content += "Детали заказа:\n"
    report_content += "{:<30} {:<10} {:<10} {:<10}\n".format("Название", "Цена", "Кол-во", "Сумма")

    for detail in order_details:
        name, price, quantity, subtotal = detail
        report_content += "{:<30} {:<10.2f} {:<10} {:<10.2f}\n".format(name, price, quantity, subtotal)

    report_content += "\nОбщая сумма: {:.2f} руб.\n".format(total_price)

    # Сохраняем отчет в файл
    file_name = f"order_{order_id}.txt"
    with open(file_name, "w", encoding="utf-8") as file:
        file.write(report_content)

    messagebox.showinfo("Успех", f"Отчет о заказе сохранен в файле: {os.path.abspath(file_name)}")

# Функция для получения данных клиентов
def view_clients_data():
    cursor.execute('SELECT id, name, phone FROM clients')
    return cursor.fetchall()


# Функция для загрузки данных запчастей в Treeview
def view_parts_data(tree):
    tree.delete(*tree.get_children())
    cursor.execute('''
        SELECT parts.id, parts.name, parts.articul, parts.price, categories.name, cars.brand, cars.model, parts.quantity
        FROM parts
        LEFT JOIN categories ON parts.category_id = categories.id
        LEFT JOIN cars ON parts.car_id = cars.id
    ''')
    rows = cursor.fetchall()
    for row in rows:
        tree.insert("", "end", values=row)

# Функция для добавления нового производителя
def add_manufacturer():
    name = entry_manufacturer.get()
    if name:
        cursor.execute('INSERT INTO manufacturers (name) VALUES (?)', (name,))
        conn.commit()
        messagebox.showinfo("Успех", "Производитель успешно добавлен!")
        entry_manufacturer.delete(0, tk.END)
        view_manufacturers()
    else:
        messagebox.showerror("Ошибка", "Введите название производителя.")


# Функция для удаления производителя
def delete_manufacturer():
    selected_item = tree_manufacturers.selection()
    if not selected_item:
        messagebox.showerror("Ошибка", "Выберите производителя для удаления.")
        return

    manufacturer_id = tree_manufacturers.item(selected_item)['values'][0]
    cursor.execute('DELETE FROM manufacturers WHERE id = ?', (manufacturer_id,))
    conn.commit()
    tree_manufacturers.delete(selected_item)
    messagebox.showinfo("Успех", "Производитель успешно удален!")


# Функция для редактирования производителя
def edit_manufacturer():
    def save_manufacturer():
        manufacturer_id = int(entry_manufacturer_id.get())
        name = entry_manufacturer.get()

        if name:
            cursor.execute('UPDATE manufacturers SET name = ? WHERE id = ?', (name, manufacturer_id))
            conn.commit()
            messagebox.showinfo("Успех", "Производитель успешно обновлен!")
            edit_manufacturer_window.destroy()
            view_manufacturers()
        else:
            messagebox.showerror("Ошибка", "Введите название производителя.")

    selected_item = tree_manufacturers.selection()
    if not selected_item:
        messagebox.showerror("Ошибка", "Выберите производителя для редактирования.")
        return

    manufacturer_id = tree_manufacturers.item(selected_item)['values'][0]
    name = tree_manufacturers.item(selected_item)['values'][1]

    # Создание окна редактирования производителя
    edit_manufacturer_window = tk.Toplevel(root)
    edit_manufacturer_window.title("Редактирование производителя")

    label_manufacturer_id = tk.Label(edit_manufacturer_window, text="ID:")
    label_manufacturer_id.grid(row=0, column=0, padx=5, pady=5)
    entry_manufacturer_id = tk.Entry(edit_manufacturer_window)
    entry_manufacturer_id.insert(0, str(manufacturer_id))
    entry_manufacturer_id.config(state='readonly')  # ID нельзя изменять
    entry_manufacturer_id.grid(row=0, column=1, padx=5, pady=5)

    label_manufacturer = tk.Label(edit_manufacturer_window, text="Название:")
    label_manufacturer.grid(row=1, column=0, padx=5, pady=5)
    entry_manufacturer = tk.Entry(edit_manufacturer_window)
    entry_manufacturer.insert(0, name)
    entry_manufacturer.grid(row=1, column=1, padx=5, pady=5)

    button_save = tk.Button(edit_manufacturer_window, text="Сохранить", command=save_manufacturer)
    button_save.grid(row=2, column=0, columnspan=2, pady=10)


# Функция для просмотра всех категорий
def view_categories():
    filter_tree(tree_categories, '', 'categories')


# Функция для добавления новой категории
def add_category():
    name = entry_category_name.get()
    if name:
        cursor.execute('INSERT INTO categories (name) VALUES (?)', (name,))
        conn.commit()
        messagebox.showinfo("Успех", "Категория успешно добавлена!")
        entry_category_name.delete(0, tk.END)
        view_categories()
    else:
        messagebox.showerror("Ошибка", "Введите название категории.")


# Функция для удаления категории
def delete_category():
    selected_item = tree_categories.selection()
    if not selected_item:
        messagebox.showerror("Ошибка", "Выберите категорию для удаления.")
        return

    category_id = tree_categories.item(selected_item)['values'][0]
    cursor.execute('DELETE FROM categories WHERE id = ?', (category_id,))
    conn.commit()
    tree_categories.delete(selected_item)
    messagebox.showinfo("Успех", "Категория успешно удалена!")


# Функция для редактирования категории
def edit_category():
    def save_category():
        category_id = int(entry_category_id.get())
        name = entry_category_name.get()

        if name:
            cursor.execute('UPDATE categories SET name = ? WHERE id = ?', (name, category_id))
            conn.commit()
            messagebox.showinfo("Успех", "Категория успешно обновлена!")
            edit_category_window.destroy()
            view_categories()
        else:
            messagebox.showerror("Ошибка", "Введите название категории.")

    selected_item = tree_categories.selection()
    if not selected_item:
        messagebox.showerror("Ошибка", "Выберите категорию для редактирования.")
        return

    category_id = tree_categories.item(selected_item)['values'][0]
    name = tree_categories.item(selected_item)['values'][1]

    # Создание окна редактирования категории
    edit_category_window = tk.Toplevel(root)
    edit_category_window.title("Редактирование категории")

    label_category_id = tk.Label(edit_category_window, text="ID:")
    label_category_id.grid(row=0, column=0, padx=5, pady=5)
    entry_category_id = tk.Entry(edit_category_window)
    entry_category_id.insert(0, str(category_id))
    entry_category_id.config(state='readonly')  # ID нельзя изменять
    entry_category_id.grid(row=0, column=1, padx=5, pady=5)

    label_category = tk.Label(edit_category_window, text="Название:")
    label_category.grid(row=1, column=0, padx=5, pady=5)
    entry_category_name = tk.Entry(edit_category_window)
    entry_category_name.insert(0, name)
    entry_category_name.grid(row=1, column=1, padx=5, pady=5)

    button_save = tk.Button(edit_category_window, text="Сохранить", command=save_category)
    button_save.grid(row=2, column=0, columnspan=2, pady=10)


# Функция для просмотра всех машин
def view_cars():
    filter_tree(tree_cars, '', 'cars')


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
    def save_car():
        car_id = int(entry_car_id.get())
        manufacturer = combo_manufacturer.get()
        brand = entry_brand.get()
        model = entry_model.get()

        if manufacturer and brand and model:
            manufacturer_id = None
            manufacturers = get_manufacturers()
            for man in manufacturers:
                if man[1] == manufacturer:
                    manufacturer_id = man[0]
                    break

            if manufacturer_id is None:
                messagebox.showerror("Ошибка", "Производитель не найден.")
                return

            cursor.execute('UPDATE cars SET manufacturer_id = ?, brand = ?, model = ? WHERE id = ?',
                           (manufacturer_id, brand, model, car_id))
            conn.commit()
            messagebox.showinfo("Успех", "Машина успешно обновлена!")
            edit_car_window.destroy()
            view_cars()
        else:
            messagebox.showerror("Ошибка", "Все поля должны быть заполнены.")

    selected_item = tree_cars.selection()
    if not selected_item:
        messagebox.showerror("Ошибка", "Выберите машину для редактирования.")
        return

    car_id = tree_cars.item(selected_item)['values'][0]
    manufacturer_name = tree_cars.item(selected_item)['values'][1]
    brand = tree_cars.item(selected_item)['values'][2]
    model = tree_cars.item(selected_item)['values'][3]

    # Создание окна редактирования машины
    edit_car_window = tk.Toplevel(root)
    edit_car_window.title("Редактирование машины")

    label_car_id = tk.Label(edit_car_window, text="ID:")
    label_car_id.grid(row=0, column=0, padx=5, pady=5)
    entry_car_id = tk.Entry(edit_car_window)
    entry_car_id.insert(0, str(car_id))
    entry_car_id.config(state='readonly')  # ID нельзя изменять
    entry_car_id.grid(row=0, column=1, padx=5, pady=5)

    label_manufacturer = tk.Label(edit_car_window, text="Производитель:")
    label_manufacturer.grid(row=1, column=0, padx=5, pady=5)
    combo_manufacturer = ttk.Combobox(edit_car_window, state="readonly")
    combo_manufacturer['values'] = [man[1] for man in get_manufacturers()]
    combo_manufacturer.set(manufacturer_name)
    combo_manufacturer.grid(row=1, column=1, padx=5, pady=5)

    label_brand = tk.Label(edit_car_window, text="Марка:")
    label_brand.grid(row=2, column=0, padx=5, pady=5)
    entry_brand = tk.Entry(edit_car_window)
    entry_brand.insert(0, brand)
    entry_brand.grid(row=2, column=1, padx=5, pady=5)

    label_model = tk.Label(edit_car_window, text="Модель:")
    label_model.grid(row=3, column=0, padx=5, pady=5)
    entry_model = tk.Entry(edit_car_window)
    entry_model.insert(0, model)
    entry_model.grid(row=3, column=1, padx=5, pady=5)

    button_save = tk.Button(edit_car_window, text="Сохранить", command=save_car)
    button_save.grid(row=4, column=0, columnspan=2, pady=10)


# Функция для очистки полей ввода машин
def clear_car_entries():
    combo_manufacturer.set("")
    entry_brand.delete(0, tk.END)
    entry_model.delete(0, tk.END)


# Функция для создания окна добавления новой запчасти
def open_add_part_window():
    def add_part():
        name = entry_name.get()
        articul = entry_articul.get()
        price = entry_price.get()
        selected_category = combo_category.get()
        selected_car = combo_car.get()
        quantity = entry_quantity.get()  # Новое поле: Количество

        if name and articul and price and selected_category and selected_car and quantity.isdigit():
            try:
                price = float(price)
                quantity = int(quantity)  # Преобразуем количество в целое число
                category_id = None
                categories = get_categories()
                for cat in categories:
                    if cat[1] == selected_category:
                        category_id = cat[0]
                        break

                car_id = None
                cars = get_cars()
                for car in cars:
                    if f"{car[2]} {car[3]}" == selected_car:
                        car_id = car[0]
                        break

                if category_id is None or car_id is None:
                    messagebox.showerror("Ошибка", "Категория или автомобиль не найдены.")
                    return

                cursor.execute(
                    'INSERT INTO parts (name, articul, price, category_id, car_id, quantity) VALUES (?, ?, ?, ?, ?, ?)',
                    (name, articul, price, category_id, car_id, quantity))  # Добавляем поле quantity
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
    combo_category = ttk.Combobox(add_part_window, state="readonly")
    combo_category['values'] = [cat[1] for cat in get_categories()]
    combo_category.grid(row=3, column=1, padx=5, pady=5)

    label_car = tk.Label(add_part_window, text="Автомобиль:")
    label_car.grid(row=4, column=0, padx=5, pady=5)
    combo_car = ttk.Combobox(add_part_window, state="readonly")
    combo_car['values'] = [f"{car[2]} {car[3]}" for car in get_cars()]
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
    filter_tree(tree_parts, '', 'parts')


# Функция для удаления запчасти
def delete_part():
    selected_item = tree_parts.selection()
    if not selected_item:
        messagebox.showerror("Ошибка", "Выберите запчасть для удаления.")
        return

    part_id = tree_parts.item(selected_item)['values'][0]
    cursor.execute('DELETE FROM parts WHERE id = ?', (part_id,))
    conn.commit()
    tree_parts.delete(selected_item)
    messagebox.showinfo("Успех", "Запчасть успешно удалена!")


# Функция для редактирования запчасти
def edit_part():
    def save_part():
        part_id = int(entry_part_id.get())
        name = entry_name.get()
        articul = entry_articul.get()
        price = entry_price.get()
        selected_category = combo_category.get()
        selected_car = combo_car.get()
        quantity = entry_quantity.get()

        if name and articul and price and selected_category and selected_car and quantity.isdigit():
            try:
                price = float(price)
                quantity = int(quantity)
                category_id = None
                categories = get_categories()
                for cat in categories:
                    if cat[1] == selected_category:
                        category_id = cat[0]
                        break

                car_id = None
                cars = get_cars()
                for car in cars:
                    if f"{car[2]} {car[3]}" == selected_car:
                        car_id = car[0]
                        break

                if category_id is None or car_id is None:
                    messagebox.showerror("Ошибка", "Категория или автомобиль не найдены.")
                    return

                cursor.execute('''
                    UPDATE parts 
                    SET name = ?, articul = ?, price = ?, category_id = ?, car_id = ?, quantity = ?
                    WHERE id = ?
                ''', (name, articul, price, category_id, car_id, quantity, part_id))
                conn.commit()
                messagebox.showinfo("Успех", "Запчасть успешно обновлена!")
                edit_part_window.destroy()
                view_parts()
            except ValueError:
                messagebox.showerror("Ошибка", "Цена должна быть числом, а количество — целым числом.")
        else:
            messagebox.showerror("Ошибка", "Все поля должны быть заполнены корректно.")

    selected_item = tree_parts.selection()
    if not selected_item:
        messagebox.showerror("Ошибка", "Выберите запчасть для редактирования.")
        return

    part_id = tree_parts.item(selected_item)['values'][0]
    name = tree_parts.item(selected_item)['values'][1]
    articul = tree_parts.item(selected_item)['values'][2]
    price = tree_parts.item(selected_item)['values'][3]
    category_name = tree_parts.item(selected_item)['values'][4]
    car_brand = tree_parts.item(selected_item)['values'][5]
    car_model = tree_parts.item(selected_item)['values'][6]
    quantity = tree_parts.item(selected_item)['values'][7]

    # Создание окна редактирования запчасти
    edit_part_window = tk.Toplevel(root)
    edit_part_window.title("Редактирование запчасти")

    label_part_id = tk.Label(edit_part_window, text="ID:")
    label_part_id.grid(row=0, column=0, padx=5, pady=5)
    entry_part_id = tk.Entry(edit_part_window)
    entry_part_id.insert(0, str(part_id))
    entry_part_id.config(state='readonly')  # ID нельзя изменять
    entry_part_id.grid(row=0, column=1, padx=5, pady=5)

    label_name = tk.Label(edit_part_window, text="Название:")
    label_name.grid(row=1, column=0, padx=5, pady=5)
    entry_name = tk.Entry(edit_part_window)
    entry_name.insert(0, name)
    entry_name.grid(row=1, column=1, padx=5, pady=5)

    label_articul = tk.Label(edit_part_window, text="Артикул:")
    label_articul.grid(row=2, column=0, padx=5, pady=5)
    entry_articul = tk.Entry(edit_part_window)
    entry_articul.insert(0, articul)
    entry_articul.grid(row=2, column=1, padx=5, pady=5)

    label_price = tk.Label(edit_part_window, text="Цена:")
    label_price.grid(row=3, column=0, padx=5, pady=5)
    entry_price = tk.Entry(edit_part_window)
    entry_price.insert(0, str(price))
    entry_price.grid(row=3, column=1, padx=5, pady=5)

    label_category = tk.Label(edit_part_window, text="Категория:")
    label_category.grid(row=4, column=0, padx=5, pady=5)
    combo_category = ttk.Combobox(edit_part_window, state="readonly")
    combo_category['values'] = [cat[1] for cat in get_categories()]
    combo_category.set(category_name)
    combo_category.grid(row=4, column=1, padx=5, pady=5)

    label_car = tk.Label(edit_part_window, text="Автомобиль:")
    label_car.grid(row=5, column=0, padx=5, pady=5)
    combo_car = ttk.Combobox(edit_part_window, state="readonly")
    combo_car['values'] = [f"{car[2]} {car[3]}" for car in get_cars()]
    combo_car.set(f"{car_brand} {car_model}")
    combo_car.grid(row=5, column=1, padx=5, pady=5)

    label_quantity = tk.Label(edit_part_window, text="Количество:")
    label_quantity.grid(row=6, column=0, padx=5, pady=5)
    entry_quantity = tk.Entry(edit_part_window)
    entry_quantity.insert(0, str(quantity))
    entry_quantity.grid(row=6, column=1, padx=5, pady=5)

    button_save = tk.Button(edit_part_window, text="Сохранить", command=save_part)
    button_save.grid(row=7, column=0, columnspan=2, pady=10)


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
    filter_tree(tree_clients, '', 'clients')


# Функция для очистки полей ввода клиентов
def clear_client_entries():
    entry_client_name.delete(0, tk.END)
    entry_client_phone.delete(0, tk.END)


# Функция для редактирования клиента
def edit_client():
    def save_client():
        client_id = int(entry_client_id.get())
        name = entry_client_name.get()
        phone = entry_client_phone.get()

        if name and phone:
            cursor.execute('UPDATE clients SET name = ?, phone = ? WHERE id = ?', (name, phone, client_id))
            conn.commit()
            messagebox.showinfo("Успех", "Клиент успешно обновлен!")
            edit_client_window.destroy()
            view_clients()
        else:
            messagebox.showerror("Ошибка", "Все поля должны быть заполнены.")

    selected_item = tree_clients.selection()
    if not selected_item:
        messagebox.showerror("Ошибка", "Выберите клиента для редактирования.")
        return

    client_id = tree_clients.item(selected_item)['values'][0]
    name = tree_clients.item(selected_item)['values'][1]
    phone = tree_clients.item(selected_item)['values'][2]

    # Создание окна редактирования клиента
    edit_client_window = tk.Toplevel(root)
    edit_client_window.title("Редактирование клиента")

    label_client_id = tk.Label(edit_client_window, text="ID:")
    label_client_id.grid(row=0, column=0, padx=5, pady=5)
    entry_client_id = tk.Entry(edit_client_window)
    entry_client_id.insert(0, str(client_id))
    entry_client_id.config(state='readonly')  # ID нельзя изменять
    entry_client_id.grid(row=0, column=1, padx=5, pady=5)

    label_client_name = tk.Label(edit_client_window, text="Имя:")
    label_client_name.grid(row=1, column=0, padx=5, pady=5)
    entry_client_name = tk.Entry(edit_client_window)
    entry_client_name.insert(0, name)
    entry_client_name.grid(row=1, column=1, padx=5, pady=5)

    label_client_phone = tk.Label(edit_client_window, text="Телефон:")
    label_client_phone.grid(row=2, column=0, padx=5, pady=5)
    entry_client_phone = tk.Entry(edit_client_window)
    entry_client_phone.insert(0, phone)
    entry_client_phone.grid(row=2, column=1, padx=5, pady=5)

    button_save = tk.Button(edit_client_window, text="Сохранить", command=save_client)
    button_save.grid(row=3, column=0, columnspan=2, pady=10)


# Функция для удаления клиента
def delete_client():
    selected_item = tree_clients.selection()
    if not selected_item:
        messagebox.showerror("Ошибка", "Выберите клиента для удаления.")
        return

    client_id = tree_clients.item(selected_item)['values'][0]
    cursor.execute('DELETE FROM clients WHERE id = ?', (client_id,))
    conn.commit()
    tree_clients.delete(selected_item)
    messagebox.showinfo("Успех", "Клиент успешно удален!")


# Функция для изменения статуса заказа
def update_order_status():
    selected_order = tree_orders.selection()
    if not selected_order:
        messagebox.showerror("Ошибка", "Выберите заказ для изменения статуса.")
        return

    order_id = tree_orders.item(selected_order)['values'][0]
    status = combo_status.get()

    if status:
        cursor.execute('UPDATE orders SET status = ? WHERE id = ?', (status, order_id))
        conn.commit()
        messagebox.showinfo("Успех", "Статус заказа успешно обновлен!")
        view_orders()
    else:
        messagebox.showerror("Ошибка", "Выберите статус заказа.")


# Создание GUI
root = tk.Tk()
root.title("АРМ Продавца Автозапчастей")

# Вкладки
tab_control = ttk.Notebook(root)
tab_manufacturers = ttk.Frame(tab_control)
tab_categories = ttk.Frame(tab_control)
tab_cars = ttk.Frame(tab_control)
tab_parts = ttk.Frame(tab_control)
tab_clients = ttk.Frame(tab_control)
tab_orders = ttk.Frame(tab_control)
tab_control.add(tab_manufacturers, text="Производители")
tab_control.add(tab_categories, text="Категории")
tab_control.add(tab_cars, text="Автомобили")
tab_control.add(tab_parts, text="Запчасти")
tab_control.add(tab_clients, text="Клиенты")
tab_control.add(tab_orders, text="Заказы")
tab_control.pack(expand=1, fill="both")

# Вкладка "Производители"
label_search_manufacturers = tk.Label(tab_manufacturers, text="Поиск:")
label_search_manufacturers.grid(row=0, column=0, padx=5, pady=5)
entry_search_manufacturers = tk.Entry(tab_manufacturers)
entry_search_manufacturers.grid(row=0, column=1, padx=5, pady=5)


def search_manufacturers():
    query = entry_search_manufacturers.get()
    filter_tree(tree_manufacturers, query, 'manufacturers')


entry_search_manufacturers.bind('<KeyRelease>', lambda event: search_manufacturers())

button_add_manufacturer = tk.Button(tab_manufacturers, text="Добавить", command=add_manufacturer)
button_add_manufacturer.grid(row=1, column=0, pady=10)

button_edit_manufacturer = tk.Button(tab_manufacturers, text="Редактировать", command=edit_manufacturer)
button_edit_manufacturer.grid(row=1, column=1, pady=5)

button_delete_manufacturer = tk.Button(tab_manufacturers, text="Удалить", command=delete_manufacturer)
button_delete_manufacturer.grid(row=1, column=2, pady=5)

columns_manufacturers = ("ID", "Название")
tree_manufacturers = ttk.Treeview(tab_manufacturers, columns=columns_manufacturers, show="headings")
for col in columns_manufacturers:
    tree_manufacturers.heading(col, text=col)
    tree_manufacturers.column(col, width=100)
tree_manufacturers.grid(row=2, column=0, columnspan=3, padx=10, pady=10)

# Вкладка "Категории"
label_search_categories = tk.Label(tab_categories, text="Поиск:")
label_search_categories.grid(row=0, column=0, padx=5, pady=5)
entry_search_categories = tk.Entry(tab_categories)
entry_search_categories.grid(row=0, column=1, padx=5, pady=5)

def search_categories():
    query = entry_search_categories.get()
    filter_tree(tree_categories, query, 'categories')

entry_search_categories.bind('<KeyRelease>', lambda event: search_categories())

# Добавление категории
label_category_name = tk.Label(tab_categories, text="Название:")
label_category_name.grid(row=1, column=0, padx=5, pady=5)
entry_category_name = tk.Entry(tab_categories)  # Определение entry_category_name
entry_category_name.grid(row=1, column=1, padx=5, pady=5)

button_add_category = tk.Button(tab_categories, text="Добавить", command=add_category)
button_add_category.grid(row=2, column=0, pady=10)

button_edit_category = tk.Button(tab_categories, text="Редактировать", command=edit_category)
button_edit_category.grid(row=2, column=1, pady=5)

button_delete_category = tk.Button(tab_categories, text="Удалить", command=delete_category)
button_delete_category.grid(row=2, column=2, pady=5)

# Таблица категорий
columns_categories = ("ID", "Название")
tree_categories = ttk.Treeview(tab_categories, columns=columns_categories, show="headings")
for col in columns_categories:
    tree_categories.heading(col, text=col)
    tree_categories.column(col, width=100)
tree_categories.grid(row=3, column=0, columnspan=3, padx=10, pady=10)

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
        tree_order_details.column(col, width=150)
    tree_order_details.pack(padx=10, pady=10)

    for row in rows:
        tree_order_details.insert("", "end", values=row)

# Вкладка "Автомобили"
tab_cars = ttk.Frame(tab_control)
tab_control.add(tab_cars, text="Автомобили")

# Поиск автомобилей
label_search_cars = tk.Label(tab_cars, text="Поиск:")
label_search_cars.grid(row=0, column=0, padx=5, pady=5)
entry_search_cars = tk.Entry(tab_cars)
entry_search_cars.grid(row=0, column=1, padx=5, pady=5)

def search_cars():
    query = entry_search_cars.get()
    filter_tree(tree_cars, query, 'cars')

entry_search_cars.bind('<KeyRelease>', lambda event: search_cars())

# Выбор производителя через Combobox
label_manufacturer = tk.Label(tab_cars, text="Производитель:")
label_manufacturer.grid(row=1, column=0, padx=5, pady=5)
combo_manufacturer = ttk.Combobox(tab_cars, state="readonly")
combo_manufacturer['values'] = [man[1] for man in get_manufacturers()]  # Заполняем Combobox данными из базы
combo_manufacturer.grid(row=1, column=1, padx=5, pady=5)

# Марка автомобиля
label_brand = tk.Label(tab_cars, text="Марка:")
label_brand.grid(row=2, column=0, padx=5, pady=5)
entry_brand = tk.Entry(tab_cars)
entry_brand.grid(row=2, column=1, padx=5, pady=5)

# Модель автомобиля
label_model = tk.Label(tab_cars, text="Модель:")
label_model.grid(row=3, column=0, padx=5, pady=5)
entry_model = tk.Entry(tab_cars)
entry_model.grid(row=3, column=1, padx=5, pady=5)

# Кнопки управления автомобилями
button_add_car = tk.Button(tab_cars, text="Добавить машину", command=add_car)
button_add_car.grid(row=4, column=0, columnspan=2, pady=10)

button_edit_car = tk.Button(tab_cars, text="Редактировать", command=edit_car)
button_edit_car.grid(row=5, column=0, pady=5)

button_delete_car = tk.Button(tab_cars, text="Удалить", command=delete_car)
button_delete_car.grid(row=5, column=1, pady=5)

# Таблица автомобилей
columns_cars = ("ID", "Производитель", "Марка", "Модель")
tree_cars = ttk.Treeview(tab_cars, columns=columns_cars, show="headings")
for col in columns_cars:
    tree_cars.heading(col, text=col)
    tree_cars.column(col, width=100)
tree_cars.grid(row=6, column=0, columnspan=2, padx=10, pady=10)

# Вкладка "Запчасти"
label_search_parts = tk.Label(tab_parts, text="Поиск:")
label_search_parts.grid(row=0, column=0, padx=5, pady=5)
entry_search_parts = tk.Entry(tab_parts)
entry_search_parts.grid(row=0, column=1, padx=5, pady=5)

def search_parts():
    query = entry_search_parts.get()
    filter_tree(tree_parts, query, 'parts')

entry_search_parts.bind('<KeyRelease>', lambda event: search_parts())

button_add_part = tk.Button(tab_parts, text="Добавить запчасть", command=open_add_part_window)
button_add_part.grid(row=1, column=0, pady=10)

button_edit_part = tk.Button(tab_parts, text="Изменить", command=edit_part)
button_edit_part.grid(row=1, column=1, pady=10)

button_delete_part = tk.Button(tab_parts, text="Удалить", command=delete_part)
button_delete_part.grid(row=1, column=2, pady=10)

columns_parts = ("ID", "Название", "Артикул", "Цена", "Категория", "Марка авто", "Модель авто", "Количество")
tree_parts = ttk.Treeview(tab_parts, columns=columns_parts, show="headings")
for col in columns_parts:
    tree_parts.heading(col, text=col)
    tree_parts.column(col, width=100)
tree_parts.grid(row=2, column=0, columnspan=3, padx=10, pady=10)

# Вкладка "Клиенты"
label_search_clients = tk.Label(tab_clients, text="Поиск:")
label_search_clients.grid(row=0, column=0, padx=5, pady=5)
entry_search_clients = tk.Entry(tab_clients)
entry_search_clients.grid(row=0, column=1, padx=5, pady=5)

def search_clients():
    query = entry_search_clients.get()
    filter_tree(tree_clients, query, 'clients')

entry_search_clients.bind('<KeyRelease>', lambda event: search_clients())

label_client_name = tk.Label(tab_clients, text="Имя:")
label_client_name.grid(row=1, column=0, padx=5, pady=5)
entry_client_name = tk.Entry(tab_clients)
entry_client_name.grid(row=1, column=1, padx=5, pady=5)

label_client_phone = tk.Label(tab_clients, text="Телефон:")
label_client_phone.grid(row=2, column=0, padx=5, pady=5)
entry_client_phone = tk.Entry(tab_clients)
entry_client_phone.grid(row=2, column=1, padx=5, pady=5)

button_add_client = tk.Button(tab_clients, text="Добавить клиента", command=add_client)
button_add_client.grid(row=3, column=0, columnspan=2, pady=10)

button_edit_client = tk.Button(tab_clients, text="Редактировать", command=edit_client)
button_edit_client.grid(row=4, column=0, pady=5)

button_delete_client = tk.Button(tab_clients, text="Удалить", command=delete_client)
button_delete_client.grid(row=4, column=1, pady=5)

columns_clients = ("ID", "Имя", "Телефон")
tree_clients = ttk.Treeview(tab_clients, columns=columns_clients, show="headings")
for col in columns_clients:
    tree_clients.heading(col, text=col)
    tree_clients.column(col, width=100)
tree_clients.grid(row=5, column=0, columnspan=2, padx=10, pady=10)


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

        total_price = 0  # Для расчета общей суммы заказа

        for item in selected_parts:
            part_id = tree_selected_parts.item(item)['values'][0]
            quantity = tree_selected_parts.item(item)['values'][3]

            # Проверяем, достаточно ли товара на складе
            cursor.execute('SELECT quantity, price FROM parts WHERE id = ?', (part_id,))
            current_quantity, part_price = cursor.fetchone()
            if current_quantity < quantity:
                messagebox.showerror("Ошибка", f"Недостаточно запчастей в наличии для заказа (ID: {part_id}).")
                return

            # Уменьшаем количество на складе
            new_quantity = current_quantity - quantity
            cursor.execute('UPDATE parts SET quantity = ? WHERE id = ?', (new_quantity, part_id))

            # Добавляем запчасть в заказ
            cursor.execute('INSERT INTO order_parts (order_id, part_id, quantity) VALUES (?, ?, ?)',
                           (selected_order_id, part_id, quantity))

            # Рассчитываем общую сумму заказа
            total_price += part_price * quantity

        conn.commit()

        # Формируем отчет о заказе
        generate_order_report(selected_order_id, selected_client, order_date, total_price)

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
                tree_selected_parts.item(item, values=(part_id, part_name, part_price, int(current_quantity) + int(quantity)))
                return

        # Если запчасти нет в заказе, добавляем её
        tree_selected_parts.insert("", "end", values=(part_id, part_name, part_price, quantity))

    # Создание окна создания заказа
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


# Функция для просмотра всех заказов
def view_orders():
    tree_orders.delete(*tree_orders.get_children())
    cursor.execute('''
        SELECT orders.id, clients.name, clients.phone, orders.order_date, orders.status
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
        tree_orders.insert("", "end", values=(order_id, row[1], row[2], row[3], row[4], total))

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
        tree_order_details.column(col, width=150)
    tree_order_details.pack(padx=10, pady=10)

    for row in rows:
        tree_order_details.insert("", "end", values=row)

# Вкладка "Заказы"
tab_orders = ttk.Frame(tab_control)
tab_control.add(tab_orders, text="Заказы")

# Поиск заказов
label_search_orders = tk.Label(tab_orders, text="Поиск:")
label_search_orders.grid(row=0, column=0, padx=5, pady=5)
entry_search_orders = tk.Entry(tab_orders)
entry_search_orders.grid(row=0, column=1, padx=5, pady=5)

def search_orders():
    query = entry_search_orders.get()
    filter_tree(tree_orders, query, 'orders')

entry_search_orders.bind('<KeyRelease>', lambda event: search_orders())

# Кнопки управления заказами
button_create_order = tk.Button(tab_orders, text="Создать заказ", command=create_order)
button_create_order.grid(row=1, column=0, pady=10)

button_view_orders = tk.Button(tab_orders, text="Просмотреть заказы", command=view_orders)
button_view_orders.grid(row=1, column=1, pady=10)

# Таблица заказов
columns_orders = ("ID", "Клиент", "Телефон", "Дата", "Статус", "Общая сумма")
tree_orders = ttk.Treeview(tab_orders, columns=columns_orders, show="headings")
for col in columns_orders:
    tree_orders.heading(col, text=col)
    tree_orders.column(col, width=150)
tree_orders.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

# Кнопка просмотра деталей заказа
button_view_order_details = tk.Button(tab_orders, text="Посмотреть детали", command=view_order_details)
button_view_order_details.grid(row=3, column=0, pady=10)

# Выбор статуса заказа
label_status = tk.Label(tab_orders, text="Статус:")
label_status.grid(row=3, column=1, padx=5, pady=5)

combo_status = ttk.Combobox(tab_orders, values=["В обработке", "Выполнен", "Отменен"], state="readonly")
combo_status.grid(row=4, column=1, padx=5, pady=5)

# Кнопка обновления статуса заказа
button_update_status = tk.Button(tab_orders, text="Обновить статус", command=update_order_status)
button_update_status.grid(row=4, column=0, pady=10)


# Запуск приложения
view_manufacturers()
view_categories()
view_cars()
view_parts()
view_clients()
view_orders()

root.mainloop()

# Закрытие соединения с базой данных при выходе
conn.close()
