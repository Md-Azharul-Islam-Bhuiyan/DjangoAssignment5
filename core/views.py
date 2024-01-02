from django.shortcuts import render
from book.models import BookModel
from category.models import CategoryModel

def homepage(request, category_slug=None):
    data  = BookModel.objects.all()
    categories = CategoryModel.objects.all()
    if category_slug is not None:
        category = CategoryModel.objects.get(slug = category_slug)
        data = BookModel.objects.filter(category = category)
    

    return render(request, 'home.html', {'data': data, 'categories': categories})
