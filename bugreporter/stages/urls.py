from django.urls import path

from stages import views

name = 'stages'

urlpatterns = [
    path('projects/<str:username>/<str:projectname>/stages/', views.Stages.as_view({'get': 'list', 'post': 'create'})),
    path('projects/<str:username>/<str:projectname>/stages/delete/<str:id>', views.Stages.as_view({'delete': 'destroys'})),
    path('projects/<str:username>/<str:projectname>/<str:bug>/stage/', views.StagesWithReports.as_view({'post': 'update', 'get': 'list'})),
]