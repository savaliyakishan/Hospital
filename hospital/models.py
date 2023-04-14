from django.db import models
from django.contrib.auth.models import AbstractUser
from .models import *
from datetime import datetime

class Lillnes(models.Model):
    lillne_id=models.AutoField(db_column="Illnes_Id",primary_key=True)
    lillne_name=models.CharField(db_column="Illness_name",max_length=255,default=None,unique=True)

class room(models.Model):
    roomId=models.AutoField(db_column="Room_ID",primary_key=True)
    roomType=models.CharField(db_column="Room_Type",max_length=255,unique=True)
    roomPrice = models.IntegerField(db_column="Room_Price",blank=True,null=True)
    
    def __str__(self) :
        return '{} {} {}'.format(self.roomType,self.roomId,self.roomPrice)

 
class User(AbstractUser):
    lillness = models.ForeignKey(Lillnes,on_delete=models.CASCADE,blank=True,null=True,db_column="Illnes_Id")
    room=models.ForeignKey(room,on_delete=models.CASCADE,blank=True,null=True,db_column='Room_Id')
    medicines=models.TextField(db_column="Medicines",blank=True,null=True)
    fess = models.IntegerField(db_column="Fess",blank=True,null=True)
    category = models.CharField(db_column="Category",max_length=255,blank=True,null=True)
    phone = models.BigIntegerField(db_column="Phone",blank=True,null=True)
    img = models.ImageField(upload_to='img',blank=True,null=True,db_column="User_Img")
    doctor_id = models.IntegerField(db_column="Doctor_Id",blank=True,null=True)
    staff_id = models.IntegerField(db_column="Staff_Id",blank=True,null=True)
    check_out_status = models.CharField(db_column="Check_Out",default=False,max_length=255)
    user_bed = models.IntegerField(db_column="Bed_Id",blank=True,null=True)
    user_bills = models.IntegerField(db_column='Total_Bills',blank=True,null=True)

class Medicines(models.Model):
    medicinesId=models.AutoField(db_column="Medicines_Id",primary_key=True)
    lillness = models.ForeignKey(Lillnes,on_delete=models.CASCADE,blank=True,null=True)
    medicinesName=models.CharField(db_column='Medicines_Name',max_length=255,unique=True)
    medicinesPrice=models.IntegerField(db_column='Medicines_Price')
    medicinesQuantity=models.IntegerField(db_column='Medicines_Quantity')

    def __str__(self) :
        return '{} {} {} {} {}'.format(self.medicinesId,self.lillness,self.medicinesPrice,self.medicinesQuantity,self.medicinesName)

class bed(models.Model):
    bedId=models.AutoField(db_column='Bed_Id',primary_key=True)
    bedStatus=models.CharField(db_column='Bed_Status',max_length=255, default=False)
    roomId=models.ForeignKey(room,on_delete=models.CASCADE,db_column='Room_Id')
    user_id=models.ForeignKey(User,on_delete=models.CASCADE,blank=True,null=True,db_column='User_Id')
    
    def __str__(self) :
        return self.bedId,self.bedStatus,self.roomId,self.user_id

