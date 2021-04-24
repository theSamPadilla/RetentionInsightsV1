from django.contrib import admin
from .models import Feedback

#Customize displays
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('studyID', 'timestamp')
    readonly_fields = ('timestamp',)


#Register models.
admin.site.register(Feedback, FeedbackAdmin)