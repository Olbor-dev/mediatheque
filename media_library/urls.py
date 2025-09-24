"""
URL configuration for media_library project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from mediatheque import views as mediatheque_views
from medias import views as medias_views


urlpatterns = [
    path('', mediatheque_views.index, name='index'),
    path('mediaslist/', medias_views.MediaListView.as_view(), name='medias_list'),
    path('medias/', mediatheque_views.medias, name='medias'),
    path('members/', mediatheque_views.members, name='members'),
    path('members/<int:pk>/edit/', mediatheque_views.member_edit, name='member_edit'),
    path('borrows/', mediatheque_views.borrows, name='borrows'),
    path('borrows/return/<int:borrow_id>/', mediatheque_views.return_borrow, name='return_borrow'),
    path('admin/', admin.site.urls),
]
