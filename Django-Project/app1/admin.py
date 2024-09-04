from django.contrib import admin
from app1.models import Contact
from app1.models import Totpkey

# Register your models here.
admin.site.register(Contact)
admin.site.register(Totpkey)