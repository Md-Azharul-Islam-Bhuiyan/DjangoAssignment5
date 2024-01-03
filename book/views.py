from django.shortcuts import render,redirect
from django.urls import reverse_lazy
from transactions.models import Transaction
from .models import BookModel, BorrowHistory
from auth_user.models import UserLibraryAccount
from .forms import BooksForm, ReviewForm
from django.contrib import messages
from datetime import datetime
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, UpdateView, DeleteView, DetailView, ListView, TemplateView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

def send_borrow_email(user, amount, subject, template, name):
    message = render_to_string(template,{
        'user': user, 
        'amount': amount,
        'book_name': name
    })
    send_email = EmailMultiAlternatives(subject, '', to=[user.email])
    send_email.attach_alternative(message, "text/html")
    send_email.send()

@method_decorator(login_required, name='dispatch')
class AddBookView(CreateView):
    model = BookModel
    form_class = BooksForm
    template_name = 'add_book.html'
    success_url = reverse_lazy('add_book')

    def form_valid(self, form):
        form.instance.auth_user = self.request.user
        messages.success(self.request, 'Book Successfully Added.')
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['type'] = 'Add Book'
        return context


def Profile(request):
    user = UserLibraryAccount.objects.get(user= request.user)
    # print("username: line 47")
    return render(request, 'user_profile.html', {'data': user})

def borrowNow(request, id):
    
    book = BookModel.objects.get(id=id)
    user = UserLibraryAccount.objects.get(user=request.user)
    # borrower= BorrowHistory.objects.get(user=request.user)
    # print(user)
    if book.quantity> 0 and user.balance >= book.price:
        book.quantity-=1
        user.balance -= book.price
        balanace_after_transaction = user.balance
        book.save()
        user.save()
        BorrowHistory.objects.create(borrower=user, book=book, balanace_after_transaction=balanace_after_transaction)
    # messages.SUCCESS(request,'Book Succesfully Borrowed')
        send_borrow_email(request.user, book.price, "Borrow Messages", 'borrow_email.html', book.book_name)    
    return redirect('home')


def ReturnBook(request, id):
    user = UserLibraryAccount.objects.get(user=request.user)
    borrow = BorrowHistory.objects.get(id=id)
    book = BookModel.objects.get(id=borrow.book.id)
    book.quantity +=1
    user.balance += book.price
    borrow.is_returned = True
    user.save()
    book.save()
    borrow.save()
    
    return redirect('profile')

class BorrowReportView(LoginRequiredMixin , ListView): 
    template_name='profile.html'
    model = BorrowHistory
    balance = 0
    
    def get_queryset(self) :
        user = UserLibraryAccount.objects.get(user=self.request.user)
        queryset= super().get_queryset().filter(
           borrower = user
        )
    
        start_date_str = self.request.GET.get('start_date')
        end_date_str = self.request.GET.get('end_date')

        if start_date_str and end_date_str:
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date() 
            end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()

            queryset = queryset.filter(borrow_date__date__gte=start_date, borrow_date__date__lte=end_date)
            self.balance = BorrowHistory.objects.filter(borrow_date__date__gte= start_date, borrow_date__date__lte= end_date)
        else:
            self.balance = user.balance

        
        return queryset.distinct() 
    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'account':self.request.user
        })
        
        return context

class DetailBookview(DetailView):
    model = BookModel
    pk_url_kwarg= 'id'
    template_name = 'details.html'
    
    
    def post(self, request, *args, **kwargs):
        
        review_form = ReviewForm(data=self.request.POST)
        
        
        book = self.get_object()
        print(book)
        if review_form.is_valid():
            new_review = review_form.save(commit=False)
            new_review.book = book
            
            new_review.save()
        return self.get(request, *args, **kwargs)
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        book = self.object # post model er object ekhane store korlam
        reviews = book.reviews.all()
        review_form = ReviewForm()
        
        context['reviews'] = reviews
        context['review_form'] = review_form
        context['borrow'] = BorrowHistory.objects.all()
        context['book_id'] = self.object.id
        return context

