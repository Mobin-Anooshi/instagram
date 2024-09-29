from django.urls import path
from . import views

app_name = 'home'
urlpatterns = [
    path('',views.HomeView.as_view(),name='home'),
    path('add_post',views.UserAddPost.as_view(),name='add_post'),
    path('post_detail/<int:post_id>/<slug:post_slug>/',views.PostDetailView.as_view(),name='post_detail'),
    path('edit_post/<int:post_id>/',views.PostEditView.as_view(),name='edit_post'),
    path('delete_post/<int:post_id>/',views.DeletePostView.as_view(),name='post_delete'),
    path('like/<int:post_id>/',views.LikePostView.as_view(),name='user_like'),
    path('save_message/<int:post_id>/',views.SaveMessagesView.as_view(),name='save'),
    path('save_posts/',views.SavePostView.as_view(),name='save_post'),
    path('follow/<int:user_id>/',views.UserRelationView.as_view(),name='user_relations'),
    path('request/<int:user_id>/',views.UserRequestView.as_view(),name='user_request'),
    path('requets/list/<int:user_id>/',views.UserDetailRequestsView.as_view(),name='requests'),
    path('requets/accept/<int:user_id>/',views.UserAcceptView.as_view(),name='user_accept'),
]
