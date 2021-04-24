from django.urls import path #type: ignore

from . import views

app_name = 'feedback'

urlpatterns = [
    path('<str:name>/', views.GetFeedbackPage, name='GetFeedbackPage'),
    path('<str:name>/recorded/', views.GetRecordedPage, name='FeedbackRecorded'),
    path('<str:name>/submit/', views.SubmitFeedback, name='SubmitFeedback'),
]