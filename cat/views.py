# views.py

from rest_framework import status, generics,permissions
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import CatsSerializer
from django.views.decorators.csrf import ensure_csrf_cookie
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import CustomUser,Messages,Comments,FriendRequest, Profile,Photos, Videos, MessagesChat
from .serializers import FriendRequestSerializerAll, UserSerializer,MessageSerializer,CommentsSerializer,CommentsAllSerializer, Comments_By_Message_Serializer,PhotoSerializer1, ProfileSerializer, CustomfriendsSerializer,FriendsSerializer, CustomUserMinimalSerializer, ProfileSerializer1, PhotoSerializer, VideosSerializer, VideosSerializer1, CommentsphotosSerializer, Comments_By_Photo_Serializer, Comments_By_Video_Serializer, CommentsvideosSerializer, ProfileSerializer3, ChatSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.contrib.auth import authenticate, login, logout
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from django.http import JsonResponse
from django.middleware.csrf import get_token
from django.shortcuts import get_object_or_404
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.exceptions import NotFound, ValidationError
from rest_framework.views import APIView




# CSRF TOKEN 
class GetCsrfToken(APIView):
    @method_decorator(ensure_csrf_cookie)
    def get(self, request):
        csrf_token = get_token(request)
        return JsonResponse({'csrfToken': csrf_token})

 
# USER 
# GET ALL USERS
class UserrequestAll(generics.ListAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserMinimalSerializer
    permission_classes = [IsAuthenticated]

# GET ALL FRIENDS
class FriendsListView(generics.ListAPIView):
    serializer_class = CustomUser
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return user.friends.all()
    

# GET USER BY USERNAME
class UserByUsernameView(generics.GenericAPIView):
    serializer_class = CustomUserMinimalSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        username = request.query_params.get('username', None)
        if not username:
            return Response({"detail": "Username parameter is required."}, status=400)

        try:
            user = CustomUser.objects.get(username=username)
        except CustomUser.DoesNotExist:
            raise NotFound("User not found.")

        serializer = self.serializer_class(user)
        return Response(serializer.data)


# GET FRIENDS OF ACTUAL USER
class UserFriendsView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, *args, **kwargs):
        user = request.user  # Récupère l'utilisateur connecté
        serializer = CustomfriendsSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

# SEARCH USER
class searchUserFriend (generics.ListAPIView):

   serializer_class = FriendsSerializer

   def get_queryset(self):
        
        queryset = CustomUser.objects.all()
        username_startswith = self.request.query_params.get('query', None)

        # If the 'query' parameter is provided, filter users by the first 3 characters of the username
        if username_startswith is not None:
            if not isinstance(username_startswith, str):
                raise ValidationError('Query parameter must be a string.')
            # Limit the filter to the first 3 characters
            username_startswith = username_startswith[:3]
            queryset = queryset.filter(username__startswith=username_startswith)

        # Return the filtered queryset
        return queryset
   

