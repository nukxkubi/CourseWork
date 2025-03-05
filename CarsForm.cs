using System;
using System.Data;
using System.Data.SQLite;
using System.Windows.Forms;

namespace AutoPartsSellerApp
{
    public partial class CarsForm : Form
    {
        private const string ConnectionString = "Data Source=AutoParts.db;Version=3;";

        public CarsForm()
        {
            InitializeComponent();
            LoadData();
        }

        private void LoadData()
        {
            using (SQLiteConnection conn = new SQLiteConnection(ConnectionString))
            {
                conn.Open();
                string sql = "SELECT * FROM Cars";
                using (SQLiteDataAdapter da = new SQLiteDataAdapter(sql, conn))
                {
                    DataTable dt = new DataTable();
                    da.Fill(dt);

                    dataGridView.DataSource = dt;

                    dataGridView.Columns["Id"].HeaderText = "Id";
                    dataGridView.Columns["Make"].HeaderText = "Марка";
                    dataGridView.Columns["Model"].HeaderText = "Модель";
                    dataGridView.Columns["Year"].HeaderText = "Год выпуска";

                    dataGridView.AutoSizeColumnsMode = DataGridViewAutoSizeColumnsMode.Fill;
                }
            }
        }

        private void btnAdd_Click(object sender, EventArgs e)
        {
            using (SQLiteConnection conn = new SQLiteConnection(ConnectionString))
            {
                conn.Open();
                string sql = "INSERT INTO Cars (Make, Model, Year) VALUES (@Make, @Model, @Year)";
                using (SQLiteCommand cmd = new SQLiteCommand(sql, conn))
                {
                    cmd.Parameters.AddWithValue("@Make", txtMake.Text);
                    cmd.Parameters.AddWithValue("@Model", txtModel.Text);
                    cmd.Parameters.AddWithValue("@Year", int.Parse(txtYear.Text));
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
                    string sql = "UPDATE Cars SET Make = @Make, Model = @Model, Year = @Year WHERE Id = @Id";
                    using (SQLiteCommand cmd = new SQLiteCommand(sql, conn))
                    {
                        cmd.Parameters.AddWithValue("@Make", txtMake.Text);
                        cmd.Parameters.AddWithValue("@Model", txtModel.Text);
                        cmd.Parameters.AddWithValue("@Year", int.Parse(txtYear.Text));
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
                    string sql = "DELETE FROM Cars WHERE Id = @Id";
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