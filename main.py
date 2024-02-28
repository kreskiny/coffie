import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QDialog
from PyQt5.uic import loadUi
import sqlite3

class CoffeeApp(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi("main.ui", self)
        self.setWindowTitle("Информация о кофе")
        self.load_data()
        self.addButton.clicked.connect(self.open_add_edit_form)

    def load_data(self):
        connection = sqlite3.connect("coffee.sqlite")
        cursor = connection.cursor()

        cursor.execute("SELECT * FROM Coffee")

        coffee_data = cursor.fetchall()

        connection.close()

        self.tableWidget.setRowCount(len(coffee_data))
        self.tableWidget.setColumnCount(len(coffee_data[0]))
        self.tableWidget.setHorizontalHeaderLabels(["ID", "Название сорта", "Степень обжарки", "Молотый/в зернах", "Описание вкуса", "Цена", "Объем упаковки"])

        for row_number, row_data in enumerate(coffee_data):
            for column_number, data in enumerate(row_data):
                self.tableWidget.setItem(row_number, column_number, QTableWidgetItem(str(data)))

    def open_add_edit_form(self):
        add_edit_form = AddEditCoffeeForm(edit_mode=True)
        if add_edit_form.exec_() == QDialog.Accepted:
            self.load_data()




class AddEditCoffeeForm(QDialog):
    def __init__(self, edit_mode=False):
        super().__init__()
        self.edit_mode = edit_mode
        loadUi("addEditCoffeeForm.ui", self)
        self.setWindowTitle("Add/Edit Coffee")

        self.saveButton.clicked.connect(self.save_data)

    def save_data(self):

        # Получение значений из всех полей формы
        fields = {
            "sort_name": self.sortNameLineEdit.text(),
            "roast_degree": self.roastDegreeLineEdit.text(),
            "ground_or_whole": self.groundOrWholeLineEdit.text(),
            "taste_description": self.tasteDescriptionLineEdit.text(),
            "price": self.priceLineEdit.text(),
            "package_volume": self.packageVolumeLineEdit.text()
        }
        print(fields)
        connection = sqlite3.connect("coffee.sqlite")
        cursor = connection.cursor()

        try:
            query_type = "UPDATE" if self.edit_mode else "INSERT INTO Coffee"
        except Exception as e:
            print(f"An error occurred while determining the query type: {e}")

        print('type')

        connection = sqlite3.connect("coffee.sqlite")
        cursor = connection.cursor()

        # Формирование SQL-запроса для вставки новой записи
        query = '''INSERT INTO Coffee (sort_name, roast_degree, ground_or_whole, taste_description, price, package_volume)
                       VALUES (?, ?, ?, ?, ?, ?)'''

        # Выполнение запроса на вставку новой записи
        cursor.execute(query, tuple(fields.values()))

        # Сохранение изменений в базе данных и закрытие соединения
        connection.commit()
        connection.close()

        # Закрытие формы
        self.accept()


def main():
    try:
        app = QApplication(sys.argv)
        window = CoffeeApp()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        print("An error occurred:", e)

if __name__ == "__main__":
    main()
