from django.shortcuts import render,redirect
from django.contrib.auth import logout, authenticate, login
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .forms import ProfileForm, RequestForm
from .models import  Req
from django.contrib.auth.models import User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .fusioncharts import FusionCharts
from collections import OrderedDict

from django.shortcuts import render
from django.http import HttpResponse

from collections import OrderedDict

# Include the `fusioncharts.py` file that contains functions to embed the charts.
# from fusioncharts import FusionCharts

# Create your views here.
def homepage(request):
    return render(request, 'main/homepage.html')

def visualspage(request):

    # Chart data is passed to the `dataSource` parameter, as dictionary in the form of key-value pairs.
    dataSource = OrderedDict()

    # The `chartConfig` dict contains key-value pairs data for chart attribute
    chartConfig = OrderedDict()
    chartConfig["caption"] = "Your Diabetes Tracker Over the Years"
    chartConfig["subCaption"] = "In mg/dL"
    chartConfig["xAxisName"] = "Years"
    chartConfig["yAxisName"] = "Blood Sugar Levels (In mg/dL)"
    chartConfig["numberSuffix"] = " "
    chartConfig["theme"] = "fusion"

    # The `chartData` dict contains key-value pairs data
    chartData = OrderedDict()
    chartData["November 2021"] = 100
    chartData["December 2021"] = 110
    chartData["January 2022"] = 105
    chartData["February 2022"] = 140
    chartData["March 2022"] = 150
    chartData["April 2022"] = 160
    chartData["May 2022"] = 155
    chartData["June 2022"] = 165


    dataSource["chart"] = chartConfig
    dataSource["data"] = []

    # Convert the data in the `chartData` array into a format that can be consumed by FusionCharts.
    # The data for the chart should be in an array wherein each element of the array is a JSON object
    # having the `label` and `value` as keys.

    # Iterate through the data in `chartData` and insert in to the `dataSource['data']` list.
    for key, value in chartData.items():
        data = {}
        data["label"] = key
        data["value"] = value
        dataSource["data"].append(data)


    # Create an object for the column 2D chart using the FusionCharts class constructor
    # The chart data is passed to the `dataSource` parameter.
    column2D = FusionCharts("column2d", "ex1" , "600", "400", "chart-1", "json", dataSource)

    #Load dial indicator values from simple string array# e.g.dialValues = ["52", "10", "81", "95"]
    dialValues = ["100000"]

    # widget data is passed to the `dataSource` parameter, as dict, in the form of key-value pairs.
    dataSource = OrderedDict()

    # The `widgetConfig` dict contains key-value pairs of data for widget attribute
    widgetConfig = OrderedDict()
    widgetConfig["caption"] = "Platelet Count"
    widgetConfig["lowerLimit"] = "0"
    widgetConfig["upperLimit"] = "400000"
    widgetConfig["showValue"] = "1"
    widgetConfig["numberSuffix"] = " L/cumm"
    widgetConfig["theme"] = "fusion"
    widgetConfig["showToolTip"] = "0"

    # The `colorData` dict contains key-value pairs of data for ColorRange of dial
    colorRangeData = OrderedDict()
    colorRangeData["color"] = [{
            "minValue": "0",
            "maxValue": "10000",
            "code": "#F2726F"
        },
        {
            "minValue": "10000",
            "maxValue": "140000",
            "code": "#FFC533"
        },
        {
            "minValue": "140000",
            "maxValue": "400000",
            "code": "#62B58F"
        }
    ]

    # Convert the data in the `dialData` array into a format that can be consumed by FusionCharts.
    dialData = OrderedDict()
    dialData["dial"] = []

    dataSource["chart"] = widgetConfig
    dataSource["colorRange"] = colorRangeData
    dataSource["dials"] = dialData

    # Iterate through the data in `dialValues` and insert into the `dialData["dial"]` list.
    # The data for the `dial`should be in an array wherein each element of the
    # array is a JSON object# having the `value` as keys.
    for i in range(len(dialValues)):
        dialData["dial"].append({
        "value": dialValues[i]
    })
   # Create an object for the angular-gauge using the FusionCharts class constructor
   # The widget data is passed to the `dataSource` parameter.
    angulargaugeWidget = FusionCharts("angulargauge", "myFirstWidget", "100%", "200", "myFirstwidget-container", "json", dataSource)

   # returning complete JavaScript and HTML code, which is used to generate widget in the browsers.

    return  render(request, 'main/visualspage.html', {'output' : column2D.render(), 'output1' : angulargaugeWidget.render(), 'chartTitle': 'Simple Chart Using Array'})

def signup(request):
    f = ProfileForm()
    f1 = UserCreationForm()
    if request.method=='POST':
        f1 = UserCreationForm(request.POST)
        f = ProfileForm(request.POST)
        if f1.is_valid() and f.is_valid():
            user = f1.save()
            profile = f.save(commit=False)
            profile.user = user
            username = f1.cleaned_data.get('username')
            password = f1.cleaned_data.get('password')
            user.set_password(password)
            profile.save()
            messages.success(request, "New account created: {username}".format(username=username))
            login(request,user)
            return redirect('main:homepage')
        else:
            for msg in f1.error_messages:
                messages.error(request, "{msg}: {form}[{msg}]".format(msg=msg,form=f1.error_messages))
            return render(request, 'main/signup.html',{'form': f,'form_user':f1})
    else:
        f1 = UserCreationForm()
        f = ProfileForm()
    return render(request, 'main/signup.html',{'form': f,'form_user':f1})

def login_(request):
        if request.method == 'POST':
            form = AuthenticationForm(data=request.POST)
            if form.is_valid():
                username = form.cleaned_data.get('username')
                password = form.cleaned_data.get('password')
                user = authenticate(username=username,password=password)
                if user is not None:
                    login(request,user)
                    messages.success(request,'You have logged in as {}'.format(username))
                    return redirect('/')
                else:
                    messages.error(request, "Invalid username or password1")
            else:
                messages.error(request,'Invalid username or password2')
        form = AuthenticationForm()
        return render(request,'main/login.html',{'form':form})


def logout_(request):
    logout(request)
    messages.success(request,"You've logged out successfully!")
    return redirect('main:homepage')


def requests(request):
    if request.method == 'POST':
        f = RequestForm(request.POST)
        if f.is_valid():
            user1 = f.cleaned_data.get('username1')
            user2 = f.cleaned_data.get('username2')
            text = f.cleaned_data.get('text')
            try:
                req_by = User.objects.get(username=user1)
                req_for = User.objects.get(username=user2)
            except User.DoesNotExist:
                messages.error(request,"Username does not exist.")
                return redirect('/requests')
            req = Req()
            req.req_by = req_by
            req.req_for = req_for
            req.text = text
            req.save()
            messages.success(request,"Added")
            return redirect("main:homepage")
        else:
            messages.success(request,"Documents Added")
    f = RequestForm()
    if request.user.is_authenticated:
        return render(request, 'main/request.html', {'form':f})
    else:
        messages.error(request,"You must log in first!")
        return redirect("/login")

def donate(request):
    request_list = Req.objects.all()
    page = request.GET.get('page',1)
    paginator = Paginator(request_list,2)
    try:
        reqs = paginator.page(page)
    except PageNotAnInteger:
        reqs = paginator.page(1)
    except EmptyPage:
        reqs = paginator.page(paginator.num_pages)
    return render(request, 'main/donate.html', {'reqs': reqs})
