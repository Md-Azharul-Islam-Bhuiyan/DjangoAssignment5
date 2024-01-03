from django.db import models
from category.models import CategoryModel
from auth_user.models import UserLibraryAccount

class BookModel(models.Model):
    book_id = models.CharField(max_length=30)
    book_name = models.CharField(max_length=100)
    quantity = models.IntegerField()
    image = models.ImageField(upload_to='book/media/uploads/',blank=True, null=True)
    price = models.IntegerField()
    category = models.ManyToManyField(CategoryModel, null=True, blank=True)
    description = models.TextField()

    def __str__(self):
        return self.book_name

class Review(models.Model):
    book = models.ForeignKey(BookModel, on_delete=models.CASCADE, related_name='reviews')
    name = models.CharField(max_length=30)
    email = models.EmailField(null=True,blank=True)
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Reviewed by {self.name}" 

class BorrowHistory(models.Model):
    borrower =  models.ForeignKey(UserLibraryAccount,on_delete=models.CASCADE)
    book = models.ForeignKey(BookModel,on_delete=models.CASCADE)
    balanace_after_transaction = models.DecimalField(decimal_places=2, max_digits=12,null=True, blank=True)
    is_returned = models.BooleanField(default=False)
    borrow_date = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['borrow_date']
   
    

