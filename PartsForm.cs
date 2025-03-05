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
            LoadData();
        }

        private void LoadData()
        {
            using (SQLiteConnection conn = new SQLiteConnection(ConnectionString))
            {
                conn.Open();
                string sql = "SELECT * FROM Parts";
                using (SQLiteDataAdapter da = new SQLiteDataAdapter(sql, conn))
                {
                    DataTable dt = new DataTable();
                    da.Fill(dt);

                    // Назначаем DataGridView данные из таблицы
                    dataGridView.DataSource = dt;

                    // Переименовываем колонки на русский язык
                    dataGridView.Columns["Id"].HeaderText = "Id";
                    dataGridView.Columns["Name"].HeaderText = "Название";
                    dataGridView.Columns["Description"].HeaderText = "Описание";
                    dataGridView.Columns["Price"].HeaderText = "Цена";
                    dataGridView.Columns["StockQuantity"].HeaderText = "Количество на складе";

                    // Подгоняем размер таблицы
                    dataGridView.AutoSizeColumnsMode = DataGridViewAutoSizeColumnsMode.Fill;
                }
            }
        }

        private void btnAdd_Click(object sender, EventArgs e)
        {
            using (SQLiteConnection conn = new SQLiteConnection(ConnectionString))
            {
                conn.Open();
                string sql = "INSERT INTO Parts (Name, Description, Price, StockQuantity) VALUES (@Name, @Description, @Price, @StockQuantity)";
                using (SQLiteCommand cmd = new SQLiteCommand(sql, conn))
                {
                    cmd.Parameters.AddWithValue("@Name", txtName.Text);
                    cmd.Parameters.AddWithValue("@Description", txtDescription.Text);
                    cmd.Parameters.AddWithValue("@Price", decimal.Parse(txtPrice.Text));
                    cmd.Parameters.AddWithValue("@StockQuantity", int.Parse(txtStockQuantity.Text));
                    cmd.ExecuteNonQuery();
                }
            }
            LoadData(); // Обновляем данные после добавления
        }

        private void btnEdit_Click(object sender, EventArgs e)
        {
            if (dataGridView.SelectedRows.Count > 0)
            {
                int id = Convert.ToInt32(dataGridView.SelectedRows[0].Cells["Id"].Value);

                using (SQLiteConnection conn = new SQLiteConnection(ConnectionString))
                {
                    conn.Open();
                    string sql = "UPDATE Parts SET Name = @Name, Description = @Description, Price = @Price, StockQuantity = @StockQuantity WHERE Id = @Id";
                    using (SQLiteCommand cmd = new SQLiteCommand(sql, conn))
                    {
                        cmd.Parameters.AddWithValue("@Name", txtName.Text);
                        cmd.Parameters.AddWithValue("@Description", txtDescription.Text);
                        cmd.Parameters.AddWithValue("@Price", decimal.Parse(txtPrice.Text));
                        cmd.Parameters.AddWithValue("@StockQuantity", int.Parse(txtStockQuantity.Text));
                        cmd.Parameters.AddWithValue("@Id", id);
                        cmd.ExecuteNonQuery();
                    }
                }
                LoadData(); // Обновляем данные после редактирования
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
                LoadData(); // Обновляем данные после удаления
            }
            else
            {
                MessageBox.Show("Выберите запись для удаления.");
            }
        }
    }
}