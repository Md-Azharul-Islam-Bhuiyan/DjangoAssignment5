from django.shortcuts import render
from django.urls import reverse_lazy
from .forms import DepositeForm
from .constants import DEPOSIT
from transactions.models import Transaction
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

def send_transaction_email(user, amount, subject, template):
    message = render_to_string(template,{
        'user': user, 
        'amount': amount
    })
    send_email = EmailMultiAlternatives(subject, '', to=[user.email])
    send_email.attach_alternative(message, "text/html")
    send_email.send()


class TransactinViewsMixin(LoginRequiredMixin, CreateView):
    template_name = 'transactions/deposit.html'
    model = Transaction
    title = ''
    success_url = reverse_lazy('deposit_money')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({
            'account': self.request.user.account
        })
        return kwargs
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'title': self.title
        })
        
        return context
    

class DepositMoneyView(TransactinViewsMixin):
    form_class = DepositeForm
    title = 'Deposite Form'

    def get_initial(self):
         initial = {'transaction_type': DEPOSIT}
         return initial
    
    def form_valid(self, form):
        amount = form.cleaned_data.get('amount')
        account = self.request.user.account
        account.balance += amount

        account.save(
           update_fields= [
               'balance'
            ]
        )

        messages.success(self.request, f'{"{:,.2f}".format(float(amount))}৳ was deposited to your account successfully')

        send_transaction_email(self.request.user, amount, "Deposite Messages", 'transactions/deposit_email.html')
        return super().form_valid(form)
