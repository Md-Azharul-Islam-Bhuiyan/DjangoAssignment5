from django.shortcuts import render
from django.urls import reverse_lazy
from .models import CategoryModel
from  category.forms import CategoryForm
from django.views.generic import CreateView
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required


@method_decorator(login_required, name='dispatch')
class AddCategoryView(CreateView):
    model = CategoryModel
    form_class = CategoryForm
    template_name = 'add_category.html' 
    success_url = reverse_lazy('home')
    def form_valid(self, form):
        messages.success(self.request, 'Category successfully added')
        return super().form_valid(form)

