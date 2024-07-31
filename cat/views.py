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
from .models import Cats, CustomUser,Messages,Comments,ListeChats,Points,Fun_Categories,FriendRequest, Profile,Photos, Videos
from .serializers import CatsSerializer, UserSerializer,MessageSerializer,CommentsSerializer,CommentsAllSerializer, Comments_By_Message_Serializer, FriendsSerializer,PhotoSerializer1, ProfileSerializer,ListeChatsSerializer,PointsSerializer,FunCategoriesSerializer, CustomfriendsSerializer,FriendRequestSerializer,CustomUserMinimalSerializer,FriendRequestSerializerAll, ProfileSerializer1, PhotoSerializer, VideosSerializer, VideosSerializer1, CommentsphotosSerializer, Comments_By_Photo_Serializer
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.contrib.auth import authenticate, login, logout
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from django.http import JsonResponse
from django.middleware.csrf import get_token
from django.shortcuts import get_object_or_404
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.exceptions import NotFound
from rest_framework.views import APIView





class ChatCreateView(APIView):
    def post(self, request):
        super_admin_username = request.data.get('maitre')
        print(super_admin_username)
        # Rechercher le super administrateur par nom d'utilisateur
        try:
            print("yen a marrrrrrrrrrrrrrrrrre")
            super_admin = CustomUser.objects.get(username=super_admin_username, is_superuser=True)
        except CustomUser.DoesNotExist:
            return Response({'error': 'Super admin not found'}, status=400)
        print("eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee")

        # Ajouter l'utilisateur actuel au chat (ou créer le chat)
        request.data['maitre'] = super_admin.id
        print(request.data['maitre'])
        serializer = CatsSerializer(data=request.data)
        print(request.data)
        if serializer.is_valid():
            serializer.save()
            print("eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee", serializer.data)

            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class RegisterView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            if CustomUser.objects.filter(username=serializer.validated_data['username']).exists():
                return Response({'error': "Cet utilisateur existe déjà. Veuillez choisir un autre nom d'utilisateur ou vous connecter s'il s'agit du vôtre."}, status=status.HTTP_400_BAD_REQUEST)
            if CustomUser.objects.filter(email=serializer.validated_data['email']).exists():
                return Response({'error': "Email déjà enregistré. Veuillez vous rendre sur SE CONNECTER"}, status=status.HTTP_400_BAD_REQUEST)

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


class RegisterView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Registration successful'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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


class CommentsView(generics.CreateAPIView):
    serializer_class = CommentsSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save(auteur=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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
class MessagesListView(generics.ListAPIView):
    queryset = Messages.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Messages.objects.filter(auteur=user).order_by('-timestamp')
    
"""class FeedPhotoListView(generics.ListAPIView):
    queryset = FeedPhoto.objects.all()
    serializer_class = FeedPhotoSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return FeedPhoto.objects.filter(owner=user).order_by('-timestamp')
    
"""



class CommentsListView(generics.ListAPIView):
    queryset = Comments.objects.all()
    serializer_class = CommentsSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Comments.objects.filter(auteur=user).order_by('-timestamp')
    

class GetCsrfToken(APIView):
    @method_decorator(ensure_csrf_cookie)
    def get(self, request):
        csrf_token = get_token(request)
        return JsonResponse({'csrfToken': csrf_token})

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
        


class MessageLikesCountAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, message_id):
        try:
            # Récupérer le message par son ID
            message = get_object_or_404(Messages, id=message_id)
            
            # Récupérer le nombre de likes pour ce message
            likes_count = message.likes.count()

            # Retourner la réponse avec le nombre de likes
            return Response({"likes_count": likes_count}, status=status.HTTP_200_OK)

        except Messages.DoesNotExist:
            return Response({"error": "Message non trouvé."}, status=status.HTTP_404_NOT_FOUND)
        
class PhotoLikesCountTestAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, photo_id):
        try:
            # Récupérer le message par son ID
            photo = get_object_or_404(Photos, id=photo_id)
            
            # Récupérer le nombre de likes pour ce message
            likes_count = photo.likes.count()

            # Retourner la réponse avec le nombre de likes
            return Response({"likes_count": likes_count}, status=status.HTTP_200_OK)

        except Photos.DoesNotExist:
            return Response({"error": "Message non trouvé."}, status=status.HTTP_404_NOT_FOUND)



class PhotosLikesCountAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, photo_id):
        try:
            # Récupérer le message par son ID
            photo = get_object_or_404(Photos, id=photo_id)
            
            # Récupérer le nombre de likes pour ce message
            likes_count = photo.likes.count()

            # Retourner la réponse avec le nombre de likes
            return Response({"likes_count": likes_count}, status=status.HTTP_200_OK)

        except Photos.DoesNotExist:
            return Response({"error": "Message non trouvé."}, status=status.HTTP_404_NOT_FOUND)


class LikePhotosAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, photo_id):
        try:
            print('Received photo_id:', photo_id)
            print('Request Method:', request.method)
            print('Photo ID:', photo_id)
            photo = Photos.objects.get(id=photo_id)
            print('Photo Retrieved:', photo)
            action = request.data.get('action')
            print('Action:', action)
            user = request.user
            print('User:', user)

            if action == 'like':
                if user not in photo.likes.all():
                    photo.likes.add(user)
                    photo.save()
                    print('User liked the photo')
                else:
                    print('User already liked the photo')
                    return Response({"error": "Vous avez déjà liké cette photo."}, status=status.HTTP_400_BAD_REQUEST)
            elif action == 'unlike':
                if user in photo.likes.all():
                    photo.likes.remove(user)
                    photo.save()
                    print('User unliked the photo')
                else:
                    print('User has not liked the photo yet')
                    return Response({"error": "Vous n'avez pas encore liké cette photo."}, status=status.HTTP_400_BAD_REQUEST)
            else:
                print('Invalid action')
                return Response({"error": "Action non valide."}, status=status.HTTP_400_BAD_REQUEST)

            # Renvoyer la représentation de la photo mise à jour
            serializer = PhotoSerializer1(photo)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Photos.DoesNotExist:
            print('Photo does not exist')
            return Response({"error": "Photo non trouvée."}, status=status.HTTP_404_NOT_FOUND)
        


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


class PhotoslinkmessageAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, photo_id):
        try:
            # Récupérer le message par son ID
            photo = get_object_or_404(Photos, id=photo_id)

            # Récupérer les commentaires associés à ce message
            photos = photo.comments.all()

            # Sérialiser les commentaires
            serializer = PhotoSerializer(photos, many=True)

            # Retourner la réponse avec les commentaires sérialisés
            return Response(serializer.data, status=status.HTTP_200_OK)

        except photo.DoesNotExist:
            return Response({"error": "Photo non trouvé."}, status=status.HTTP_404_NOT_FOUND)
        



class VideoLikesCountAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, video_id):
        try:
            # Récupérer le message par son ID
            video = get_object_or_404(Videos, id=video_id)
            
            # Récupérer le nombre de likes pour ce message
            likes_count = video.likes.count()

            # Retourner la réponse avec le nombre de likes
            return Response({"videos_count": likes_count}, status=status.HTTP_200_OK)

        except Videos.DoesNotExist:
            return Response({"error": "Video non trouvé."}, status=status.HTTP_404_NOT_FOUND) 
        

# Commentaires

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


class CommentsphotoCountAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, photo_id):
        try:
            # Récupérer le message par son ID
            comments = get_object_or_404(Photos, id=photo_id)
            
            # Récupérer le nombre de likes pour ce message
            comments_count = comments.likes.count()

            # Retourner la réponse avec le nombre de likes
            return Response({"comments_count": comments_count}, status=status.HTTP_200_OK)

        except Comments.DoesNotExist:
            return Response({"error": "Message non trouvé."}, status=status.HTTP_404_NOT_FOUND)
               


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


class CommentslinkphotoAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, photo_id):
        try:
            # Récupérer le message par son ID
            message = get_object_or_404(Photos, id=photo_id)

            # Récupérer les commentaires associés à ce message
            comments = message.comments.all()

            # Sérialiser les commentaires
            serializer = CommentsphotosSerializer(comments, many=True)

            # Retourner la réponse avec les commentaires sérialisés
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Messages.DoesNotExist:
            return Response({"error": "Message non trouvé."}, status=status.HTTP_404_NOT_FOUND)
        
        



            
            
            
class VideoslinkmessageAPIView(APIView):
      permission_classes = [IsAuthenticated]

      def get(self, request, video_id):
        try:
            # Récupérer le message par son ID
            video = get_object_or_404(Videos, id=video_id)

            # Récupérer les commentaires associés à ce message
            videos = video.comments.all()

            # Sérialiser les commentaires
            serializer = VideosSerializer(videos, many=True)

            # Retourner la réponse avec les commentaires sérialisés
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Videos.DoesNotExist:
            return Response({"error": "Video non trouvé."}, status=status.HTTP_404_NOT_FOUND)


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

