from PyQt5.QtWidgets import (QApplication, QMainWindow,
                             QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                             QComboBox, QSpinBox, QPushButton, QMessageBox)
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

            self.prod_combo.clear()
            self.prod_combo.addItems(products_data)

        except Exception as err:
            QMessageBox.critical(self, "Ошибка", f"Не удалось загрузить товары: {err}")
    
    def get_product_info(self, name: str) -> dict:
        try:
            product_data = self.controller.get_good_info(name)
            return product_data
        
        except Exception as err:
            print(f'ERROR WITH GOOD INFO --- {err}')
            return {}
    
    def update_available_quantity(self):
        try:
            product_name = self.prod_combo.currentText()
            if not product_name:
                return
                
            product_info = self.controller.get_good_by_name(product_name)
            if product_info:
                available_qty = product_info["amount"]
                self.qty_spin.setRange(1, available_qty)
                self.qty_spin.setValue(1)

        except Exception as err:
            QMessageBox.critical(self, "Ошибка", f"Не удалось получить информацию о товаре: {err}")
    
    def buy_product(self):
        product_name = self.prod_combo.currentText()
        quantity = self.qty_spin.value()
        
        if not product_name:
            QMessageBox.warning(self, "Предупреждение", "Выберите товар")
            return
        
        # TODO
        # Здесь должен быть вызов метода контроллера для оформления покупки
        success = self.controller.process_purchase(product_name, quantity)
        if success:
            # Обновляем список товаров, чтобы отобразить измененное количество
            self.load_products()
            # Обновляем информацию о доступном количестве текущего товара
            self.update_available_quantity()
            QMessageBox.information(self, "Успех", success)

        else:
            QMessageBox.warning(self, "Ошибка", "Не удалось оформить покупку")
    
    def show_receipts(self):
        # TODO
        # Здесь должен быть код для открытия окна с чеками
        QMessageBox.information(self, "Информация", "Функция в разработке")
