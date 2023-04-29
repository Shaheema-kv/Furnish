from .models import Categorie
from store.models import Product
from django.shortcuts import render

# ctgry  = Categorie.objects.all()
# Create your views here.

def category(request):
    # ctgry               = Categorie.objects.all()
    all_product_stock   = Product.objects.all().count()
    cat_product_stock   = Product.objects.select_related('cat_id').count()
    context={
        # 'ctgry': ctgry,
        'all_product_stock': all_product_stock,
        'cat_product_stock': cat_product_stock  
    }
    return render(request, 'category/shop-category.html',context)

