import sqlite3
import sys
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

class DataEntry(QDialog):
    def __init__(self, parent = None):
        super().__init__(parent)
        self.parent = parent
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Add Entry to Database')
        self.setGeometry(100,100,400,200)

        self.layout = QVBoxLayout()

        self.name_label = QLabel('Name', self)
        self.name_input = QLineEdit(self)

        self.age_label = QLabel('Age:', self)
        self.age_input = QLineEdit(self)

        self.add_button = QPushButton('Add Entry', self)
        self.add_button.clicked.connect(self.add_entry)

        self.back_button = QPushButton('Go Back', self)
        self.back_button.clicked.connect(self.go_back)


        self.layout.addWidget(self.name_label)
        self.layout.addWidget(self.name_input)
        self.layout.addWidget(self.age_label)
        self.layout.addWidget(self.age_input)
        self.layout.addWidget(self.add_button)
        self.layout.addWidget(self.back_button)
        self.setLayout(self.layout)

    def go_back(self):
        self.parent.show()
        self.hide()


    def add_entry(self):
        name = self.name_input.text()
        age = self.age_input.text()

        if name and age:
            try:
                age = int(age)
                conn = sqlite3.connect('example.db')
                cur = conn.cursor()

                cur.execute("INSERT INTO users2 (name, age) VALUES (?, ?)", (name, age))
                conn.commit()

                QMessageBox.information(self, 'Success', 'Entry added successfully!')

                self.name_input.clear()
                self.age_input.clear()
                self.parent.load_data()

                conn.close()
                self.close()

            except ValueError:
                QMessageBox.warning(self, 'Error', 'Age must be an integer')
        else:
            QMessageBox.warning(self, 'Error', 'All fields must be filled')



if __name__ == '__main__':
    app = QApplication(sys.argv)
    Data_enter = DataEntry()
    Data_enter.show()
    sys.exit(app.exec_())
