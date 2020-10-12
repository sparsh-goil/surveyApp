from django.urls import path,include
from survey_module.views import *

urlpatterns = [
    path('create_survey/',CreateSurvey.as_view(),name='create a survey'),
    path('display_survey/',DisplaySurveys.as_view(),name='display all surveys'),
    path('take_survey/',TakeSurvey.as_view(),name='take a survey'),
    path('survey_results/',SurveyResults.as_view(),name='results of survey'),
    path('generate_thumbnail/',GenerateThumbnail.as_view(),name='thumbnail of image')
]