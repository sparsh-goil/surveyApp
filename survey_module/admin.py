from django.contrib import admin
from survey_module.models import *

# Register your models here.
admin.site.register(Survey)
admin.site.register(SurveyQuestions)
admin.site.register(SurveyResponses)