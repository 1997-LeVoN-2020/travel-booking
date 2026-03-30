from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
import uuid


class TimeStampedModel(models.Model):
    """Абстрактная модель с временными метками"""
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True, db_index=True)
    
    class Meta:
        abstract = True


class Hotel(TimeStampedModel):
    """Модель отеля"""
    
    class HotelStatus(models.TextChoices):
        ACTIVE = 'ACTIVE', 'Активный'
        INACTIVE = 'INACTIVE', 'Неактивный'
        MAINTENANCE = 'MAINTENANCE', 'На обслуживании'
    
    class HotelCategory(models.TextChoices):
        BUDGET = 'BUDGET', 'Бюджетный'
        STANDARD = 'STANDARD', 'Стандартный'
        COMFORT = 'COMFORT', 'Комфорт'
        BUSINESS = 'BUSINESS', 'Бизнес'
        LUXURY = 'LUXURY', 'Люкс'
        BOUTIQUE = 'BOUTIQUE', 'Бутик'
        RESORT = 'RESORT', 'Курортный'
    
    # Основная информация
    name = models.CharField(max_length=200, verbose_name='Название отеля')
    code = models.CharField(max_length=50, unique=True, verbose_name='Код отеля')
    description = models.TextField(blank=True, verbose_name='Описание')
    
    # Статус и категория
    status = models.CharField(
        max_length=20,
        choices=HotelStatus.choices,
        default=HotelStatus.ACTIVE,
        verbose_name='Статус'
    )
    category = models.CharField(
        max_length=20,
        choices=HotelCategory.choices,
        default=HotelCategory.STANDARD,
        verbose_name='Категория'
    )
    stars = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        verbose_name='Количество звезд',
        null=True,
        blank=True
    )
    
    # Контактная информация
    address = models.TextField(verbose_name='Адрес')
    city = models.CharField(max_length=100, verbose_name='Город')
    country = models.CharField(max_length=100, verbose_name='Страна', default='Россия')
    postal_code = models.CharField(max_length=20, blank=True, verbose_name='Почтовый индекс')
    phone = models.CharField(max_length=20, verbose_name='Телефон')
    email = models.EmailField(verbose_name='Email')
    website = models.URLField(blank=True, verbose_name='Веб-сайт')
    
    # Географические данные
    latitude = models.DecimalField(
        max_digits=9, 
        decimal_places=6, 
        null=True, 
        blank=True,
        verbose_name='Широта'
    )
    longitude = models.DecimalField(
        max_digits=9, 
        decimal_places=6, 
        null=True, 
        blank=True,
        verbose_name='Долгота'
    )
    
    # Временные настройки
    timezone = models.CharField(
        max_length=50, 
        default='Europe/Moscow',
        verbose_name='Часовой пояс'
    )
    check_in_time = models.TimeField(default='14:00', verbose_name='Время заезда')
    check_out_time = models.TimeField(default='12:00', verbose_name='Время выезда')
    
    # Настройки управления
    is_auto_confirm = models.BooleanField(
        default=True,
        verbose_name='Автоподтверждение бронирований'
    )
    max_advance_days = models.PositiveIntegerField(
        default=365,
        verbose_name='Максимальное дней для бронирования вперед'
    )
    
    class Meta:
        verbose_name = 'Отель'
        verbose_name_plural = 'Отели'
        ordering = ['name']
        indexes = [
            models.Index(fields=['status', 'category']),
            models.Index(fields=['city', 'country']),
        ]
    
    def __str__(self):
        return f"{self.name} ({self.city})"
    
    @property
    def full_address(self):
        return f"{self.country}, {self.city}, {self.address}"
    
    @property
    def is_active(self):
        return self.status == self.HotelStatus.ACTIVE
    
    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('hotels:detail', kwargs={'pk': self.pk})


