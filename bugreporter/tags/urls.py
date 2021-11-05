from django.urls import path

from tags import views

name = 'tags'
urlpatterns = [
    path('projects/<str:username>/<str:projectname>/tags/', views.Tags.as_view({'get': 'list', 'post': 'create'})),
    path('projects/<str:username>/<str:projectname>/<str:bug>/addtag/', views.TagsWithBugs.as_view({'post': 'create'})),
    path('projects/<str:username>/<str:projectname>/<str:bug>/deltag/<str:id>', views.TagsWithBugs.as_view({'delete': 'destroy'})),
    path('projects/<str:username>/<str:projectname>/<str:bug>/alltags/', views.TagsWithBugs.as_view({'get': 'list'}))
]