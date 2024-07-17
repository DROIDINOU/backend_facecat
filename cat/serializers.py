# myapp/serializers.py

from rest_framework import serializers
from .models import CustomUser,Messages, Comments

from rest_framework import serializers
from .models import CustomUser, Cats

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'first_name', 'last_name','password']

class CatsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cats
        fields = ['id', 'name', 'race','presentation','created_at', 'maitre']

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'password']
        extra_kwargs = {
            'password': {'write_only': True, 'min_length': 8},
            'email': {'required': True, 'allow_blank': False}
        }

    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )
        return user
    
class FriendsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['username']

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Messages
        fields = ['id', 'message', 'timestamp', 'auteur', 'likes',]#'commentaires'
        read_only_fields = ['id', 'timestamp', 'auteur', 'likes', ]#'commentaires'

class CommentsSerializer(serializers.ModelSerializer):
    message_id = serializers.IntegerField(write_only=True)  # Ajout du champ message_id

    class Meta:
        model = Comments
        fields = ['id', 'content', 'timestamp', 'auteur', 'likes', 'message', 'message_id']
        read_only_fields = ['id', 'timestamp', 'auteur', 'likes', 'message']

    def create(self, validated_data):
        message_id = validated_data.pop('message_id')
        message = Messages.objects.get(pk=message_id)
        comment = Comments.objects.create(message=message, **validated_data)
        return comment
    
class CommentsAllSerializer(serializers.ModelSerializer):
      class Meta:
        model = Comments
        fields = '__all__'
        read_only_fields = ['id', 'content', 'timestamp', 'auteur', 'likes', 'message']


class Comments_By_Message_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Comments
        fields = ['id', 'content', 'timestamp', 'auteur', 'likes', 'message']
        read_only_fields = ['id', 'timestamp', 'auteur', 'likes']
