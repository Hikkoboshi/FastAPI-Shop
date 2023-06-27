from _decimal import Decimal

BASKET_SESSION_ID = 'basket'


class Basket:
    def __init__(self, request):
        self.session = request.session
        basket = self.session.get(BASKET_SESSION_ID)
        if BASKET_SESSION_ID not in request.session:
            basket = self.session[BASKET_SESSION_ID] = {}
        self.basket = basket

    def add(self, product, quantity=1, update_quantity=False):

        product_id = str(product.id)
        if product_id not in self.basket:
            self.basket[product_id] = {'quantity': 0, 'price': str(product.price)}
        if update_quantity:
            self.basket[product_id]['quantity'] = quantity
        else:
            self.basket[product_id]['quantity'] += quantity

    def __iter__(self):
    #     product_ids = self.basket.keys()
    #     products = Product.objects.filter(id__in=product_ids)
        basket = self.basket.copy()
    #
    #     for product in products:
    #         basket[str(product.id)]["product"] = product
        for item in basket.values():
            item["price"] = Decimal(item["price"])
            item["total_price"] = item["price"] * item["quantity"]
            yield item

    def __len__(self):
        return sum(item["quantity"] for item in self.basket.values())

    def update(self, product, quantity):
        product_id = str(product.id)
        if product_id in self.basket:
            self.basket[product_id]["quantity"] = quantity
        self.save()

    def get_subtotal_price(self):
        return sum(Decimal(item["price"]) * item["quantity"] for item in self.basket.values())

    def get_delivery_price(self):
        delivery = 0.00

        return delivery

    def get_total_price(self):
        subtotal = self.get_subtotal_price()

        total = subtotal
        return total

    def basket_update_delivery(self, delivery_price=0):
        subtotal = self.get_subtotal_price()
        total = subtotal + Decimal(delivery_price)
        return total

    def delete(self, product):
        product_id = str(product)

        if product_id in self.basket:
            del self.basket[product_id]
            self.save()

    def clear(self):
        del self.session[BASKET_SESSION_ID]
        self.save()

    def save(self):
        self.session.modified = True
