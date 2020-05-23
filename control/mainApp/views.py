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
        "edit": [ "材料运输单", "预先发货清单"],
        "editCode": [ 4, 8],
        "browse": ["采购订单", "采购退货单", "收货回执"],
        "browseCode": [2, 3, 5],
        "name": "供应商用户"},
    3: {
        "edit": ["系统用户信息", "权限管理", "供应商档案", "采购入库单", "物料清单"],
        "editCode": [10, 11, 1, 6, 7],
        "browse": ["采购订单", "采购退货单", "物料清单", "材料运输单", "出库单", "预先发货清单", "收货回执"],
        "browseCode": [2, 3, 7, 4, 12, 8, 5],
        "name": "制单员"},
    4: {
        "edit": ["材料运输单", "运输调度单"],
        "editCode": [4, 13],
        "browse": ["采购订单", "采购入库单", "采购退货单", "出库单", "预先发货清单"],
        "browseCode": [2, 6, 3, 12, 8],
        "name": "运输调度员"},
    5: {
        "edit": ["采购入库单", "采购退货单", "物料清单", "出库单", "材料运输单", "出库单"],
        "editCode": [6, 3, 7, 12, 4, 12],
        "browse": ["采购订单", "预先发货清单", "运输调度单"],
        "browseCode": [2, 8, 13]},
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

        supplier_id = request.POST.get("supplier_id").strip()
        name = request.POST.get("name").strip()
        phone = request.POST.get("phone").strip()
        user_name = request.POST.get("user_name").strip()
        adress = request.POST.get("adress").strip()
        category = request.POST.get("category").strip()
        if supplier_id == "" or name == "" or phone == "" or user_name == "" or adress == "" or category == "":
            message = "参数不能为空"
            return render(request, 'supplier.html', locals())
        Supplier.objects.create(supplier_id=supplier_id, name=name, phone=phone, user_name=user_name, adress=adress,
                                category=category)

        return redirect("/supplier/")


class DeleteSupplierView(View):
    def get(self, request):
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
        supplier_id = request.POST.get("supplier_id").strip()
        name = request.POST.get("name").strip()
        phone = request.POST.get("phone").strip()
        user_name = request.POST.get("user_name").strip()
        adress = request.POST.get("adress").strip()
        category = request.POST.get("category").strip()

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




class PurshcaseOrderView(View):
    def get(self, request):
        isPermession=permissionFunc(request,2)
        if isPermession is None:
            return redirect("/login")
        keywords = request.GET.get("keyword", None)
        if keywords is None or keywords=="":
            resultlst = PurchaseOrder.objects.all()
        else:
            resultlst = PurchaseOrder.objects.filter(id=keywords)
        return render(request, 'PurshcaseOrder.html', locals())

    def post(self, request):
        isPermession = permissionFunc(request, 2)
        if isPermession is None:
            return redirect("/login")

        id = request.POST.get("id")
        Warehouse = request.POST.get("Warehouse").strip()
        supplier_id = request.POST.get("supplier_id").strip()
        supplier_name = request.POST.get("supplier_name").strip()
        goods_id = request.POST.get("goods_id").strip()
        goods_name = request.POST.get("goods_name").strip()
        Specification = request.POST.get("Specification").strip()
        unit_of_measurement = request.POST.get("unit_of_measurement").strip()
        unit_price = request.POST.get("unit_price").strip()
        num = request.POST.get("num").strip()
        channel = request.POST.get("channel").strip()
        code = request.POST.get("code").strip()
        if Warehouse == "" or supplier_id == "" or supplier_name == "" or goods_id == "" or goods_name == "" or \
                Specification == "" or unit_of_measurement=="" or unit_price=="" or num==""  or channel=="" or code=="":
            message = "参数不能为空"
            return render(request, 'PurshcaseOrder.html', locals())

        try:

            price=float(unit_price)*float(num)
        except:
            message = "单价必须为数字"
            return render(request, 'PurshcaseOrder.html', locals())
        PurchaseOrder.objects.create(id=id,warehouse=Warehouse, supplier_id=supplier_id, supplier_name=supplier_name, goods_id=goods_id,
                                goods_name=goods_name,Specification=Specification,unit_of_measurement=unit_of_measurement,
                                unit_price=unit_price,num=num,price=price,channel=channel,code=code)

        return redirect("/purshcaseorder/")


class DeletePurshcaseOrderView(View):
    def get(self, request):
        isPermession = permissionFunc(request, 2)
        if isPermession is None:
            return redirect("/login")
        id = request.GET.get("id", None)
        keyword = request.GET.get("keyword", None)
        PurchaseOrder.objects.get(id=id).delete()
        if keyword is None:
            return redirect("/purshcaseorder/")
        return redirect("/purshcaseorder/?keyword=" + keyword)