# ADD FRIENDS TO USER
class AddFriendsView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, *args, **kwargs):
        serializer = CustomfriendsSerializer(data=request.data, partial=True)
        if serializer.is_valid():
            user = request.user
            friends_ids = serializer.validated_data.get('friends', [])

            # Ajoute les amis
            for friend_id in friends_ids:
                try:
                    friend = CustomUser.objects.get(id=friend_id)
                    if user != friend:
                        user.add_friend(friend)
                except CustomUser.DoesNotExist:
                    return Response({"error": f"User with ID {friend_id} does not exist."}, status=status.HTTP_404_NOT_FOUND)

            return Response({"message": "Friends added successfully."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# REMOVE FRIENDS FROM USER 
class RemoveFriendsView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, *args, **kwargs):
        serializer = CustomfriendsSerializer(data=request.data, partial=True)
        if serializer.is_valid():
            user = request.user
            friends_ids = serializer.validated_data.get('friends', [])

            # Retire les amis
            for friend_id in friends_ids:
                try:
                    friend = CustomUser.objects.get(id=friend_id)
                    if user != friend:
                        user.remove_friend(friend)
                except CustomUser.DoesNotExist:
                    return Response({"error": f"User with ID {friend_id} does not exist."}, status=status.HTTP_404_NOT_FOUND)

            return Response({"message": "Friends removed successfully."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)








## REGISTER  LOGIN AND LOGOUT


class RegisterView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            if CustomUser.objects.filter(username=serializer.validated_data['username']).exists():
                return Response({'message': "Cet utilisateur existe déjà. Veuillez choisir un autre nom d'utilisateur ou vous connecter s'il s'agit du vôtre."}, status=status.HTTP_400_BAD_REQUEST)
            if CustomUser.objects.filter(email=serializer.validated_data['email']).exists():
                return Response({'message': "Email déjà enregistré. Veuillez vous rendre sur SE CONNECTER"}, status=status.HTTP_400_BAD_REQUEST)

            user = serializer.save()
            login(request, user)  # Connecte automatiquement l'utilisateur après l'enregistrement

            return Response({'message': "Vous êtes bien enregistré et connecté."}, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class LoginView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        user_data = CustomUserMinimalSerializer(user).data

        if user is not None:
            login(request, user)
            return Response({'message': 'Login successful', 'user': user_data}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


class LogoutView(APIView):
    def post(self, request):
        logout(request)
        return Response({'message': 'Logged out successfully'}, status=status.HTTP_200_OK)
    
    



## MESSAGE
# CREATE MESSAGE
class MessagesView(generics.CreateAPIView):
    queryset = Messages.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]
    print("1")

    def post(self, request, *args, **kwargs):
        print("1")
        print("Request received at MessagesView POST method")
        print("Request Headers:", request.headers)
        print("Request Cookies:", request.COOKIES)
        print("CSRF Token in Request Headers:", request.META.get('HTTP_X_CSRFTOKEN'))
        print("CSRF Token Expected:", get_token(request))
        
        return self.create(request, *args, **kwargs)

    def perform_create(self, serializer):
        print("Inside perform_create method")
        print("Current User:", self.request.user)
        print("Request Data:", self.request.data)
        serializer.save(auteur=self.request.user)

#  GET MESSAGE BY USER
class MessagesListView(generics.ListAPIView):
    queryset = Messages.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Messages.objects.filter(auteur=user).order_by('timestamp')

#GET MESSAGES FROM FRIENDS
class FriendsMessagesView(generics.ListAPIView):
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        friends = user.friends.all()
        return Messages.objects.filter(auteur__in=friends)
    
# CREATE LIKES BY MESSAGE ID 
class LikeMessageAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, message_id):
        try:
            message = Messages.objects.get(id=message_id)
            action = request.data.get('action')
            user = request.user

            if action == 'like':
                if user not in message.likes.all():
                    message.likes.add(user)
                    message.save()
                else:
                    return Response({"error": "Vous avez déjà liké ce message."}, status=status.HTTP_400_BAD_REQUEST)
            elif action == 'unlike':
                if user in message.likes.all():
                    message.likes.remove(user)
                    message.save()
                else:
                    return Response({"error": "Vous n'avez pas encore liké ce message."}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({"error": "Action non valide."}, status=status.HTTP_400_BAD_REQUEST)

            # Renvoyer la représentation du message mise à jour
            serializer = MessageSerializer(message)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Messages.DoesNotExist:
            return Response({"error": "Message non trouvé."}, status=status.HTTP_404_NOT_FOUND)


# GET LIKES BY MESSAGE ID
class MessageLikesCountAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, message_id):
        try:
            # Récupérer le message par son ID
            message = get_object_or_404(Messages, id=message_id)
            
            # Récupérer le nombre de likes pour ce message
            likes_count = message.likes.count()

            # Retourner la réponse avec le nombre de likes
            return Response({"likes": likes_count}, status=status.HTTP_200_OK)

        except Messages.DoesNotExist:
            return Response({"error": "Message non trouvé."}, status=status.HTTP_404_NOT_FOUND)
        

# GET COMMENTS BY MESSAGE ID
class CommentslinkmessageAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, message_id):
        try:
            # Récupérer le message par son ID
            message = get_object_or_404(Messages, id=message_id)

            # Récupérer les commentaires associés à ce message
            comments = message.comments.all()

            # Sérialiser les commentaires
            serializer = CommentsSerializer(comments, many=True)

            # Retourner la réponse avec les commentaires sérialisés
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Messages.DoesNotExist:
            return Response({"error": "Message non trouvé."}, status=status.HTTP_404_NOT_FOUND)


 # PROFILE
# GET ALL PROFILES PICTURES
class ProfilePictureAllView(APIView):

  def get(self, request):

        user_id = request.user.id  # Récupère l'ID de l'utilisateur actuel
        print("????????????????????????????", user_id)
        # Filtrer les profils pour exclure ceux où user_id est dans les likes
        profiles = Profile.objects.exclude(likes__id=user_id)
        # Sérialiser les profils restants
        serializer = ProfileSerializer3(profiles, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


# CREATE PROFILE PICTURE
class ProfilePhotoUploadView(generics.UpdateAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser,)

    
    def get_object(self):
        return self.request.user.profile

    def post(self, request, *args, **kwargs):
        print(f"User: {request.user}")  # Imprime l'utilisateur actuel
        print(f"User ID: {request.user.id}")  # Imprime l'ID de l'utilisateur actuel
        print(f"User Profile: {self.get_object()}")  # Imprime le profil de l'utilisateur actuel

        profile = self.get_object()
        profile.profile_picture = request.FILES.get('profile_picture')  # Récupère le fichier envoyé via 'profile_picture'
        profile.save()
        serializer = self.serializer_class(profile)
        return Response(serializer.data)
    

    def put(self, request, *args, **kwargs):
        profile = self.get_object()
        profile.profile_picture = request.FILES.get('profile_picture')
        profile.save()
        serializer = self.serializer_class(profile)
        return Response(serializer.data)



class LikeProfileViewtest(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        print(f"Authenticated User: {request.user}")  # Vérifie l'utilisateur authentifié

        # ID de l'utilisateur cible, dont le profil sera liké
        target_user_id = request.data.get('user_id')  # Extraction de l'ID du corps de la requête
        print(f"Target User ID: {target_user_id}")

        if not target_user_id:
            return Response({"detail": "User ID is required."}, status=status.HTTP_400_BAD_REQUEST)
        
        # Récupérer le profil de l'utilisateur cible
        target_profile = get_object_or_404(Profile, user__id=target_user_id)
        
        # Récupérer le profil de l'utilisateur actuel
        current_user = request.user
        try:
            current_profile = get_object_or_404(Profile, user=current_user)
        except Profile.DoesNotExist:
            return Response({"detail": "Current user's profile does not exist."}, status=status.HTTP_404_NOT_FOUND)
        
        # Vérifier si l'utilisateur a déjà liké ce profil
        if target_profile.user in current_profile.likes.all():
            return Response({"detail": "Vous avez déjà liké ce profil."}, status=status.HTTP_400_BAD_REQUEST)
        
        # Ajouter l'utilisateur cible aux likes du profil de l'utilisateur actuel
        current_profile.likes.add(target_profile.user)
        
        # Sérialiser et retourner le profil mis à jour
        serializer = ProfileSerializer3(current_profile)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def get(self, request, *args, **kwargs):
        profile_id = kwargs.get('profile_id')
        if not profile_id:
            return Response({"detail": "Profile ID is required."}, status=status.HTTP_400_BAD_REQUEST)

        profile = get_object_or_404(Profile, id=profile_id)
        serializer = ProfileSerializer3(profile)
        return Response(serializer.data)
    
    
class LikesProfileAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, profile_id, *args, **kwargs):
        # Récupérer le profil en utilisant l'ID passé en paramètre
        profile = get_object_or_404(Profile, id=profile_id)

        # Vérifier si l'utilisateur a déjà liké ce profil
        if profile.likes.filter(id=request.user.id).exists():
            return Response({"detail": "Vous avez déjà liké ce profil."}, status=status.HTTP_400_BAD_REQUEST)

        # Ajouter l'utilisateur à la liste des likes
        profile.likes.add(request.user)
        
        # Sérialiser et retourner le profil mis à jour
        serializer = ProfileSerializer3(profile)
        return Response(serializer.data, status=status.HTTP_200_OK)

# GET PHOTOPROFILE BY USERNAME
class ProfileByUsernameView(generics.GenericAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        # Récupérer le paramètre de requête 'username'
        username = request.query_params.get('username', None)
        if not username:
            return Response({"detail": "Username parameter is required."}, status=400)

        # Récupérer l'utilisateur en fonction du nom d'utilisateur
        try:
            user = CustomUser.objects.get(username=username)
            profile = user.profile
        except CustomUser.DoesNotExist:
            raise NotFound("User not found.")

        # Sérialiser et retourner les données du profil
        serializer = self.serializer_class(profile)
        return Response(serializer.data)






## PHOTOS AND VIDEOS 
# CREATE PSEUDO PRIVATE PHOTOS        
class PhotoUploadView(APIView):
    serializer_class = PhotoSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser,)

    def get(self, request, *args, **kwargs):
        # Récupère toutes les photos de l'utilisateur connecté
        photos = Photos.objects.filter(owner=request.user)
        serializer = self.serializer_class(photos, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        print(f"User: {request.user}")  # Imprime l'utilisateur actuel
        print(f"User ID: {request.user.id}")  # Imprime l'ID de l'utilisateur actuel
        
        # Appelle perform_create pour sauvegarder la nouvelle photo
        return self.create(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user, is_published=False)

# CREATE PHOTO NEWS FEED
class PhotoUploadfilView(APIView):
    serializer_class = PhotoSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser,)

    def get(self, request, *args, **kwargs):
        # Récupère toutes les photos de l'utilisateur connecté
        photos = Photos.objects.filter(owner=request.user)
        serializer = self.serializer_class(photos, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        print(f"User: {request.user}")  # Imprime l'utilisateur actuel
        print(f"User ID: {request.user.id}")  # Imprime l'ID de l'utilisateur actuel
        
        # Appelle perform_create pour sauvegarder la nouvelle photo
        return self.create(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user, is_published=True)

    
# GET ALL PHOTOS
class PhotosAll(generics.ListAPIView):
    queryset = Photos.objects.all()
    serializer_class = PhotoSerializer1
    permission_classes = [IsAuthenticated]


# GET LIKES BY PHOTO ID 
class PhotoLikesCountTestAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, photo_id):
        try:
            # Récupérer le message par son ID
            photo = get_object_or_404(Photos, id=photo_id)
            
            # Récupérer le nombre de likes pour ce message
            likes = photo.likes.count()

            # Retourner la réponse avec le nombre de likes
            return Response({"likes": likes}, status=status.HTTP_200_OK)

        except Photos.DoesNotExist:
            return Response({"error": "Message non trouvé."}, status=status.HTTP_404_NOT_FOUND)


class PhotosLikesCountAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, photo_id):
        try:
            # Récupérer le message par son ID
            photo = get_object_or_404(Photos, id=photo_id)
            
            # Récupérer le nombre de likes pour ce message
            likes = photo.likes.count()

            # Retourner la réponse avec le nombre de likes
            return Response({"likes": likes}, status=status.HTTP_200_OK)

        except Photos.DoesNotExist:
            return Response({"error": "Message non trouvé."}, status=status.HTTP_404_NOT_FOUND)

# CREATE LIKES BY PHOTO ID
class LikePhotosAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, photo_id):
        try:
            photos = Photos.objects.get(id=photo_id)
            action = request.data.get('action')
            user = request.user

            if action == 'like':
                if user not in photos.likes.all():
                    photos.likes.add(user)
                    photos.save()
                else:
                    return Response({"error": "Vous avez déjà liké cette photo."}, status=status.HTTP_400_BAD_REQUEST)
            elif action == 'unlike':
                if user in photos.likes.all():
                    photos.likes.remove(user)
                    photos.save()
                else:
                    return Response({"error": "Vous n'avez pas encore liké cette photo."}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({"error": "Action non valide."}, status=status.HTTP_400_BAD_REQUEST)

            # Renvoyer la représentation du message mise à jour
            serializer = PhotoSerializer(photos)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Photos.DoesNotExist:
            return Response({"error": "Photo non trouvé."}, status=status.HTTP_404_NOT_FOUND)        


# GET PHOTOS BY USERNAME
class PhotosByUsernameView(generics.GenericAPIView):
    serializer_class = PhotoSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        # Récupérer le paramètre de requête 'username'
        username = request.query_params.get('username', None)
        if not username:
            return Response({"detail": "Username parameter is required."}, status=400)

        # Récupérer l'utilisateur en fonction du nom d'utilisateur
        try:
            user = CustomUser.objects.get(username=username)
        except CustomUser.DoesNotExist:
            raise NotFound("User not found.")
        
        photos = Photos.objects.filter(owner=user)

        # Sérialiser et retourner les données du profil
        serializer = self.serializer_class(photos,many = True)
        return Response(serializer.data)


#GET  PHOTOS FROM FRIENDS
class FriendsPhotosView(generics.ListAPIView):
    serializer_class = PhotoSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        friends = user.friends.all()
        return Photos.objects.filter(owner__in=friends)


# GET ALL VIDEOS
class VideosAll(generics.ListAPIView):
    queryset = Videos.objects.all()
    serializer_class = VideosSerializer1
    permission_classes = [IsAuthenticated]


# CREATE VIDEOS FEEDS
class VideoUploadfilView(APIView):
    serializer_class = VideosSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser,)

    def get(self, request, *args, **kwargs):
        # Récupère toutes les photos de l'utilisateur connecté
        videos = Videos.objects.filter(owner=request.user)
        serializer = self.serializer_class(videos, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        print(f"User: {request.user}")  # Imprime l'utilisateur actuel
        print(f"User ID: {request.user.id}")  # Imprime l'ID de l'utilisateur actuel
        
        # Appelle perform_create pour sauvegarder la nouvelle photo
        return self.create(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user, is_published=True)#  ,is_published=True"""

# CREATE PSEUDO PRIVATE VIDEOS
class VideoUploadView(APIView):
    serializer_class = VideosSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser,)

    def get(self, request, *args, **kwargs):
        # Récupère toutes les photos de l'utilisateur connecté
        videos = Videos.objects.filter(owner=request.user)
        serializer = self.serializer_class(videos, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        print(f"User: {request.user}")  # Imprime l'utilisateur actuel
        print(f"User ID: {request.user.id}")  # Imprime l'ID de l'utilisateur actuel
        
        # Appelle perform_create pour sauvegarder la nouvelle photo
        return self.create(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)



# GET LIKES BY VIDEO
class VideoLikesCountAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, video_id):
        try:
            # Récupérer le message par son ID
            video = get_object_or_404(Videos, id=video_id)
            
            # Récupérer le nombre de likes pour ce message
            likes_count = video.likes.count()

            # Retourner la réponse avec le nombre de likes
            return Response({"likes": likes_count}, status=status.HTTP_200_OK)

        except Videos.DoesNotExist:
            return Response({"error": "Video non trouvé."}, status=status.HTTP_404_NOT_FOUND) 
        
