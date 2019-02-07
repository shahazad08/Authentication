from django.contrib import admin
from .models import User
# from adminplus.sites import AdminSitePlus

admin.site.register(User)
admin.autodiscover()