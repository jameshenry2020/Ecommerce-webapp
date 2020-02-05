from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import MyAccount

# Register your models here.
class AccountAdmin(UserAdmin):
    list_display=('email', 'first_name','last_name','username','date_joined','last_login','is_admin','is_staff')
    search_fields=('email','username',)
    readonly_fields=('date_joined', 'last_login')

    filter_horizontal=()
    list_filter=('date_joined','last_login')
    fieldsets=()


admin.site.register(MyAccount, AccountAdmin)
