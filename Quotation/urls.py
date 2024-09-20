from django.urls import path,include
from .views import *

urlpatterns = [
    path('create', create),
    path('all', all),
    path('all_filter', all_filter),
    path('one',one),
    path('update',update),
    path('delete',delete),
    path('fav',fav),
    path('approve',approve)
]
