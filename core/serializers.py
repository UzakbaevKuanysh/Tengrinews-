from rest_framework import serializers
from .models import Category, News, NewsImage, Author


class CategorySerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField()

    def create(self, validated_data):
        category = Category()
        category.name = validated_data.get('name')
        category.save()
        return category

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name')
        instance.save()
        return instance


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsImage
        fields = ('id', 'src',)


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = '__all__'


class NewsSerializer(serializers.ModelSerializer):
    author = AuthorSerializer()
    category = CategorySerializer()
    images = ImageSerializer(many=True)

    class Meta:
        model = News
        fields = '__all__'


class NewsCreateSerializer(serializers.Serializer):
    category_id = serializers.IntegerField()
    title = serializers.CharField()
    body = serializers.CharField()

    def create(self, validated_data):
        news = News()
        news.title = validated_data.get('title')
        news.body = validated_data.get('body')
        news.category_id = validated_data.get('category_id')
        news.author = validated_data.get('author')
        news.save()
        return news

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title')
        instance.body = validated_data.get('body')
        instance.category_id = validated_data.get('category_id')
        instance.save()
        return instance
