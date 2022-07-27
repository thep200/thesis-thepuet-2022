from django import forms
from django.db import models
from django.forms import fields
from .models import ImageNT
from django.forms import ModelForm

class UserImage(ModelForm):
    class Meta:
        model = ImageNT
        fields = '__all__'
