using System;
using System.Windows.Forms;

namespace AutoPartsSellerApp
{
    public partial class Form1 : Form
    {
        public Form1()
        {
            InitializeComponent();
            // Добавьте обработчики событий
            btnCategories.Click += BtnCategories_Click;
            btnStock.Click += BtnStock_Click;
            btnOrder.Click += BtnOrder_Click;
            btnSettings.Click += BtnSettings_Click;
            btnHelp.Click += BtnHelp_Click;
        }

        private void BtnCategories_Click(object sender, EventArgs e)
        {
            MessageBox.Show("Открыта категория товаров!");
        }

        private void BtnStock_Click(object sender, EventArgs e)
        {
            MessageBox.Show("Просмотр склада!");
        }

        private void BtnOrder_Click(object sender, EventArgs e)
        {
            MessageBox.Show("Оформление заказа!");
        }

        private void BtnSettings_Click(object sender, EventArgs e)
        {
            MessageBox.Show("Открыты настройки!");
        }

        private void BtnHelp_Click(object sender, EventArgs e)
        {
            MessageBox.Show("Справка по приложению!");
        }
    }
}
