using System;
using System.Data;
using System.Data.SQLite;
using System.Windows.Forms;

namespace AutoPartsSellerApp
{
    public partial class CustomersForm : Form
    {
        private const string ConnectionString = "Data Source=AutoParts.db;Version=3;";

        public CustomersForm()
        {
            InitializeComponent();
            LoadData();
        }

        private void LoadData()
        {
            using (SQLiteConnection conn = new SQLiteConnection(ConnectionString))
            {
                conn.Open();
                string sql = "SELECT * FROM Customers";
                using (SQLiteDataAdapter da = new SQLiteDataAdapter(sql, conn))
                {
                    DataTable dt = new DataTable();
                    da.Fill(dt);

                    dataGridView.DataSource = dt;

                    dataGridView.Columns["Id"].HeaderText = "Id";
                    dataGridView.Columns["Name"].HeaderText = "Имя";
                    dataGridView.Columns["Phone"].HeaderText = "Телефон";
                    dataGridView.Columns["Email"].HeaderText = "Email";

                    dataGridView.AutoSizeColumnsMode = DataGridViewAutoSizeColumnsMode.Fill;
                }
            }
        }

        private void btnAdd_Click(object sender, EventArgs e)
        {
            using (SQLiteConnection conn = new SQLiteConnection(ConnectionString))
            {
                conn.Open();
                string sql = "INSERT INTO Customers (Name, Phone, Email) VALUES (@Name, @Phone, @Email)";
                using (SQLiteCommand cmd = new SQLiteCommand(sql, conn))
                {
                    cmd.Parameters.AddWithValue("@Name", txtName.Text);
                    cmd.Parameters.AddWithValue("@Phone", txtPhone.Text);
                    cmd.Parameters.AddWithValue("@Email", txtEmail.Text);
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
                    string sql = "UPDATE Customers SET Name = @Name, Phone = @Phone, Email = @Email WHERE Id = @Id";
                    using (SQLiteCommand cmd = new SQLiteCommand(sql, conn))
                    {
                        cmd.Parameters.AddWithValue("@Name", txtName.Text);
                        cmd.Parameters.AddWithValue("@Phone", txtPhone.Text);
                        cmd.Parameters.AddWithValue("@Email", txtEmail.Text);
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
                    string sql = "DELETE FROM Customers WHERE Id = @Id";
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