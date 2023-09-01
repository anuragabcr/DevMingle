from django.db.models.signals import post_save, post_delete
from .models import Profile
from django.contrib.auth.models import User


def createProfile(sender, instance, created, **kwargs):
    user = instance
    if created:
        profile = Profile.objects.create(
            user=user,
            username=user.username,
        )
    else:
        profile = Profile.objects.get(user=user)
        profile.email = user.email
        profile.name = user.first_name + ' ' + user.last_name
        profile.save()


def deleteUser(sender, instance, **kwargs):
    user = instance.user
    user.delete()


post_save.connect(createProfile, sender=User)
post_delete.connect(deleteUser, sender=Profile)
