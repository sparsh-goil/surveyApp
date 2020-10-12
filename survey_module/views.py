from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import HttpResponse
from rest_framework.permissions import IsAuthenticated
from survey_module.models import *
from django.conf import settings
from survey_module.serializers import *
from django.core import serializers
from django.db.models import Count, Sum, Case, When, Value
import urllib
from PIL import Image


# Create your views here.
class CreateSurvey(APIView):
    permission_classes = [IsAuthenticated]

    def post(self,request):
        data = request.data
        # print(data)
        S = Survey.objects.create(
            created_by = request.user,
            survey_name = data["surveyName"],
        )
        quesNumber=1
        for question in data["questions"]:
            SurveyQuestions.objects.create(
                survey_question_id = quesNumber,
                survey_question = question,
                survey_id = S,
            )
            quesNumber+=1
        result = {"status": "Success! Your survey has been created"}
        return Response(result) #status=status.HTTP_201_CREATED)

#Class based view to return all the available surveys
class DisplaySurveys(APIView):
    permission_classes = [IsAuthenticated]

    def get(self,request):
        surveys = Survey.objects.all()
        result = SurveySerializer(surveys,many=True).data
        return Response(result)

#Class based view to take a survey for a given survey id.
class TakeSurvey(APIView):
    permission_classes = [IsAuthenticated]

    def post(self,request):
        data = request.data
        survey_id = Survey.objects.get(survey_id = uuid.UUID(data['survey_id']))
        user = request.user
        if SurveyResponses.objects.filter(answered_by = user).exists:
            return Response({"result":"You have already filled the form."})
        for response in data['questionResponses']:
            for question,answer in response.items():
                question_id = SurveyQuestions.objects.filter(survey_id=survey_id).get(survey_question=question)
                SR = SurveyResponses.objects.create(
                    answered_by = user,
                    survey_question_id = question_id,
                    answer = True if answer == "True" else False,
                    survey_id = survey_id,
                )
        return Response({"result":"Thank You! Your Survey has been filled!"})


#Class based view to return results of a survey given survey id.
class SurveyResults(APIView):
    permission_classes = [IsAuthenticated]

    def get(self,request):
        data = request.data
        user = request.user
        survey_id = Survey.objects.get(survey_id = uuid.UUID(data['survey_id']))
        result = SurveyResponses.objects.values('survey_question_id__survey_question').annotate(
            yes = Count(Case(When(answer = True, then=Value(1)))),
            no = Count(Case(When(answer = False, then=Value(1))))
        )
        return Response(result)


#Class based view to generate thumbnail
class GenerateThumbnail(APIView):
    permission_classes = [IsAuthenticated]

    def post(self,request):
        data = request.data
        #download image
        urllib.request.urlretrieve(data['image_url'],"test.jpg")
        img = Image.open("test.jpg")
        img_small = img.resize((50,50), Image.ANTIALIAS)
        img_small.save("test_small.jpg")
        with open("test_small.jpg",'rb') as f:
            return HttpResponse(f.read(),content_type = "image/jpeg")
