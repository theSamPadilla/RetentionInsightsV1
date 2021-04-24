from django.db import models
from django.utils import timezone
from surveys.models import Study #type: ignore

class Feedback(models.Model):
    studyID = models.ForeignKey(Study, on_delete=models.CASCADE)
    text = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    #Display functions 
    def displayTimetamp(self):
        return str(timezone.localtime(self.timestamp).strftime("%A, %B %-d, %Y at %-I:%M %p"))
