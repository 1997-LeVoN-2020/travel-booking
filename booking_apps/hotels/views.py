from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.db.models import Q, Count, Sum
from django.utils import timezone
from .models import Hotel, RoomType, HotelContact
from .forms import HotelForm, RoomTypeForm, HotelContactForm
#from .services import HotelService, RoomTypeService


class HotelListView(LoginRequiredMixin, ListView):
    model = Hotel
    template_name = 'hotels/list.html'
    context_object_name = 'hotels'
    paginate_by = 12
    
    def get_queryset(self):
        queryset = Hotel.objects.all().prefetch_related('room_types')
        
        # Фильтрация по статусу
        status = self.request.GET.get('status')
        if status:
            queryset = queryset.filter(status=status)
        
        # Фильтрация по городу
        city = self.request.GET.get('city')
        if city:
            queryset = queryset.filter(city__icontains=city)
        
        # Поиск
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
                Q(name__icontains=search) |
                Q(city__icontains=search) |
                Q(code__icontains=search)
            )
        
        return queryset.order_by('name')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_hotels'] = Hotel.objects.count()
        context['active_hotels'] = Hotel.objects.filter(status=Hotel.HotelStatus.ACTIVE).count()
        
        # Уникальные города для фильтра
        context['cities'] = Hotel.objects.values_list('city', flat=True).distinct().order_by('city')
        
        return context


class HotelDetailView(LoginRequiredMixin, DetailView):
    """Детальная информация об отеле"""
    model = Hotel
    template_name = 'hotels/detail.html'
    context_object_name = 'hotel'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        hotel = self.object
        
        # Статистика отеля
        context['stats'] = HotelService.get_hotel_stats(hotel.id)
        context['room_types'] = hotel.room_types.all()
        context['contacts'] = hotel.contacts.all()
        context['primary_contact'] = hotel.contacts.filter(is_primary=True).first()
        
        return context


class HotelCreateView(LoginRequiredMixin, CreateView):
    """Создание нового отеля"""
    model = Hotel
    form_class = HotelForm
    template_name = 'hotels/create.html'
    success_url = reverse_lazy('hotels:list')
    
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, f'Отель "{self.object.name}" успешно создан')
        return response


class HotelUpdateView(LoginRequiredMixin, UpdateView):
    """Редактирование отеля"""
    model = Hotel
    form_class = HotelForm
    template_name = 'hotels/edit.html'
    
    def get_success_url(self):
        return reverse_lazy('hotels:detail', kwargs={'pk': self.object.pk})
    
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, f'Отель "{self.object.name}" успешно обновлен')
        return response


class HotelDeleteView(LoginRequiredMixin, DeleteView):
    """Удаление отеля"""
    model = Hotel
    template_name = 'hotels/delete.html'
    success_url = reverse_lazy('hotels:list')
    
    def delete(self, request, *args, **kwargs):
        hotel = self.get_object()
        messages.success(request, f'Отель "{hotel.name}" успешно удален')
        return super().delete(request, *args, **kwargs)


class RoomTypeCreateView(LoginRequiredMixin, CreateView):
    """Создание типа номера"""
    model = RoomType
    form_class = RoomTypeForm
    template_name = 'hotels/roomtype_form.html'
    
    def get_initial(self):
        initial = super().get_initial()
        hotel_id = self.kwargs.get('hotel_id')
        if hotel_id:
            initial['hotel'] = get_object_or_404(Hotel, id=hotel_id)
        return initial
    
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, f'Тип номера "{self.object.name}" успешно создан')
        return response
    
    def get_success_url(self):
        return reverse_lazy('hotels:detail', kwargs={'pk': self.object.hotel.pk})


# Дополнительные view functions
def hotel_dashboard(request, pk):
    """Дашборд отеля"""
    hotel = get_object_or_404(Hotel, pk=pk)
    stats = HotelService.get_hotel_stats(pk)
    
    # Последние бронирования
    from booking_apps.bookings.models import Booking
    recent_bookings = Booking.objects.filter(hotel=hotel).order_by('-created_at')[:10]
    
    context = {
        'hotel': hotel,
        'stats': stats,
        'recent_bookings': recent_bookings,
    }
    
    return render(request, 'hotels/dashboard.html', context)


def hotel_quick_stats(request):
    """Быстрая статистика по отелям (для AJAX)"""
    from django.http import JsonResponse
    
    stats = {
        'total_hotels': Hotel.objects.count(),
        'active_hotels': Hotel.objects.filter(status=Hotel.HotelStatus.ACTIVE).count(),
        'cities_count': Hotel.objects.values('city').distinct().count(),
    }
    
    return JsonResponse(stats)