class EditPurshcaseOrderView(View):
    def get(self, request):
        isPermession = permissionFunc(request, 2)
        if isPermession is None:
            return redirect("/login")
        id = request.GET.get("id", None)
        purchaseOrder = PurchaseOrder.objects.get(id=id)
        keywords = request.GET.get("keyword", None)
        if keywords is None:
            resultlst = PurchaseOrder.objects.all()
        else:
            resultlst = PurchaseOrder.objects.filter(id=keywords)

        edit = True
        return render(request, 'PurshcaseOrder.html', locals())

    def post(self, request):
        isPermession = permissionFunc(request, 2)
        if isPermession is None:
            return redirect("/login")
        id = request.POST.get("id")
        Warehouse = request.POST.get("Warehouse").strip()
        supplier_id = request.POST.get("supplier_id").strip()
        supplier_name = request.POST.get("supplier_name").strip()
        goods_id = request.POST.get("goods_id").strip()
        goods_name = request.POST.get("goods_name").strip()
        Specification = request.POST.get("Specification").strip()
        unit_of_measurement = request.POST.get("unit_of_measurement").strip()
        unit_price = request.POST.get("unit_price").strip()
        num = request.POST.get("num").strip()
        channel = request.POST.get("channel").strip()
        code = request.POST.get("code").strip()
        keyword = request.GET.get("keyword", None)

        if Warehouse == "" or supplier_id == "" or supplier_name == "" or goods_id == "" or goods_name == "" or \
                Specification == "" or unit_of_measurement == "" or unit_price == "" or num == "" or channel == "" or code == "":
            message = "参数不能为空"

        try:

            price = float(unit_price) * float(num)
        except:
            message = "单价必须为数字"
            return render(request, 'PurshcaseOrder.html', locals())
        purchaseOrder = PurchaseOrder.objects.get(id=id)
        purchaseOrder.warehouse = Warehouse
        purchaseOrder.supplier_id = supplier_id
        purchaseOrder.supplier_name = supplier_name
        purchaseOrder.goods_id = goods_id
        purchaseOrder.goods_name = goods_name
        purchaseOrder.Specification = Specification
        purchaseOrder.unit_of_measurement = unit_of_measurement
        purchaseOrder.unit_price = unit_price
        purchaseOrder.num = num
        purchaseOrder.price = price
        purchaseOrder.channel = channel
        purchaseOrder.code = code
        purchaseOrder.save()
        if keyword is None:
            return redirect("/purshcaseorder/")
        return redirect("/purshcaseorder/?keyword=" + keyword)









class PurchaseReturnView(View):
    def get(self, request):
        isPermession=permissionFunc(request,3)
        if isPermession is None:
            return redirect("/login")
        keywords = request.GET.get("keyword", None)
        if keywords is None or keywords=="":
            resultlst = PurchaseReturn.objects.all()
        else:
            resultlst = PurchaseReturn.objects.filter(id=keywords)
        return render(request, 'purchaseReturn.html', locals())

    def post(self, request):
        isPermession = permissionFunc(request, 3)
        if isPermession is None:
            return redirect("/login")

        id = request.POST.get("id")
        warehouse = request.POST.get("warehouse").strip()
        goods_id = request.POST.get("goods_id").strip()
        goods_name = request.POST.get("goods_name").strip()
        Specification = request.POST.get("Specification").strip()
        unit_of_measurement = request.POST.get("unit_of_measurement").strip()
        unit_price = request.POST.get("unit_price").strip()
        num = request.POST.get("num").strip()

        if  goods_id == "" or goods_name == "" or \
                Specification == "" or unit_of_measurement=="" or unit_price=="" or num=="" :
            message = "参数不能为空"
            return render(request, 'PurchaseReturn.html', locals())

        try:

            price=float(unit_price)*float(num)
        except:
            message = "单价必须为数字"
            return render(request, 'PurchaseReturn.html', locals())
        PurchaseReturn.objects.create(id=id, goods_id=goods_id,warehouse=warehouse,
                                goods_name=goods_name,Specification=Specification,unit_of_measurement=unit_of_measurement,
                                unit_price=unit_price,num=num,price=price)

        return redirect("/purchasereturn/")


class DeletePurchaseReturnView(View):
    def get(self, request):
        isPermession = permissionFunc(request, 3)
        if isPermession is None:
            return redirect("/login")
        id = request.GET.get("id", None)
        keyword = request.GET.get("keyword", None)
        PurchaseReturn.objects.get(id=id).delete()
        if keyword is None:
            return redirect("/purchasereturn/")
        return redirect("/purchasereturn/?keyword=" + keyword)