# GET LIKES BY VIDEO MEME QU AU DESSUS 
class VideoLikesCountTestAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, video_id):
        try:
            # Récupérer le message par son ID
            video = get_object_or_404(Videos, id=video_id)
            
            # Récupérer le nombre de likes pour ce message
            likes_count = video.likes.count()
            print(likes_count)

            # Retourner la réponse avec le nombre de likes
            return Response({"likes": likes_count}, status=status.HTTP_200_OK)

        except Videos.DoesNotExist:
            return Response({"error": "Video non trouvé."}, status=status.HTTP_404_NOT_FOUND) 


# GET VIDEOS BY USERNAME
class VideosByUsernameView(generics.GenericAPIView):
    serializer_class = VideosSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        # Récupérer le paramètre de requête 'username'
        username = request.query_params.get('username', None)
        if not username:
            return Response({"detail": "Username parameter is required."}, status=400)

        # Récupérer l'utilisateur en fonction du nom d'utilisateur
        try:
            user = CustomUser.objects.get(username=username)
        except CustomUser.DoesNotExist:
            raise NotFound("User not found.")
        
        videos = Videos.objects.filter(owner=user)

        # Sérialiser et retourner les données du profil
        serializer = self.serializer_class(videos,many = True)
        return Response(serializer.data)
    

