from django.contrib import admin
from django import forms
from django.contrib.auth.admin import UserAdmin
from .models import User
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

admin.site.register(User, CustomUserAdmin)