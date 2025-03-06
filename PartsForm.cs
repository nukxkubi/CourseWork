using System;
using System.Data;
using System.Data.SQLite;
using System.Windows.Forms;

namespace AutoPartsSellerApp
{
    public partial class PartsForm : Form
    {
        private const string ConnectionString = "Data Source=AutoParts.db;Version=3;";

        public PartsForm()
        {
            InitializeComponent();
            InitializeControls();
            LoadData();
            LoadCars();
            LoadSuppliers();
        }

        private void InitializeControls()
        {
            // Настройка формы
            this.Text = "Автозапчасти";
            this.Size = new System.Drawing.Size(800, 450);

            // Создание и настройка элементов управления
            label1 = new Label { Text = "Название:", Location = new System.Drawing.Point(20, 20), AutoSize = true };
            txtName = new TextBox { Location = new System.Drawing.Point(120, 20), Width = 200 };

            label2 = new Label { Text = "Описание:", Location = new System.Drawing.Point(20, 50), AutoSize = true };
            txtDescription = new TextBox { Location = new System.Drawing.Point(120, 50), Width = 200 };

            label3 = new Label { Text = "Цена:", Location = new System.Drawing.Point(20, 80), AutoSize = true };
            txtPrice = new TextBox { Location = new System.Drawing.Point(120, 80), Width = 200 };

            label4 = new Label { Text = "Количество на складе:", Location = new System.Drawing.Point(20, 110), AutoSize = true };
            txtStockQuantity = new TextBox { Location = new System.Drawing.Point(120, 110), Width = 200 };

            label5 = new Label { Text = "Автомобиль:", Location = new System.Drawing.Point(20, 140), AutoSize = true };
            comboBoxCars = new ComboBox { Location = new System.Drawing.Point(120, 140), Width = 200, DropDownStyle = ComboBoxStyle.DropDownList };

            label6 = new Label { Text = "Поставщик:", Location = new System.Drawing.Point(20, 170), AutoSize = true };
            comboBoxSuppliers = new ComboBox { Location = new System.Drawing.Point(120, 170), Width = 200, DropDownStyle = ComboBoxStyle.DropDownList };

            btnAdd = new Button { Text = "Добавить", Location = new System.Drawing.Point(20, 200), Width = 100 };
            btnAdd.Click += btnAdd_Click;

            btnEdit = new Button { Text = "Редактировать", Location = new System.Drawing.Point(130, 200), Width = 100 };
            btnEdit.Click += btnEdit_Click;

            btnDelete = new Button { Text = "Удалить", Location = new System.Drawing.Point(240, 200), Width = 100 };
            btnDelete.Click += btnDelete_Click;

            dataGridView = new DataGridView { Location = new System.Drawing.Point(20, 240), Width = 740, Height = 180 };
            dataGridView.AutoSizeColumnsMode = DataGridViewAutoSizeColumnsMode.Fill;

            // Добавление элементов на форму
            this.Controls.Add(label1);
            this.Controls.Add(txtName);
            this.Controls.Add(label2);
            this.Controls.Add(txtDescription);
            this.Controls.Add(label3);
            this.Controls.Add(txtPrice);
            this.Controls.Add(label4);
            this.Controls.Add(txtStockQuantity);
            this.Controls.Add(label5);
            this.Controls.Add(comboBoxCars);
            this.Controls.Add(label6);
            this.Controls.Add(comboBoxSuppliers);
            this.Controls.Add(btnAdd);
            this.Controls.Add(btnEdit);
            this.Controls.Add(btnDelete);
            this.Controls.Add(dataGridView);
        }

        private void LoadData()
        {
            try
            {
                using (SQLiteConnection conn = new SQLiteConnection(ConnectionString))
                {
                    conn.Open();
                    string sql = @"
                        SELECT Parts.Id, Parts.Name, Parts.Description, Parts.Price, Parts.StockQuantity, 
                               Cars.Make || ' ' || Cars.Model AS Car, Suppliers.Name AS Supplier
                        FROM Parts
                        LEFT JOIN Cars ON Parts.CarId = Cars.Id
                        LEFT JOIN Suppliers ON Parts.SupplierId = Suppliers.Id";
                    using (SQLiteDataAdapter da = new SQLiteDataAdapter(sql, conn))
                    {
                        DataTable dt = new DataTable();
                        da.Fill(dt);

                        dataGridView.DataSource = dt;

                        // Переименовываем колонки на русский язык
                        dataGridView.Columns["Id"].HeaderText = "Id";
                        dataGridView.Columns["Name"].HeaderText = "Название";
                        dataGridView.Columns["Description"].HeaderText = "Описание";
                        dataGridView.Columns["Price"].HeaderText = "Цена";
                        dataGridView.Columns["StockQuantity"].HeaderText = "Количество на складе";
                        dataGridView.Columns["Car"].HeaderText = "Автомобиль";
                        dataGridView.Columns["Supplier"].HeaderText = "Поставщик";
                    }
                }
            }
            catch (Exception ex)
            {
                MessageBox.Show("Ошибка при загрузке данных: " + ex.Message);
            }
        }