#GET VIDEOS FROM FRIENDS
class FriendsVideosView(generics.ListAPIView):
    serializer_class = VideosSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        friends = user.friends.all()
        return Videos.objects.filter(owner__in=friends)
    

# CREATE LIKES VIDEO

class LikeVideosAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, video_id):
        try:
            video = Videos.objects.get(id=video_id)
            action = request.data.get('action')
            user = request.user

            if action == 'like':
                if user not in video.likes.all():
                    video.likes.add(user)
                    video.save()
                else:
                    return Response({"error": "Vous avez déjà liké cette video."}, status=status.HTTP_400_BAD_REQUEST)
            elif action == 'unlike':
                if user in video.likes.all():
                    video.likes.remove(user)
                    video.save()
                else:
                    return Response({"error": "Vous n'avez pas encore liké cette video."}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({"error": "Action non valide."}, status=status.HTTP_400_BAD_REQUEST)

            # Renvoyer la représentation du message mise à jour
            serializer = VideosSerializer(video)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Videos.DoesNotExist:
            return Response({"error": "Video non trouvé."}, status=status.HTTP_404_NOT_FOUND)
        






    


## COMMENTS
# GET ALL COMMENTS
class CommentsAll(generics.ListAPIView):
    queryset = Comments.objects.all()
    serializer_class = CommentsAllSerializer
    permission_classes = [IsAuthenticated]
# CREATE COMMENTS
class CommentsView(generics.CreateAPIView):
    serializer_class = CommentsSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save(auteur=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# CREATE COMMENTS BY PHOTO ID
class CommentsViewidphoto(generics.CreateAPIView):
        
        serializer_class = CommentsphotosSerializer
        def post(self, request, *args, **kwargs):
          serializer = self.get_serializer(data=request.data)
          if serializer.is_valid():
            photo_id = serializer.validated_data.get('photo_id')
            content = serializer.validated_data.get('content')
            
            try:
                photo = Photos.objects.get(id=photo_id)
            except Photos.DoesNotExist:
                return Response({'error': 'Photo not found.'}, status=status.HTTP_404_NOT_FOUND)

            # Créez le commentaire et associez-le à la photo
            comment = Comments.objects.create(
                content=content,
                photo=photo,
                auteur=request.user
            )

            response_serializer = self.get_serializer(comment)
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)
        
          return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

# CREATE COMMENTS BY VIDEO ID       
class CommentsViewidvideo(generics.CreateAPIView):
        serializer_class = CommentsvideosSerializer

        def post(self, request, *args, **kwargs):
          serializer = self.get_serializer(data=request.data)
          if serializer.is_valid():
            video_id = serializer.validated_data.get('video_id')
            content = serializer.validated_data.get('content')
            
            try:
                video = Videos.objects.get(id=video_id)
            except Videos.DoesNotExist:
                return Response({'error': 'Video not found.'}, status=status.HTTP_404_NOT_FOUND)

            # Créez le commentaire et associez-le à la photo
            comment = Comments.objects.create(
                content=content,
                video=video,
                auteur=request.user
            )

            response_serializer = self.get_serializer(comment)
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)
        
          return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# GET COMMENTS BY MESSAGE
