from django.shortcuts import render , redirect
from rest_framework import generics
from .models import Designations , Survey, TestQuestionnaire , QuestionnaireApi , Report 
from django.db.models import Sum , Avg 
from .serializers import DesignationsSerializer,SurveySerializer,QuestionnaireApiSerializer , ReportSerializer
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .forms import DataForm , CreateUserForm
from django.contrib import messages
from django.contrib.auth import authenticate , login , logout
from django.contrib.auth.models import User
from rest_framework.decorators import api_view
from rest_framework.response import Response
import pandas as pd
# auth
from django.contrib.auth.forms import UserCreationForm

# from Auth.serializer import *

# Create your views here.
class DesignationsList(generics.ListCreateAPIView):
    queryset = Designations.objects.all()
    serializer_class = DesignationsSerializer

class DesignationsDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Designations.objects.all()
    serializer_class = DesignationsSerializer   
#for survey
class SurveyList(generics.ListCreateAPIView):
    queryset = Survey.objects.all()
    serializer_class = SurveySerializer

class SurveyDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Survey.objects.all()
    serializer_class = SurveySerializer   

 # for questionnaire
class QuestionnaireApiList(generics.ListCreateAPIView):
    queryset = QuestionnaireApi.objects.all()
    serializer_class = QuestionnaireApiSerializer

class QuestionnaireApiDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = QuestionnaireApi.objects.all()
    serializer_class = QuestionnaireApiSerializer   
 
# for reports
class ReportList(generics.ListCreateAPIView):
    queryset = Report.objects.all() 
    serializer_class = ReportSerializer

class ReportDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Report.objects.all()
    serializer_class = ReportSerializer

@login_required(login_url='login')
def index(request):
    qs = Report.objects.all()
    total = Report.objects.all().count()
    active = Report.objects.filter(isActive=True).count()
    num_of_reports= Report.objects.aggregate(Total=Sum('number_of_reports'))['Total']
    # creating querset for dynamic chart update with model
    qs = Report.objects.all().values()
    df= pd.DataFrame(qs)
    df1 = df.title.tolist()
    df = df['number_of_reports'].tolist()
    # create queryset for gender participation update
    query_set= Report.objects.all().values()
    m_num= pd.DataFrame(query_set)
    q_title=m_num.title.tolist()
    m_num=m_num['number_of_male'].tolist()
    query_set2 = Report.objects.all().values()
    f_num=pd.DataFrame(query_set2)
    f_num=f_num['number_of_female'].tolist()
    q_performance = Report.objects.aggregate(Total=Avg('number_of_reports'))['Total']/num_of_reports * 100
    value = q_performance
    rounded = (round(value, 1))
    
    
   
   
    


    
    

    context = {'total':total , 'active':active, 'num_of_reports':num_of_reports ,
               'q_performance':q_performance ,"rounded":rounded ,  'df':df, 
        'df1':df1 , 'q_title':q_title ,'m_num':m_num, 'f_num':f_num }
    return render(request, 'dashboard/index.html',
     context 
  
    )


def charts(request):
    return render(request, 'dashboard/charts.html')

@login_required(login_url='login')
def new_questionnaire(request):
    
    if request.method == 'POST' :
        post = QuestionnaireApi()
        post.name = request.POST.get('title')
        post.status = request.POST.get('isActive')
        post.description = request.POST.get('description')
        post.active_till = request.POST.get('active_till')
        post.num_questions = request.POST.get('number_of_questions')
        post.target_app =  request.POST.get('target_app')
        
        post.save()
        return HttpResponse('Database updated successfuly with New Questionnaire')
           
    return  render(request, "dashboard/new_questionnaire.html")
       
    
def users(request):

    return render(request, "dashboard/users.html")

def RegisterPage(request):

    if request.user.is_authenticated :
        return redirect('dashboard')
    else:
        
        form = CreateUserForm()
        context = {'form': form}    
        if request.method == 'POST':
           form = CreateUserForm(request.POST)
           if form.is_valid():
               form.save()
           user = form.cleaned_data.get('username')
           messages.success(request, 'account was created successfully for ' + user )
           return redirect('login')
        #    messages.info(request, ' username or password does not exist ') 

    return render(request, 'accounts/reg_form.html', context)
def loginPage(request):
    if request.user.is_authenticated :
        return redirect('dashboard')
    else:    
        if request.method == 'POST':
           username = request.POST.get('username')
           password = request.POST.get('password')

           user = authenticate(request, username=username , password=password)
           if user is not None:
                login(request, user)
           return redirect('dashboard')
        else:
                # messages.info(request, ' username or password does not exist ')   
                context = {}      
    return render(request, 'accounts/login.html')

def logoutuser(request):
    logout(request)
    return redirect('login')

def dbfetch(request):
    return render(request, "dashboard/dbfetch.html")

@login_required(login_url='login')
def questionnaires(request):
    post = QuestionnaireApi.objects.all()
    count = QuestionnaireApi.objects.all().count()
    context = {'post': post, 'count':count}
    # if request.method == 'POST' :
        
        # name = request.POST.get['title']                      
        # isActive = request.GET['isActive']
        # active_till = request.GET['active_till'] 
        # number_of_questions = request.GET['num_questions']                      

        
    return render(request, "dashboard/questionnaires.html", context)
# reports

@login_required(login_url='login')
def new_report(request):
    
    if request.method == 'POST' :
        post_report = Report()
        post_report.title = request.POST.get('title')
        post_report.isActive = request.POST.get('isActive')
        # post.active_till = request.POST.get('active_till')
        post_report.number_of_male = request.POST.get('number_of_male')
        post_report.number_of_female =request.POST.get('number_of_female')
        post_report.number_of_reports = request.POST.get('number_of_reports')
        post_report.target_app = request.POST.get('target_app')
        
        post_report.save()
        return HttpResponse('Database updated successfuly with New Questionnaire Reports')
           
    return  render(request, "dashboard/new_report.html")

def Reports(request):
    post_report= Report.objects.all()
    count = Report.objects.all().count()
    context = {'post_report': post_report, 'count':count}
    # if request.method == 'POST':
        # name= request.POST.get['title']
        # isActive = request.GET['isActive']
        # number_of_reports= request.GET['number_of_reports']
        # number_of_male= request.GET['number_of_male']
        # number_of_femae=request.GET['number_of_female']

    return render(request, 'dashboard/reports.html', context)
# rest_framework views


# get all questionnaires
@api_view(['GET'])
def getQuestionnaires(request):
        Questionnaires = QuestionnaireApi.objects.all()
        serializer = QuestionnaireApiSerializer(Questionnaires, many=True)
        return Response(serializer.data)

# get Questionnaire by id
@api_view(['GET'])
def getQuestionnaire(request, pk):
        Questionnaire = QuestionnaireApi.objects.get(id=pk)
        serializer = QuestionnaireApiSerializer(Questionnaire, many=False)
        return Response(serializer.data)

# create Questionnaire
@api_view(['POST'])
def CreateQuestionnaire(request):
     
    serializer = QuestionnaireApiSerializer(data = request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)

# update Questionnaire
@api_view(['PUT'])
def updateQuestionnaire(request, pk):
    # pk = int(pk)
    Questionnaire = QuestionnaireApi.objects.get(id=pk)
    serializer = QuestionnaireApiSerializer(instance=Questionnaire, data = request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)    

# delete Questionnaire
@api_view(['DELETE'])
def deleteQuestionnaire(request, pk):
    pk = int(pk)
    questionnaire = QuestionnaireApi.objects.get(id=pk)
    questionnaire.delete()
    return Response('Questionnaire was deleted')     
        


    



    
    









