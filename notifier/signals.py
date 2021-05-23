# signals
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.db import transaction
from .models import BaseNotification, Notification

User = get_user_model()


# decorator for m2m relation on post save trigger
def on_transaction_commit(func):
    def inner(*args, **kwargs):
        transaction.on_commit(lambda: func(*args, **kwargs))

    return inner


# post save trigger auto create instance notification for user
@receiver(post_save, sender=BaseNotification)
@on_transaction_commit
def create_user_notification(sender, instance, created, **kwargs):
    if created:
        for user in instance.receivers.all():
            Notification.objects.create(
                receiver=user, notification=instance
            )


# channels send notification
@receiver(post_save, sender=Notification)
def announce_new_notification(sender, instance, created, **kwargs):
    if created:
        title = instance.notification.title
        group_name = 'group_%s' % instance.receiver.get_username()
        time_stamp = str(instance.notification.created_at)
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            "gossip", {"type": "user.gossip",
                       'group': group_name,
                       'time_stamp': time_stamp,
                       "event": "New Notification",
                       "income": title})
