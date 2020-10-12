from rest_framework import serializers
from survey_module.models import *

class SurveySerializer(serializers.ModelSerializer):
    created_by = serializers.StringRelatedField()
    questions = serializers.StringRelatedField(many=True)

    class Meta:
        model = Survey
        fields =  ['survey_id','survey_name','created_by','questions']