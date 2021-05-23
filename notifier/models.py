# models
from django.contrib.auth.models import AbstractUser
from django.db import models


# auth user model
class User(AbstractUser):
    email = models.EmailField(unique=True, null=False, blank=False)

    class Meta:
        ordering = ('username',)

    def __str__(self):
        return self.username


# base notification model, accepts one or more receivers
class BaseNotification(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    title = models.CharField(max_length=120)
    body = models.TextField()
    receivers = models.ManyToManyField(User, related_name='base_notifications')

    class Meta:
        ordering = ('-created_at',)

    @property
    def group_whois(self):
        return 'group_%s' % self.id

    def __str__(self):
        return self.title


# user notifications table
class Notification(models.Model):
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    notification = models.ForeignKey(BaseNotification, on_delete=models.CASCADE, related_name='receivers_notifications')
    is_seen = models.BooleanField(default=False)

    class Meta:
        ordering = ('receiver__username', '-notification__created_at')

    def __str__(self):
        return '%s, %s' % (self.receiver.username, self.notification.title)
