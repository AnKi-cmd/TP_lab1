import PySimpleGUI as sg
from abc import ABCMeta, abstractmethod
import sys
import re

sg.theme('black')

input_info = [
    [sg.Text("Введите входные данные. В противном случае будут установлены значения по умолчанию", font="35",
             text_color="green")],
    [sg.Text("ФИО", font="20"), sg.InputText(size=(30, 3), key="FIO", font="35"),
     sg.Text("П/У: Кислицын Андрей Дмитриевич", font="20", text_color="grey")],
    [sg.Text("Кол-во бонусных баллов", font="20"), sg.InputText(size=(30, 3), key="bonus_coins", font="35"),
     sg.Text("П/У: 100 бонусов", font="20", text_color="grey")],
    [sg.Text("Кол-во наличных", font="20"), sg.InputText(size=(30, 3), key="balance", font="35"),
     sg.Text("П/У: 1000 рублей", font="20", text_color="grey")],
    [sg.Button("Подтвердить", font="30", key="Confirm")]
]

input_weight_products = [
    [sg.Text(
        "Введите данные по ВЕСОВЫМ продуктам.",
        font="35", text_color="green")],
    [sg.Text("Наименование", font="20"), sg.InputText(size=(30, 3), key="product_name", font="35")],
    [sg.Text("Количество продукта (кг)", font="20"), sg.InputText(size=(30, 3), key="amount", font="35")],
    [sg.Text("Цена (за кг)", font="20"), sg.InputText(size=(30, 3), key="cost", font="35")],
    [sg.Button("Добавить продукт", font="30", key="Add_Product"),
     sg.Button("Завершить ввод", font="30", key="End_Adding")]
]

input_perpiece_products = [
    [sg.Text(
        "Введите данные по ПОШТУЧНЫМ продуктам.",
        font="35", text_color="green")],
    [sg.Text("Наименование", font="20"), sg.InputText(size=(30, 3), key="product_name", font="35")],
    [sg.Text("Количество продукта (упаковок)", font="20"), sg.InputText(size=(30, 3), key="amount", font="35")],
    [sg.Text("Цена (за упаковку)", font="20"), sg.InputText(size=(30, 3), key="cost", font="35")],
    [sg.Button("Добавить продукт", font="30", key="Add_Product"),
     sg.Button("Завершить ввод", font="30", key="End_Adding")]
]

pay_menu = [
    [sg.Output(size=(30, 10))],
    [sg.Button("Выход", key="END")]
]

select_payment = [
    [sg.Button("Оплатить наличкой", key="Наличка")],
    [sg.Button("Оплатить бонусами", key="Бонусы")],
    [sg.Button("Оплатить наличкой и бонусами", key="Наличка_бонусы")]
]


def create_main_menu():
    main_menu = [
        [sg.Text("Доступные опции:")],
        [sg.Button("Выбрать товар", key="Select_product"), sg.Button("Оплатить товары", key="Pay")],
        [sg.Text("Список выбранных товаров и расценки")],
        [sg.Listbox(size=(30, 5), values=[], key="main_menu_box")],
        [sg.Button("Выложить выбранный продукт", key="Delete")],
        [sg.Text("В корзине товаров на 0 рублей", font="25", text_color="pink", key="Summ_Text")]
    ]
    return main_menu


def create_product_list():
    product_list = [
        [sg.Text("Товары:")],
        [sg.Listbox(values=[], size=(20, 5), key="Spisok")],
        [sg.Button("Добавить в корзину", key="Add_product")]
    ]
    return product_list


def create_choose_value():
    choose_value = [
        [sg.Text("Выберите количество товара (кол-во упаковок)", font="35", text_color="green", key="Edit_text")],
        [sg.Slider(range=(0, 500), default_value=0, size=(20, 15), orientation='horizontal', key="Slid")],
        [sg.Button("Подтвердить", key="Confirm")]
    ]
    return choose_value


class Product():
    __metaclass__ = ABCMeta
    name = ""
    cost = 0
    amount = 0
    list_of_products = {}

    def add_products_info(self, name, cost, amount):
        try:
            if name != "":
                example = self.list_of_products[name]
                sg.popup_error("Такой продукт уже есть в списке")
            else:
                sg.popup_error("Не введено наименование товара")
        except:
            self.set_name(name)
            self.set_cost(cost)
            self.set_amount(amount)
            self.list_of_products[self.name] = {}
            self.list_of_products[self.name]["Цена"] = self.cost
            self.list_of_products[self.name]["Количество"] = self.amount
            # print(self.list_of_products)
        """Добавление данных о продукте"""

    @abstractmethod
    def set_amount(self, amount):
        """Добавить количество товара"""

    def set_cost(self, cost):
        if (cost.isdigit()) and (float(cost) > 0):
            self.cost = float(cost)
        else:
            self.cost = 50
        """Добавить цену товара"""

    @abstractmethod
    def set_name(self, name):
        if name != "":
            self.name = name
        """Добавить наименование товара"""


