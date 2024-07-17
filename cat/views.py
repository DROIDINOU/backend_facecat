# views.py

from rest_framework import status, generics,permissions
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Cats
from .serializers import CatsSerializer

from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Cats, CustomUser,Messages,Comments
from .serializers import CatsSerializer, UserSerializer,MessageSerializer,CommentsSerializer,CommentsAllSerializer, Comments_By_Message_Serializer, FriendsSerializer, ProfileSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.contrib.auth import authenticate, login, logout
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from django.http import JsonResponse
from django.middleware.csrf import get_token
from django.shortcuts import get_object_or_404


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
        if user is not None:
            login(request, user)
            return Response({'message': 'Login successful'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

class LogoutView(APIView):
    def post(self, request):
        logout(request)
        return Response({'message': 'Logout successful'}, status=status.HTTP_200_OK)

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
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(auteur=self.request.user)

class CommentsView(generics.CreateAPIView):
    serializer_class = CommentsSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save(auteur=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class MessagesListView(generics.ListAPIView):
    queryset = Messages.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Messages.objects.filter(auteur=user).order_by('-timestamp')

class CommentsListView(generics.ListAPIView):
    queryset = Comments.objects.all()
    serializer_class = CommentsSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Comments.objects.filter(auteur=user).order_by('-timestamp')
    
def get_csrf_token(request):
    return JsonResponse({'csrfToken': get_token(request)})

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



class LikeCommentsAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, comments_id):
        try:
            comments = Comments.objects.get(id=comments_id)
            action = request.data.get('action')
            user = request.user

            if action == 'comment':
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

        except Messages.DoesNotExist:
            return Response({"error": "Message non trouvé."}, status=status.HTTP_404_NOT_FOUND)

class CommentsAll(generics.ListAPIView):
    queryset = Comments.objects.all()
    serializer_class = CommentsAllSerializer
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
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        # Retourne le profil de l'utilisateur actuel
        return self.request.user.profile