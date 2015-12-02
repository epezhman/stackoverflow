from rest_framework import serializers

from . import models


class TagSerializer(serializers.ModelSerializer):
    text = serializers.CharField(source='name', read_only=True)

    class Meta:
        model = models.Tag
        fields = ('id', 'text',)
