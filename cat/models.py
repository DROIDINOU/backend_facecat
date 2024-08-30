from django.db import models
from django.contrib.auth import get_user_model

from django.contrib.auth.models import AbstractUser
from datetime import date
from django.conf import settings
from django.utils import timezone




# USER MODEL
class CustomUser(AbstractUser):
        
        email = models.EmailField(unique=True, blank=False)
        friends = models.ManyToManyField(
        'self', 
        blank=True, 
        symmetrical=False,  # Important pour éviter la symétrie dans la relation
        related_name='related_to'
    )


# MESSAGES FOR NEWS FEED AND MESSAGES FOR CONVERSATION CHAT
class Messages (models.Model):
       message = models.TextField()
       timestamp = models.DateTimeField(auto_now_add=True)
       auteur = models.ForeignKey (get_user_model(), on_delete= models.CASCADE, related_name = 'mes_messages')  
       likes = models.ManyToManyField(get_user_model(), related_name='messages_liked', blank=True)

       class Meta:
        ordering = ['timestamp']


class MessagesChat(models.Model):
    sender = models.ForeignKey(get_user_model(), related_name='sent_messages', on_delete=models.CASCADE)
    receiver = models.ForeignKey(get_user_model(), related_name='received_messages', on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)

    class Meta:
        ordering = ['timestamp']

    def __str__(self):
        return f"{self.sender} to {self.receiver} at {self.timestamp}"

    


# COMMENTS
class Comments (models.Model):
     content = models.TextField()
     timestamp = models.DateTimeField(auto_now_add=True)
     auteur = models.ForeignKey (get_user_model(), on_delete= models.CASCADE, related_name = 'mes_commentaires') 
     likes = models.ManyToManyField(get_user_model(), related_name='comments_liked', blank=True)
     photo = models.ForeignKey('Photos', on_delete=models.CASCADE, related_name='photo_comments', null=True, blank=True)
     video = models.ForeignKey('Videos', on_delete=models.CASCADE, related_name='videos', null=True, blank=True)
     message = models.ForeignKey(Messages, on_delete=models.CASCADE, related_name='message_comments',null=True, blank=True)

     class Meta:
        ordering = ['timestamp']

#PHOTOS
class Photos(models.Model):
    title = models.CharField(max_length=255, blank=True, null=True)
    photo = models.ImageField(upload_to='photos/')
    timestamp = models.DateTimeField(default=timezone.now)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='mes_photos')
    likes = models.ManyToManyField(get_user_model(), related_name='likes_photos', blank=True)
    is_published = models.BooleanField(default=False) 
    
    class Meta:
        ordering = ['timestamp']



    def __str__(self):
        return self.title



# FRIEND REQUEST
class FriendRequest(models.Model):
    from_user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='sent_friend_requests', on_delete=models.CASCADE)
    to_user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='received_friend_requests', on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=[('pending', 'Pending'), ('accepted', 'Accepted'), ('rejected', 'Rejected')], default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['from_user', 'to_user'], name='unique_friend_request')
        ]

    def __str__(self):
        return f"{self.from_user} -> {self.to_user} ({self.status})"
    


# VIDEO
class Videos(models.Model):
    title = models.CharField(max_length=255)
    video = models.FileField(upload_to='videos/')
    timestamp = models.DateTimeField(default=timezone.now)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='mes_videos')
    likes = models.ManyToManyField(get_user_model(), related_name='videosdetestet', blank=True)
    is_published = models.BooleanField(default=False) 


    def __str__(self):
        return self.title
    
# PICTURE PROFILE
class Profile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)
    likes = models.ManyToManyField(get_user_model(), related_name='likes_profile', blank=True)



# GAME CATEGORIES
class Cats(models.Model):
     name =  models.CharField(max_length= 110,null=True, blank=True)
     race = models.CharField(max_length= 60,null=True, blank=True)
     owner = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='liste_chats')
     presentation = models.TextField( blank=True, null=True)
     birth_date = models.DateField()
     created_at = models.DateTimeField(auto_now_add=True)


     @property
     def age(self):
        today = date.today()
        return today.year - self.date_naissance.year - ((today.month, today.day) < (self.date_naissance.month, self.date_naissance.day))
     

class Fun_Categories(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Points(models.Model):
    cat = models.ForeignKey(Cats, on_delete=models.CASCADE)
    category = models.ForeignKey(Fun_Categories, on_delete=models.CASCADE, related_name='categorie')
    points = models.IntegerField(default=0)
    timestamp = models.DateTimeField(auto_now_add=True)  # Add this field to store creation time

    class meta:
       ordering = ['timestamp']
    
    
    def __str__(self):
        return f"{self.cat.name} - {self.category.name} : {self.points} points"
    


    


       







