"""
URL configuration for cms_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from blog.views import CreateUserView, LoginView, GetUserView, DeleteUserView, UpdateUserView, CreateRetrievePostView, RetrieveUpdateDeletePostView, LikeView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts', CreateUserView.as_view()),
    path('accounts/login', LoginView.as_view()),
    path('me', GetUserView.as_view()),
    path('accounts/delete', DeleteUserView.as_view()),
    path('accounts/update', UpdateUserView.as_view()),
    path('blog', CreateRetrievePostView.as_view()),
    path('blog/<int:id>', RetrieveUpdateDeletePostView.as_view()),
    path('like/<int:blog_id>', LikeView.as_view())
]
