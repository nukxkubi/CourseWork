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
        }

        private void LoadData()
        {
            using (SQLiteConnection conn = new SQLiteConnection(ConnectionString))
            {
                conn.Open();
                string sql = "SELECT * FROM Orders";
                using (SQLiteDataAdapter da = new SQLiteDataAdapter(sql, conn))
                {
                    DataTable dt = new DataTable();
                    da.Fill(dt);

                    dataGridView.DataSource = dt;

                    dataGridView.Columns["Id"].HeaderText = "Id";
                    dataGridView.Columns["CustomerId"].HeaderText = "ID клиента";
                    dataGridView.Columns["PartId"].HeaderText = "ID запчасти";
                    dataGridView.Columns["Quantity"].HeaderText = "Количество";
                    dataGridView.Columns["OrderDate"].HeaderText = "Дата заказа";

                    dataGridView.AutoSizeColumnsMode = DataGridViewAutoSizeColumnsMode.Fill;
                }
            }
        }

        private void btnAdd_Click(object sender, EventArgs e)
        {
            using (SQLiteConnection conn = new SQLiteConnection(ConnectionString))
            {
                conn.Open();
                string sql = "INSERT INTO Orders (CustomerId, PartId, Quantity, OrderDate) VALUES (@CustomerId, @PartId, @Quantity, @OrderDate)";
                using (SQLiteCommand cmd = new SQLiteCommand(sql, conn))
                {
                    cmd.Parameters.AddWithValue("@CustomerId", int.Parse(txtCustomerId.Text));
                    cmd.Parameters.AddWithValue("@PartId", int.Parse(txtPartId.Text));
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
                    string sql = "UPDATE Orders SET CustomerId = @CustomerId, PartId = @PartId, Quantity = @Quantity, OrderDate = @OrderDate WHERE Id = @Id";
                    using (SQLiteCommand cmd = new SQLiteCommand(sql, conn))
                    {
                        cmd.Parameters.AddWithValue("@CustomerId", int.Parse(txtCustomerId.Text));
                        cmd.Parameters.AddWithValue("@PartId", int.Parse(txtPartId.Text));
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