class Per_Peace_Products(Product):
    def set_amount(self, amount):
        if (amount.isdigit()) and (int(amount)):
            self.amount = int(amount)
        else:
            self.amount = 5

    def set_name(self, name):
        if name != "":
            self.name = name + "_Уп"


class Weignt_Products(Product):
    def set_amount(self, amount):
        if ((amount.replace('.', '', 1).isdigit()) and (float(amount) > 0)):
            self.amount = float(amount)
            self.amount = round(self.amount, 3)
        else:
            self.amount = 5.0

    def set_name(self, name):
        if name != "":
            self.name = name + "_Вес"


class Shop():
    weight_prod = Weignt_Products()
    perpiece_prod = Per_Peace_Products()

    def add_weight_products(self, name, cost, amount):
        self.weight_prod.add_products_info(name, cost, amount)

    def add_perpiece_products(self, name, cost, amount):
        self.perpiece_prod.add_products_info(name, cost, amount)

    def get_amount_of_product(self, name):
        value = self.get_from_list(name)
        return self.weight_prod.list_of_products[value]["Количество"]

    def get_shop_product_list(self):
        shop_product_list = list()
        for mes in self.weight_prod.list_of_products.keys():
            shop_product_list.append(mes)
        return shop_product_list

    def get_from_list(self, name):
        value = str(name)
        value = value[2:-2]
        return value

    def check_exist_weight_product(self, name):
        example = self.weight_prod.list_of_products.get(name + "_Вес")
        if example == None:
            return False
        else:
            return True

    def check_exist_perpiece_product(self, name):
        example = self.weight_prod.list_of_products.get(name + "_Уп")
        if example == None:
            return False
        else:
            return True

    def check_exist_list(self):
        if self.weight_prod.list_of_products == {}:
            return False
        return True


class Customer():
    fio = "Кислицын Андрей Дмитриевич"
    bonus_coins = 100
    balance = 1000
    list_to_buy = {}

    def set_fio(self, FIO):
        if FIO != "":
            self.fio = FIO

    def set_bonus_coins(self, bon_coins):
        if bon_coins.isdigit():
            if int(bon_coins) >= 0:
                self.bonus_coins = int(bon_coins)

    def set_balance(self, cash):
        if cash.isdigit():
            if (int(cash) >= 0):
                self.balance = int(cash)

    def get_buy_list(self):
        products_to_buy = list()
        for mes in self.list_to_buy.keys():
            products_to_buy.append(mes)
        return products_to_buy

    def add_to_buylist(self, name, amount):
        try:
            if name != "":
                example = self.list_to_buy[name]
                sg.popup_error("Такой продукт уже есть в списке")
            else:
                sg.popup_error("Не введено наименование товара")
        except:
            self.list_to_buy[str(name)] = amount
            print(self.list_to_buy)

    def delete_from_list(self, name):
        del self.list_to_buy[str(name)]

    def __init__(self, FIO, bon_coins, cash):
        self.set_fio(FIO)
        self.set_bonus_coins(bon_coins)
        self.set_balance(cash)
        if (self.balance == 0) and (self.bonus_coins == 0):
            sg.popup_error("Нет бонусных баллов и наличных. Продолжение работы программы не имеет смысла.")
            sys.exit()

    def __str__(self):
        info = "ФИО: " + self.fio + "\nКол-во бонусов = " + str(self.bonus_coins) + "\nБаланс: " + str(
            self.balance)
        return info

class Shop_and_customer_interaction():
    def __init__(self, customer, shop):
        self.customer = customer
        self.shop = shop

    def get_buy_summ(self):
        summ = 0
        key = self.customer.list_to_buy.keys()
        for mes in self.customer.list_to_buy.keys():
            summ += self.shop.weight_prod.list_of_products[mes]['Цена'] * self.customer.list_to_buy[mes]
        return round(summ, 2)

    def pay_for_products(self, payment_way):
        printed = False
        if payment_way == "Наличка":
            all_cash = self.customer.balance
        elif payment_way == "Бонусы":
            all_cash = self.customer.bonus_coins
        else:
            all_cash = self.customer.balance + self.customer.bonus_coins
        print("У вас с собой " + str(all_cash))
        while (self.get_buy_summ() > all_cash):
            if printed == False:
                print("Недостаточно денег. Убираем товары из корзины")
                printed = True
            for mes in self.customer.list_to_buy.keys():
                print("Удален продукт " + str(mes))
                if (re.search("_Уп", mes)) and (self.customer.list_to_buy[mes] > 1):
                    self.customer.list_to_buy[mes] -= 1
                else:
                    self.customer.delete_from_list(mes)
                break
        print("\nЧЕК:")
        for mes in self.customer.list_to_buy.keys():
            amount = self.customer.list_to_buy[mes]
            cost = self.shop.weight_prod.list_of_products[mes]['Цена']
            print(str(mes) + "  " + str(amount) + " * " + str(cost) + " = " + str(round(amount * cost, 2)))
        print("\nИТОГО: " + str(round(self.get_buy_summ(), 2)) + " рублей")


