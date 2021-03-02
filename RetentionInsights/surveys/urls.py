# pylint: disable=relative-beyond-top-level
from django.urls import path #type: ignore

from . import views

app_name = 'surveys'

urlpatterns = [
    path('<str:token>/', views.GetSurvey, name='GetSurvey'),
    path('<str:token>/recorded/', views.GetRecordedView, name='ResponseRecorded'),
    path('<str:token>/submit/', views.SubmitResponse, name='SubmitResponse'),
]
