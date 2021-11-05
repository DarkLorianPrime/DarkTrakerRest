from django.urls import path

from bugs.views import BugsReport, CommentsWithReports, BugsVisible

name = 'bugs'
urlpatterns = [
    path('projects/<str:username>/<str:projectname>/', BugsReport.as_view({'get': 'list', 'post': 'create'})),
    path('projects/<str:username>/<str:projectname>/<str:bug>/isOpened', BugsVisible.as_view({'post': 'update'})),
    path('projects/<str:username>/<str:projectname>/<str:bug>/comments/', CommentsWithReports.as_view({'get': 'list', 'post': 'create'}))
               ]
