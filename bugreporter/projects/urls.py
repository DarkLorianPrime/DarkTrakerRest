from django.urls import path

from projects import views

name = 'projects'

urlpatterns = [
    path('projects/<str:username>/', views.UserProjects.as_view({'get': 'list', 'post': 'create'})),
    path('projects/<str:username>/<str:projectname>/visible/',
         views.Settings.as_view({'post': 'update'})),
    path('projects/<str:username>/delete/<str:id>/', views.UserProjects.as_view({'delete': 'destroys'}))
]
