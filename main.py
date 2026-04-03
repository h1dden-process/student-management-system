from PyQt6.QtWidgets import QApplication, QBoxLayout, QLabel, QWidget, QGridLayout, QLineEdit, QPushButton, QMainWindow, QTableWidget, QTableWidgetItem, QDialog, QVBoxLayout, QComboBox, QToolBar
from PyQt6.QtGui import QAction, QIcon
from PyQt6.QtCore import Qt

import sys
import sqlite3


class MainWindow(QMainWindow): 

    def __init__(self):

        super().__init__()

        self.setWindowTitle("Student Management System")
        self.setMinimumSize(800, 600)

        file_menu_item = self.menuBar().addMenu("&File")
        help_menu_item = self.menuBar().addMenu("&Help")
        edit_menu_item = self.menuBar().addMenu("&Edit")

        add_student_action = QAction(QIcon("./add.png"),"Add student", self)

        add_student_action.triggered.connect(self.insert)
        file_menu_item.addAction(add_student_action)


        about_action = QAction("About", self)
        help_menu_item.addAction(about_action)

        search_action = QAction(QIcon("./search.png"), "Search", self)

        search_action.triggered.connect(self.search)
        edit_menu_item.addAction(search_action)

        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(("id", "Name", "Course", "Mobile"))
        self.table.verticalHeader().setVisible(False)
        self.setCentralWidget(self.table)

        toolbar = QToolBar()

        toolbar.setMovable(True)

        self.addToolBar(toolbar)
        toolbar.addAction(add_student_action)
        toolbar.addAction(search_action)



    def load_data(self):
        conn = sqlite3.connect("./database.db", check_same_thread=False)

        results = conn.execute("SELECT * FROM students").fetchall()

        self.table.setRowCount(0)

        for row_number, row_data in enumerate(results):
           self.table.insertRow(row_number)
           for column_number, data in enumerate(row_data):
               self.table.setItem(row_number, column_number, QTableWidgetItem(str(data)))
        
        conn.close()

    def insert(self):
        dialog = InsertDialog()
        dialog.exec()

    def search(self):
        dialog = SearchDialog()
        dialog.exec()


class InsertDialog(QDialog):
    def __init__(self):

        super().__init__()

        self.setWindowTitle("Insert Student Data")
        self.setFixedWidth(300)
        self.setFixedHeight(300)

        layout = QVBoxLayout()

        self.student_name = QLineEdit()
        self.student_name.setPlaceholderText("Name")
        layout.addWidget(self.student_name)

        self.course_name = QComboBox()
        courses = ["Biology", "Math", "Astronomy", "Physics"]
        self.course_name.addItems(courses)
        layout.addWidget(self.course_name)

        self.mobile = QLineEdit()
        self.mobile.setPlaceholderText("Mobile")
        layout.addWidget(self.mobile)

        button = QPushButton("Submit")
        button.clicked.connect(self.add_student)
        layout.addWidget(button)


        self.setLayout(layout)
    
    def add_student(self): 
        name = self.student_name.text()
        course = self.course_name.itemText(self.course_name.currentIndex())
        mobile = self.mobile.text()
        conn = sqlite3.connect("./database.db", check_same_thread=False)

        cursor = conn.cursor()
        cursor.execute("INSERT INTO students (name, course, mobile) VALUES (?, ?, ?)", (name, course, mobile))

        conn.commit()
        cursor.close()
        conn.close()
        mainWindow.load_data()

class SearchDialog(QDialog):

    def __init__(self):
        super().__init__()
        
        self.setFixedWidth(300)
        self.setFixedHeight(300)

        grid = QVBoxLayout()


        self.setWindowTitle("Search Student")

        self.student_search = QLineEdit()

        self.student_search.setPlaceholderText("Name")

        grid.addWidget(self.student_search)

        button = QPushButton("Search")

        button.clicked.connect(self.search)

        grid.addWidget(button)

        self.setLayout(grid)

    def search(self):

        name = self.student_search.text()

        conn = sqlite3.connect("./database.db", check_same_thread = False)

        cursor = conn.cursor()

        result = cursor.execute("SELECT * FROM students WHERE name = ?", (name, )).fetchall()


        items = mainWindow.table.findItems(name, Qt.MatchFlag.MatchFixedString)

        for item in items: 
            
            mainWindow.table.item(item.row(), 1).setSelected(True)
        
        
        cursor.close()
        conn.close()


app = QApplication(sys.argv)

mainWindow = MainWindow()
mainWindow.load_data()

mainWindow.show()

sys.exit(app.exec())

