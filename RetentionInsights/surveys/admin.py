from django.contrib import admin
from .models import Study, User, Factor, Survey, Question_Text, Question, Response, Reward

#Customize displays
class StudyAdmin(admin.ModelAdmin):
    list_display = ('studyName', 'studyID', 'contactPerson', 'contactEmail', 'active_participants', 'surveys_sent', 'responses', 'response_rate', 'data_points')

class UserAdmin(admin.ModelAdmin):
    list_display = ('firstName', 'userID', 'active_p', 'total_responses', 'studyID', 'userGroup')

class FactorAdmin(admin.ModelAdmin):
    list_display = ('factorName', 'studyID', 'factorID')

class SurveyAdmin (admin.ModelAdmin):
    list_display = ('surveyID', 'token', 'creationDate', 'completed_p', 'expired', 'study')

class Question_TextAdmin(admin.ModelAdmin):
    list_display = ('text', 'factor', 'study', 'questionTextID')

class QuestionAdmin(admin.ModelAdmin):
    list_display = ('questionID', 'survey', 'text', 'factor', 'study')

class ResponseAdmin(admin.ModelAdmin):
    list_display = ('questionID', 'text', 'response', 'study')

class RewardAdmin(admin.ModelAdmin):
    list_display = ('name', 'study')

# Register your models here.
admin.site.register(Study, StudyAdmin)
admin.site.register(User, UserAdmin)
admin.site.register(Factor, FactorAdmin)
admin.site.register(Survey, SurveyAdmin)
admin.site.register(Question_Text, Question_TextAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Response, ResponseAdmin)
admin.site.register(Reward, RewardAdmin)