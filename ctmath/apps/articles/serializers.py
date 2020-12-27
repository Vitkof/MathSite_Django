from rest_framework import serializers
from .models import *

class ArticleSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=96)
    description = serializers.CharField(max_length=256)
    text = serializers.CharField()
    pub_date = serializers.DateTimeField()
    new_period = serializers.DurationField()
    image = serializers.ImageField()

    def create(self, validated_data):
        return Article.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)
        instance.text = validated_data.get('text', instance.text)
        instance.new_period = validated_data.get('new_period', instance.new_period)
        instance.image = validated_data.get('image', instance.image)

        instance.save()
        return instance
