﻿namespace AutoPartsSellerApp
{
    partial class SuppliersForm
    {
        private System.ComponentModel.IContainer components = null;
        private System.Windows.Forms.DataGridView dataGridView;
        private System.Windows.Forms.TextBox txtName;
        private System.Windows.Forms.TextBox txtContactPerson;
        private System.Windows.Forms.TextBox txtPhone;
        private System.Windows.Forms.TextBox txtEmail;
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
            this.tableLayoutPanel = new System.Windows.Forms.TableLayoutPanel();
            this.dataGridView = new System.Windows.Forms.DataGridView();
            this.txtName = new System.Windows.Forms.TextBox();
            this.txtContactPerson = new System.Windows.Forms.TextBox();
            this.txtPhone = new System.Windows.Forms.TextBox();
            this.txtEmail = new System.Windows.Forms.TextBox();
            this.btnAdd = new System.Windows.Forms.Button();
            this.btnEdit = new System.Windows.Forms.Button();
            this.btnDelete = new System.Windows.Forms.Button();
            this.label1 = new System.Windows.Forms.Label();
            this.label2 = new System.Windows.Forms.Label();
            this.label3 = new System.Windows.Forms.Label();
            this.label4 = new System.Windows.Forms.Label();
            this.tableLayoutPanel.SuspendLayout();
            ((System.ComponentModel.ISupportInitialize)(this.dataGridView)).BeginInit();
            this.SuspendLayout();

            // tableLayoutPanel
            this.tableLayoutPanel.ColumnCount = 2;
            this.tableLayoutPanel.ColumnStyles.Add(new System.Windows.Forms.ColumnStyle(System.Windows.Forms.SizeType.Percent, 30F));
            this.tableLayoutPanel.ColumnStyles.Add(new System.Windows.Forms.ColumnStyle(System.Windows.Forms.SizeType.Percent, 70F));
            this.tableLayoutPanel.Controls.Add(this.label1, 0, 0);
            this.tableLayoutPanel.Controls.Add(this.txtName, 1, 0);
            this.tableLayoutPanel.Controls.Add(this.label2, 0, 1);
            this.tableLayoutPanel.Controls.Add(this.txtContactPerson, 1, 1);
            this.tableLayoutPanel.Controls.Add(this.label3, 0, 2);
            this.tableLayoutPanel.Controls.Add(this.txtPhone, 1, 2);
            this.tableLayoutPanel.Controls.Add(this.label4, 0, 3);
            this.tableLayoutPanel.Controls.Add(this.txtEmail, 1, 3);
            this.tableLayoutPanel.Controls.Add(this.btnAdd, 0, 4);
            this.tableLayoutPanel.Controls.Add(this.btnEdit, 1, 4);
            this.tableLayoutPanel.Controls.Add(this.btnDelete, 1, 5);
            this.tableLayoutPanel.Controls.Add(this.dataGridView, 0, 6);
            this.tableLayoutPanel.Dock = System.Windows.Forms.DockStyle.Fill;
            this.tableLayoutPanel.Location = new System.Drawing.Point(0, 0);
            this.tableLayoutPanel.Name = "tableLayoutPanel";
            this.tableLayoutPanel.RowCount = 7;
            this.tableLayoutPanel.RowStyles.Add(new System.Windows.Forms.RowStyle(System.Windows.Forms.SizeType.Absolute, 30F));
            this.tableLayoutPanel.RowStyles.Add(new System.Windows.Forms.RowStyle(System.Windows.Forms.SizeType.Absolute, 30F));
            this.tableLayoutPanel.RowStyles.Add(new System.Windows.Forms.RowStyle(System.Windows.Forms.SizeType.Absolute, 30F));
            this.tableLayoutPanel.RowStyles.Add(new System.Windows.Forms.RowStyle(System.Windows.Forms.SizeType.Absolute, 30F));
            this.tableLayoutPanel.RowStyles.Add(new System.Windows.Forms.RowStyle(System.Windows.Forms.SizeType.Absolute, 40F));
            this.tableLayoutPanel.RowStyles.Add(new System.Windows.Forms.RowStyle(System.Windows.Forms.SizeType.Absolute, 40F));
            this.tableLayoutPanel.RowStyles.Add(new System.Windows.Forms.RowStyle(System.Windows.Forms.SizeType.Percent, 100F));
            this.tableLayoutPanel.Size = new System.Drawing.Size(800, 450);
            this.tableLayoutPanel.TabIndex = 0;

            // dataGridView
            this.dataGridView.ColumnHeadersHeightSizeMode = System.Windows.Forms.DataGridViewColumnHeadersHeightSizeMode.AutoSize;
            this.tableLayoutPanel.SetColumnSpan(this.dataGridView, 2);
            this.dataGridView.Dock = System.Windows.Forms.DockStyle.Fill;
            this.dataGridView.Location = new System.Drawing.Point(3, 183);
            this.dataGridView.Name = "dataGridView";
            this.dataGridView.Size = new System.Drawing.Size(794, 264);
            this.dataGridView.TabIndex = 0;

            // txtName
            this.txtName.Dock = System.Windows.Forms.DockStyle.Fill;
            this.txtName.Location = new System.Drawing.Point(243, 3);
            this.txtName.Name = "txtName";
            this.txtName.Size = new System.Drawing.Size(554, 20);
            this.txtName.TabIndex = 1;

            // txtContactPerson
            this.txtContactPerson.Dock = System.Windows.Forms.DockStyle.Fill;
            this.txtContactPerson.Location = new System.Drawing.Point(243, 33);
            this.txtContactPerson.Name = "txtContactPerson";
            this.txtContactPerson.Size = new System.Drawing.Size(554, 20);
            this.txtContactPerson.TabIndex = 2;

            // txtPhone
            this.txtPhone.Dock = System.Windows.Forms.DockStyle.Fill;
            this.txtPhone.Location = new System.Drawing.Point(243, 63);
            this.txtPhone.Name = "txtPhone";
            this.txtPhone.Size = new System.Drawing.Size(554, 20);
            this.txtPhone.TabIndex = 3;

            // txtEmail
            this.txtEmail.Dock = System.Windows.Forms.DockStyle.Fill;
            this.txtEmail.Location = new System.Drawing.Point(243, 93);
            this.txtEmail.Name = "txtEmail";
            this.txtEmail.Size = new System.Drawing.Size(554, 20);
            this.txtEmail.TabIndex = 4;

            // btnAdd
            this.btnAdd.Dock = System.Windows.Forms.DockStyle.Fill;
            this.btnAdd.Location = new System.Drawing.Point(3, 123);
            this.btnAdd.Name = "btnAdd";
            this.btnAdd.Size = new System.Drawing.Size(234, 34);
            this.btnAdd.TabIndex = 5;
            this.btnAdd.Text = "Добавить";
            this.btnAdd.Click += new System.EventHandler(this.btnAdd_Click);

            // btnEdit
            this.btnEdit.Dock = System.Windows.Forms.DockStyle.Fill;
            this.btnEdit.Location = new System.Drawing.Point(243, 123);
            this.btnEdit.Name = "btnEdit";
            this.btnEdit.Size = new System.Drawing.Size(554, 34);
            this.btnEdit.TabIndex = 6;
            this.btnEdit.Text = "Редактировать";
            this.btnEdit.Click += new System.EventHandler(this.btnEdit_Click);

            // btnDelete
            this.btnDelete.Dock = System.Windows.Forms.DockStyle.Fill;
            this.btnDelete.Location = new System.Drawing.Point(243, 163);
            this.btnDelete.Name = "btnDelete";
            this.btnDelete.Size = new System.Drawing.Size(554, 34);
            this.btnDelete.TabIndex = 7;
            this.btnDelete.Text = "Удалить";
            this.btnDelete.Click += new System.EventHandler(this.btnDelete_Click);

            // label1
            this.label1.AutoSize = true;
            this.label1.Dock = System.Windows.Forms.DockStyle.Fill;
            this.label1.Location = new System.Drawing.Point(3, 0);
            this.label1.Name = "label1";
            this.label1.Size = new System.Drawing.Size(234, 30);
            this.label1.TabIndex = 8;
            this.label1.Text = "Название:";
            this.label1.TextAlign = System.Drawing.ContentAlignment.MiddleLeft;

            // label2
            this.label2.AutoSize = true;
            this.label2.Dock = System.Windows.Forms.DockStyle.Fill;
            this.label2.Location = new System.Drawing.Point(3, 30);
            this.label2.Name = "label2";
            this.label2.Size = new System.Drawing.Size(234, 30);
            this.label2.TabIndex = 9;
            this.label2.Text = "Контактное лицо:";
            this.label2.TextAlign = System.Drawing.ContentAlignment.MiddleLeft;

            // label3
            this.label3.AutoSize = true;
            this.label3.Dock = System.Windows.Forms.DockStyle.Fill;
            this.label3.Location = new System.Drawing.Point(3, 60);
            this.label3.Name = "label3";
            this.label3.Size = new System.Drawing.Size(234, 30);
            this.label3.TabIndex = 10;
            this.label3.Text = "Телефон:";
            this.label3.TextAlign = System.Drawing.ContentAlignment.MiddleLeft;

            // label4
            this.label4.AutoSize = true;
            this.label4.Dock = System.Windows.Forms.DockStyle.Fill;
            this.label4.Location = new System.Drawing.Point(3, 90);
            this.label4.Name = "label4";
            this.label4.Size = new System.Drawing.Size(234, 30);
            this.label4.TabIndex = 11;
            this.label4.Text = "Email:";
            this.label4.TextAlign = System.Drawing.ContentAlignment.MiddleLeft;

            // SuppliersForm
            this.ClientSize = new System.Drawing.Size(800, 450);
            this.Controls.Add(this.tableLayoutPanel);
            this.Name = "SuppliersForm";
            this.Text = "Поставщики";
            this.tableLayoutPanel.ResumeLayout(false);
            this.tableLayoutPanel.PerformLayout();
            ((System.ComponentModel.ISupportInitialize)(this.dataGridView)).EndInit();
            this.ResumeLayout(false);
        }
    }
}