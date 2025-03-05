namespace AutoPartsSellerApp
{
    partial class MainForm
    {
        private System.ComponentModel.IContainer components = null;
        private System.Windows.Forms.MenuStrip menuStrip;
        private System.Windows.Forms.ToolStripMenuItem referenceMenu;
        private System.Windows.Forms.ToolStripMenuItem fileMenu;
        private System.Windows.Forms.ToolStripMenuItem reportMenu;
        private System.Windows.Forms.ToolStripMenuItem helpMenu;
        private System.Windows.Forms.StatusStrip statusStrip;
        private System.Windows.Forms.ToolStripStatusLabel statusLabel;

        protected override void Dispose(bool disposing)
        {
            if (disposing && (components != null))
            {
                components.Dispose();
            }
            base.Dispose(disposing);
        }

        private void InitializeComponent()
        {
            this.components = new System.ComponentModel.Container();
            this.menuStrip = new System.Windows.Forms.MenuStrip();
            this.referenceMenu = new System.Windows.Forms.ToolStripMenuItem();
            this.fileMenu = new System.Windows.Forms.ToolStripMenuItem();
            this.reportMenu = new System.Windows.Forms.ToolStripMenuItem();
            this.helpMenu = new System.Windows.Forms.ToolStripMenuItem();
            this.statusStrip = new System.Windows.Forms.StatusStrip();
            this.statusLabel = new System.Windows.Forms.ToolStripStatusLabel();
            this.menuStrip.SuspendLayout();
            this.statusStrip.SuspendLayout();
            this.SuspendLayout();

            // menuStrip
            this.menuStrip.Items.AddRange(new System.Windows.Forms.ToolStripItem[] {
                this.referenceMenu,
                this.fileMenu,
                this.reportMenu,
                this.helpMenu
            });
            this.menuStrip.Location = new System.Drawing.Point(0, 0);
            this.menuStrip.Name = "menuStrip";
            this.menuStrip.Size = new System.Drawing.Size(800, 24);
            this.menuStrip.TabIndex = 0;
            this.menuStrip.Text = "menuStrip";

            // referenceMenu
            this.referenceMenu.Text = "Справочники";
            this.referenceMenu.DropDownItems.AddRange(new System.Windows.Forms.ToolStripItem[] {
                new System.Windows.Forms.ToolStripMenuItem("Автозапчасти", null, (s, ev) => OpenForm(new PartsForm())),
                new System.Windows.Forms.ToolStripMenuItem("Клиенты", null, (s, ev) => OpenForm(new CustomersForm())),
                new System.Windows.Forms.ToolStripMenuItem("Поставщики", null, (s, ev) => OpenForm(new SuppliersForm())),
                new System.Windows.Forms.ToolStripMenuItem("Автомобили", null, (s, ev) => OpenForm(new CarsForm())),
                new System.Windows.Forms.ToolStripMenuItem("Заказы", null, (s, ev) => OpenForm(new OrdersForm()))
            });

            // fileMenu
            this.fileMenu.Text = "Файл";
            this.fileMenu.DropDownItems.AddRange(new System.Windows.Forms.ToolStripItem[] {
                new System.Windows.Forms.ToolStripMenuItem("Импорт из Excel", null, (s, ev) => ImportFromExcel()),
                new System.Windows.Forms.ToolStripMenuItem("Экспорт в Excel", null, (s, ev) => ExportToExcel())
            });

            // reportMenu
            this.reportMenu.Text = "Отчет";
            this.reportMenu.DropDownItems.AddRange(new System.Windows.Forms.ToolStripItem[] {
                new System.Windows.Forms.ToolStripMenuItem("Сформировать отчет", null, (s, ev) => GenerateReport())
            });

            // helpMenu
            this.helpMenu.Text = "Справка";
            this.helpMenu.DropDownItems.AddRange(new System.Windows.Forms.ToolStripItem[] {
                new System.Windows.Forms.ToolStripMenuItem("О программе", null, (s, ev) => ShowAbout())
            });

            // statusStrip
            this.statusStrip.Items.AddRange(new System.Windows.Forms.ToolStripItem[] {
                this.statusLabel
            });
            this.statusStrip.Location = new System.Drawing.Point(0, 428);
            this.statusStrip.Name = "statusStrip";
            this.statusStrip.Size = new System.Drawing.Size(800, 22);
            this.statusStrip.TabIndex = 1;
            this.statusStrip.Text = "statusStrip";

            // statusLabel
            this.statusLabel.Name = "statusLabel";
            this.statusLabel.Size = new System.Drawing.Size(118, 17);
            this.statusLabel.Text = "Готово к работе";

            // MainForm
            this.ClientSize = new System.Drawing.Size(800, 450);
            this.Controls.Add(this.statusStrip);
            this.Controls.Add(this.menuStrip);
            this.IsMdiContainer = true;
            this.MainMenuStrip = this.menuStrip;
            this.Name = "MainForm";
            this.Text = "АРМ продавца автозапчастей";
            this.WindowState = System.Windows.Forms.FormWindowState.Maximized;
            this.menuStrip.ResumeLayout(false);
            this.menuStrip.PerformLayout();
            this.statusStrip.ResumeLayout(false);
            this.statusStrip.PerformLayout();
            this.ResumeLayout(false);
            this.PerformLayout();
        }
    }
}