class EditPurchaseReturnView(View):
    def get(self, request):
        isPermession = permissionFunc(request, 3)
        if isPermession is None:
            return redirect("/login")
        id = request.GET.get("id", None)
        purchaseReturn = PurchaseReturn.objects.get(id=id)
        keywords = request.GET.get("keyword", None)
        if keywords is None:
            resultlst = PurchaseReturn.objects.all()
        else:
            resultlst = PurchaseReturn.objects.filter(id=keywords)

        edit = True
        return render(request, 'PurchaseReturn.html', locals())

    def post(self, request):
        isPermession = permissionFunc(request, 3)
        if isPermession is None:
            return redirect("/login")
        id = request.POST.get("id")
        Warehouse = request.POST.get("warehouse").strip()

        goods_id = request.POST.get("goods_id").strip()
        goods_name = request.POST.get("goods_name").strip()
        Specification = request.POST.get("Specification").strip()
        unit_of_measurement = request.POST.get("unit_of_measurement").strip()
        unit_price = request.POST.get("unit_price").strip()
        num = request.POST.get("num").strip()

        keyword = request.GET.get("keyword", None)

        if Warehouse == ""  or goods_id == "" or goods_name == "" or \
                Specification == "" or unit_of_measurement == "" or unit_price == "" or num == "":
            message = "参数不能为空"

        try:

            price = float(unit_price) * float(num)
        except:
            message = "单价必须为数字"
            return render(request, 'PurchaseReturn.html', locals())
        purchaseReturn = PurchaseReturn.objects.get(id=id)
        purchaseReturn.warehouse = Warehouse

        purchaseReturn.goods_id = goods_id
        purchaseReturn.goods_name = goods_name
        purchaseReturn.Specification = Specification
        purchaseReturn.unit_of_measurement = unit_of_measurement
        purchaseReturn.unit_price = unit_price
        purchaseReturn.num = num
        purchaseReturn.price = price

        purchaseReturn.save()
        if keyword is None:
            return redirect("/purchasereturn/")
        return redirect("/purchasereturn/?keyword=" + keyword)






    #出库单
class OutboundOrderView(View):
    def get(self, request):
        isPermession=permissionFunc(request,12)
        if isPermession is None:
            return redirect("/login")
        keywords = request.GET.get("keyword", None)
        if keywords is None or keywords=="":
            resultlst = OutboundOrder.objects.all()
        else:
            resultlst = OutboundOrder.objects.filter(id=keywords)
        return render(request, 'outBoundOrder.html', locals())

    def post(self, request):
        isPermession = permissionFunc(request, 12)
        if isPermession is None:
            return redirect("/login")

        id = request.POST.get("id")

        warehouse = request.POST.get("warehouse").strip()
        goods_id = request.POST.get("goods_id").strip()
        goods_name = request.POST.get("goods_name").strip()
        Specification = request.POST.get("Specification").strip()
        unit_of_measurement = request.POST.get("unit_of_measurement").strip()
        num = request.POST.get("num").strip()
        location = request.POST.get("location").strip()

        if  goods_id == "" or goods_name == "" or location=="" or \
                Specification == "" or unit_of_measurement==""  or num=="" :
            message = "参数不能为空"
            return render(request, 'OutboundOrder.html', locals())


        OutboundOrder.objects.create(id=id, goods_id=goods_id,warehouse=warehouse,
                                goods_name=goods_name,Specification=Specification,unit_of_measurement=unit_of_measurement,
                              num=num,location=location)

        return redirect("/outboundorder/")


class DeleteOutboundOrderView(View):
    def get(self, request):
        isPermession = permissionFunc(request, 12)
        if isPermession is None:
            return redirect("/login")
        id = request.GET.get("id", None)
        keyword = request.GET.get("keyword", None)
        OutboundOrder.objects.get(id=id).delete()
        if keyword is None:
            return redirect("/outboundorder/")
        return redirect("/outboundorder/?keyword=" + keyword)


class EditOutboundOrderView(View):
    def get(self, request):
        isPermession = permissionFunc(request, 12)
        if isPermession is None:
            return redirect("/login")
        id = request.GET.get("id", None)
        outBoundOrder = OutboundOrder.objects.get(id=id)
        keywords = request.GET.get("keyword", None)
        if keywords is None:
            resultlst = OutboundOrder.objects.all()
        else:
            resultlst = OutboundOrder.objects.filter(id=keywords)

        edit = True
        return render(request, 'OutboundOrder.html', locals())

    def post(self, request):
        isPermession = permissionFunc(request, 12)
        if isPermession is None:
            return redirect("/login")
        id = request.POST.get("id")
        Warehouse = request.POST.get("warehouse").strip()
        goods_id = request.POST.get("goods_id").strip()
        goods_name = request.POST.get("goods_name").strip()
        Specification = request.POST.get("Specification").strip()
        unit_of_measurement = request.POST.get("unit_of_measurement").strip()
        num = request.POST.get("num").strip()
        location = request.POST.get("location").strip()


        keyword = request.GET.get("keyword", None)

        if Warehouse == ""  or goods_id == "" or goods_name == "" or location=="" or \
                Specification == "" or unit_of_measurement == ""  or num == "":
            message = "参数不能为空"
            return render(request, 'OutboundOrder.html', locals())

        outBoundOrder = OutboundOrder.objects.get(id=id)
        outBoundOrder.warehouse = Warehouse

        outBoundOrder.goods_id = goods_id
        outBoundOrder.goods_name = goods_name
        outBoundOrder.Specification = Specification
        outBoundOrder.unit_of_measurement = unit_of_measurement

        outBoundOrder.num = num

        outBoundOrder.save()
        if keyword is None:
            return redirect("/outboundorder/")
        return redirect("/outboundorder/?keyword=" + keyword)



#收货回执

