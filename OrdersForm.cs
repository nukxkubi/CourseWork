using System;
using System.Data;
using System.Data.SQLite;
using System.Windows.Forms;

namespace AutoPartsSellerApp
{
    public partial class OrdersForm : Form
    {
        private const string ConnectionString = "Data Source=AutoParts.db;Version=3;";

        public OrdersForm()
        {
            InitializeComponent();
            LoadData();
            LoadCustomers();
            LoadParts();
        }

        private void LoadData()
        {
            using (SQLiteConnection conn = new SQLiteConnection(ConnectionString))
            {
                conn.Open();
                string sql = @"
                    SELECT Orders.Id, 
                           Customers.Name AS CustomerName, 
                           Parts.Name AS PartName, 
                           Orders.Quantity, 
                           Orders.OrderDate
                    FROM Orders
                    LEFT JOIN Customers ON Orders.CustomerId = Customers.Id
                    LEFT JOIN Parts ON Orders.PartId = Parts.Id";
                using (SQLiteDataAdapter da = new SQLiteDataAdapter(sql, conn))
                {
                    DataTable dt = new DataTable();
                    da.Fill(dt);

                    dataGridView.DataSource = dt;

                    // Переименовываем колонки на русский язык
                    dataGridView.Columns["Id"].HeaderText = "Id";
                    dataGridView.Columns["CustomerName"].HeaderText = "Клиент";
                    dataGridView.Columns["PartName"].HeaderText = "Запчасть";
                    dataGridView.Columns["Quantity"].HeaderText = "Количество";
                    dataGridView.Columns["OrderDate"].HeaderText = "Дата заказа";

                    dataGridView.AutoSizeColumnsMode = DataGridViewAutoSizeColumnsMode.Fill;
                }
            }
        }

        private void LoadCustomers()
        {
            using (SQLiteConnection conn = new SQLiteConnection(ConnectionString))
            {
                conn.Open();
                string sql = "SELECT Id, Name FROM Customers";
                using (SQLiteDataAdapter da = new SQLiteDataAdapter(sql, conn))
                {
                    DataTable dt = new DataTable();
                    da.Fill(dt);

                    comboBoxCustomers.DataSource = dt;
                    comboBoxCustomers.DisplayMember = "Name";
                    comboBoxCustomers.ValueMember = "Id";
                }
            }
        }

        private void LoadParts()
        {
            using (SQLiteConnection conn = new SQLiteConnection(ConnectionString))
            {
                conn.Open();
                string sql = "SELECT Id, Name FROM Parts";
                using (SQLiteDataAdapter da = new SQLiteDataAdapter(sql, conn))
                {
                    DataTable dt = new DataTable();
                    da.Fill(dt);

                    comboBoxParts.DataSource = dt;
                    comboBoxParts.DisplayMember = "Name";
                    comboBoxParts.ValueMember = "Id";
                }
            }
        }

        private void btnAdd_Click(object sender, EventArgs e)
        {
            using (SQLiteConnection conn = new SQLiteConnection(ConnectionString))
            {
                conn.Open();
                string sql = @"
                    INSERT INTO Orders (CustomerId, PartId, Quantity, OrderDate)
                    VALUES (@CustomerId, @PartId, @Quantity, @OrderDate)";
                using (SQLiteCommand cmd = new SQLiteCommand(sql, conn))
                {
                    cmd.Parameters.AddWithValue("@CustomerId", comboBoxCustomers.SelectedValue);
                    cmd.Parameters.AddWithValue("@PartId", comboBoxParts.SelectedValue);
                    cmd.Parameters.AddWithValue("@Quantity", int.Parse(txtQuantity.Text));
                    cmd.Parameters.AddWithValue("@OrderDate", DateTime.Now.ToString("yyyy-MM-dd"));
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
                        UPDATE Orders 
                        SET CustomerId = @CustomerId, PartId = @PartId, Quantity = @Quantity, OrderDate = @OrderDate
                        WHERE Id = @Id";
                    using (SQLiteCommand cmd = new SQLiteCommand(sql, conn))
                    {
                        cmd.Parameters.AddWithValue("@CustomerId", comboBoxCustomers.SelectedValue);
                        cmd.Parameters.AddWithValue("@PartId", comboBoxParts.SelectedValue);
                        cmd.Parameters.AddWithValue("@Quantity", int.Parse(txtQuantity.Text));
                        cmd.Parameters.AddWithValue("@OrderDate", DateTime.Now.ToString("yyyy-MM-dd"));
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
                    string sql = "DELETE FROM Orders WHERE Id = @Id";
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
