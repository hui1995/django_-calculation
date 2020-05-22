from django.shortcuts import render, redirect

# Create your views here.
from django.views import View
from user.models import *
from .models import *

userPostion = {1: {
    "edit": ["供应商档案", "采购订单", "采购退货单", "材料运输单", "收货回执"],
    "editCode": [1, 2, 3, 4, 5],
    "browse": ["采购入库单", "物料清单"],
    "browseCode": [6, 7],
    "name": "制造企业用户"},
    2: {
        "edit": ["采购报价单", "材料运输单", "预先发货清单"],
        "editCode": [8, 4, 9],
        "browse": ["采购订单", "采购退货单", "收货回执"],
        "browseCode": [2, 3, 5],
        "name": "供应商用户"},
    3: {
        "edit": ["系统用户信息", "权限管理", "供应商档案", "采购入库单", "物料清单"],
        "editCode": [10, 11, 1, 6, 7],
        "browse": ["采购订单", "采购退货单", "物料清单", "材料运输单", "出库单", "预先发货清单", "收货回执"],
        "browseCode": [2, 3, 7, 4, 12, 9, 5],
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


class IndexView(View):
    def get(self, request):
        try:
            user = request.session["user"]
        except:
            return redirect("/login")

        userType = user["position"]
        postionInfo=userPostion[userType]

        departmentPostion = DepartmentPostion.objects.get(id=userType)

        return render(request, 'index.html', locals())


class SupplierView(View):
    def get(self, request):
        permission=1
        isPermession=permissionFunc(request,1)
        if isPermession is None:
            return redirect("/login")
        keywords = request.GET.get("keyword", None)
        if keywords is None:
            resultlst = Supplier.objects.all()
        else:
            resultlst = Supplier.objects.filter(supplier_id=keywords)
        return render(request, 'supplier.html', locals())

    def post(self, request):
        permission = 1
        isPermession = permissionFunc(request, 1)
        if isPermession is None:
            return redirect("/login")

        supplier_id = request.POST.get("supplier_id")
        name = request.POST.get("name")
        phone = request.POST.get("phone")
        user_name = request.POST.get("user_name")
        adress = request.POST.get("adress")
        category = request.POST.get("category")
        if supplier_id == "" or name == "" or phone == "" or user_name == "" or adress == "" or category == "":
            message = "参数不能为空"
            return render(request, 'supplier.html', locals())
        Supplier.objects.create(supplier_id=supplier_id, name=name, phone=phone, user_name=user_name, adress=adress,
                                category=category)

        return redirect("/supplier/")


class DeleteSupplierView(View):
    def get(self, request):
        permission = 1
        isPermession = permissionFunc(request, 1)
        if isPermession is None:
            return redirect("/login")
        id = request.GET.get("id", None)
        keyword = request.GET.get("keyword", None)
        Supplier.objects.get(supplier_id=id).delete()
        if keyword is None:
            return redirect("/supplier/")
        return redirect("/supplier/?keyword=" + keyword)


class EditSupplierView(View):
    def get(self, request):
        permission = 1
        isPermession = permissionFunc(request, 1)
        if isPermession is None:
            return redirect("/login")
        id = request.GET.get("id", None)
        supplier = Supplier.objects.get(supplier_id=id)
        keywords = request.GET.get("keyword", None)
        if keywords is None:
            resultlst = Supplier.objects.all()
        else:
            resultlst = Supplier.objects.filter(supplier_id=keywords)

        edit = True
        return render(request, 'supplier.html', locals())

    def post(self, request):
        permission = 1
        isPermession = permissionFunc(request, 1)
        if isPermession is None:
            return redirect("/login")
        supplier_id = request.POST.get("supplier_id")
        name = request.POST.get("name")
        phone = request.POST.get("phone")
        user_name = request.POST.get("user_name")
        adress = request.POST.get("adress")
        category = request.POST.get("category")

        keyword = request.GET.get("keyword", None)

        if name == "" or phone == "" or user_name == "" or adress == "" or category == "":
            message = "参数不能为空"
            return render(request, 'supplier.html', locals())
        supplier = Supplier.objects.get(supplier_id=supplier_id)
        supplier.name = name
        supplier.phone = phone
        supplier.user_name = user_name
        supplier.adress = adress
        supplier.category = category
        supplier.save()
        if keyword is None:
            return redirect("/supplier/")
        return redirect("/supplier/?keyword=" + keyword)



    
