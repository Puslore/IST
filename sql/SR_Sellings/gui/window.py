from PyQt5.QtWidgets import (QDialog, QMainWindow,
                             QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                             QComboBox, QSpinBox, QPushButton, QMessageBox,
                             QDateEdit, QTableWidget, QTableWidgetItem,
                             QHeaderView)
from PyQt5.QtCore import QDate, Qt
from controllers.controller import ShopController

# TODO
# доработать, исправить отображение товаров
# ShopWindow.buy_product, ShopWindow.buy_receipts

class ShopWindow(QMainWindow):
    def __init__(self, controller: ShopController):
        super().__init__()
        self.controller = controller
        self.setWindowTitle('Магазин')
        self.setGeometry(100, 100, 400, 250)

        # Создаем центральный виджет и основной layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        
        # Блок выбора категории
        cat_layout = QHBoxLayout()
        cat_label = QLabel('Категория:')
        self.cat_combo = QComboBox()
        self.load_categories()  # Загружаем категории из БД

        # При выборе категории загружаем соответствующие товары
        self.cat_combo.currentIndexChanged.connect(self.load_products)

        cat_layout.addWidget(cat_label)
        cat_layout.addWidget(self.cat_combo)
        main_layout.addLayout(cat_layout)

        # Блок выбора продукта
        prod_layout = QHBoxLayout()
        prod_label = QLabel('Товар:')
        self.prod_combo = QComboBox()
        self.prod_combo.currentIndexChanged.connect(self.update_available_quantity)
        prod_layout.addWidget(prod_label)
        prod_layout.addWidget(self.prod_combo)
        main_layout.addLayout(prod_layout)
        
        # Блок выбора количества
        qty_layout = QHBoxLayout()
        qty_label = QLabel('Количество:')
        self.qty_spin = QSpinBox()
        self.qty_spin.setRange(1, 10000)  # Будет обновляться в зависимости от наличия товара
        qty_layout.addWidget(qty_label)
        qty_layout.addWidget(self.qty_spin)
        main_layout.addLayout(qty_layout)
        
        # Блок кнопок
        btn_layout = QHBoxLayout()
        self.buy_btn = QPushButton('Купить')
        self.buy_btn.clicked.connect(self.buy_product)
        self.receipts_btn = QPushButton('Просмотр чеков')
        self.receipts_btn.clicked.connect(self.show_receipts)
        btn_layout.addWidget(self.buy_btn)
        btn_layout.addWidget(self.receipts_btn)
        main_layout.addLayout(btn_layout)
        
    def load_categories(self):
        try:
            categories = self.controller.get_all_categories()
            self.cat_combo.clear()
            self.cat_combo.addItems(categories)

        except Exception as err:
            QMessageBox.critical(self, "Ошибка", f"Не удалось загрузить категории: {err}")
    
    def load_products(self):
        try:
            category_name = self.cat_combo.currentText()
            products_list = self.controller.get_goods_by_category(category_name)
            products_data = []
            for product in products_list:
                product_info = self.get_product_info(product)
                products_data.append(f'{product}, цена за шт: {product_info["price"]}, на складе:{product_info["amount"]} шт.')
            print(products_data, 'тут инфа о продуктах')

            self.prod_combo.clear()
            self.prod_combo.addItems(products_data)
            # print(self.prod_combo.currentText(), 'тут текст который в списке')

        except Exception as err:
            QMessageBox.critical(self, "Ошибка", f"Не удалось загрузить товары: {err}")
    
    def get_product_info(self, name: str) -> dict:
        try:
            product_data = self.controller.get_good_info(name)
            return product_data
        
        except Exception as err:
            print(f'ERROR WITH GOOD INFO --- {err}')
            return {}
    
    def extract_product_name(self, full_text):
        return full_text.split(',')[0]

    
    def update_available_quantity(self):
        try:
            product_text = self.prod_combo.currentText()
            product_name = self.extract_product_name(product_text)
                
            product_info = self.controller.get_good_by_name(product_name)
            if product_info:
                available_qty = product_info["amount"]
                self.qty_spin.setRange(1, available_qty)
                self.qty_spin.setValue(1)

        except Exception as err:
            QMessageBox.critical(self, "Ошибка", f"Не удалось получить информацию о товаре: {err}")

    # def update_available_quantity_from_buy_process(self, name:str, quantity: int):
    #     try:
    #         product_info = self.controller.get_good_by_name(name)
    #         available_qty = product_info["amount"]
    #         new_available_quantity = available_qty - quantity
    #         self.qty_spin.setRange(1, new_available_quantity)
    #         self.qty_spin.setValue(1)

    #     except Exception as err:
    #         QMessageBox.critical(self, "Ошибка", f"Не удалось получить информацию о товаре: {err}")
  
    def buy_product(self):
        text = self.prod_combo.currentText()
        product_name = self.extract_product_name(text)
        print(product_name, 'отладка в buy---------')
        quantity = self.qty_spin.value()
        
        if not product_name:
            QMessageBox.warning(self, "Предупреждение", "Выберите товар")
            return
        
        success = self.controller.process_purchase(product_name, quantity)
        if success is not None:
            new_available_quantity = self.get_product_info(product_name)['amount'] - quantity
            self.controller.update_product_quantity(product_name, new_available_quantity)
            # Обновляем информацию о доступном количестве текущего товара
            self.update_available_quantity()
            # Обновляем список товаров, чтобы отобразить измененное количество
            self.load_products()
            QMessageBox.information(self, "Успех", success)

        else:
            QMessageBox.warning(self, "Ошибка", "Не удалось оформить покупку")
    
    def show_receipts(self):
        try:
            # Создаем диалоговое окно
            receipts_dialog = QDialog(self)
            receipts_dialog.setWindowTitle('Просмотр чеков')
            receipts_dialog.setMinimumWidth(600)
            receipts_dialog.setMinimumHeight(400)
            
            # Основной layout для диалога
            main_layout = QVBoxLayout(receipts_dialog)
            
            # Блок выбора даты и отображения выручки
            date_layout = QHBoxLayout()
            date_label = QLabel('Дата:')
            date_picker = QDateEdit()
            date_picker.setCalendarPopup(True)  # Включаем выпадающий календарь
            date_picker.setDate(QDate.currentDate())  # Устанавливаем текущую дату
            
            # Добавляем метку для отображения выручки
            revenue_label = QLabel('Выручка за день: 0 руб.')
            revenue_label.setStyleSheet("font-weight: bold; color: green;")
            
            date_layout.addWidget(date_label)
            date_layout.addWidget(date_picker)
            date_layout.addWidget(revenue_label)
            date_layout.addStretch()
            
            # Таблица чеков
            receipts_table = QTableWidget()
            receipts_table.setColumnCount(5)  # ID, Товар, Количество, Общая цена, Время
            receipts_table.setHorizontalHeaderLabels(['ID', 'Товар', 'Количество', 'Общая цена', 'Время'])
            receipts_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
            
            # Соединяем изменение даты с обновлением таблицы и метки выручки
            date_picker.dateChanged.connect(
                lambda: self.load_receipts_for_date(date_picker, receipts_table, revenue_label)
            )
            
            # Кнопка закрытия
            button_layout = QHBoxLayout()
            close_btn = QPushButton('Закрыть')
            close_btn.clicked.connect(receipts_dialog.accept)
            button_layout.addStretch()
            button_layout.addWidget(close_btn)
            
            # Добавление всех компонентов в основной layout
            main_layout.addLayout(date_layout)
            main_layout.addWidget(receipts_table)
            main_layout.addLayout(button_layout)
            
            # Загрузка чеков за текущую дату
            self.load_receipts_for_date(date_picker, receipts_table, revenue_label)
            
            # Отображаем диалоговое окно
            receipts_dialog.exec_()
            
        except Exception as err:
            QMessageBox.critical(self, "Ошибка", f"Не удалось открыть просмотр чеков: {err}")

    def load_receipts_for_date(self, date_picker, receipts_table, revenue_label):
        try:
            # Очистка таблицы
            receipts_table.setRowCount(0)
            
            # Получение выбранной даты
            selected_date = date_picker.date().toString("yyyy-MM-dd")
            
            # Получение чеков из контроллера
            receipts = self.controller.get_receipts_by_date(selected_date)
            
            # Рассчитываем суммарную выручку за день
            total_revenue = 0.0
            
            # Заполнение таблицы
            for row_idx, receipt in enumerate(receipts):
                receipts_table.insertRow(row_idx)
                
                # ID чека
                receipts_table.setItem(row_idx, 0, QTableWidgetItem(str(receipt['id'])))
                
                # Товар
                receipts_table.setItem(row_idx, 1, QTableWidgetItem(receipt['product_name'][0]))
                
                # Количество
                receipts_table.setItem(row_idx, 2, QTableWidgetItem(str(receipt['quantity'])))
                
                # Общая цена
                receipts_table.setItem(row_idx, 3, QTableWidgetItem(f"{receipt['total_price']} руб."))
                
                # Время
                time_part = receipt['date'].split(' ')[1] if ' ' in receipt['date'] else receipt['date']
                receipts_table.setItem(row_idx, 4, QTableWidgetItem(time_part))
                
                # Суммируем выручку
                total_revenue += float(receipt['total_price'])
            
            # Настройка ячеек таблицы (только для чтения)
            for row in range(receipts_table.rowCount()):
                for col in range(receipts_table.columnCount()):
                    item = receipts_table.item(row, col)
                    if item:
                        item.setFlags(item.flags() & ~Qt.ItemIsEditable)
            
            # Обновляем метку с выручкой
            # Ограничиваем до 2 знаков после запятой
            formatted_revenue = "{:.2f}".format(total_revenue)
            revenue_label.setText(f'Выручка за день: {formatted_revenue} руб.')
                
            # Если нет чеков за эту дату
            if len(receipts) == 0:
                receipts_table.setRowCount(1)
                receipts_table.setSpan(0, 0, 1, 5)
                no_data_item = QTableWidgetItem("Нет чеков за выбранную дату")
                no_data_item.setTextAlignment(Qt.AlignCenter)
                receipts_table.setItem(0, 0, no_data_item)
                
                # Обнуляем метку выручки
                revenue_label.setText('Выручка за день: 0.00 руб.')
        
        except Exception as err:
            QMessageBox.critical(self, "Ошибка", f"Не удалось загрузить чеки: {err}")
