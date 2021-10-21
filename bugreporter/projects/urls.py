from django.urls import path

from projects import views

name = 'authserver'

urlpatterns = [
    path('projects/', views.UserProjects.as_view({'get': 'list', 'post': 'create'})),
    path('projects/<int:pk>', views.UserProjects.as_view({'delete': 'destroy'}))
    # path('projects/', views.UserProjects.as_view({'get': 'list_projects', 'post': 'create_project'})),
    # path('projects/<str:username>/', views.UserProjects.as_view({'get': 'get_projects'}))
]