        private void LoadCars()
        {
            try
            {
                using (SQLiteConnection conn = new SQLiteConnection(ConnectionString))
                {
                    conn.Open();
                    string sql = "SELECT Id, Make || ' ' || Model AS Car FROM Cars";
                    using (SQLiteDataAdapter da = new SQLiteDataAdapter(sql, conn))
                    {
                        DataTable dt = new DataTable();
                        da.Fill(dt);

                        // Вывод данных в консоль для проверки
                        foreach (DataRow row in dt.Rows)
                        {
                            Console.WriteLine($"Id: {row["Id"]}, Car: {row["Car"]}");
                        }

                        comboBoxCars.DataSource = dt;
                        comboBoxCars.DisplayMember = "Car";
                        comboBoxCars.ValueMember = "Id";
                    }
                }
            }
            catch (Exception ex)
            {
                MessageBox.Show("Ошибка при загрузке автомобилей: " + ex.Message);
            }
        }

        private void LoadSuppliers()
        {
            try
            {
                using (SQLiteConnection conn = new SQLiteConnection(ConnectionString))
                {
                    conn.Open();
                    string sql = "SELECT Id, Name FROM Suppliers";
                    using (SQLiteDataAdapter da = new SQLiteDataAdapter(sql, conn))
                    {
                        DataTable dt = new DataTable();
                        da.Fill(dt);

                        // Вывод данных в консоль для проверки
                        foreach (DataRow row in dt.Rows)
                        {
                            Console.WriteLine($"Id: {row["Id"]}, Name: {row["Name"]}");
                        }

                        comboBoxSuppliers.DataSource = dt;
                        comboBoxSuppliers.DisplayMember = "Name";
                        comboBoxSuppliers.ValueMember = "Id";
                    }
                }
            }
            catch (Exception ex)
            {
                MessageBox.Show("Ошибка при загрузке поставщиков: " + ex.Message);
            }
        }

        private void btnAdd_Click(object sender, EventArgs e)
        {
            try
            {
                using (SQLiteConnection conn = new SQLiteConnection(ConnectionString))
                {
                    conn.Open();
                    string sql = @"
                        INSERT INTO Parts (Name, Description, Price, StockQuantity, CarId, SupplierId)
                        VALUES (@Name, @Description, @Price, @StockQuantity, @CarId, @SupplierId)";
                    using (SQLiteCommand cmd = new SQLiteCommand(sql, conn))
                    {
                        cmd.Parameters.AddWithValue("@Name", txtName.Text);
                        cmd.Parameters.AddWithValue("@Description", txtDescription.Text);
                        cmd.Parameters.AddWithValue("@Price", decimal.Parse(txtPrice.Text));
                        cmd.Parameters.AddWithValue("@StockQuantity", int.Parse(txtStockQuantity.Text));
                        cmd.Parameters.AddWithValue("@CarId", comboBoxCars.SelectedValue);
                        cmd.Parameters.AddWithValue("@SupplierId", comboBoxSuppliers.SelectedValue);
                        cmd.ExecuteNonQuery();
                    }
                }
                LoadData();
            }
            catch (Exception ex)
            {
                MessageBox.Show("Ошибка при добавлении записи: " + ex.Message);
            }
        }

        private void btnEdit_Click(object sender, EventArgs e)
        {
            try
            {
                if (dataGridView.SelectedRows.Count > 0)
                {
                    int id = Convert.ToInt32(dataGridView.SelectedRows[0].Cells["Id"].Value);

                    using (SQLiteConnection conn = new SQLiteConnection(ConnectionString))
                    {
                        conn.Open();
                        string sql = @"
                            UPDATE Parts 
                            SET Name = @Name, Description = @Description, Price = @Price, 
                                StockQuantity = @StockQuantity, CarId = @CarId, SupplierId = @SupplierId
                            WHERE Id = @Id";
                        using (SQLiteCommand cmd = new SQLiteCommand(sql, conn))
                        {
                            cmd.Parameters.AddWithValue("@Name", txtName.Text);
                            cmd.Parameters.AddWithValue("@Description", txtDescription.Text);
                            cmd.Parameters.AddWithValue("@Price", decimal.Parse(txtPrice.Text));
                            cmd.Parameters.AddWithValue("@StockQuantity", int.Parse(txtStockQuantity.Text));
                            cmd.Parameters.AddWithValue("@CarId", comboBoxCars.SelectedValue);
                            cmd.Parameters.AddWithValue("@SupplierId", comboBoxSuppliers.SelectedValue);
                            cmd.Parameters.AddWithValue("@Id", id);
                            cmd.ExecuteNonQuery();
                        }
                    }
                    LoadData();
                }
                else
                {
                    MessageBox.Show("Выберите запись для редактирования.");
                }
            }
            catch (Exception ex)
            {
                MessageBox.Show("Ошибка при редактировании записи: " + ex.Message);
            }
        }

        private void btnDelete_Click(object sender, EventArgs e)
        {
            try
            {
                if (dataGridView.SelectedRows.Count > 0)
                {
                    int id = Convert.ToInt32(dataGridView.SelectedRows[0].Cells["Id"].Value);

                    using (SQLiteConnection conn = new SQLiteConnection(ConnectionString))
                    {
                        conn.Open();
                        string sql = "DELETE FROM Parts WHERE Id = @Id";
                        using (SQLiteCommand cmd = new SQLiteCommand(sql, conn))
                        {
                            cmd.Parameters.AddWithValue("@Id", id);
                            cmd.ExecuteNonQuery();
                        }
                    }
                    LoadData();
                }
                else
                {
                    MessageBox.Show("Выберите запись для удаления.");
                }
            }
            catch (Exception ex)
            {
                MessageBox.Show("Ошибка при удалении записи: " + ex.Message);
            }
        }
    }
}