class PhotostestAPIView(APIView):
    def post(self, request, photo_id=None, format=None):
        try:
            photo = Photos.objects.get(id=photo_id)
            # Ajoutez votre logique de traitement des likes ici
            return Response({'status': 'like added'}, status=status.HTTP_200_OK)
        except Photos.DoesNotExist:
            return Response({'error': 'Photo not found'}, status=status.HTTP_404_NOT_FOUND)
        
class LikeVideosAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, videos_id):
        try:
            videos = Videos.objects.get(id=videos_id)
            action = request.data.get('action')
            user = request.user

            if action == 'like':
                if user not in videos.likes.all():
                    videos.likes.add(user)
                    videos.save()
                else:
                    return Response({"error": "Vous avez déjà liké cete video."}, status=status.HTTP_400_BAD_REQUEST)
            elif action == 'unlike':
                if user in videos.likes.all():
                    videos.likes.remove(user)
                    videos.save()
                else:
                    return Response({"error": "Vous n'avez pas encore liké cette video."}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({"error": "Action non valide."}, status=status.HTTP_400_BAD_REQUEST)

            # Renvoyer la représentation du message mise à jour
            serializer = VideosSerializer(videos)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Videos.DoesNotExist:
            return Response({"error": "Video non trouvé."}, status=status.HTTP_404_NOT_FOUND)
            


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
            
            

class CommentsAll(generics.ListAPIView):
    queryset = Comments.objects.all()
    serializer_class = CommentsAllSerializer
    permission_classes = [IsAuthenticated]


class PhotosAll(generics.ListAPIView):
    queryset = Photos.objects.all()
    serializer_class = PhotoSerializer1
    permission_classes = [IsAuthenticated]


class VideosAll(generics.ListAPIView):
    queryset = Videos.objects.all()
    serializer_class = VideosSerializer1
    permission_classes = [IsAuthenticated]

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
    

class searchUserFriend (generics.ListAPIView):

   serializer_class = FriendsSerializer

   def get_queryset(self):
        
        queryset = CustomUser.objects.all()
        username_startswith = self.request.query_params.get('query', None)
        if username_startswith is not None:
            queryset = queryset.filter(username__startswith=username_startswith[:3])
        return queryset

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
    
    def get(self, request, *args, **kwargs):
        profile = self.get_object()
        serializer = self.serializer_class(profile)
        return Response(serializer.data)


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
        serializer.save(owner=self.request.user, is_published=False)#  ,is_published=False


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
        serializer.save(owner=self.request.user, is_published=True)#  ,is_published=True"""




# vue pour les chats et points 

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


    
class profilebisview(generics.ListAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer1


class photobisview(generics.ListAPIView):
    queryset = Photos.objects.all()
    serializer_class = PhotoSerializer1

class videobisview(generics.ListAPIView):
    queryset = Videos.objects.all()
    serializer_class = VideosSerializer1
    
class ListeChatView(generics.ListAPIView):
    queryset = ListeChats.objects.all()
    serializer_class = ListeChatsSerializer

class FuncategoriesView(generics.RetrieveAPIView):
    queryset = Fun_Categories.objects.all()
    serializer_class = FunCategoriesSerializer


class PointsView(generics.RetrieveAPIView):
    queryset = Points.objects.all()
    serializer_class = PointsSerializer



class UserFriendsView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, *args, **kwargs):
        user = request.user  # Récupère l'utilisateur connecté
        serializer = CustomfriendsSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)



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
    



# demandes d'amitié
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
            return Response({"error": "You cannot send a friend request to yourself."}, status=status.HTTP_400_BAD_REQUEST)

        friend_request, created = FriendRequest.objects.get_or_create(from_user=request.user, to_user=to_user)
        if created:
            return Response({"message": "Friend request sent."}, status=status.HTTP_200_OK)
        else:
            return Response({"message": "Friend request already sent."}, status=status.HTTP_400_BAD_REQUEST)
        

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


class UserrequestAll(generics.ListAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserMinimalSerializer
    permission_classes = [IsAuthenticated]





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
    
class LogoutView(APIView):
    def post(self, request):
        logout(request)
        return Response({'message': 'Logged out successfully'}, status=status.HTTP_200_OK)
    
    
class FriendsListView(generics.ListAPIView):
    serializer_class = CustomUser
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return user.friends.all()
    



