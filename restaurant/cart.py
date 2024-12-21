from decimal import Decimal
from django.conf import settings
from restaurant.models import Dish


class Cart(object):
    def __init__(self, request):
        # Инициализация корзины пользователя
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            # Сохраняем корзину пользователя в сессию
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    # Добавление товар в корзину пользователя
    # или обновление количества товаров
    def add(self, Dish, quantity=1, update_quantity=False):
        Dish_id = str(Dish.id)
        if Dish_id not in self.cart:
            self.cart[Dish_id] = {'quantity': 0,
                                     'price': str(Dish.price)}
        if update_quantity:
            self.cart[Dish_id]['quantity'] = quantity
        else:
            self.cart[Dish_id]['quantity'] += quantity
        self.save()

        # Сохранение данных в сессию
    def save(self):
        self.session[settings.CART_SESSION_ID] = self.cart
        # Указываем, что сессия изменена
        self.session.modified = True

        # Удаление товара из корзины
    def remove(self, Dish):
        Dish_id = str(Dish.id)
        if Dish_id in self.cart:
            del self.cart[Dish_id]
            self.save()


    # Итерация по товарам
    def __iter__(self):
        Dish_ids = self.cart.keys()
        Dish = Dish.objects.filter(id__in=Dish_ids)
        for Dish in Dish:
            self.cart[str(Dish.id)]['Dish'] = Dish

        for item in self.cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    # Количество товаро
    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())

    def get_total_price(self):
        return sum(Decimal(item['price'])*item['quantity'] for item in self.cart.values())

    def clear(self):
        del self.session[settings.CART_SESSION_ID]
        self.session.modified = True