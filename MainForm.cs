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
            Database.InitializeDatabase(); // Инициализация базы данных
        }

        private void MainForm_Load(object sender, EventArgs e)
        {
            // Инициализация меню
            MenuStrip menuStrip = new MenuStrip();
            this.MainMenuStrip = menuStrip;

            // Меню "Справочники"
            ToolStripMenuItem referenceMenu = new ToolStripMenuItem("Справочники");
            referenceMenu.DropDownItems.Add("Автозапчасти", null, (s, ev) => OpenForm(new PartsForm()));
            referenceMenu.DropDownItems.Add("Клиенты", null, (s, ev) => OpenForm(new CustomersForm()));
            referenceMenu.DropDownItems.Add("Поставщики", null, (s, ev) => OpenForm(new SuppliersForm()));
            referenceMenu.DropDownItems.Add("Автомобили", null, (s, ev) => OpenForm(new CarsForm()));
            referenceMenu.DropDownItems.Add("Заказы", null, (s, ev) => OpenForm(new OrdersForm()));

            // Меню "Файл"
            ToolStripMenuItem fileMenu = new ToolStripMenuItem("Файл");
            fileMenu.DropDownItems.Add("Импорт из Excel", null, (s, ev) => ImportFromExcel());
            fileMenu.DropDownItems.Add("Экспорт в Excel", null, (s, ev) => ExportToExcel());

            // Меню "Отчет"
            ToolStripMenuItem reportMenu = new ToolStripMenuItem("Отчет");
            reportMenu.DropDownItems.Add("Сформировать отчет", null, (s, ev) => GenerateReport());

            // Меню "Справка"
            ToolStripMenuItem helpMenu = new ToolStripMenuItem("Справка");
            helpMenu.DropDownItems.Add("О программе", null, (s, ev) => ShowAbout());

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
            MessageBox.Show("Функция импорта из Excel пока не реализована.");
        }

        private void ExportToExcel()
        {
            MessageBox.Show("Функция экспорта в Excel пока не реализована.");
        }

        private void GenerateReport()
        {
            MessageBox.Show("Функция формирования отчета пока не реализована.");
        }

        private void ShowAbout()
        {
            MessageBox.Show("АРМ продавца автозапчастей\nВерсия 1.0", "О программе");
        }
    }
}