def set_window(title_text, menu_name):
    window = sg.Window(title_text, menu_name)
    window.Finalize()
    return window


def main():
    global iterator
    window = set_window('Ввод данных', input_info)
    event, values = window.read()
    if event in (None, 'Exit', 'Cancel'):
        sys.exit()
    if event == "Confirm":
        window.close()
        person = Customer(values['FIO'], values['bonus_coins'], values['balance'])
        shop = Shop()
        interaction = Shop_and_customer_interaction(person, shop)
        window = set_window('Ввод данных по весовым продуктам', input_weight_products)
        while (True):
            event, values = window.read()
            if event == "Add_Product":
                if shop.check_exist_weight_product(values['product_name']) == False:
                    shop.add_weight_products(values['product_name'], values['cost'], values['amount'])
                else:
                    sg.popup_error("Такой продукт уже есть в списке")
                window['product_name'].Update("")
                window['cost'].Update("")
                window['amount'].Update("")
            if event == "End_Adding":
                window.close()
                break
        window = set_window('Ввод данных по поштучным продуктам', input_perpiece_products)
        while (True):
            event, values = window.read()
            if event == "Add_Product":
                if shop.check_exist_perpiece_product(values['product_name']) == False:
                    shop.add_perpiece_products(values['product_name'], values['cost'], values['amount'])
                else:
                    sg.popup_error("Такой продукт уже есть в списке")
                window['product_name'].Update("")
                window['cost'].Update("")
                window['amount'].Update("")
            if event == "End_Adding":
                window.close()
                list_exist = shop.check_exist_list()
                if list_exist == False:
                    shop.add_perpiece_products("Молоко", "65", "20")
                    shop.add_weight_products("Творог", "300", "10")
                    shop.add_weight_products("Мясо", "400", "10")
                    shop.add_perpiece_products("Пельмени", "200", "20")
                break
        while (True):
            window = set_window("Основное меню", create_main_menu())
            spisok = person.get_buy_list()
            buys_now = interaction.get_buy_summ()
            window['main_menu_box'].Update(values=spisok)
            window['Summ_Text'].Update("В корзине товаров на " + str(buys_now) + " рублей")
            event, values = window.read()
            if event in (None, 'Exit', 'Cancel'):
                sys.exit()
            if event == "Select_product":
                window.close()
                window = set_window("Выбор товаров", create_product_list())
                spisok = shop.get_shop_product_list()
                window['Spisok'].Update(values=spisok)
                while (True):
                    event, values = window.read()
                    if event in (None, 'Exit', 'Cancel'):
                        sys.exit()
                    if (event == "Add_product") and (values['Spisok'] != []):
                        window.close()
                        window = set_window("Выбор количества", create_choose_value())
                        num = shop.get_amount_of_product(values['Spisok'])
                        now_name = shop.get_from_list(values['Spisok'])
                        if re.search("_Вес", str(values['Spisok'])):
                            num = num * 1000
                            window['Edit_text'].Update("Выберите количество товара (граммы)")
                        window['Slid'].Update(range=(1, num))
                        event, values = window.read()
                        if event in (None, 'Exit', 'Cancel'):
                            sys.exit()
                        if event == "Confirm":
                            amount = values['Slid']
                            amount = float(amount)
                            if num > 1000:
                                amount /= 1000
                            person.add_to_buylist(now_name, amount)
                            window.close()
                            break

            elif event == "Pay":
                window.close()
                window = set_window("Выбор оплаты", select_payment)
                event, values = window.read()
                if event in (None, 'Exit', 'Cancel'):
                    return 0
                window.close()
                window = set_window("Итог", pay_menu)
                interaction.pay_for_products(event)
                event, values = window.read()
                return 0
            elif event == "Delete":
                now_name = shop.get_from_list(values['main_menu_box'])
                if now_name != "":
                    person.delete_from_list(now_name)
                window.close()

main()