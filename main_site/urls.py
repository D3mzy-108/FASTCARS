from django.urls import path

from .views import add_customer_review, add_query, book_car, booking_history, car_details, cars, cars_by_brand, contact, faqs, home


urlpatterns = [
    path('', home, name="home"),
    path('cars/', cars, name="cars"),
    path('cars/<slug:slug>', cars_by_brand, name="cars_by_brand"),
    path('car_details/<slug:slug>/', car_details, name="car_details"),
    path('book_car/<slug:slug>/', book_car, name="book_car"),
    path('booking_history/', booking_history, name="booking_history"),
    path('faqs/', faqs, name="faqs"),
    path('contact/', contact, name="contact"),
    path('contact/add_query/', add_query, name="add_query"),
    path('contact/add_review/', add_customer_review, name="add_customer_review"),
]