class ReceiptView(View):
    def get(self, request):
        isPermession=permissionFunc(request,5)
        if isPermession is None:
            return redirect("/login")
        keywords = request.GET.get("keyword", None)
        if keywords is None:
            resultlst = Receipt.objects.all()
        else:
            resultlst = Receipt.objects.filter(id=keywords)
        return render(request, 'receipt.html', locals())

    def post(self, request):
        isPermession = permissionFunc(request, 5)
        if isPermession is None:
            return redirect("/login")

        id = request.POST.get("id")
        goods_id = request.POST.get("goods_id").strip()
        goods_name = request.POST.get("goods_name").strip()
        Specification = request.POST.get("Specification").strip()
        unit_of_measurement = request.POST.get("unit_of_measurement").strip()
        num = request.POST.get("num").strip()
        date=request.POST.get("date").strip()

        if  goods_id == "" or goods_name == "" or \
                Specification == "" or unit_of_measurement=="" or date=="" or num=="" :
            message = "参数不能为空"
            return render(request, 'Receipt.html', locals())


        Receipt.objects.create(id=id, goods_id=goods_id,
                                goods_name=goods_name,Specification=Specification,unit_of_measurement=unit_of_measurement,num=num,
                               date=date)

        return redirect("/receipt/")


class DeleteReceiptView(View):
    def get(self, request):
        isPermession = permissionFunc(request, 5)
        if isPermession is None:
            return redirect("/login")
        id = request.GET.get("id", None)
        keyword = request.GET.get("keyword", None)
        Receipt.objects.get(id=id).delete()
        if keyword is None:
            return redirect("/receipt/")
        return redirect("/receipt/?keyword=" + keyword)


class EditReceiptView(View):
    def get(self, request):
        isPermession = permissionFunc(request, 5)
        if isPermession is None:
            return redirect("/login")
        id = request.GET.get("id", None)
        receipt = Receipt.objects.get(id=id)
        keywords = request.GET.get("keyword", None)
        if keywords is None:
            resultlst = Receipt.objects.all()
        else:
            resultlst = Receipt.objects.filter(id=keywords)

        edit = True
        return render(request, 'Receipt.html', locals())

    def post(self, request):
        isPermession = permissionFunc(request, 5)
        if isPermession is None:
            return redirect("/login")
        id = request.POST.get("id")

        goods_id = request.POST.get("goods_id").strip()
        goods_name = request.POST.get("goods_name").strip()
        Specification = request.POST.get("Specification").strip()
        unit_of_measurement = request.POST.get("unit_of_measurement").strip()
        num = request.POST.get("num").strip()


        keyword = request.GET.get("keyword", None)

        if  goods_id == "" or goods_name == "" or \
                Specification == "" or unit_of_measurement == "" or num == "":
            message = "参数不能为空"


            return render(request, 'Receipt.html', locals())
        receipt = Receipt.objects.get(id=id)

        receipt.goods_id = goods_id
        receipt.goods_name = goods_name
        receipt.Specification = Specification
        receipt.unit_of_measurement = unit_of_measurement
        receipt.num = num

        receipt.save()
        if keyword is None:
            return redirect("/receipt/")
        return redirect("/receipt/?keyword=" + keyword)






class AdvancedShippingNoteView(View):
    def get(self, request):
        isPermession = permissionFunc(request, 8)
        if isPermession is None:
            return redirect("/login")
        keywords = request.GET.get("keyword", None)
        if keywords is None:
            resultlst = AdvancedShippingNote.objects.all()
        else:
            resultlst = AdvancedShippingNote.objects.filter(id=keywords)
        return render(request, 'advancedShippingNote.html', locals())

    def post(self, request):
        isPermession = permissionFunc(request, 8)
        if isPermession is None:
            return redirect("/login")




        id = request.POST.get("id")
        goods_id = request.POST.get("goods_id").strip()
        goods_name = request.POST.get("goods_name").strip()
        Specification = request.POST.get("Specification").strip()
        unit_of_measurement = request.POST.get("unit_of_measurement").strip()
        type_of_shipping = request.POST.get("type_of_shipping").strip()
        num = request.POST.get("num").strip()
        arrival_date = request.POST.get("arrival_date").strip()

        if goods_id == "" or goods_name == "" or \
                Specification == "" or unit_of_measurement == "" or type_of_shipping == "" or num == "" or arrival_date=="":
            message = "参数不能为空"
            return render(request, 'AdvancedShippingNote.html', locals())

        AdvancedShippingNote.objects.create(id=id, goods_id=goods_id,
                                            goods_name=goods_name, Specification=Specification,
                                            unit_of_measurement=unit_of_measurement,
                                            arrival_date=arrival_date, num=num, type_of_shipping=type_of_shipping)

        return redirect("/advancedShippingNote/")

class DeleteAdvancedShippingNoteView(View):
    def get(self, request):
        isPermession = permissionFunc(request, 8)
        if isPermession is None:
            return redirect("/login")
        id = request.GET.get("id", None)
        keyword = request.GET.get("keyword", None)
        AdvancedShippingNote.objects.get(id=id).delete()
        if keyword is None:
            return redirect("/advancedShippingNote/")
        return redirect("/advancedShippingNote/?keyword=" + keyword)

