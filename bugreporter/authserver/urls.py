from django.urls import path

from authserver import views

name = 'authserver'

urlpatterns = [
    path('login/', views.Login.as_view({'get': 'isLoggined', 'post': 'login'})),
    path('logout/', views.Logout.as_view({'get': 'logout'})),
    path('registration/', views.Regisration.as_view({'get': 'isRegistered', 'post': 'registration'})),
    # path('projects/', views.UserProjects.as_view({'get': 'list_projects'})),
    # path('projects/', views.UserProjects.as_view({'create': 'list_projects'})),
    # path('projects/<str:username>/', views.UserProjects.as_view({'get': 'get_projects'}))
]