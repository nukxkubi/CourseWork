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

                string sql = @"
                    CREATE TABLE IF NOT EXISTS Parts (
                        Id INTEGER PRIMARY KEY AUTOINCREMENT,
                        Name TEXT NOT NULL,
                        Description TEXT,
                        Price REAL NOT NULL,
                        StockQuantity INTEGER NOT NULL
                    );

                    CREATE TABLE IF NOT EXISTS Customers (
                        Id INTEGER PRIMARY KEY AUTOINCREMENT,
                        Name TEXT NOT NULL,
                        Phone TEXT,
                        Email TEXT
                    );

                    CREATE TABLE IF NOT EXISTS Suppliers (
                        Id INTEGER PRIMARY KEY AUTOINCREMENT,
                        Name TEXT NOT NULL,
                        ContactPerson TEXT,
                        Phone TEXT,
                        Email TEXT
                    );

                    CREATE TABLE IF NOT EXISTS Cars (
                        Id INTEGER PRIMARY KEY AUTOINCREMENT,
                        Make TEXT NOT NULL,
                        Model TEXT NOT NULL,
                        Year INTEGER NOT NULL
                    );

                    CREATE TABLE IF NOT EXISTS Orders (
                        Id INTEGER PRIMARY KEY AUTOINCREMENT,
                        CustomerId INTEGER NOT NULL,
                        PartId INTEGER NOT NULL,
                        Quantity INTEGER NOT NULL,
                        OrderDate TEXT NOT NULL,
                        FOREIGN KEY(CustomerId) REFERENCES Customers(Id),
                        FOREIGN KEY(PartId) REFERENCES Parts(Id)
                    );";

                using (SQLiteCommand cmd = new SQLiteCommand(sql, conn))
                {
                    cmd.ExecuteNonQuery();
                }
            }
        }
    }
}