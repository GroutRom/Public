from django.contrib import admin
from listings.models import Band, Ad

# Register your models here.
class BandAdmin(admin.ModelAdmin):
	list_display = ('name', 'year_formed', 'genre')

class AdAdmin(admin.ModelAdmin):
	list_display = ('title', 'band', 'types')

admin.site.register(Band, BandAdmin)
admin.site.register(Ad, AdAdmin)