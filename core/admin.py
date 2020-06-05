from django.contrib import admin
from django import forms
from django.contrib.auth.admin import UserAdmin
from .models import User, UserProfile, OrderDetails, OrderItems
from django.utils.translation import ugettext_lazy as _


# Register your models here.
class PlainUserForm(forms.ModelForm):
    class Meta:
        model = User
        exclude = ('username', 'password')

class CustomUserAdmin(UserAdmin):
    model = User
    search_fields = ['phone_number']
    add_fieldsets = ((None, {
        'classes': ('wide',),
        'fields' : ('phone_number', 'first_name', 'last_name')
    }), )
    fieldsets = ( (None, {'fields': ('phone_number', 'username', 'password')}),
                    (_('Personal info'), {'fields': ('first_name', 'last_name')}),
                    (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
                )
    add_form = PlainUserForm


class UserProfileAdmin(admin.ModelAdmin):
    list_display = [field.name for field in UserProfile._meta.get_fields() if field.auto_created == False]


class OrderDetailsAdmin(admin.ModelAdmin):
    list_display = [field.name for field in OrderDetails._meta.get_fields() if field.auto_created == False]


class OrderItemsAdmin(admin.ModelAdmin):
    list_display = [field.name for field in OrderItems._meta.get_fields() if field.auto_created == False]


admin.site.register(OrderItems, OrderItemsAdmin)
admin.site.register(OrderDetails, OrderDetailsAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(User, CustomUserAdmin)