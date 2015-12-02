from django.contrib import admin

from . import models


@admin.register(models.Tag)
class TagAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ['name']}


@admin.register(models.Question)
class QuestionAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ['title']}


@admin.register(models.Answer)
class AnswerAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ['title']}


@admin.register(models.Vote)
class VoteAdmin(admin.ModelAdmin):
    pass
