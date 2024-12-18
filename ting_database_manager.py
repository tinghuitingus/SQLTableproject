import sqlite3
import sys
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from data_entry_sheet import DataEntry

class EditDialog(QDialog):
    def __init__(self, row_data, column_names):
        super().__init__()
        self.row_data = row_data
        self.column_names = column_names
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Edit Row')
        self.setGeometry(200,200,400,300)

        layout = QVBoxLayout()

        self.inputs = []
        for i, (name, value) in enumerate(zip(self.column_names, self.row_data)):
            if i != 0 :
                label = QLabel(name, self)
                line_edit = QLineEdit(self)
                line_edit.setText(str(value))
                self.inputs.append(line_edit)
                layout.addWidget(label)
                layout.addWidget(line_edit)

        self.buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        layout.addWidget(self.buttonBox)
        self.setLayout(layout)

    def get_new_data(self):
        return [input.text() for input in self.inputs]


class TingDB(QDialog):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Ting's DB")
        self.setGeometry(100,100,1000,500)
        self.bt1 = QPushButton("Add Entry", self)
        self.bt1.clicked.connect(self.open_data_entry)
        self.bt2 = QPushButton("Delete Entry", self)
        self.bt2.clicked.connect(self.delete_data_entry)
        self.bt3 = QPushButton("Edit Entry", self)
        self.bt3.clicked.connect(self.edit_data_entry)
        layout = QVBoxLayout()
        layout.addWidget(self.bt1)
        layout.addWidget(self.bt2)
        layout.addWidget(self.bt3)

        self.table = QTableWidget(self)
        self.load_data()

        layout.addWidget(self.table)
        self.setLayout(layout)

    def open_data_entry(self):
        self.data_entry = DataEntry(self)
        self.data_entry.show()




    def delete_data_entry(self):
        selected_row = self.table.currentRow()
        if selected_row >= 0:
            user_id = self.table.item(selected_row, 0).text()

            reply = QMessageBox.question(self, 'Confirm Deletion?', 'Are you sure you want to delete the selected entry', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if reply == QMessageBox.Yes:
                database_path = 'example.db'
                conn = sqlite3.connect(database_path)
                cur = conn.cursor()
                cur.execute("DELETE FROM users2 WHERE id=?", (user_id,))
                conn.commit()
                conn.close()

                self.table.removeRow(selected_row)
                QMessageBox.information(self, 'Success', 'Entry deleted successfully!')
            else:
                QMessageBox.warning(self, 'Error', 'No entry selected!')
    def edit_data_entry(self):
        selected_row = self.table.currentRow()
        if selected_row >= 0:
            row_data = [self.table.item(selected_row,col).text() for col in range(self.table.columnCount())]
            column_names = [self.table.horizontalHeaderItem(col).text() for col in range(self.table.columnCount())]

            dialog = EditDialog(row_data, column_names)
            if dialog.exec() == QDialog.Accepted:
                new_data = dialog.get_new_data()
                user_id = self.table.item(selected_row, 0).text()

                for col, value in enumerate(new_data):
                    if col != 0:
                        self.table.item(selected_row, col).setText(value)

                database_path = 'example.db'
                conn = sqlite3.connect(database_path)
                cur = conn.cursor()
                for col, value in enumerate(new_data):
                    if col != 0:
                        column_name = self.table.horizontalHeaderItem(col).text()
                        cur.execute(f"UPDATE users2 SET {column_name} = ? WHERE id = ?", (value, user_id))
                conn.commit()
                conn.close()

                QMessageBox.information(self, 'Success', 'Row Updated successfully!')
            else:
                QMessageBox.warning(self, 'Error', 'No row selected!')


    def load_data(self):
        conn = sqlite3.connect('example.db')
        curr = conn.cursor()

        table_name = 'users2'
        curr.execute(f"SELECT * FROM {table_name}")

        rows = curr.fetchall()
        col_names = [n[0] for n in curr.description]

        self.table.setRowCount(len(rows))
        self.table.setColumnCount(len(col_names))

        self.table.setHorizontalHeaderLabels(col_names)

        for row_idx, row in enumerate(rows):
            for col_idx, value in enumerate(row):
                item = QTableWidgetItem(str(value))
                item.setFlags(item.flags() & ~Qt.ItemIsEditable)
                self.table.setItem(row_idx, col_idx, item)
                conn.commit()
        conn.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = TingDB()
    ex.show()
    sys.exit(app.exec_())