class EditAdvancedShippingNoteView(View):
    def get(self, request):
        isPermession = permissionFunc(request, 8)
        if isPermession is None:
            return redirect("/login")
        id = request.GET.get("id", None)
        advancedShippingNote = AdvancedShippingNote.objects.get(id=id)
        keywords = request.GET.get("keyword", None)
        if keywords is None:
            resultlst = AdvancedShippingNote.objects.all()
        else:
            resultlst = AdvancedShippingNote.objects.filter(id=keywords)

        edit = True
        return render(request, 'AdvancedShippingNote.html', locals())

    def post(self, request):
        isPermession = permissionFunc(request, 8)
        if isPermession is None:
            return redirect("/login")

        id = request.POST.get("id")
        goods_id = request.POST.get("goods_id").strip()
        goods_name = request.POST.get("goods_name").strip()
        Specification = request.POST.get("Specification").strip()
        unit_of_measurement = request.POST.get("unit_of_measurement").strip()
        type_of_shipping = request.POST.get("type_of_shipping").strip()
        num = request.POST.get("num").strip()

        keyword = request.GET.get("keyword", None)

        if goods_id == "" or goods_name == "" or \
                Specification == "" or unit_of_measurement == "" or type_of_shipping == "" or num == "":
            message = "参数不能为空"
            return render(request, 'AdvancedShippingNote.html', locals())

        advancedShippingNote = AdvancedShippingNote.objects.get(id=id)

        advancedShippingNote.goods_id = goods_id
        advancedShippingNote.goods_name = goods_name
        advancedShippingNote.Specification = Specification
        advancedShippingNote.unit_of_measurement = unit_of_measurement
        advancedShippingNote.type_of_shipping = type_of_shipping
        advancedShippingNote.num = num

        advancedShippingNote.save()
        if keyword is None:
            return redirect("/advancedShippingNote/")
        return redirect("/advancedShippingNote/?keyword=" + keyword)
















class PurchaseReceiptView(View):
    def get(self, request):
        isPermession=permissionFunc(request,6)
        if isPermession is None:
            return redirect("/login")
        keywords = request.GET.get("keyword", None)
        if keywords is None:
            resultlst = PurchaseReceipt.objects.all()
        else:
            resultlst = PurchaseReceipt.objects.filter(id=keywords)
        return render(request, 'purchaseReceipt.html', locals())

    def post(self, request):
        isPermession = permissionFunc(request, 6)
        if isPermession is None:
            return redirect("/login")

        id = request.POST.get("id")
        Warehouse = request.POST.get("Warehouse").strip()

        goods_id = request.POST.get("goods_id").strip()
        goods_name = request.POST.get("goods_name").strip()
        Specification = request.POST.get("Specification").strip()
        unit_of_measurement = request.POST.get("unit_of_measurement").strip()
        unit_price = request.POST.get("unit_price").strip()
        num = request.POST.get("num").strip()
        channel = request.POST.get("channel").strip()
        code = request.POST.get("code").strip()
        location = request.POST.get("location").strip()
        if Warehouse == "" or location == ""  or goods_id == "" or goods_name == "" or \
                Specification == "" or unit_of_measurement == "" or unit_price == "" or num == "" or channel == "" or code == "":
            message = "参数不能为空"
            return render(request, 'PurchaseReceipt.html', locals())

        try:

            price=float(unit_price)*float(num)
        except:
            message = "单价必须为数字"
            return render(request, 'PurchaseReceipt.html', locals())


        PurchaseReceipt.objects.create(id=id,warehouse=Warehouse,goods_id=goods_id,
                                goods_name=goods_name,Specification=Specification,unit_of_measurement=unit_of_measurement,
                                unit_price=unit_price,num=num,price=price,channel=channel,code=code,location=location)

        return redirect("/purchaseReceipt/")


class DeletePurchaseReceiptView(View):
    def get(self, request):
        isPermession = permissionFunc(request, 6)
        if isPermession is None:
            return redirect("/login")
        id = request.GET.get("id", None)
        keyword = request.GET.get("keyword", None)
        PurchaseReceipt.objects.get(id=id).delete()
        if keyword is None:
            return redirect("/purchaseReceipt/")
        return redirect("/purchaseReceipt/?keyword=" + keyword)


