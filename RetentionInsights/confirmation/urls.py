from django.urls import path #type: ignore

from . import views

app_name = 'confirmation'

urlpatterns = [
    path('<str:token>/', views.GetConfirmationPage, name='GetConfirmationPage'),
    path('<str:token>/recorded/', views.GetConfirmationRecordedPage, name='ConfirmationRecorded'),
    path('<str:token>/submit/', views.SubmitConfirmation, name='SubmitConfirmation'),
]