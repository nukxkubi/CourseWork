using System;
using System.Collections.Generic;
using System.Linq;
using System.Windows.Forms;

namespace AutoPartsSellerApp
{
    public partial class Form1 : Form
    {
        private Dictionary<string, List<string>> carBrandsAndModels;

        public Form1()
        {
            InitializeComponent();
            InitializeData();
            InitializeEvents();
        }

        // Инициализация данных
        private void InitializeData()
        {
            carBrandsAndModels = new Dictionary<string, List<string>>()
            {
                { "Toyota", new List<string> { "Camry", "Corolla", "RAV4", "Land Cruiser" } },
                { "Лада", new List<string> { "Гранта", "Приора", "Веста", "2107" } },
                { "Nissan", new List<string> { "X-Trail", "Note", "Juke", "Teana" } },
                { "Honda", new List<string> { "Fit", "CR-V", "HR-V", "Accord" } },
                { "Hyundai", new List<string> { "Solaris", "Santa Fe", "Tucson", "Creta", "Accent" } },
                { "Audi", new List<string> { "A6", "A4", "Q7", "Q5", "A3", "A7", "A8", "Q8" } },
                { "BMW", new List<string> { "5-Series", "X5", "3-Series", "X6", "X3", "M3", "M5", "X1" } },
                { "Lexus", new List<string> { "RX350", "RX300", "LX570", "GX460", "RX450h", "GX470", "ES300" } },
                { "Mazda", new List<string> { "Mazda3", "Mazda6", "CX-5", "Demio", "Axela", "RX-7", "RX-8" } },
                { "Mercedes-Benz", new List<string> { "E-Class", "C-Class", "S-Class", "M-Class", "G-Class", "S-Class" } },
                { "Mitsubishi", new List<string> { "Outlander", "Lancer", "Pajero", "Pajero Sport", "ASX", "Delica", "Galant", "Mirage" } }
            };

            cbCarBrands.Items.AddRange(carBrandsAndModels.Keys.ToArray());
        }


        // Инициализация событий
        private void InitializeEvents()
        {
            btnCategories.Click += BtnCategories_Click;
            btnStock.Click += BtnStock_Click;
            btnOrder.Click += BtnOrder_Click;
            cbCarBrands.SelectedIndexChanged += CbCarBrands_SelectedIndexChanged;
        }

        // Событие: кнопка "Категории"
        private void BtnCategories_Click(object sender, EventArgs e)
        {
            ToggleCarSelectionControls(true);
        }

        // Событие: кнопка "Склад"
        private void BtnStock_Click(object sender, EventArgs e)
        {
            ToggleCarSelectionControls(false);
            MessageBox.Show("Просмотр склада!");
        }

        // Событие: кнопка "Оформление заказа"
        private void BtnOrder_Click(object sender, EventArgs e)
        {
            ToggleCarSelectionControls(false);
            MessageBox.Show("Оформление заказа!");
        }

        // Событие: выбор марки автомобиля
        private void CbCarBrands_SelectedIndexChanged(object sender, EventArgs e)
        {
            cbCarModels.Items.Clear(); // Очищаем список моделей
            cbCarModels.Enabled = false; // Отключаем ComboBox для моделей

            if (cbCarBrands.SelectedIndex != -1)
            {
                string selectedBrand = cbCarBrands.SelectedItem?.ToString();  // Получаем выбранную марку

                if (!string.IsNullOrEmpty(selectedBrand) && carBrandsAndModels.ContainsKey(selectedBrand))
                {
                    // Добавляем модели в cbCarModels
                    cbCarModels.Items.AddRange(carBrandsAndModels[selectedBrand].ToArray());
                    cbCarModels.Enabled = true; // Включаем ComboBox для моделей
                }
                else
                {
                    MessageBox.Show("Не найдено моделей для выбранной марки.");
                }
            }
        }

        // Включение/выключение контролов выбора марки и модели автомобиля
        private void ToggleCarSelectionControls(bool isVisible)
        {
            lblSelectCarBrand.Visible = isVisible;
            cbCarBrands.Visible = isVisible;
            lblSelectCarModel.Visible = isVisible;
            cbCarModels.Visible = isVisible;
        }
    }
}
