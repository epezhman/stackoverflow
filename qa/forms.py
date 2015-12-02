from django import forms

from . import models


class AnswerForm(forms.ModelForm):
    class Meta:
        fields = ['title', 'body',]
        model = models.Answer
