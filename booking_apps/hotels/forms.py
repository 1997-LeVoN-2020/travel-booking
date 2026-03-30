from django import forms
from django.core.exceptions import ValidationError
from .models import Hotel, RoomType, HotelContact


class HotelForm(forms.ModelForm):
    """Форма для создания/редактирования отеля"""
    
    class Meta:
        model = Hotel
        fields = [
            'name', 'code', 'description', 'status', 'category', 'stars',
            'address', 'city', 'country', 'postal_code', 'phone', 'email', 'website',
            'latitude', 'longitude', 'timezone', 'check_in_time', 'check_out_time',
            'is_auto_confirm', 'max_advance_days'
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'code': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'check_in_time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'check_out_time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
        }
    
    def clean_code(self):
        code = self.cleaned_data['code']
        if not code.isalnum():
            raise ValidationError('Код отеля должен содержать только буквы и цифры')
        return code.upper()
    
    def clean_stars(self):
        stars = self.cleaned_data['stars']
        if stars and (stars < 1 or stars > 5):
            raise ValidationError('Количество звезд должно быть от 1 до 5')
        return stars


class RoomTypeForm(forms.ModelForm):
    """Форма для создания/редактирования типа номера"""
    
    class Meta:
        model = RoomType
        fields = [
            'hotel', 'name', 'code', 'description',
            'max_adults', 'max_children', 'room_size',
            'bed_type', 'bed_count',
            'has_wifi', 'has_tv', 'has_ac', 'has_minibar', 
            'has_safe', 'has_balcony', 'is_smoking', 'is_accessible',
            'image', 'sort_order'
        ]
        widgets = {
            'hotel': forms.HiddenInput(),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'code': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'max_adults': forms.NumberInput(attrs={'class': 'form-control'}),
            'max_children': forms.NumberInput(attrs={'class': 'form-control'}),
            'room_size': forms.NumberInput(attrs={'class': 'form-control'}),
            'bed_type': forms.Select(attrs={'class': 'form-control'}),
            'bed_count': forms.NumberInput(attrs={'class': 'form-control'}),
            'sort_order': forms.NumberInput(attrs={'class': 'form-control'}),
        }
    
    def clean(self):
        cleaned_data = super().clean()
        max_adults = cleaned_data.get('max_adults')
        max_children = cleaned_data.get('max_children')
        
        if max_adults and max_children and (max_adults + max_children) > 10:
            raise ValidationError('Общее количество гостей не может превышать 10')
        
        return cleaned_data


class HotelContactForm(forms.ModelForm):
    """Форма для контактных лиц отеля"""
    
    class Meta:
        model = HotelContact
        fields = ['hotel', 'first_name', 'last_name', 'role', 'email', 'phone', 'is_primary']
        widgets = {
            'hotel': forms.HiddenInput(),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'role': forms.Select(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
        }