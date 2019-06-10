from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST

from cart.forms import AddProductForm
from .cart import *


@require_POST # 포스트 방식인지를 체크해주는 문법.
# annotation(in JAVA): if문 역할을 대신함. 파이썬에서는 decorator라 함
def add(request, product_id):
    # print('장바구니에 넣는 제품 id: ', product_id)
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    # 유효한 값이 들어있는지 체크
    # input에 들어간 values를 가지고 옴
    form = AddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data # 입력값 딕셔너리 형태로 가져 옴
        cart.add(product=product, quantity=cd['quantity'], is_update=cd['is_update'])
    return redirect('cart:detail')
    # 다른페이지인 detail 쪽으로 요청하라는 의미(서버가 클라이언트에게 이렇게 하라고 요청)
    # 다른 함수 호출하는 것

def detail(request):
    cart = Cart(request)
    for product in cart:
        product['quantity_form'] = AddProductForm(initial={'quantity': product['quantity'], 'is_update':True})

    return render(request, 'cart/detail.html', {'cart': cart})

def remove(request):
    pass



