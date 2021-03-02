from django.urls import path #type: ignore

from . import views

app_name = 'confirmation'

urlpatterns = [
    path('<str:token>', views.GetConfirmationPage, name='GetConfirmationPage')
]