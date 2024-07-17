from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser

# Create your models here.

class CustomUser(AbstractUser):
        friends = models.ManyToManyField('self',blank=True)

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
     message = models.ForeignKey(Messages, on_delete=models.CASCADE, related_name='comments')


class Photos(models.Model):
    title = models.CharField(max_length=255)
    photo = models.ImageField(upload_to='photos/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='photos')

    def __str__(self):
        return self.title

class Videos(models.Model):
    title = models.CharField(max_length=255)
    video = models.FileField(upload_to='videos/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='videos')

    def __str__(self):
        return self.title
    

class Profile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)

       







