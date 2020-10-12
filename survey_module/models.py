from django.db import models
import uuid
from django.conf import settings

# Create your models here.
class Survey(models.Model):
    survey_id = models.UUIDField(primary_key=True, default = uuid.uuid4)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete = models.CASCADE)
    survey_name = models.CharField(max_length = 20)

    def __str__(self):
        return self.survey_name

class SurveyQuestions(models.Model):
    survey_question_id = models.IntegerField()
    survey_question = models.CharField(max_length = 100 ,blank = False)
    survey_id = models.ForeignKey(Survey,related_name='questions',on_delete=models.CASCADE)
    # responses = models.ManyToManyField(SurveyResponses)

    def __str__(self):
        return self.survey_question

    class Meta:
        ordering = ['survey_question_id']
        unique_together = [['survey_question_id','survey_id']]

class SurveyResponses(models.Model):
    answered_by = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete = models.CASCADE)
    survey_question_id = models.ForeignKey(SurveyQuestions,on_delete = models.CASCADE)
    answer = models.BooleanField()
    survey_id = models.ForeignKey(Survey,on_delete = models.CASCADE)
