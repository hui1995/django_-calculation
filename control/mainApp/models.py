from django.db import models

# Create your models here.
class Supplier(models.Model):
    supplier_id=models.CharField(max_length=10)
    name=models.CharField(max_length=20)
    phone=models.CharField(max_length=11)
    user_name=models.CharField(max_length=20)
    adress=models.TextField()
    category=models.CharField(max_length=20)

class PurchaseOrder(models.Model):
    Warehouse=models.CharField(max_length=10)
    supplier_id=models.IntegerField
    supplier_name=models.CharField(max_length=20)
    goods_id=models.CharField(max_length=10)
    goods_name=models.CharField(max_length=20)
    Specification=models.CharField(max_length=20)
    unit_of_measurement=models.CharField(max_length=6)
    unit_price=models.DecimalField(max_digits=20,decimal_places=2)
    num=models.FloatField(max_length=20)
    price=models.DecimalField(max_digits=20,decimal_places=2)
    channel=models.CharField(max_length=20)
    code=models.CharField(max_length=6)


class PurchaseReceipt(models.Model):
    Warehouse=models.CharField(max_length=10)
    goods_id = models.CharField(max_length=10)
    goods_name = models.CharField(max_length=20)
    Specification = models.CharField(max_length=20)
    unit_of_measurement = models.CharField(max_length=6)
    unit_price = models.DecimalField(max_digits=20,decimal_places=2)
    num = models.FloatField(max_length=20)
    price = models.DecimalField(max_digits=20,decimal_places=2)
    location = models.CharField(max_length=20)
    channel=models.CharField(max_length=20)
    code=models.CharField(max_length=6)



class PurchaseReturn(models.Model):
    Warehouse=models.CharField(max_length=10)
    goods_id = models.CharField(max_length=10)
    goods_name = models.CharField(max_length=20)
    Specification = models.CharField(max_length=20)
    unit_of_measurement = models.CharField(max_length=6)
    unit_price = models.DecimalField(max_digits=20,decimal_places=2)
    num = models.FloatField(max_length=20)
    price = models.DecimalField(max_digits=20,decimal_places=2)


class BillOfMaterials(models.Model):
    goods_id = models.CharField(max_length=10)
    goods_name = models.CharField(max_length=20)
    channel=models.CharField(max_length=20)
    Specification = models.CharField(max_length=20)
    unit_of_measurement = models.CharField(max_length=6)
    num = models.FloatField(max_length=20)
    warehouse=models.CharField(max_length=10)
    warehouse_admin=models.CharField(max_length=10)
    code=models.CharField(max_length=6)


class MaterialTransportationList(models.Model):
    goods_id = models.CharField(max_length=10)
    goods_name = models.CharField(max_length=20)
    Specification = models.CharField(max_length=20)
    unit_of_measurement = models.CharField(max_length=6)
    num = models.FloatField(max_length=20)
    collection_center=models.CharField(max_length=6)
    inspection_and_warehousing=models.CharField(max_length=6)
    in_warehousing=models.CharField(max_length=6)
    Warehouse=models.CharField(max_length=10)
    re_out_warehousing=models.CharField(max_length=6)
    out_warehousing=models.CharField(max_length=6)
    loading_and_distribution=models.CharField(max_length=6)
    car_num=models.CharField(max_length=6)
    arrival_station=models.CharField(max_length=6)
    confirm_receipt=models.CharField(max_length=6)



class AdvancedShippingNote(models.Model):
    goods_id = models.CharField(max_length=10)
    goods_name = models.CharField(max_length=20)
    Specification = models.CharField(max_length=20)
    unit_of_measurement = models.CharField(max_length=6)
    num = models.FloatField(max_length=20)
    type_of_shipping=models.CharField(max_length=10)
    arrival_date=models.DateTimeField()



class TransportationDispatch(models.Model):
    goods_id = models.CharField(max_length=10)
    goods_name = models.CharField(max_length=20)
    start_point=models.CharField(max_length=50)
    end_point=models.CharField(max_length=50)
    unit_of_measurement = models.CharField(max_length=6)
    num = models.FloatField(max_length=20)
    mileage=models.FloatField(max_length=20)
    accepted_by= models.CharField(max_length=20)
    date=models.DateTimeField()


class OutboundOrder(models.Model):
    warehouse=models.CharField(max_length=10)
    goods_id = models.CharField(max_length=10)
    goods_name = models.CharField(max_length=20)
    Specification = models.CharField(max_length=20)
    unit_of_measurement = models.CharField(max_length=6)
    num = models.FloatField(max_length=20)
    location= models.CharField(max_length=20)



class Receipt(models.Model):
    goods_id = models.CharField(max_length=10)
    goods_name = models.CharField(max_length=20)
    Specification = models.CharField(max_length=20)
    unit_of_measurement = models.CharField(max_length=6)
    num = models.FloatField(max_length=20)
    date=models.DateTimeField()






















