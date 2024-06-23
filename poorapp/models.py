from django.db import models 
from ckeditor.fields import RichTextField

# Create your models here.

class HelpCategory(models.Model):
    category_name = models.CharField(max_length=50) 
    
    def __str__(self):
        return self.category_name



class PaymentType(models.Model):
    payment_type = models.CharField(max_length=50)
    status       = models.BooleanField(default=True)

    def __str__(self):
        return self.payment_type
    

class VerifiedDocument(models.Model):
    document_type = models.CharField(max_length=50)

    def __str__(self):
        return self.document_type
    
    
class ApplicantProffession(models.Model):
    proffession_type = models.CharField(max_length=50)

    def __str__(self):
        return self.proffession_type
    
class FatherProffession(models.Model):
    proffession_type = models.CharField(max_length=50)

    def __str__(self):
        return self.proffession_type

class DistrictList(models.Model):
    district_name = models.CharField(max_length=100)   

    def __str__(self):
        return self.district_name
    

class CityList(models.Model):
    district    = models.ForeignKey(DistrictList, on_delete=models.CASCADE)
    city_name   = models.CharField(max_length=100)

    def __str__(self):
        return self.city_name
    

class Receivers(models.Model):  
    
    name                    = models.CharField(max_length=150)
    email                   = models.EmailField(max_length=150, blank=True)
    mobile_number           = models.IntegerField()
    password                = models.CharField(max_length = 30, default="123456")
    aplicant_proffessions   = models.ForeignKey('ApplicantProffession', on_delete=models.CASCADE)
    gender_list = (
        ('F','Female'),
        ('M','Male'),
        ('O','Other')
    )
    aplicant_gender         = models.CharField(max_length=1,default = 1,choices=gender_list)
    aplicant_age            = models.IntegerField(default=30)
    image                   = models.ImageField(upload_to='uploads/')
    father_name             = models.CharField(max_length=150)
    father_proffession      = models.ForeignKey('FatherProffession', on_delete=models.CASCADE)
    father_contact_number   = models.IntegerField()
    mother_name             = models.CharField(max_length=150)
    help_type               = models.ForeignKey('HelpCategory', on_delete=models.CASCADE)
    amount                  = models.IntegerField()
    amount_received         = models.IntegerField(default=0) 
    require_date            = models.DateField()
    city_name               = models.ForeignKey(CityList, on_delete= models.CASCADE)
    district_name           = models.ForeignKey(DistrictList, on_delete= models.CASCADE)
    post_code               = models.CharField(max_length=20)
    address                 = models.TextField(max_length=500)
    payment_type            = models.ForeignKey('PaymentType', on_delete=models.CASCADE, default=0,null=True)
    payment_type_account    = models.IntegerField(blank=True,null=True) 
    identity_document_lists = (
        ('DL','Driving License'),
        ('PP','Passport'),
        ('NC','NID Card'),
        ('BC','Birth Certificate'),
    )
    identity_doc_type       = models.CharField(max_length=2, choices=identity_document_lists)
    identity_doc            = models.ImageField(upload_to='uploads/')
    identity_doc_number     = models.IntegerField(blank=True)  
    document_file_one       = models.ImageField(upload_to='uploads/', blank=True)
    problem_description     = RichTextField(blank=True,null=True)
    status                  = models.BooleanField(default=False)
    complete_status         = models.BooleanField(default=False)
    timestamp               = models.DateField(auto_now_add=True, auto_now=False)
    update                  = models.DateField(auto_now=True, auto_now_add=False)
    # ------------clothing------------
    cloth_count             = models.IntegerField(default=0);
    cloth_size              = models.CharField(max_length=200,default='0');
    # ------------education------------
    edu_items               = models.CharField(max_length=300,default='');
    # ---------food-----------
    food_quantity           = models.IntegerField(default=0);
    food_time               = models.CharField(max_length=200,null=True, blank=True);
    

    def __str__(self):
        return self.name

class PermessionCheck(models.Model):
    user = models.ForeignKey(Receivers, on_delete=models.CASCADE)
    view_action = models.BooleanField(default=False)
    delete_action = models.BooleanField(default = False)
    update_action = models.BooleanField(default = False)
    insert_action = models.BooleanField(default = False)


class Doner(models.Model):
    doner_name      = models.CharField(max_length = 120)
    gender_list = (
        ('F','Female'),
        ('M','Male'),
        ('O','Other')
    )
    doner_gender    = models.CharField(max_length=1,choices=gender_list, null=True)
    doner_age       = models.IntegerField(null=True,blank=True)
    doner_phone     = models.CharField(max_length=15)
    doner_email     = models.EmailField(max_length=50,blank=True)
    doner_pass      = models.CharField(max_length = 300)
    doner_image     = models.ImageField(upload_to='uploads/',blank = True)
    joining_date    = models.DateField(auto_now=False, auto_now_add=True) 
    district_name   = models.ForeignKey(DistrictList, on_delete= models.CASCADE)
    city_name       = models.ForeignKey(CityList, on_delete= models.CASCADE)
    status          = models.BooleanField(default=False)
    complete        = models.BooleanField(default=False)
    request         = models.BooleanField(default=False)
    
    
    
    def __str__(self):
        return self.doner_name
    
class DonerLoginHisoty(models.Model):
    doner_name = models.ForeignKey(Doner, on_delete= models.CASCADE)
    doner_ip   = models.CharField(max_length=20)
    login_date = models.DateField(auto_now_add=True)
    login_status = models.BooleanField(default=True)


class PaymentProcess(models.Model):
    payment_type    = models.ForeignKey(PaymentType, on_delete=models.CASCADE) 
    payment_to      = models.ForeignKey(Receivers, on_delete=models.CASCADE)
    payment_by      = models.ForeignKey(Doner, on_delete=models.CASCADE)
    payment_amount  = models.IntegerField()
    bank_account    = models.IntegerField(blank=True, null=True)
    transaction_num = models.CharField(default='1234',max_length=10)
    payment_date    = models.DateField(auto_now_add= True, auto_now=False)
    status          = models.BooleanField(default= False)

    def __str__(self):
        return "total"


    

    
# class DonerLoginHistory(models.Model):
#     ip_address = models.