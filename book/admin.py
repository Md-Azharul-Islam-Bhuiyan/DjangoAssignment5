from django.contrib import admin
from .models import BookModel, BorrowHistory, Review

admin.site.register(BookModel)
admin.site.register(Review)
admin.site.register(BorrowHistory)
