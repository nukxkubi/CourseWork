using System;
using System.Data.Entity;
using System.Windows.Forms;

namespace AutoPartsSellerApp
{
    public partial class MainForm : Form
    {
        public MainForm()
        {
            InitializeComponent();
            Database.InitializeDatabase(); // ������������� ���� ������
        }

        private void MainForm_Load(object sender, EventArgs e)
        {
            // ������������� ����
            MenuStrip menuStrip = new MenuStrip();
            this.MainMenuStrip = menuStrip;

            // ���� "�����������"
            ToolStripMenuItem referenceMenu = new ToolStripMenuItem("�����������");
            referenceMenu.DropDownItems.Add("������������", null, (s, ev) => OpenForm(new PartsForm()));
            referenceMenu.DropDownItems.Add("�������", null, (s, ev) => OpenForm(new CustomersForm()));
            referenceMenu.DropDownItems.Add("����������", null, (s, ev) => OpenForm(new SuppliersForm()));
            referenceMenu.DropDownItems.Add("����������", null, (s, ev) => OpenForm(new CarsForm()));
            referenceMenu.DropDownItems.Add("������", null, (s, ev) => OpenForm(new OrdersForm()));

            // ���� "����"
            ToolStripMenuItem fileMenu = new ToolStripMenuItem("����");
            fileMenu.DropDownItems.Add("������ �� Excel", null, (s, ev) => ImportFromExcel());
            fileMenu.DropDownItems.Add("������� � Excel", null, (s, ev) => ExportToExcel());

            // ���� "�����"
            ToolStripMenuItem reportMenu = new ToolStripMenuItem("�����");
            reportMenu.DropDownItems.Add("������������ �����", null, (s, ev) => GenerateReport());

            // ���� "�������"
            ToolStripMenuItem helpMenu = new ToolStripMenuItem("�������");
            helpMenu.DropDownItems.Add("� ���������", null, (s, ev) => ShowAbout());

            menuStrip.Items.Add(referenceMenu);
            menuStrip.Items.Add(fileMenu);
            menuStrip.Items.Add(reportMenu);
            menuStrip.Items.Add(helpMenu);

            this.Controls.Add(menuStrip);
        }

        private void OpenForm(Form form)
        {
            form.MdiParent = this;
            form.Show();
        }

        private void ImportFromExcel()
        {
            MessageBox.Show("������� ������� �� Excel ���� �� �����������.");
        }

        private void ExportToExcel()
        {
            MessageBox.Show("������� �������� � Excel ���� �� �����������.");
        }

        private void GenerateReport()
        {
            MessageBox.Show("������� ������������ ������ ���� �� �����������.");
        }

        private void ShowAbout()
        {
            MessageBox.Show("��� �������� �������������\n������ 1.0", "� ���������");
        }
    }
}