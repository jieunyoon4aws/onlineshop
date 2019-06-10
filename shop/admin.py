from django.contrib import admin

from .models import *

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name','slug']
    # 이름을 넣었을 때 공백이 있으면 자동으로 _ 넣어줌
    prepopulated_fields = {'slug': ('name',)}

class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'category', 'price','stock', 'available_display',
                    'available_order', 'created', 'updated']
    prepopulated_fields = {'slug': ('name',)}
    # admin에서 바로 검색해볼 수 있게 필터링하는 기능
    list_filter = ['available_display', 'created', 'updated', 'category']
    list_editable = ['price', 'stock', 'available_display', 'available_order']

# CategoryAdmin은 화면을 그 클래스 안의 항목을 갖고 만들겠다는 의미
admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)