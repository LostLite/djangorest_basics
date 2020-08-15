from rest_framework import serializers
from .models import Article

# When using the Serializer serializer, remembers to specify the create and update methods
# This is not necessary if you use a ModelSerializer
class ArticleSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=100)
    author = serializers.CharField(max_length=100)
    email = serializers.EmailField(max_length=100)


    # define create method for 
    def create(self, validated_data):
        return Article.objects.create(**validated_data)

    
    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.author = validated_data.get('author', instance.author)
        instance.email = validated_data.get('email', instance.email)

        # save and return the instance that you have edited
        instance.save()
        return instance


# When using ModelSerializers, you keep your code clean and free of unnecessary implementation 
# of create and update
class ArticleModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ['id', 'title', 'author', 'email']