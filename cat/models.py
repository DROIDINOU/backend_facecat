from django.db import models
from django.contrib.auth import get_user_model

from django.contrib.auth.models import AbstractUser
from datetime import date
from django.conf import settings
from django.utils import timezone




# Create your models here.

class CustomUser(AbstractUser):
    friends = models.ManyToManyField(
        'self', 
        blank=True, 
        symmetrical=False,  # Important pour éviter la symétrie dans la relation
        related_name='related_to'
    )

"""username: Nom d'utilisateur hérité de AbstractUser.
email: Email hérité de AbstractUser.
first_name: Prénom hérité de AbstractUser.
last_name: Nom de famille hérité de AbstractUser.
password: Mot de passe hérité de AbstractUser.
friends: Champ ManyToManyField qui fait référence à lui-même ('self'). Il représente une relation d'amitié entre utilisateurs."""















class Cats (models.Model):
     name = models.CharField(max_length=100)
     race = models.CharField(max_length=100)
     presentation = models.TextField()
     created_at = models.DateTimeField(auto_now_add=True)
     maitre = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name = 'mes_chats')


class Messages (models.Model):
       message = models.TextField()
       timestamp = models.DateTimeField(auto_now_add=True)
       auteur = models.ForeignKey (get_user_model(), on_delete= models.CASCADE, related_name = 'mes_messages')  
       likes = models.ManyToManyField(get_user_model(), related_name='messages_liked', blank=True)
       #commentaires = models.ManyToManyField(get_user_model(), related_name='comments', blank=True)

       class Meta:
        ordering = ['timestamp']



class Comments (models.Model):
     content = models.TextField()
     timestamp = models.DateTimeField(auto_now_add=True)
     auteur = models.ForeignKey (get_user_model(), on_delete= models.CASCADE, related_name = 'mes_commentaires') 
     likes = models.ManyToManyField(get_user_model(), related_name='comments_liked', blank=True)
     photo = models.ForeignKey('Photos', on_delete=models.CASCADE, related_name='photo_comments', null=True, blank=True)
     video = models.ForeignKey('Videos', on_delete=models.CASCADE, related_name='videos', null=True, blank=True)
     message = models.ForeignKey(Messages, on_delete=models.CASCADE, related_name='message_comments',null=True, blank=True)


class Photos(models.Model):
    title = models.CharField(max_length=255, blank=True, null=True)
    photo = models.ImageField(upload_to='photos/')
    timestamp = models.DateTimeField(default=timezone.now)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='mes_photos')
    likes = models.ManyToManyField(get_user_model(), related_name='likes_photos', blank=True)
    is_published = models.BooleanField(default=False) 




    def __str__(self):
        return self.title

"""class FeedPhoto(models.Model):
    title = models.CharField(max_length=255, blank=True, null=True)
    photo = models.ImageField(upload_to='feed_photos/')
    timestamp = models.DateTimeField(default=timezone.now)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='feed_photos')
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='likes_feed_photos', blank=True)

    class Meta:
        ordering = ['timestamp']"""



class Videos(models.Model):
    title = models.CharField(max_length=255)
    video = models.FileField(upload_to='videos/')
    timestamp = models.DateTimeField(default=timezone.now)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='mes_videos')
    likes = models.ManyToManyField(get_user_model(), related_name='videos', blank=True)

    def __str__(self):
        return self.title
    

class Profile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)
    


# Tables des chats et les catégories pour lesquelles ils vont obtenir des points
class ListeChats(models.Model):
     name =  models.CharField(max_length= 110)
     race = models.CharField(max_length= 60)
     owner = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='Liste_chats')
     date_naissance = models.DateField()

     @property
     def age(self):
        today = date.today()
        return today.year - self.date_naissance.year - ((today.month, today.day) < (self.date_naissance.month, self.date_naissance.day))
     

class Fun_Categories(models.Model):
    nom = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.nom


class Points(models.Model):
    chat = models.ForeignKey(ListeChats, on_delete=models.CASCADE)
    categorie = models.ForeignKey(Fun_Categories, on_delete=models.CASCADE)
    points = models.IntegerField(default=0)

    class meta:
       ordering = ['-timestamp']
    
    
    def __str__(self):
        return f"{self.chat.nom} - {self.categorie.nom} : {self.points} points"
    

# demandes d -'amitié
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
    

   

    


       