class EditPurchaseReceiptView(View):
    def get(self, request):
        isPermession = permissionFunc(request, 6)
        if isPermession is None:
            return redirect("/login")
        id = request.GET.get("id", None)
        purchaseReceipt = PurchaseReceipt.objects.get(id=id)
        keywords = request.GET.get("keyword", None)
        if keywords is None:
            resultlst = PurchaseReceipt.objects.all()
        else:
            resultlst = PurchaseReceipt.objects.filter(id=keywords)

        edit = True
        return render(request, 'PurchaseReceipt.html', locals())

    def post(self, request):
        isPermession = permissionFunc(request, 6)
        if isPermession is None:
            return redirect("/login")
        id = request.POST.get("id")
        Warehouse = request.POST.get("Warehouse").strip()

        goods_id = request.POST.get("goods_id").strip()
        goods_name = request.POST.get("goods_name").strip()
        Specification = request.POST.get("Specification").strip()
        unit_of_measurement = request.POST.get("unit_of_measurement").strip()
        unit_price = request.POST.get("unit_price").strip()
        num = request.POST.get("num").strip()
        channel = request.POST.get("channel").strip()
        code = request.POST.get("code").strip()
        location = request.POST.get("location").strip()
        if Warehouse == "" or location == "" or goods_id == "" or goods_name == "" or \
                Specification == "" or unit_of_measurement == "" or unit_price == "" or num == "" or channel == "" or code == "":
            message = "参数不能为空"
            return render(request, 'PurchaseReceipt.html', locals())

        keyword = request.GET.get("keyword", None)


        try:

            price = float(unit_price) * float(num)
        except:
            message = "单价必须为数字"
            return render(request, 'PurchaseReceipt.html', locals())
        purchaseReceipt = PurchaseReceipt.objects.get(id=id)
        purchaseReceipt.warehouse = Warehouse

        purchaseReceipt.goods_id = goods_id
        purchaseReceipt.goods_name = goods_name
        purchaseReceipt.Specification = Specification
        purchaseReceipt.unit_of_measurement = unit_of_measurement
        purchaseReceipt.unit_price = unit_price
        purchaseReceipt.num = num
        purchaseReceipt.price = price
        purchaseReceipt.location = location
        purchaseReceipt.channel=channel
        purchaseReceipt.code=code

        purchaseReceipt.save()
        if keyword is None:
            return redirect("/purchaseReceipt/")
        return redirect("/purchaseReceipt/?keyword=" + keyword)






class BillOfMaterialsView(View):
    def get(self, request):
        isPermession=permissionFunc(request,7)
        if isPermession is None:
            return redirect("/login")
        keywords = request.GET.get("keyword", None)
        if keywords is None:
            resultlst = BillOfMaterials.objects.all()
        else:
            resultlst = BillOfMaterials.objects.filter(id=keywords)
        return render(request, 'billOfMaterials.html', locals())

    def post(self, request):
        isPermession = permissionFunc(request, 7)
        if isPermession is None:
            return redirect("/login")



        id = request.POST.get("id")
        warehouse = request.POST.get("warehouse").strip()
        warehouse_admin = request.POST.get("warehouse_admin").strip()
        goods_name = request.POST.get("goods_name").strip()
        Specification = request.POST.get("Specification").strip()
        unit_of_measurement = request.POST.get("unit_of_measurement").strip()
        num = request.POST.get("num").strip()
        code = request.POST.get("code").strip()
        channel=request.POST.get("channel").strip()

        if  id=="" or goods_name == "" or warehouse_admin=="" or code =="" or channel=="" or \
                Specification == "" or unit_of_measurement=="" or warehouse=="" or num=="" :
            message = "参数不能为空"
            return render(request, 'BillOfMaterials.html', locals())

        BillOfMaterials.objects.create(id=id, warehouse=warehouse,warehouse_admin=warehouse_admin,channel=channel,
                                goods_name=goods_name,Specification=Specification,unit_of_measurement=unit_of_measurement,num=num,code=code)

        return redirect("/billOfMaterials/")


class DeleteBillOfMaterialsView(View):
    def get(self, request):
        isPermession = permissionFunc(request, 7)
        if isPermession is None:
            return redirect("/login")
        id = request.GET.get("id", None)
        keyword = request.GET.get("keyword", None)
        BillOfMaterials.objects.get(id=id).delete()
        if keyword is None:
            return redirect("/billOfMaterials/")
        return redirect("/billOfMaterials/?keyword=" + keyword)


class EditBillOfMaterialsView(View):
    def get(self, request):
        isPermession = permissionFunc(request, 7)
        if isPermession is None:
            return redirect("/login")
        id = request.GET.get("id", None)
        billOfMaterials = BillOfMaterials.objects.get(id=id)
        keywords = request.GET.get("keyword", None)
        if keywords is None:
            resultlst = BillOfMaterials.objects.all()
        else:
            resultlst = BillOfMaterials.objects.filter(id=keywords)

        edit = True
        return render(request, 'BillOfMaterials.html', locals())

    def post(self, request):
        isPermession = permissionFunc(request, 7)
        if isPermession is None:
            return redirect("/login")
        id = request.POST.get("id")
        warehouse = request.POST.get("warehouse").strip()
        warehouse_admin = request.POST.get("warehouse_admin").strip()
        goods_name = request.POST.get("goods_name").strip()
        Specification = request.POST.get("Specification").strip()
        unit_of_measurement = request.POST.get("unit_of_measurement").strip()
        num = request.POST.get("num").strip()
        code = request.POST.get("code").strip()
        channel = request.POST.get("channel").strip()

        if  goods_name == "" or warehouse_admin=="" or code =="" or \
                Specification == "" or unit_of_measurement=="" or warehouse=="" or num=="" :
            message = "参数不能为空"
            return render(request, 'BillOfMaterials.html', locals())

        keyword = request.GET.get("keyword", None)


        billOfMaterials = BillOfMaterials.objects.get(id=id)
        billOfMaterials.warehouse = warehouse
        billOfMaterials.warehouse_admin = warehouse_admin

        billOfMaterials.goods_name = goods_name
        billOfMaterials.Specification = Specification
        billOfMaterials.unit_of_measurement = unit_of_measurement
        billOfMaterials.num = num
        billOfMaterials.code = code
        billOfMaterials.channel=channel

        billOfMaterials.save()
        if keyword is None:
            return redirect("/billOfMaterials/")
        return redirect("/billOfMaterials/?keyword=" + keyword)









