using System;
using System.Collections.Generic;
using System.Linq;
using System.Windows.Forms;

namespace AutoPartsSellerApp
{
    public partial class Form1 : Form
    {
        private Dictionary<string, List<string>> categories;

        public Form1()
        {
            InitializeComponent();
            InitializeData();
            InitializeEvents();
        }

        // Инициализация данных
        private void InitializeData()
        {
            // Категории и подкатегории
            // TODO: Подключить базу данных для полного списка запчастей.
            
            categories = new Dictionary<string, List<string>>()
            {
                { "Двигатель", new List<string> { "Поршни", "Масляный фильтр", "Ремень ГРМ" } },
                { "Подвеска", new List<string> { "Амортизаторы", "Пружины", "Стабилизатор" } },
                { "Кузов", new List<string> { "Бампер", "Капот", "Зеркала" } }
            };

            cbCategories.Items.AddRange(categories.Keys.ToArray());
        }

        // Инициализация событий
        private void InitializeEvents()
        {
            btnCategories.Click += BtnCategories_Click;
            btnStock.Click += BtnStock_Click;
            btnOrder.Click += BtnOrder_Click;
            cbCategories.SelectedIndexChanged += CbCategories_SelectedIndexChanged;
        }

        // Событие: кнопка "Категории"
        private void BtnCategories_Click(object sender, EventArgs e)
        {
            ToggleCategoryControls(true);
        }

        // Событие: кнопка "Склад"
        private void BtnStock_Click(object sender, EventArgs e)
        {
            ToggleCategoryControls(false);
            MessageBox.Show("Просмотр склада!");
        }

        // Событие: кнопка "Оформление заказа"
        private void BtnOrder_Click(object sender, EventArgs e)
        {
            ToggleCategoryControls(false);
            MessageBox.Show("Оформление заказа!");
        }

        // Событие: выбор категории
        private void CbCategories_SelectedIndexChanged(object sender, EventArgs e)
        {
            cbSubCategories.Items.Clear();
            cbSubCategories.Enabled = false;

            if (cbCategories.SelectedIndex != -1)
            {
                string selectedCategory = cbCategories.SelectedItem.ToString();
                cbSubCategories.Items.AddRange(categories[selectedCategory].ToArray());
                cbSubCategories.Enabled = true;
            }
        }

        // Включение/выключение контролов
        private void ToggleCategoryControls(bool isVisible)
        {
            lblSelectCategory.Visible = isVisible;
            cbCategories.Visible = isVisible;
            lblSelectSubCategory.Visible = isVisible;
            cbSubCategories.Visible = isVisible;
        }
    }
}
