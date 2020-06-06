"""Information_storage URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
# from django.contrib import admin
from django.urls import path, re_path
from information import views

urlpatterns = [
    #    path('admin/', admin.site.urls),
    # 公共url
    path('welcome/', views.welcome),
    re_path('login/', views.login),
    path('logout/', views.logout),
    path('register/', views.register),

    # 学生url
    path('sindex/', views.sindex),
    path('add_storage/', views.add_storage),
    path('my_storage_page/', views.my_storage_page),
    path('my_storage/', views.my_storage),
    path('update_s/', views.update_s),
    path('personal_information/', views.personal_information),
    path('updatepwd/', views.updatepwd),

    # 老师url
    path('tindex/', views.tindex),
    path('all_user_page/', views.all_user_page),
    path('all_user/', views.all_user),
    path('all_unapprove_storage/', views.all_unapprove_storage),
    path('all_unapprove_storage_page/', views.all_unapprove_storage_page),
    path('all_storage_page/', views.all_storage_page),
    path('all_storage/', views.all_storage),
    path('delete_user/', views.delete_user),
    path('t_add_storage/', views.t_add_storage),
    path('Approved/', views.Approved),
    path('search_by_number/', views.search_by_number),
]