class TransportationDispatchView(View):
    def get(self, request):
        isPermession=permissionFunc(request,13)
        if isPermession is None:
            return redirect("/login")
        keywords = request.GET.get("keyword", None)
        if keywords is None:
            resultlst = TransportationDispatch.objects.all()
        else:
            resultlst = TransportationDispatch.objects.filter(id=keywords)
        return render(request, 'transportationDispatch.html', locals())

    def post(self, request):
        isPermession = permissionFunc(request, 13)
        if isPermession is None:
            return redirect("/login")



        id = request.POST.get("id")
        goods_name = request.POST.get("goods_name").strip()
        start_point = request.POST.get("start_point").strip()
        end_point = request.POST.get("end_point").strip()
        unit_of_measurement = request.POST.get("unit_of_measurement").strip()
        num = request.POST.get("num").strip()
        mileage = request.POST.get("mileage").strip()
        accepted_by = request.POST.get("accepted_by").strip()
        date = request.POST.get("date").strip()

        if  id == "" or goods_name == "" or mileage=="" or accepted_by=="" or date=="" or\
                start_point == "" or unit_of_measurement=="" or end_point=="" or num=="" :
            message = "参数不能为空"
            return render(request, 'TransportationDispatch.html', locals())


        TransportationDispatch.objects.create(id=id, start_point=start_point,end_point=end_point,
                                goods_name=goods_name,mileage=mileage,unit_of_measurement=unit_of_measurement,
                                              accepted_by=accepted_by,num=num,date=date)

        return redirect("/transportationDispatch/")


class DeleteTransportationDispatchView(View):
    def get(self, request):
        isPermession = permissionFunc(request, 13)
        if isPermession is None:
            return redirect("/login")
        id = request.GET.get("id", None)
        keyword = request.GET.get("keyword", None)
        TransportationDispatch.objects.get(id=id).delete()
        if keyword is None:
            return redirect("/transportationDispatch/")
        return redirect("/transportationDispatch/?keyword=" + keyword)


class EditTransportationDispatchView(View):
    def get(self, request):
        isPermession = permissionFunc(request, 13)
        if isPermession is None:
            return redirect("/login")
        id = request.GET.get("id", None)
        transportationDispatch = TransportationDispatch.objects.get(id=id)
        keywords = request.GET.get("keyword", None)
        if keywords is None:
            resultlst = TransportationDispatch.objects.all()
        else:
            resultlst = TransportationDispatch.objects.filter(id=keywords)

        edit = True
        return render(request, 'TransportationDispatch.html', locals())

    def post(self, request):
        isPermession = permissionFunc(request, 13)
        if isPermession is None:
            return redirect("/login")

        id = request.POST.get("id")
        goods_name = request.POST.get("goods_name").strip()
        start_point = request.POST.get("start_point").strip()
        end_point = request.POST.get("end_point").strip()
        unit_of_measurement = request.POST.get("unit_of_measurement").strip()
        num = request.POST.get("num").strip()
        mileage = request.POST.get("mileage").strip()
        accepted_by = request.POST.get("accepted_by").strip()

        if  goods_name == "" or mileage == "" or accepted_by == ""  or \
                start_point == "" or unit_of_measurement == "" or end_point == "" or num == "":
            message = "参数不能为空"
            return render(request, 'TransportationDispatch.html', locals())
        keyword = request.GET.get("keyword", None)

        transportationDispatch = TransportationDispatch.objects.get(id=id)


        transportationDispatch.id = id

        transportationDispatch.goods_name = goods_name
        transportationDispatch.start_point = start_point
        transportationDispatch.end_point = end_point
        transportationDispatch.mileage = mileage
        transportationDispatch.unit_of_measurement = unit_of_measurement
        transportationDispatch.accepted_by = accepted_by
        transportationDispatch.num = num

        transportationDispatch.save()
        if keyword is None:
            return redirect("/transportationDispatch/")
        return redirect("/transportationDispatch/?keyword=" + keyword)




