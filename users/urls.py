from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from users.apps import UsersConfig
from users.views import PaymentListAPIView, UserListAPIView, UserCreateAPIView, UserRetrieveAPIView, UserUpdateAPIView, \
    UserDestroyAPIView

app_name = UsersConfig.name

urlpatterns = [
    path('payments/', PaymentListAPIView.as_view(), name='payments-list'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('users/list/', UserListAPIView.as_view(), name='user_list'),
    path('users/create/', UserCreateAPIView.as_view(), name='user_create'),
    path('users/<int:pk>/', UserRetrieveAPIView.as_view(), name='user_detail'),
    path('users/<int:pk>/update/', UserUpdateAPIView.as_view(), name='user_update'),
    path('users/<int:pk>/delete/', UserDestroyAPIView.as_view(), name='user_delete'),
]
