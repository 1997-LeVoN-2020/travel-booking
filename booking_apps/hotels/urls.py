from django.urls import path
from . import views

app_name = 'hotels'

urlpatterns = [
    # Список отелей
    path('', views.HotelListView.as_view(), name='list'),
    
    # Создание отеля
    path('create/', views.HotelCreateView.as_view(), name='create'),
    
    # Детали отеля
    path('<int:pk>/', views.HotelDetailView.as_view(), name='detail'),
    path('<int:pk>/dashboard/', views.hotel_dashboard, name='dashboard'),
    
    # Редактирование отеля
    path('<int:pk>/edit/', views.HotelUpdateView.as_view(), name='edit'),
    
    # Удаление отеля
    path('<int:pk>/delete/', views.HotelDeleteView.as_view(), name='delete'),
    
    # Типы номеров
    path('<int:hotel_id>/room-types/create/', 
         views.RoomTypeCreateView.as_view(), 
         name='roomtype_create'),
    
    # API для статистики
    path('api/quick-stats/', views.hotel_quick_stats, name='quick_stats'),
]