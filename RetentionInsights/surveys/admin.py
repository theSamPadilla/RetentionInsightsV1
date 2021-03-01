from django.contrib import admin
from .models import Study, User, Factor, Survey, Question_Text, Question, Response, Reward

# Register your models here.
admin.site.register(Study)
admin.site.register(User)
admin.site.register(Factor)
admin.site.register(Survey)
admin.site.register(Question_Text)
admin.site.register(Question)
admin.site.register(Response)
admin.site.register(Reward)