using System;
using System.Windows.Forms;

namespace AutoPartsSellerApp
{
    public partial class Form1 : Form
    {
        public Form1()
        {
            InitializeComponent();
            // �������� ����������� �������
            btnCategories.Click += BtnCategories_Click;
            btnStock.Click += BtnStock_Click;
            btnOrder.Click += BtnOrder_Click;
            btnSettings.Click += BtnSettings_Click;
            btnHelp.Click += BtnHelp_Click;
        }

        private void BtnCategories_Click(object sender, EventArgs e)
        {
            MessageBox.Show("������� ��������� �������!");
        }

        private void BtnStock_Click(object sender, EventArgs e)
        {
            MessageBox.Show("�������� ������!");
        }

        private void BtnOrder_Click(object sender, EventArgs e)
        {
            MessageBox.Show("���������� ������!");
        }

        private void BtnSettings_Click(object sender, EventArgs e)
        {
            MessageBox.Show("������� ���������!");
        }

        private void BtnHelp_Click(object sender, EventArgs e)
        {
            MessageBox.Show("������� �� ����������!");
        }
    }
}