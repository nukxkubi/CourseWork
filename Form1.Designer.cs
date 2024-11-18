namespace AutoPartsSellerApp
{
    partial class Form1
    {
        private System.Windows.Forms.Panel panelMenu; // Панель меню
        private System.Windows.Forms.Button btnCategories; // Кнопка "Категории"
        private System.Windows.Forms.Button btnStock; // Кнопка "Склад"
        private System.Windows.Forms.Button btnOrder; // Кнопка "Оформление заказа"
        private System.Windows.Forms.Button btnSettings; // Кнопка "Настройки"
        private System.Windows.Forms.Button btnHelp; // Кнопка "Справка"

        private System.Windows.Forms.Label lblSelectCategory; // Текст "Выберите категорию"
        private System.Windows.Forms.ComboBox cbCategories; // Выпадающий список категорий
        private System.Windows.Forms.Label lblSelectSubCategory; // Текст "Выберите подкатегорию"
        private System.Windows.Forms.ComboBox cbSubCategories; // Выпадающий список подкатегорий

        private void InitializeComponent()
        {
            this.panelMenu = new System.Windows.Forms.Panel();
            this.btnCategories = new System.Windows.Forms.Button();
            this.btnStock = new System.Windows.Forms.Button();
            this.btnOrder = new System.Windows.Forms.Button();
            this.btnSettings = new System.Windows.Forms.Button();
            this.btnHelp = new System.Windows.Forms.Button();

            this.lblSelectCategory = new System.Windows.Forms.Label();
            this.cbCategories = new System.Windows.Forms.ComboBox();
            this.lblSelectSubCategory = new System.Windows.Forms.Label();
            this.cbSubCategories = new System.Windows.Forms.ComboBox();

            // 
            // Form1
            // 
            this.ClientSize = new System.Drawing.Size(800, 450);
            this.Controls.Add(this.panelMenu);
            this.Controls.Add(this.lblSelectCategory);
            this.Controls.Add(this.cbCategories);
            this.Controls.Add(this.lblSelectSubCategory);
            this.Controls.Add(this.cbSubCategories);
            this.Name = "Form1";
            this.Text = "АРМ Продавца Автозапчастей";

            // 
            // panelMenu
            // 
            this.panelMenu.Dock = System.Windows.Forms.DockStyle.Left;
            this.panelMenu.Width = 200;
            this.panelMenu.BackColor = System.Drawing.Color.LightGray;
            this.panelMenu.Controls.Add(this.btnHelp);
            this.panelMenu.Controls.Add(this.btnSettings);
            this.panelMenu.Controls.Add(this.btnOrder);
            this.panelMenu.Controls.Add(this.btnStock);
            this.panelMenu.Controls.Add(this.btnCategories);

            // 
            // btnCategories
            // 
            this.btnCategories.Dock = System.Windows.Forms.DockStyle.Top;
            this.btnCategories.Height = 50;
            this.btnCategories.Text = "Категории";
            this.btnCategories.Name = "btnCategories";

            // 
            // btnStock
            // 
            this.btnStock.Dock = System.Windows.Forms.DockStyle.Top;
            this.btnStock.Height = 50;
            this.btnStock.Text = "Склад";
            this.btnStock.Name = "btnStock";

            // 
            // btnOrder
            // 
            this.btnOrder.Dock = System.Windows.Forms.DockStyle.Top;
            this.btnOrder.Height = 50;
            this.btnOrder.Text = "Оформление заказа";
            this.btnOrder.Name = "btnOrder";

            // 
            // btnSettings
            // 
            this.btnSettings.Dock = System.Windows.Forms.DockStyle.Bottom;
            this.btnSettings.Height = 50;
            this.btnSettings.Text = "Настройки";
            this.btnSettings.Name = "btnSettings";

            // 
            // btnHelp
            // 
            this.btnHelp.Dock = System.Windows.Forms.DockStyle.Bottom;
            this.btnHelp.Height = 50;
            this.btnHelp.Text = "Справка";
            this.btnHelp.Name = "btnHelp";

            // 
            // lblSelectCategory
            // 
            this.lblSelectCategory.AutoSize = true;
            this.lblSelectCategory.Location = new System.Drawing.Point(220, 30);
            this.lblSelectCategory.Name = "lblSelectCategory";
            this.lblSelectCategory.Size = new System.Drawing.Size(200, 20);
            this.lblSelectCategory.Text = "Выберите категорию запчасти:";
            this.lblSelectCategory.Visible = false;

            // 
            // cbCategories
            // 
            this.cbCategories.DropDownStyle = System.Windows.Forms.ComboBoxStyle.DropDownList;
            this.cbCategories.Location = new System.Drawing.Point(220, 60);
            this.cbCategories.Name = "cbCategories";
            this.cbCategories.Size = new System.Drawing.Size(300, 28);
            this.cbCategories.Visible = false;

            // 
            // lblSelectSubCategory
            // 
            this.lblSelectSubCategory.AutoSize = true;
            this.lblSelectSubCategory.Location = new System.Drawing.Point(220, 110);
            this.lblSelectSubCategory.Name = "lblSelectSubCategory";
            this.lblSelectSubCategory.Size = new System.Drawing.Size(200, 20);
            this.lblSelectSubCategory.Text = "Выберите что именно вас интересует:";
            this.lblSelectSubCategory.Visible = false;

            // 
            // cbSubCategories
            // 
            this.cbSubCategories.DropDownStyle = System.Windows.Forms.ComboBoxStyle.DropDownList;
            this.cbSubCategories.Location = new System.Drawing.Point(220, 140);
            this.cbSubCategories.Name = "cbSubCategories";
            this.cbSubCategories.Size = new System.Drawing.Size(300, 28);
            this.cbSubCategories.Visible = false;
        }
    }
}
