# 카트 기능 한꺼번에 클래스로 묶어버리기 위한 모듈
from decimal import Decimal
from django.conf import settings
from shop.models import Product


class Cart(object):

    def __init__(self, request):
        self.session = request.session
        # 브라우저가 연결될 때 세션이 자동 생성되므로, 이를 가져오면 됨
        # 하지만 쿠키는 내장된 게 아니기 때문에 따로 코딩을 해야 함

        # CART_ID key를 가진 세션이 있는지 체크
        cart = self.session.get(settings.CART_ID)
        # loginid = self.session.get(settings.LOGIN_SESSION_ID)

        # 세션이 없으면, 딕셔너리를 만들어야 함
        if not cart:
            # 세션은 {키: value}로 값을 갖고 있음(제품: 개수)
            # 이를 이용해 삭제하거나 카트를 변경함
            cart = self.session[settings.CART_ID] = {}

        # 세션이 있으면, 딕셔너리를 가져옴
        self.cart = cart

    def add(self, product, quantity=1, is_update = False):
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': 0, 'price':str(product.price)}
        if is_update:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity

        self.save()

    def save(self):
        self.session[settings.CART_ID] = self.cart
        self.session.modified = True # 세션 저장


    def remove(self, product):
        product_id = str(product.id) # dictionary에 string으로 들어가야 돼서
        if product_id in self.cart:
            del(self.cart[product_id])
            self.save()


    def clear(self):
        self.session[settings.CART_ID] = {} # 초기화
        self.session.modified = True

    def __len__(self): # 카트에 몇 개의 값이 들어가 있는지 자동으로 세어 줌
        return sum(item['quantity'] for item in self.cart.values())

    def __iter__(self): # 반복자 (iterater)
        product_ids = self.cart.keys() # 키 한번에 다 가져옴
        products = Product.objects.filter(id__in = product_ids)
        # 장바구니 정보 한번에 다 가져옴
        # id__in: id 중 product_ids에 있으면 모두 필터링해서 가져온다는 의미.
        # 즉, 장바구니 목록 다 가져오는 것

        for product in products:
            self.cart[str(product.id)]['product'] = product

        for item in self.cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']

            yield item # return과 같음.
            # 이때, 위의 item 값들 가지고 있게끔 return 대신 yield 사용

    def get_product_total(self):
        return sum(Decimal(item['price'])*item['quantity'] for item in self.cart.values())