'''This file defines all the URLs patterns to redirect user to the correct view.'''
from django.urls import path
from .views import home_view, login_view, logout_view, register_view, main_board, create_note, view_note, edit_note, delete_note, profile_view

urlpatterns = [
    path('', home_view, name='home'), # home view
    path('login/', login_view, name='login'),  # login view
    path('main_board/', main_board, name='main_board'), # main board view
    path('logout/', logout_view, name='logout'), # logout view
    path('register/', register_view, name='register'), # register view
    path('create_note/', create_note, name='create_note'), # create note view
    path('view_note/<int:note_id>/', view_note, name='view_note'), # view note view
    path('edit_note/<int:note_id>/', edit_note, name='edit_note'), # edit note view
    path('delete_note/<int:note_id>/', delete_note, name='delete_note'), # delete note view
    path('profile/', profile_view, name='profile') # displays and allow user to edit profile
]