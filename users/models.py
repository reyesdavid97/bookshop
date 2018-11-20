# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.forms import ModelForm


class Profile(models.Model):
    user = models.OneToOneField(
        User, related_name='user', on_delete=models.CASCADE, primary_key=True)
    nick_name = models.CharField(
        'Nick name', max_length=30, blank=True, default='')
    image = models.ImageField(upload_to='profile_image', blank=True)

    def __str__(self):
        return self.user.username


class UploadPicForm(ModelForm):
    class Meta:
        model = Profile
        fields = ('image', )


def create_profile(sender, **kwargs):
    user = kwargs["instance"]
    if kwargs["created"]:
        profile = Profile(user=user)
        profile.nick_name = ''
        profile.save()


post_save.connect(create_profile, sender=User)