class MaterialTransportationListView(View):
    def get(self, request):
        isPermession=permissionFunc(request,4)


        if isPermession is None:
            return redirect("/login")
        keywords = request.GET.get("keyword", None)
        if keywords is None:
            resultlst = MaterialTransportationList.objects.all()
        else:
            resultlst = MaterialTransportationList.objects.filter(id=keywords)
        user = request.session["user"]
        position=user['position']
        return render(request, 'materialTransportationList.html', locals())

    def post(self, request):
        isPermession = permissionFunc(request, 4)
        if isPermession is None:
            return redirect("/login")




        id = request.POST.get("id")
        goods_name = request.POST.get("goods_name").strip()
        Specification = request.POST.get("Specification").strip()
        unit_of_measurement = request.POST.get("unit_of_measurement").strip()
        num = request.POST.get("num").strip()
        collection_center = request.POST.get("collection_center").strip()
        inspection_and_warehousing = request.POST.get("inspection_and_warehousing").strip()
        in_warehousing = request.POST.get("in_warehousing").strip()
        Warehouse = request.POST.get("Warehouse").strip()
        re_out_warehousing = request.POST.get("re_out_warehousing").strip()
        out_warehousing = request.POST.get("out_warehousing").strip()
        loading_and_distribution = request.POST.get("loading_and_distribution").strip()
        car_num = request.POST.get("car_num").strip()
        arrival_station = request.POST.get("arrival_station").strip()
        confirm_receipt = request.POST.get("confirm_receipt").strip()

        if  id == "" or goods_name == "" or \
                Specification == "" or unit_of_measurement==""  or num=="" :
            message = "参数不能为空"
            user = request.session["user"]
            position = user['position']
            return render(request, 'MaterialTransportationList.html', locals())
        MaterialTransportationList.objects.create(id=id, goods_name=goods_name,Specification=Specification,
                                                  unit_of_measurement=unit_of_measurement,num=num,
                                                  collection_center=collection_center,inspection_and_warehousing=inspection_and_warehousing,
                                                  in_warehousing=in_warehousing,Warehouse=Warehouse,out_warehousing=out_warehousing,
                                                  re_out_warehousing=re_out_warehousing,loading_and_distribution=loading_and_distribution,
                                                  car_num=car_num,arrival_station=arrival_station,confirm_receipt=confirm_receipt)

        return redirect("/materialTransportationList/")


class DeleteMaterialTransportationListView(View):
    def get(self, request):
        isPermession = permissionFunc(request, 4)
        if isPermession is None:
            return redirect("/login")
        id = request.GET.get("id", None)
        keyword = request.GET.get("keyword", None)
        MaterialTransportationList.objects.get(id=id).delete()
        if keyword is None:
            return redirect("/materialTransportationList/")
        return redirect("/materialTransportationList/?keyword=" + keyword)


class EditMaterialTransportationListView(View):
    def get(self, request):
        isPermession = permissionFunc(request, 4)
        if isPermession is None:
            return redirect("/login")
        id = request.GET.get("id", None)
        materialTransportationList = MaterialTransportationList.objects.get(id=id)
        keywords = request.GET.get("keyword", None)
        if keywords is None:
            resultlst = MaterialTransportationList.objects.all()
        else:
            resultlst = MaterialTransportationList.objects.filter(id=keywords)

        edit = True
        user = request.session["user"]
        position = user['position']
        return render(request, 'MaterialTransportationList.html', locals())

    def post(self, request):
        isPermession = permissionFunc(request, 4)
        if isPermession is None:
            return redirect("/login")
        id = request.POST.get("id")
        goods_name = request.POST.get("goods_name").strip()
        Specification = request.POST.get("Specification").strip()
        unit_of_measurement = request.POST.get("unit_of_measurement").strip()
        num = request.POST.get("num").strip()
        collection_center = request.POST.get("collection_center").strip()
        inspection_and_warehousing = request.POST.get("inspection_and_warehousing").strip()
        in_warehousing = request.POST.get("in_warehousing").strip()
        Warehouse = request.POST.get("Warehouse").strip()
        re_out_warehousing = request.POST.get("re_out_warehousing").strip()
        out_warehousing = request.POST.get("out_warehousing").strip()
        loading_and_distribution = request.POST.get("loading_and_distribution").strip()
        car_num = request.POST.get("car_num").strip()
        arrival_station = request.POST.get("arrival_station").strip()
        confirm_receipt = request.POST.get("confirm_receipt").strip()

        keyword = request.GET.get("keyword", None)


        if  id == "" or goods_name == "" or \
                Specification == "" or unit_of_measurement==""  or num=="" :
            message = "参数不能为空"
            user = request.session["user"]
            position = user['position']
            return render(request, 'MaterialTransportationList.html', locals())
        materialTransportationList = MaterialTransportationList.objects.get(id=id)


        materialTransportationList.goods_name = goods_name
        materialTransportationList.unit_of_measurement = unit_of_measurement
        materialTransportationList.Specification = Specification
        materialTransportationList.collection_center = collection_center
        materialTransportationList.inspection_and_warehousing = inspection_and_warehousing
        materialTransportationList.num = num
        materialTransportationList.in_warehousing = in_warehousing
        materialTransportationList.Warehouse = Warehouse
        materialTransportationList.re_out_warehousing = re_out_warehousing
        materialTransportationList.out_warehousing = out_warehousing
        materialTransportationList.loading_and_distribution = loading_and_distribution
        materialTransportationList.car_num = car_num
        materialTransportationList.arrival_station = arrival_station
        materialTransportationList.confirm_receipt = confirm_receipt

        materialTransportationList.save()
        if keyword is None:
            return redirect("/materialTransportationList/")
        return redirect("/materialTransportationList/?keyword=" + keyword)