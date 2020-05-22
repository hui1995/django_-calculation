from django.shortcuts import render,redirect
from django.views import View
from .models import *

# Create your views here.

class LoginView(View):
    def get(self,request):
        return render(request,'login.html')


    def post(self,request):
        id=request.POST.get("username")
        password=request.POST.get("password")

        try:
            user=User.objects.get(id=id)
        except:
            message="该工号不存在"
            return render(request,'login.html',locals())
        if user.password!=password:
            message = "密码不正确"
            return render(request, 'login.html', locals())

        dict1={}
        dict1['name']=user.user_name
        dict1['id']=user.id
        dict1['position']=user.postionId


        request.session['user'] = dict1
        return redirect("/index")
