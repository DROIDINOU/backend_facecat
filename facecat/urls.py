
from django.urls import path
from cat.views import (ChatCreateView,RegisterView, LoginView,MessagesView,MessagesListView, get_csrf_token, 
                       LikeMessageAPIView,MessageLikesCountAPIView, CommentsCountAPIView,CommentsListView,CommentsView,
                       LikeCommentsAPIView,CommentslinkmessageAPIView,CommentsAll,CommentsByMessage, searchUserFriend,
                       ProfilePhotoUploadView, AddFriendsView,RemoveFriendsView,UserFriendsView)

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from django.conf import settings
from django.conf.urls.static import static

router = routers.DefaultRouter()

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/add-cat/', ChatCreateView.as_view(), name='add-cat'),
    path('api/register/', RegisterView.as_view(), name='register'),    
    path('api/log/', LoginView.as_view(), name='log'),
    path('csrf/', get_csrf_token, name='get-csrf-token'),
    path('comments/try/', CommentsView.as_view(), name='commentscreation'),
    path('messages/create/', MessagesView.as_view(), name='message-create'),
    path('messages/creates/', MessagesListView.as_view(), name='messages-creates'),
    path('messages/getlikes/<int:message_id>/',MessageLikesCountAPIView.as_view() , name='messages-get'),
    path('messages/createlikes/<int:message_id>/', LikeMessageAPIView.as_view(), name='messages-creates'),
    path('comments/obtain/', CommentsListView.as_view(), name='comments-creates'),
    path('comments/getlikes/<int:message_id>/',CommentsCountAPIView.as_view() , name='commentslike-get'),
    path('comments/createlikes/<int:message_id>/', LikeCommentsAPIView.as_view(), name='commentslike-create'),
    path('messages/comments/link/<int:message_id>/', CommentslinkmessageAPIView.as_view(), name='comment-links'),
    path('comments/all/', CommentsAll.as_view(), name='comments-creates'),
    path('comments/commentsbymessage/link/<int:message>/', CommentsByMessage.as_view(), name='comment-by-message'),
    path('search/friends/', searchUserFriend.as_view(), name='search-user'),
    path('getfriends/', UserFriendsView.as_view(), name='getfriends'),
    path('addfriends/', AddFriendsView.as_view(), name='addfriends'),
    path('removefriends/', RemoveFriendsView.as_view(), name='removefriends'),
    path('api/profile/photo/', ProfilePhotoUploadView.as_view(), name='profile-photo-upload'),

  

]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
