# myapp/serializers.py

from rest_framework import serializers
from .models import (CustomUser, Messages, MessagesChat, Comments, Profile, Fun_Categories, Points, Photos,  Cats, Videos, Fun_Categories, Points, FriendRequest)
from rest_framework import serializers



# USER
class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id','username', 'first_name','last_name','password', 'email','friends']


class CustomUserMinimalSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username']  # Inclure uniquement les champs que vous souhaitez récupérer


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'first_name', 'last_name', 'password','email',]
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


class CustomfriendsSerializer(serializers.ModelSerializer):
    friends = serializers.PrimaryKeyRelatedField(many=True, queryset=CustomUser.objects.all())
    
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'friends']



# MESSAGES
class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Messages
        fields = ['id', 'message', 'timestamp', 'auteur', 'likes',]
        read_only_fields = ['id', 'timestamp', 'auteur', 'likes', ]

# friends
class FriendsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['username']


class FriendRequestSerializerAll(serializers.ModelSerializer):
      class Meta:
        model = FriendRequest
        fields = '__all__'
        read_only_fields = ['id', 'from_user', 'to_user', 'status', 'created_at']


# COMMENTAIRES
        

class CommentsSerializer(serializers.ModelSerializer):
    message_id = serializers.IntegerField(write_only=True)  # Ajout du champ message_id

    class Meta:
        model = Comments
        fields = ['id', 'content', 'timestamp', 'auteur', 'likes', 'message','photo','video', 'message_id']
        read_only_fields = ['id', 'timestamp', 'auteur', 'likes', 'message', 'photo','video']

    def create(self, validated_data):
        message_id = validated_data.pop('message_id')
        message = Messages.objects.get(pk=message_id)
        comment = Comments.objects.create(message=message, **validated_data)
        return comment
    

class CommentsAllSerializer(serializers.ModelSerializer):
      class Meta:
        model = Comments
        fields = '__all__'
        read_only_fields = ['id', 'content', 'timestamp', 'auteur', 'likes', 'message','photo','video']


class Comments_By_Message_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Comments
        fields = ['id', 'content', 'timestamp', 'auteur', 'likes', 'message']
        read_only_fields = ['id', 'timestamp', 'auteur', 'likes','photo','video']


class Comments_By_Photo_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Comments
        fields = ['id', 'content', 'timestamp', 'auteur', 'likes', 'photo']
        read_only_fields = ['id', 'timestamp', 'auteur', 'likes','video','message']


class Comments_By_Video_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Comments
        fields = ['id', 'content', 'timestamp', 'auteur', 'likes', 'video']
        read_only_fields = ['id', 'timestamp', 'auteur', 'likes','photo','message']



class CommentsphotosSerializer(serializers.ModelSerializer):
    photo_id = serializers.IntegerField(write_only=True)  # Ajout du champ message_id

    class Meta:
        model = Comments
        fields = ['id', 'content', 'timestamp', 'auteur', 'likes', 'message','photo','video', 'photo_id']
        read_only_fields = ['id', 'timestamp', 'auteur', 'likes', 'message', 'photo','video']


class CommentsvideosSerializer(serializers.ModelSerializer):
    video_id = serializers.IntegerField(write_only=True)  # Ajout du champ message_id

    class Meta:
        model = Comments
        fields = ['id', 'content', 'timestamp', 'auteur', 'likes', 'message','photo','video', 'video_id']
        read_only_fields = ['id', 'timestamp', 'auteur', 'likes', 'message', 'photo','video']

   


# PHOTO PROFIL
class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['profile_picture']


class ProfileSerializer1(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'


class ProfileSerializer3(serializers.ModelSerializer):
    
    class Meta:
        model = Profile
        fields = ['user','profile_picture']

# CATS
class CatsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cats
        fields = ['id', 'name', 'race','owner','presentation','birth_date', 'created_at']
        read_only_fields = ['id', 'created_at']

class CatSerializer_for_id_name_owner_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Cats
        fields = ['id','name, owner']
        read_only_fields = ['id','name, owner']


class CatsSerializer_by_owner(serializers.ModelSerializer):
    owner_username = serializers.SerializerMethodField()
    owner_id = serializers.SerializerMethodField()

    class Meta:
        model = Cats
        fields = ['id', 'name', 'race', 'owner_username', 'owner_email', 'presentation', 'birth_date', 'created_at']
        read_only_fields = ['id', 'created_at']

    def get_owner_username(self, obj):
        return obj.owner.username

    def get_owner_id(self, obj):
        return obj.owner.id
    
# funk categories / points
class Points_Serializer(serializers.ModelSerializer):
    category = serializers.SerializerMethodField()
    cat = serializers.SerializerMethodField()
    class Meta:
        model = Points
        fields = ['category','cat','points']
        read_only_fields = ['category','cat','points']
        
        def get_category(self, obj):
           return obj.category.name
        
        
        def get_cat(self, obj):
           return obj.cat.name


#PHOTOS + VIDEOS
        
class PhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photos
        fields = ['id', 'title', 'photo','timestamp', 'uploaded_at', 'owner', 'likes','is_published']
        read_only_fields = ['id','title','timestamp', 'uploaded_at', 'owner', 'likes']



class PhotoSerializer1(serializers.ModelSerializer):
     class Meta:
        model = Photos
        fields = ['id', 'title', 'photo', 'timestamp', 'uploaded_at', 'owner', 'likes', 'is_published']
        read_only_fields = ['id', 'timestamp', 'uploaded_at', 'owner']



class VideosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Videos
        fields = ['id', 'title', 'video','timestamp', 'uploaded_at', 'owner', 'likes', 'is_published']
        read_only_fields = ['id','title','timestamp', 'uploaded_at', 'owner',]



class VideosSerializer1(serializers.ModelSerializer):
    class Meta:
        model = Videos
        fields = '__all__'










    