class RoomType(TimeStampedModel):
    """Тип номера в отеле"""
    
    class BedType(models.TextChoices):
        SINGLE = 'SINGLE', 'Односпальная'
        DOUBLE = 'DOUBLE', 'Двуспальная'
        TWIN = 'TWIN', 'Две односпальные'
        QUEEN = 'QUEEN', 'Кровать Queen size'
        KING = 'KING', 'Кровать King size'
        SOFA_BED = 'SOFA_BED', 'Диван-кровать'
        BUNK = 'BUNK', 'Двухъярусная'
    
    hotel = models.ForeignKey(
        Hotel, 
        on_delete=models.CASCADE, 
        related_name='room_types',
        verbose_name='Отель'
    )
    name = models.CharField(max_length=100, verbose_name='Название типа номера')
    code = models.CharField(max_length=50, verbose_name='Код типа номера')
    description = models.TextField(blank=True, verbose_name='Описание')
    
    # Вместимость
    max_adults = models.PositiveSmallIntegerField(default=2, verbose_name='Макс. взрослых')
    max_children = models.PositiveSmallIntegerField(default=0, verbose_name='Макс. детей')
    max_guests = models.PositiveSmallIntegerField(default=2, verbose_name='Макс. гостей')
    
    # Характеристики номера
    room_size = models.PositiveIntegerField(
        null=True, 
        blank=True,
        verbose_name='Площадь номера (м²)'
    )
    bed_type = models.CharField(
        max_length=20,
        choices=BedType.choices,
        default=BedType.DOUBLE,
        verbose_name='Тип кровати'
    )
    bed_count = models.PositiveSmallIntegerField(default=1, verbose_name='Количество кроватей')
    
    # Удобства
    has_wifi = models.BooleanField(default=True, verbose_name='Wi-Fi')
    has_tv = models.BooleanField(default=True, verbose_name='Телевизор')
    has_ac = models.BooleanField(default=True, verbose_name='Кондиционер')
    has_minibar = models.BooleanField(default=False, verbose_name='Минибар')
    has_safe = models.BooleanField(default=True, verbose_name='Сейф')
    has_balcony = models.BooleanField(default=False, verbose_name='Балкон')
    is_smoking = models.BooleanField(default=False, verbose_name='Для курящих')
    is_accessible = models.BooleanField(default=False, verbose_name='Доступный для инвалидов')
    
    # Фотографии
    image = models.ImageField(
        upload_to='room_types/',
        null=True,
        blank=True,
        verbose_name='Фотография номера'
    )
    
    # Порядок отображения
    sort_order = models.PositiveIntegerField(default=0, verbose_name='Порядок сортировки')
    
    class Meta:
        verbose_name = 'Тип номера'
        verbose_name_plural = 'Типы номеров'
        ordering = ['hotel', 'sort_order', 'name']
        unique_together = ['hotel', 'code']
    
    def __str__(self):
        return f"{self.hotel.name} - {self.name}"
    
    @property
    def total_rooms(self):
        """Общее количество номеров этого типа"""
        from booking_apps.hotels.models import Inventory
        return Inventory.objects.filter(
            room_type=self,
            date=timezone.now().date()
        ).aggregate(models.Sum('total_rooms'))['total_rooms__sum'] or 0
    
    @property
    def available_rooms(self):
        """Доступные номера на сегодня"""
        from booking_apps.hotels.models import Inventory
        inventory = Inventory.objects.filter(
            room_type=self,
            date=timezone.now().date()
        ).first()
        return inventory.available_rooms if inventory else 0


class HotelContact(TimeStampedModel):
    """Контактные лица отеля"""
    
    class ContactRole(models.TextChoices):
        MANAGER = 'MANAGER', 'Менеджер'
        RECEPTION = 'RECEPTION', 'Ресепшн'
        RESERVATION = 'RESERVATION', 'Бронирование'
        ADMIN = 'ADMIN', 'Администратор'
        OWNER = 'OWNER', 'Владелец'
    
    hotel = models.ForeignKey(
        Hotel,
        on_delete=models.CASCADE,
        related_name='contacts',
        verbose_name='Отель'
    )
    first_name = models.CharField(max_length=100, verbose_name='Имя')
    last_name = models.CharField(max_length=100, verbose_name='Фамилия')
    role = models.CharField(
        max_length=20,
        choices=ContactRole.choices,
        default=ContactRole.MANAGER,
        verbose_name='Должность'
    )
    email = models.EmailField(verbose_name='Email')
    phone = models.CharField(max_length=20, verbose_name='Телефон')
    is_primary = models.BooleanField(default=False, verbose_name='Основной контакт')
    
    class Meta:
        verbose_name = 'Контактное лицо'
        verbose_name_plural = 'Контактные лица'
        ordering = ['-is_primary', 'last_name', 'first_name']
    
    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.get_role_display()}"
    
    def save(self, *args, **kwargs):
        # Если это основной контакт, снимаем флаг с других контактов отеля
        if self.is_primary:
            HotelContact.objects.filter(
                hotel=self.hotel, 
                is_primary=True
            ).exclude(pk=self.pk).update(is_primary=False)
        super().save(*args, **kwargs)