"""control URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from user.views import *
from mainApp.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', LoginView.as_view()),
    path('', IndexView.as_view()),
    path('supplier/', SupplierView.as_view()),
    path('supplier/delete', DeleteSupplierView.as_view()),
    path('supplier/edit', EditSupplierView.as_view()),

    path('purshcaseorder/', PurshcaseOrderView.as_view()),
    path('purshcaseorder/delete', DeletePurshcaseOrderView.as_view()),
    path('purshcaseorder/edit', EditPurshcaseOrderView.as_view()),

    path('purchasereturn/', PurchaseReturnView.as_view()),
    path('purchasereturn/delete', DeletePurchaseReturnView.as_view()),
    path('purchasereturn/edit', EditPurchaseReturnView.as_view()),

    path('outboundorder/', OutboundOrderView.as_view()),
    path('outboundorder/delete', DeleteOutboundOrderView.as_view()),
    path('outboundorder/edit', EditOutboundOrderView.as_view()),

    path('receipt/', ReceiptView.as_view()),
    path('receipt/delete', DeleteReceiptView.as_view()),
    path('receipt/edit', EditReceiptView.as_view()),

    path('advancedShippingNote/', AdvancedShippingNoteView.as_view()),
    path('advancedShippingNote/delete', DeleteAdvancedShippingNoteView.as_view()),
    path('advancedShippingNote/edit', EditAdvancedShippingNoteView.as_view()),

    path('purchaseReceipt/', PurchaseReceiptView.as_view()),
    path('purchaseReceipt/delete', DeletePurchaseReceiptView.as_view()),
    path('purchaseReceipt/edit', EditPurchaseReceiptView.as_view()),

    path('billOfMaterials/', BillOfMaterialsView.as_view()),
    path('billOfMaterials/delete', DeleteBillOfMaterialsView.as_view()),
    path('billOfMaterials/edit', EditBillOfMaterialsView.as_view()),




    path('transportationDispatch/', TransportationDispatchView.as_view()),
    path('transportationDispatch/delete', DeleteTransportationDispatchView.as_view()),
    path('transportationDispatch/edit', EditTransportationDispatchView.as_view()),

    path('materialTransportationList/', MaterialTransportationListView.as_view()),
    path('materialTransportationList/delete', DeleteMaterialTransportationListView.as_view()),
    path('materialTransportationList/edit', EditMaterialTransportationListView.as_view()),

    path('user/', UserView.as_view()),
    path('user/delete', DeleteUserView.as_view()),
    path('user/edit', EditUserView.as_view()),
    path('depart/', DepartView.as_view()),

]
