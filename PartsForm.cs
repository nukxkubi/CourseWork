using System;
using System.Data;
using System.Data.SQLite;
using System.Linq;
using System.Windows.Forms;

namespace AutoPartsSellerApp
{
    public partial class PartsForm : Form
    {
        private const string ConnectionString = "Data Source=AutoParts.db;Version=3;";

        public PartsForm()
        {
            InitializeComponent();
            LoadData();
            LoadCars();
            LoadSuppliers();
        }

        private void LoadData()
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

                    dataGridView.AutoSizeColumnsMode = DataGridViewAutoSizeColumnsMode.Fill;
                }
            }
        }

        private void LoadCars()
        {
            using (SQLiteConnection conn = new SQLiteConnection(ConnectionString))
            {
                conn.Open();
                string sql = "SELECT Id, Make || ' ' || Model AS Car FROM Cars";
                using (SQLiteDataAdapter da = new SQLiteDataAdapter(sql, conn))
                {
                    DataTable dt = new DataTable();
                    da.Fill(dt);

                    comboBoxCars.DataSource = dt;
                    comboBoxCars.DisplayMember = "Car";
                    comboBoxCars.ValueMember = "Id";
                }
            }
        }

        private void LoadSuppliers()
        {
            using (SQLiteConnection conn = new SQLiteConnection(ConnectionString))
            {
                conn.Open();
                string sql = "SELECT Id, Name FROM Suppliers";
                using (SQLiteDataAdapter da = new SQLiteDataAdapter(sql, conn))
                {
                    DataTable dt = new DataTable();
                    da.Fill(dt);

                    comboBoxSuppliers.DataSource = dt;
                    comboBoxSuppliers.DisplayMember = "Name";
                    comboBoxSuppliers.ValueMember = "Id";
                }
            }
        }

        private void btnAdd_Click(object sender, EventArgs e)
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

        private void btnEdit_Click(object sender, EventArgs e)
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

        private void btnDelete_Click(object sender, EventArgs e)
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
    }
}
