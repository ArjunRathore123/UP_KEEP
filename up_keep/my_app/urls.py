from my_app.views import UserRegistrationView, UserProfileView, SendResetPasswordEmailView,\
    ResetPasswordView, UserLoginView, LogoutView
from django.urls import path, include
from repair_contact.router import router


urlpatterns = [
    path('register', UserRegistrationView.as_view()),
    path('login', UserLoginView.as_view()),
    path('profile', UserProfileView.as_view()),
    path('SendResetPassword/', SendResetPasswordEmailView.as_view()),
    path('reset-password/<uid>/<token>', ResetPasswordView.as_view()),
    path('AddRepair/', include(router.urls)),
    path('logout/', LogoutView.as_view()),
]
