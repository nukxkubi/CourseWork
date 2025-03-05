namespace AutoPartsSellerApp
{
    partial class PartsForm
    {
        private System.ComponentModel.IContainer components = null;
        private System.Windows.Forms.DataGridView dataGridView;
        private System.Windows.Forms.TextBox txtName;
        private System.Windows.Forms.TextBox txtDescription;
        private System.Windows.Forms.TextBox txtPrice;
        private System.Windows.Forms.TextBox txtStockQuantity;
        private System.Windows.Forms.Button btnAdd;
        private System.Windows.Forms.Button btnEdit;
        private System.Windows.Forms.Button btnDelete;
        private System.Windows.Forms.Label label1;
        private System.Windows.Forms.Label label2;
        private System.Windows.Forms.Label label3;
        private System.Windows.Forms.Label label4;
        private System.Windows.Forms.TableLayoutPanel tableLayoutPanel;

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
            tableLayoutPanel = new TableLayoutPanel();
            label1 = new Label();
            txtName = new TextBox();
            label2 = new Label();
            txtDescription = new TextBox();
            label3 = new Label();
            txtPrice = new TextBox();
            label4 = new Label();
            txtStockQuantity = new TextBox();
            btnAdd = new Button();
            btnEdit = new Button();
            btnDelete = new Button();
            dataGridView = new DataGridView();
            tableLayoutPanel.SuspendLayout();
            ((System.ComponentModel.ISupportInitialize)dataGridView).BeginInit();
            SuspendLayout();
            // 
            // tableLayoutPanel
            // 
            tableLayoutPanel.ColumnCount = 2;
            tableLayoutPanel.ColumnStyles.Add(new ColumnStyle(SizeType.Percent, 30F));
            tableLayoutPanel.ColumnStyles.Add(new ColumnStyle(SizeType.Percent, 70F));
            tableLayoutPanel.Controls.Add(label1, 0, 0);
            tableLayoutPanel.Controls.Add(txtName, 1, 0);
            tableLayoutPanel.Controls.Add(label2, 0, 1);
            tableLayoutPanel.Controls.Add(txtDescription, 1, 1);
            tableLayoutPanel.Controls.Add(label3, 0, 2);
            tableLayoutPanel.Controls.Add(txtPrice, 1, 2);
            tableLayoutPanel.Controls.Add(label4, 0, 3);
            tableLayoutPanel.Controls.Add(txtStockQuantity, 1, 3);
            tableLayoutPanel.Controls.Add(btnAdd, 0, 4);
            tableLayoutPanel.Controls.Add(btnEdit, 1, 4);
            tableLayoutPanel.Controls.Add(btnDelete, 1, 5);
            tableLayoutPanel.Controls.Add(dataGridView, 0, 6);
            tableLayoutPanel.Dock = DockStyle.Fill;
            tableLayoutPanel.Location = new Point(0, 0);
            tableLayoutPanel.Name = "tableLayoutPanel";
            tableLayoutPanel.RowCount = 7;
            tableLayoutPanel.RowStyles.Add(new RowStyle(SizeType.Absolute, 30F));
            tableLayoutPanel.RowStyles.Add(new RowStyle(SizeType.Absolute, 30F));
            tableLayoutPanel.RowStyles.Add(new RowStyle(SizeType.Absolute, 30F));
            tableLayoutPanel.RowStyles.Add(new RowStyle(SizeType.Absolute, 30F));
            tableLayoutPanel.RowStyles.Add(new RowStyle(SizeType.Absolute, 40F));
            tableLayoutPanel.RowStyles.Add(new RowStyle(SizeType.Absolute, 40F));
            tableLayoutPanel.RowStyles.Add(new RowStyle(SizeType.Percent, 100F));
            tableLayoutPanel.Size = new Size(800, 450);
            tableLayoutPanel.TabIndex = 0;
            // 
            // label1
            // 
            label1.AutoSize = true;
            label1.Dock = DockStyle.Fill;
            label1.Location = new Point(3, 0);
            label1.Name = "label1";
            label1.Size = new Size(234, 30);
            label1.TabIndex = 8;
            label1.Text = "Название:";
            label1.TextAlign = ContentAlignment.MiddleLeft;
            // 
            // txtName
            // 
            txtName.Dock = DockStyle.Fill;
            txtName.Location = new Point(243, 3);
            txtName.Name = "txtName";
            txtName.Size = new Size(554, 23);
            txtName.TabIndex = 1;
            // 
            // label2
            // 
            label2.AutoSize = true;
            label2.Dock = DockStyle.Fill;
            label2.Location = new Point(3, 30);
            label2.Name = "label2";
            label2.Size = new Size(234, 30);
            label2.TabIndex = 9;
            label2.Text = "Описание:";
            label2.TextAlign = ContentAlignment.MiddleLeft;
            // 
            // txtDescription
            // 
            txtDescription.Dock = DockStyle.Fill;
            txtDescription.Location = new Point(243, 33);
            txtDescription.Name = "txtDescription";
            txtDescription.Size = new Size(554, 23);
            txtDescription.TabIndex = 2;
            // 
            // label3
            // 
            label3.AutoSize = true;
            label3.Dock = DockStyle.Fill;
            label3.Location = new Point(3, 60);
            label3.Name = "label3";
            label3.Size = new Size(234, 30);
            label3.TabIndex = 10;
            label3.Text = "Цена:";
            label3.TextAlign = ContentAlignment.MiddleLeft;
            // 
            // txtPrice
            // 
            txtPrice.Dock = DockStyle.Fill;
            txtPrice.Location = new Point(243, 63);
            txtPrice.Name = "txtPrice";
            txtPrice.Size = new Size(554, 23);
            txtPrice.TabIndex = 3;
            // 
            // label4
            // 
            label4.AutoSize = true;
            label4.Dock = DockStyle.Fill;
            label4.Location = new Point(3, 90);
            label4.Name = "label4";
            label4.Size = new Size(234, 30);
            label4.TabIndex = 11;
            label4.Text = "Количество на складе:";
            label4.TextAlign = ContentAlignment.MiddleLeft;
            // 
            // txtStockQuantity
            // 
            txtStockQuantity.Dock = DockStyle.Fill;
            txtStockQuantity.Location = new Point(243, 93);
            txtStockQuantity.Name = "txtStockQuantity";
            txtStockQuantity.Size = new Size(554, 23);
            txtStockQuantity.TabIndex = 4;
            // 
            // btnAdd
            // 
            btnAdd.Dock = DockStyle.Fill;
            btnAdd.Location = new Point(3, 123);
            btnAdd.Name = "btnAdd";
            btnAdd.Size = new Size(234, 34);
            btnAdd.TabIndex = 5;
            btnAdd.Text = "Добавить";
            btnAdd.Click += btnAdd_Click;
            // 
            // btnEdit
            // 
            btnEdit.Dock = DockStyle.Fill;
            btnEdit.Location = new Point(243, 123);
            btnEdit.Name = "btnEdit";
            btnEdit.Size = new Size(554, 34);
            btnEdit.TabIndex = 6;
            btnEdit.Text = "Редактировать";
            btnEdit.Click += btnEdit_Click;
            // 
            // btnDelete
            // 
            btnDelete.Dock = DockStyle.Fill;
            btnDelete.Location = new Point(243, 163);
            btnDelete.Name = "btnDelete";
            btnDelete.Size = new Size(554, 34);
            btnDelete.TabIndex = 7;
            btnDelete.Text = "Удалить";
            btnDelete.Click += btnDelete_Click;
            // 
            // dataGridView
            // 
            dataGridView.ColumnHeadersHeightSizeMode = DataGridViewColumnHeadersHeightSizeMode.AutoSize;
            tableLayoutPanel.SetColumnSpan(dataGridView, 2);
            dataGridView.Dock = DockStyle.Fill;
            dataGridView.Location = new Point(3, 203);
            dataGridView.Name = "dataGridView";
            dataGridView.Size = new Size(794, 244);
            dataGridView.TabIndex = 0;
            // 
            // PartsForm
            // 
            ClientSize = new Size(800, 450);
            Controls.Add(tableLayoutPanel);
            Name = "PartsForm";
            Text = "Автозапчасти";
            tableLayoutPanel.ResumeLayout(false);
            tableLayoutPanel.PerformLayout();
            ((System.ComponentModel.ISupportInitialize)dataGridView).EndInit();
            ResumeLayout(false);
        }
    }
}