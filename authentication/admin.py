from django.contrib import admin

from authentication.models import User , Token

# Register your models here.


# Register your models here.
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'middle_name', 'last_name', 'email')



@admin.register(Token)
class TokenAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_id', 'token', 'expired', 'created_on')


# admin.site.register(Token)