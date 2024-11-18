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

        private void InitializeComponent()
        {
            this.panelMenu = new System.Windows.Forms.Panel();
            this.btnCategories = new System.Windows.Forms.Button();
            this.btnStock = new System.Windows.Forms.Button();
            this.btnOrder = new System.Windows.Forms.Button();
            this.btnSettings = new System.Windows.Forms.Button();
            this.btnHelp = new System.Windows.Forms.Button();

            // 
            // Form1
            // 
            this.ClientSize = new System.Drawing.Size(1440, 900);
            this.Controls.Add(this.panelMenu);
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
        }
    }
}
