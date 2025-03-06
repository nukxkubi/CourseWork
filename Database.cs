using System;
using System.Data.SQLite;

namespace AutoPartsSellerApp
{
    public class Database
    {
        private const string ConnectionString = "Data Source=AutoParts.db;Version=3;";

        public static void InitializeDatabase()
        {
            using (SQLiteConnection conn = new SQLiteConnection(ConnectionString))
            {
                conn.Open();

                // Создаем таблицу "Автозапчасти"
                string sqlParts = @"
                    CREATE TABLE IF NOT EXISTS Parts (
                        Id INTEGER PRIMARY KEY AUTOINCREMENT,
                        Name TEXT NOT NULL,
                        Description TEXT,
                        Price REAL NOT NULL,
                        StockQuantity INTEGER NOT NULL,
                        CarId INTEGER,
                        SupplierId INTEGER,
                        FOREIGN KEY (CarId) REFERENCES Cars(Id),
                        FOREIGN KEY (SupplierId) REFERENCES Suppliers(Id)
                    );";

                // Создаем таблицу "Клиенты"
                string sqlCustomers = @"
                    CREATE TABLE IF NOT EXISTS Customers (
                        Id INTEGER PRIMARY KEY AUTOINCREMENT,
                        Name TEXT NOT NULL,
                        Phone TEXT,
                        Email TEXT
                    );";

                // Создаем таблицу "Поставщики"
                string sqlSuppliers = @"
                    CREATE TABLE IF NOT EXISTS Suppliers (
                        Id INTEGER PRIMARY KEY AUTOINCREMENT,
                        Name TEXT NOT NULL,
                        ContactPerson TEXT,
                        Phone TEXT,
                        Email TEXT
                    );";

                // Создаем таблицу "Автомобили"
                string sqlCars = @"
                    CREATE TABLE IF NOT EXISTS Cars (
                        Id INTEGER PRIMARY KEY AUTOINCREMENT,
                        Make TEXT NOT NULL,
                        Model TEXT NOT NULL,
                        Year INTEGER NOT NULL
                    );";

                // Создаем таблицу "Заказы"
                string sqlOrders = @"
                    CREATE TABLE IF NOT EXISTS Orders (
                        Id INTEGER PRIMARY KEY AUTOINCREMENT,
                        CustomerId INTEGER NOT NULL,
                        PartId INTEGER NOT NULL,
                        Quantity INTEGER NOT NULL,
                        OrderDate TEXT NOT NULL,
                        FOREIGN KEY (CustomerId) REFERENCES Customers(Id),
                        FOREIGN KEY (PartId) REFERENCES Parts(Id)
                    );";

                // Выполняем SQL-запросы для создания таблиц
                using (SQLiteCommand cmd = new SQLiteCommand(sqlParts, conn))
                {
                    cmd.ExecuteNonQuery();
                }

                using (SQLiteCommand cmd = new SQLiteCommand(sqlCustomers, conn))
                {
                    cmd.ExecuteNonQuery();
                }

                using (SQLiteCommand cmd = new SQLiteCommand(sqlSuppliers, conn))
                {
                    cmd.ExecuteNonQuery();
                }

                using (SQLiteCommand cmd = new SQLiteCommand(sqlCars, conn))
                {
                    cmd.ExecuteNonQuery();
                }

                using (SQLiteCommand cmd = new SQLiteCommand(sqlOrders, conn))
                {
                    cmd.ExecuteNonQuery();
                }
            }
        }
    }
}
