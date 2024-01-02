from django.urls import path
from . import views

urlpatterns = [
    path('add/', views.AddBookView.as_view(), name='add_book'),
    path('details/<int:id>', views.DetailBookview.as_view(), name='detail_book'),
    path('details/borrownow/<int:id>', views.borrowNow, name='borrow_now'),
    path('details/return_book/<int:id>', views.ReturnBook, name='return_book'),
    path("report/", views.BorrowReportView.as_view(), name="borrow_report"),
    path("profile/", views.BorrowReportView.as_view(), name="profile"),
    path("user_profile/", views.Profile, name="user_profile"),
]
