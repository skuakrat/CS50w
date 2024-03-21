from django.contrib import admin
from .models import *

class TypeAdmin(admin.ModelAdmin):
    list_display = ('type', 'display_breed')

    def display_breed(self, obj):
        return ", ".join([breed.breed for breed in obj.breed_set.all()])



# Register your models here.
admin.site.register(User)
admin.site.register(Province)
admin.site.register(Type, TypeAdmin)
admin.site.register(Breed)
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Dm)
