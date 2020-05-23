from django.shortcuts import render,redirect
from django.views import View
from .models import *

# Create your views here.
userPostion = {1: {
    "edit": ["供应商档案", "采购订单", "采购退货单", "材料运输单", "收货回执"],
    "editCode": [1, 2, 3, 4, 5],
    "browse": ["采购入库单", "物料清单"],
    "browseCode": [6, 7],
    "name": "制造企业用户"},
    2: {
        "edit": [ "材料运输单", "预先发货清单"],
        "editCode": [ 4, 9],
        "browse": ["采购订单", "采购退货单", "收货回执"],
        "browseCode": [2, 3, 5],
        "name": "供应商用户"},
    3: {
        "edit": ["系统用户信息", "供应商档案", "采购入库单", "物料清单"],
        "editCode": [10, 1, 6, 7],
        "browse": ["采购订单","部门管理", "采购退货单", "物料清单", "材料运输单", "出库单", "预先发货清单", "收货回执"],
        "browseCode": [2, 11,3, 7, 4, 12, 9, 5],
        "name": "制单员"},
    4: {
        "edit": ["材料运输单", "运输调度单"],
        "editCode": [4, 13],
        "browse": ["采购订单", "采购入库单", "采购退货单", "出库单", "预先发货清单"],
        "browseCode": [2, 6, 3, 12, 9],
        "name": "运输调度员"},
    5: {
        "edit": ["采购入库单", "采购退货单", "物料清单", "出库单", "材料运输单", "出库单"],
        "editCode": [6, 3, 7, 12, 4, 12],
        "browse": ["采购订单", "预先发货清单", "运输调度单"],
        "browseCode": [2, 9, 13]},
    "name": "仓库管理员"

}

def permissionFunc(request,permission):
    try:
        user = request.session["user"]
    except:
        return None

    userType = user["position"]
    postionInfo = userPostion[userType]

    if permission in postionInfo['editCode']:
        return True

    elif permission in postionInfo["browseCode"]:
        return False
    else:
        return None
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
class DepartView(View):

    def get(self, request):
        isPermession = permissionFunc(request, 11)
        if isPermession is None:
            return redirect("/login")
        keywords = request.GET.get("keyword", None)
        if keywords is None:
            resultlst = DepartmentPostion.objects.all()
        else:
            resultlst = DepartmentPostion.objects.filter(id=keywords)


        return render(request, 'depart.html', locals())


class UserView(View):
    def get(self, request):
        isPermession=permissionFunc(request,10)
        if isPermession is None:
            return redirect("/login")
        keywords = request.GET.get("keyword", None)
        if keywords is None:
            resultlst = User.objects.all()
        else:
            resultlst = User.objects.filter(id=keywords)
        result=[]
        for i in resultlst:
            d=DepartmentPostion.objects.get(id=i.postionId)
            dict1={}

            dict1['id']=i.id
            dict1['user_name']=i.user_name
            dict1['password']=i.password
            dict1['department']=d.department
            dict1['position']=d.position
            dict1['positionId'] = d.id


            result.append(dict1)
        resultlst=result
        departmentPostion = DepartmentPostion.objects.all()


        return render(request, 'user.html', locals())

    def post(self, request):
        isPermession = permissionFunc(request, 10)
        if isPermession is None:
            return redirect("/login")


        id = request.POST.get("id")
        user_name = request.POST.get("user_name").strip()
        password = request.POST.get("password").strip()
        postionId = request.POST.get("postionId").strip()

        if  id == "" or user_name == "" or \
                password == "" or postionId=="" :
            message = "参数不能为空"
            return render(request, 'User.html', locals())
        User.objects.create(id=id, user_name=user_name,password=password,postionId=postionId)

        return redirect("/user/")


class DeleteUserView(View):
    def get(self, request):
        isPermession = permissionFunc(request, 10)
        if isPermession is None:
            return redirect("/login")
        id = request.GET.get("id", None)
        keyword = request.GET.get("keyword", None)
        User.objects.get(id=id).delete()
        if keyword is None:
            return redirect("/user/")
        return redirect("/user/?keyword=" + keyword)


class EditUserView(View):
    def get(self, request):
        isPermession = permissionFunc(request, 10)
        if isPermession is None:
            return redirect("/login")
        id = request.GET.get("id", None)
        user = User.objects.get(id=id)

        keywords = request.GET.get("keyword", None)
        if keywords is None:
            resultlst = User.objects.all()
        else:
            resultlst = User.objects.filter(id=keywords)

        result = []
        for i in resultlst:
            d = DepartmentPostion.objects.get(id=i.postionId)
            dict1 = {}

            dict1['id'] = i.id
            dict1['user_name'] = i.user_name
            dict1['password'] = i.password
            dict1['department'] = d.department
            dict1['position'] = d.position
            dict1['positionId'] = d.id
            result.append(dict1)
        resultlst = result
        departmentPostion = DepartmentPostion.objects.all()


        edit = True
        return render(request, 'User.html', locals())

    def post(self, request):
        isPermession = permissionFunc(request, 10)
        if isPermession is None:
            return redirect("/login")
        id = request.POST.get("id")
        user_name = request.POST.get("user_name").strip()
        password = request.POST.get("password").strip()
        postionId = request.POST.get("postionId").strip()

        if  id == "" or user_name == "" or \
                password == "" or postionId=="" :
            message = "参数不能为空"
            return render(request, 'User.html', locals())

        keyword = request.GET.get("keyword", None)
        user = User.objects.get(id=id)
        user.user_name = user_name
        user.password = password
        user.postionId = postionId


        user.save()
        if keyword is None:
            return redirect("/user/")
        return redirect("/user/?keyword=" + keyword)