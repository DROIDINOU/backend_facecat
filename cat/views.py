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
from .models import Cats, CustomUser,Messages,Comments,ListeChats,Points,Fun_Categories,FriendRequest, Profile
from .serializers import CatsSerializer, UserSerializer,MessageSerializer,CommentsSerializer,CommentsAllSerializer, Comments_By_Message_Serializer, FriendsSerializer, ProfileSerializer,ListeChatsSerializer,PointsSerializer,FunCategoriesSerializer, CustomfriendsSerializer,FriendRequestSerializer,CustomUserMinimalSerializer,FriendRequestSerializerAll, ProfileSerializer1
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


class MessagesListView(generics.ListAPIView):
    queryset = Messages.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Messages.objects.filter(auteur=user).order_by('-timestamp')


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
    
# vue pour les chats et points 
    
class profilebisview(generics.ListAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer1
    
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

