from django.shortcuts import render, get_object_or_404

from cart.forms import AddProductForm
from .models import *

# 모든 카테고리 출력
# 해당 카테고리 클릭하면 출력
def product_in_category(request, category_slug=None):
    # default 지정(입력값이 없으면 default 값이 반환됨)
    # 파라미터 변수=default 값 형태로 사용
    # db 검색한 결과를 템플릿에 넘겨줌
    # map 형태로 만들어서 넘겨줌(딕셔너리)
    current_category = None
    # 카테고리 없이 전체 출력
    categories = Category.objects.all()
    products = Product.objects.filter(available_display = True)

    # 카테고리 해당하는 것만 출력
    if category_slug: # 카테고리 값 있을 때 실행
        # 값 없으면 404 처리하라는 의미. objects.filter 같은 역할
        current_category = get_object_or_404(Category, slug = category_slug)
        products = products.filter(category = current_category)

    return render(request, 'shop/list.html', {
        'current_category': current_category,
        'products': products,
        'categories': categories
    })

# 제품 상세페이지에 출력
def product_detail(request, id, product_slug=None):
    product = get_object_or_404(Product, id=id, slug=product_slug)
    add_to_cart = AddProductForm(initial={'quantity':1})
    return render(request, 'shop/detail.html', {'product': product, 'add_to_cart': add_to_cart})