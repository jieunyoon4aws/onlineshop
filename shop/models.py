from django.db import models
from django.urls import reverse

class Category(models.Model):
    # name을 db 인덱스로 사용하겠다는 의미. 액세스 속도를 더 빠르게 해주는 역힐
    name = models.CharField(max_length=200, db_index=True)
    meta_description = models.TextField(blank=True) # 제품에 대한 설명
    slug = models.SlugField(max_length=200, db_index=True, unique=True, allow_unicode=True)

    class Meta: # inner class. 바깥의 클래스 밖에서는 못씀. 정렬할 때 등에 사용
        ordering = ['name'] # 이름으로 정렬
        verbose_name = 'category'
        verbose_name_plural = 'categories'
        # 관리자 모드에서 복수 처리할 때 이 이름 지정한 것

    def get_absolute_url(self):
        return reverse('shop:product_in_category', args=[self.slug])
        # args: 입력 값, shop: 뒷 부분은 urls.py의 name 부분임

    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='products')
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, db_index=True, unique=True, allow_unicode=True)

    image = models.ImageField(upload_to='products/%Y/%m/%d', blank=True)
    description = models.TextField(blank=True)
    meta_description = models.TextField(blank=True)

    price = models.DecimalField(max_digits=10, decimal_places=2) # 억 단위까지 숫자 넣을 수 있음
    stock = models.PositiveIntegerField()

    # 관리자 페이지에서 모두 보여지도록 함. 미끼 상품용 필드 ex.품절이지만 검색하면 제품
    available_display = models.BooleanField('Display', default=True)
    available_order = models.BooleanField('Order', default=True)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created'] # 최근 꺼가 젤 위로 올라옴
        # 두 개의 기본키를 사용하겠다는 의미. 문법 안에 두 개를 사용하겠다고 리스트를 넣은 것
        index_together = [['id', 'slug']]

    def get_absolute_url(self):
        return reverse('shop:product_detail', args=[self.id, self.slug])

#. 문법임
    def __str__(self):
        return self.name


