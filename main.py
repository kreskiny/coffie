import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem
from PyQt5.uic import loadUi
import sqlite3

class CoffeeApp(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi("main.ui", self)
        self.setWindowTitle("Информация о кофе")
        self.load_data()

    def load_data(self):
        connection = sqlite3.connect("../coffee.sqlite")
        cursor = connection.cursor()

        cursor.execute("SELECT * FROM Coffee")

        coffee_data = cursor.fetchall()

        connection.close()
        if coffee_data:
            self.tableWidget.setRowCount(len(coffee_data))
            self.tableWidget.setColumnCount(len(coffee_data[0]))
            self.tableWidget.setHorizontalHeaderLabels(
                ["ID", "Название сорта", "Степень обжарки", "Молотый/в зернах", "Описание вкуса", "Цена",
                 "Объем упаковки"])
        else:
            print("Нет данных о кофе")


        for row_number, row_data in enumerate(coffee_data):
            for column_number, data in enumerate(row_data):
                self.tableWidget.setItem(row_number, column_number, QTableWidgetItem(str(data)))

def main():
    app = QApplication(sys.argv)
    window = CoffeeApp()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
