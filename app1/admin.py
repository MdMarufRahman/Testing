from django.contrib import admin
from app1.models import contactUs, report,addRestaurentModel, picture, TestUser, team, history

# Register your models here.

class contactUsAdmin(admin.ModelAdmin):
    list_display = ('contactFullName', 'contactEmail', 'contactPhoneNumber', 'contactSubject', 'contactMessage')

admin.site.register(contactUs, contactUsAdmin)

class reportAdmin(admin.ModelAdmin):
    list_display = ('location', 'cause', 'damage', 'comments')

admin.site.register(report, reportAdmin)

class restaurantAdmin(admin.ModelAdmin):
    list_display = ('commpanyName', 'issuedBy', 'expiryDate', 'message')

admin.site.register(addRestaurentModel, restaurantAdmin)
    
admin.site.register([
    picture, TestUser, history
])

class teamAdmin(admin.ModelAdmin):
    list_display = ('name',)

admin.site.register(team, teamAdmin)


