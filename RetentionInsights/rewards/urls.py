from django.urls import path #type: ignore

from . import views

app_name = 'rewards'

urlpatterns = [
    path('<int:studyID>/<str:token>/check/', views.CheckRewards, name='CheckRewards'),
    path('<int:studyID>/<str:token>/update/', views.UpdateRewards, name='UpdateRewards'),
]