from django.urls import path  
from search_app import views  
  
urlpatterns = [  
    path('', views.SearchView.as_view()),  
]