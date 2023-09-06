from django.db.models.signals import post_save, post_delete
from .models import Profile
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings


def createProfile(sender, instance, created, **kwargs):
    user = instance
    if created:
        profile = Profile.objects.create(
            user=user,
            username=user.username,
            email=user.email,
            name=user.first_name + ' ' + user.last_name,
        )
        send_mail(
            subject='Welcome To Dev Mingle',
            message='We are Glad you are Here!!',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[profile.email],
            fail_silently=False
        )


def updateUser(sender, instance, created, **kwargs):
    profile = instance
    user = profile.user

    if created is False:
        user.first_name = profile.name
        user.username = profile.username
        user.email = profile.email
        user.save()


def deleteUser(sender, instance, **kwargs):
    user = instance.user
    user.delete()


post_save.connect(createProfile, sender=User)
post_save.connect(updateUser, sender=Profile)
post_delete.connect(deleteUser, sender=Profile)
