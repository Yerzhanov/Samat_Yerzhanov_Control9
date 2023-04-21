from rest_framework import serializers

import users
from posts.models import Post


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id', 'user', 'image', 'caption', 'title', 'slug', 'created']
        read_only_fields = ['created']

    def create(self, validated_data):
        return Post.objects.create(**validated_data)

    def update(self, instance, validated_data):
        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.save()
        return instance

