
from django.urls import path
from cat.views import (RegisterView, LoginView,MessagesView,MessagesListView, 
                       LikeMessageAPIView,MessageLikesCountAPIView, CommentsCountAPIView,CommentsListView,CommentsView,
                       LikeCommentsAPIView,CommentslinkmessageAPIView,CommentsAll,CommentsByMessage, searchUserFriend,
                       ProfilePhotoUploadView, AddFriendsView,RemoveFriendsView,UserFriendsView,ProfileByUsernameView,
                       CheckFriendRequestStatusView,RespondToFriendRequestView,SendFriendRequestView,UserByUsernameView, 
                       UserrequestAll,GetCsrfToken,FriendsListView,LogoutView,profilebisview,PhotoUploadView, 
                       photobisview,PhotosByUsernameView, LikePhotosAPIView,PhotosAll, VideoLikesCountAPIView, LikeVideosAPIView, 
                       VideoUploadView, videobisview, VideosByUsernameView, CommentsByPhoto, PhotoUploadfilView,PhotosLikesCountAPIView, CommentsViewidphoto, PhotoLikesCountTestAPIView,FriendrequestAll, VideoUploadfilView,VideoLikesCountTestAPIView, CommentsByVideo, CommentsViewidvideo, 
                       FriendsMessagesView, FriendsPhotosView, FriendsVideosView, ProfilePictureAllView)
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views


router = routers.DefaultRouter()

urlpatterns = [
    path('admin/', admin.site.urls),
    path('photos/getlikes/<int:photo_id>/', PhotosLikesCountAPIView.as_view(), name='photos-get-likes'),
    path('friendrequest-all/', FriendrequestAll.as_view(), name='friendrequest-all'),
    path('api/register/', RegisterView.as_view(), name='register'),
    path('api/log/', LoginView.as_view(), name='log'),
    path('csrf/', GetCsrfToken.as_view(), name='get-csrf-token'),
    path('comments/try/', CommentsView.as_view(), name='commentscreation'),
    path('comments/trytry/', CommentsViewidphoto.as_view(), name='commentscreation-idphoto'),
    path('comments/trytrytry/', CommentsViewidvideo.as_view(), name='commentscreation-idvideo'),
    path('api/friends/messages/', FriendsMessagesView.as_view(), name='friends_messages'),
    path('api/friends/photos/', FriendsPhotosView.as_view(), name='friends_photos'),
    path('api/friends/videos/', FriendsVideosView.as_view(), name='friends_videos'),
    path('messages/create/', MessagesView.as_view(), name='message-create'),
    path('messages/creates/', MessagesListView.as_view(), name='messages-list-create'),
    path('messages/getlikes/<int:message_id>/', MessageLikesCountAPIView.as_view(), name='messages-get-likes'),
    path('photo/getlikestest/<int:photo_id>/', PhotoLikesCountTestAPIView.as_view(), name='messagess-get-likes'),
    path('video/getlikesvideostest/<int:video_id>/', VideoLikesCountTestAPIView.as_view(), name='messagesss-get-likes'),
    path('videos/getlikes/<int:video_id>/', VideoLikesCountAPIView.as_view(), name='videos-get-likes'),

    path('messages/createlikes/<int:message_id>/', LikeMessageAPIView.as_view(), name='messages-create-likes'),
    path('photos/createlikes/<int:photo_id>/', LikePhotosAPIView.as_view(), name='photos-create-likes'),
    path('comments/obtain/', CommentsListView.as_view(), name='comments-list'),
    path('comments/getlikes/<int:message_id>/', CommentsCountAPIView.as_view(), name='comments-get-likes'),
    path('comments/createlikes/<int:message_id>/', LikeCommentsAPIView.as_view(), name='comments-create-likes'),
    path('videos/createlikes/<int:video_id>/', LikeVideosAPIView.as_view(), name='videos-create-likes'),
    path('messages/comments/link/<int:message_id>/', CommentslinkmessageAPIView.as_view(), name='message-comments-link'),
    path('comments/all/', CommentsAll.as_view(), name='comments-all'),
    path('photos/all/', PhotosAll.as_view(), name='photos-all'),
    path('comments/commentsbymessage/link/<int:message_id>/', CommentsByMessage.as_view(), name='comments-by-message'),
    path('comments/commentsbyphoto/link/<int:photo_id>/', CommentsByPhoto.as_view(), name='comments-by-photo'),
    path('comments/commentsbyvideo/link/<int:video_id>/', CommentsByVideo.as_view(), name='comments-by-video'),

    path('search/friends/', searchUserFriend.as_view(), name='search-user'),
    path('getfriends/', UserFriendsView.as_view(), name='get-friends'),
    path('addfriends/', AddFriendsView.as_view(), name='add-friends'),
    path('removefriends/', RemoveFriendsView.as_view(), name='remove-friends'),
    path('api/profile/photo/', ProfilePhotoUploadView.as_view(), name='profile-photo-upload'),
    path('profile/by-username/', ProfileByUsernameView.as_view(), name='profile-by-username'),
    path('send-friend-request/', SendFriendRequestView.as_view(), name='send-friend-request'),
    path('respond-friend-request/', RespondToFriendRequestView.as_view(), name='respond-friend-request'),
    path('check/', CheckFriendRequestStatusView.as_view(), name='check-friend-request-status'),
    path('user-by-username/', UserByUsernameView.as_view(), name='user-by-username'),
    path('UserrequestAll/', UserrequestAll.as_view(), name='userrequest-all'),
    path('api/logout/', LogoutView.as_view(), name='logout'),
    path('api/friendlist/', FriendsListView.as_view(), name='friendlist'),
    path('api/profilid/', profilebisview.as_view(), name='profile-id'),
    path('api/photosupload/', PhotoUploadView.as_view(), name='photos-upload'),
    path('api/photosuploadfilactu/', PhotoUploadfilView.as_view(), name='photos-upload-filactu'),
    path('api/videosuploadfilactu/', VideoUploadfilView.as_view(), name='videos-upload-filactu'),
    path('api/videosupload/', VideoUploadView.as_view(), name='videos-upload'),
    path('api/photosuploadbis/', photobisview.as_view(), name='photos-upload-bis'),
    path('api/videosuploadbis/', videobisview.as_view(), name='videos-upload-bis'),
    path('photos/by-username/', PhotosByUsernameView.as_view(), name='photos-by-username'),
    path('videos/by-username/', VideosByUsernameView.as_view(), name='videos-by-username'),
    path('profile-picture-all/', ProfilePictureAllView.as_view(), name='profile-picturebyuserid'),

]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
