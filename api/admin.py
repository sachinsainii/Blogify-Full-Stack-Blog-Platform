from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
from django.contrib.auth.forms import UserChangeForm
from .models import Postt

# Register your models here.
class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    fieldsets = (
        (None, { "fields": ( 'email', 'password',)}),
        ('Personal info',{'fields':('first_name','last_name',)}),
        ('Permissions',{'fields':('is_active','is_staff',
        'is_superuser','groups','user_permissions',)}),
        ('Important dates',{'fields':('last_login','date_joined',)}),
        ('user_info',{'fields':('native_name','phone_no','birth_date','location',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide', ),
            'fields' : ('email','password1','password2'),
        }),
    )
    list_display = ['email', 'first_name', 'last_name','is_staff',
    'native_name', 'phone_no']
    search_fields = ('email','first_name','last_name')
    ordering = ('email', )

admin.site.register(CustomUser, UserAdmin)
# admin.site.register(Postt)  