class CommentsByMessage(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        message_id = request.query_params.get('message')
        if message_id is not None:
            comments = Comments.objects.filter(message=message_id)
        else:
            comments = Comments.objects.all()

        serializer = Comments_By_Message_Serializer(comments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

# GET COMMENTS BY PHOTO   
class CommentsByPhoto(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        photo_id = request.query_params.get('photo')
        print("id photo",photo_id)
        if photo_id is not None:
            photos = Comments.objects.filter(photo=photo_id)
        else:
            photos = Comments.objects.all()

        serializer = Comments_By_Photo_Serializer(photos, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

# GET COMMENTS BY VIDEO
class CommentsByVideo(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        video_id = request.query_params.get('video')
        print("id ideo",video_id)
        if video_id is not None:
            videos = Comments.objects.filter(video=video_id)
        else:
            videos = Comments.objects.all()

        serializer = Comments_By_Video_Serializer(videos, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    



# GET ALL COMMENTS
class CommentsListView(generics.ListAPIView):
    queryset = Comments.objects.all()
    serializer_class = CommentsSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Comments.objects.filter(auteur=user).order_by('-timestamp')
                

#GET COMMENTS LIKE BY MESSAGEID      
class CommentsCountAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, message_id):
        try:
            # Récupérer le message par son ID
            comments = get_object_or_404(Comments, id=message_id)
            
            # Récupérer le nombre de likes pour ce message
            comments_count = comments.likes.count()

            # Retourner la réponse avec le nombre de likes
            return Response({"comments_count": comments_count}, status=status.HTTP_200_OK)

        except Comments.DoesNotExist:
            return Response({"error": "Message non trouvé."}, status=status.HTTP_404_NOT_FOUND)

# CREATE LIKES COMMENTS
class LikeCommentsAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, comments_id):
        try:
            comments = Comments.objects.get(id=comments_id)
            action = request.data.get('action')
            user = request.user

            if action == 'like':
                if user not in comments.likes.all():
                    comments.likes.add(user)
                    comments.save()
                else:
                    return Response({"error": "Vous avez déjà liké ce message."}, status=status.HTTP_400_BAD_REQUEST)
            elif action == 'unlike':
                if user in comments.likes.all():
                    comments.likes.remove(user)
                    comments.save()
                else:
                    return Response({"error": "Vous n'avez pas encore liké ce message."}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({"error": "Action non valide."}, status=status.HTTP_400_BAD_REQUEST)

            # Renvoyer la représentation du message mise à jour
            serializer = CommentsSerializer(comments)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Comments.DoesNotExist:
            return Response({"error": "Message non trouvé."}, status=status.HTTP_404_NOT_FOUND)


# demandes d'amitié
# ASK FOR FRIENDSHIP
class SendFriendRequestView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        to_user_id = request.data.get('to_user')
        if not to_user_id:
            return Response({"error": "to_user is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            to_user = CustomUser.objects.get(id=to_user_id)
            print(to_user_id)
        except CustomUser.DoesNotExist:
            return Response({"error": "User does not exist."}, status=status.HTTP_404_NOT_FOUND)

        if request.user == to_user:
            return Response({"message": "Tu es déjà ami avec toi-même non?"}, status=status.HTTP_400_BAD_REQUEST)

        friend_request, created = FriendRequest.objects.get_or_create(from_user=request.user, to_user=to_user)
        if created:
            return Response({"message": "Friend request sent."}, status=status.HTTP_200_OK)
        else:
            return Response({"message": "Demande d'amitié déjà envoyée."}, status=status.HTTP_400_BAD_REQUEST)
        
        
# RESPOND TO FRIENDSHIP
class RespondToFriendRequestView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        request_id = request.data.get('request_id')
        action = request.data.get('action')

        if not request_id or not action:
            return Response({"error": "request_id and action are required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            friend_request = FriendRequest.objects.get(id=request_id, to_user=request.user)
        except FriendRequest.DoesNotExist:
            return Response({"error": "Friend request does not exist."}, status=status.HTTP_404_NOT_FOUND)

        if action == 'accept':
            friend_request.status = 'accepted'
            friend_request.save()
            request.user.friends.add(friend_request.from_user)
            friend_request.from_user.friends.add(request.user)
            return Response({"message": "Friend request accepted."}, status=status.HTTP_200_OK)
        elif action == 'reject':
            friend_request.status = 'rejected'
            friend_request.save()
            return Response({"message": "Friend request rejected."}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Invalid action."}, status=status.HTTP_400_BAD_REQUEST)


# CHECK FRIENSHIP
class CheckFriendRequestStatusView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, to_user_id):
        user = request.user
        to_user = get_object_or_404(CustomUser, id=to_user_id)

        try:
            friend_request = FriendRequest.objects.get(from_user=user, to_user=to_user)
            return Response({"status": friend_request.status, "request_id": friend_request.id})
        except FriendRequest.DoesNotExist:
            pass

        try:
            friend_request = FriendRequest.objects.get(from_user=to_user, to_user=user)
            return Response({"status": "received", "request_id": friend_request.id})
        except FriendRequest.DoesNotExist:
            return Response({"status": ""}, status=status.HTTP_200_OK)


class FriendrequestAll(generics.ListAPIView):

    queryset = FriendRequest.objects.all()
    serializer_class = FriendRequestSerializerAll
    permission_classes = [IsAuthenticated]
        
# get alls generics   
class profilebisview(generics.ListAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer1


class photobisview(generics.ListAPIView):
    queryset = Photos.objects.all()
    serializer_class = PhotoSerializer1

class videobisview(generics.ListAPIView):
    queryset = Videos.objects.all()
    serializer_class = VideosSerializer1


# chat messages

# CREATE LIKES BY MESSAGE ID 

class MessagesChatCreateView(APIView):
    """
    Vue pour créer un message de chat.
    """

    def post(self, request, *args, **kwargs):
        sender_id = request.data.get('sender')
        receiver_id = request.data.get('receiver')
        content = request.data.get('content')

        try:
            sender = CustomUser.objects.get(id=sender_id)
            receiver = CustomUser.objects.get(id=receiver_id)
        except CustomUser.DoesNotExist:
            return Response({"error": "Sender or receiver not found."}, status=status.HTTP_404_NOT_FOUND)

        message = MessagesChat(sender=sender, receiver=receiver, content=content)
        message.save()

        serializer = ChatSerializer(message)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    

class MessagesChatListView(generics.ListAPIView):
    """
    Vue pour récupérer les messages entre deux utilisateurs.
    """
    serializer_class = ChatSerializer

    def get_queryset(self):
        sender_id = self.request.query_params.get('sender')
        receiver_id = self.request.query_params.get('receiver')

        if not sender_id or not receiver_id:
            return ChatSerializer.objects.none()

        queryset = ChatSerializer.objects.filter(sender_id=sender_id, receiver_id=receiver_id)
        return queryset
