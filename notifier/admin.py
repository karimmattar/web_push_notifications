# admin page
from django.contrib import admin
from .models import User, Notification, BaseNotification


admin.site.register(User)
admin.site.register(BaseNotification)
admin.site.register(Notification)
