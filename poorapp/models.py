from django.db import models 
from ckeditor.fields import RichTextField

# Create your models here.

class HelpCategory(models.Model):
    category_name = models.CharField(max_length=50) 
    
    def __str__(self):
        return self.category_name

class BlodGroup(models.Model):
    group_name      = models.CharField(max_length=30) 

    def __str__(self):
        return self.group_name
    


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
    

class PoorPeople(models.Model):  
    
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
    blood_list = (
        ('1','A+'),
        ('2','A-'),
        ('3','AB+'),
        ('4','AB-'),
        ('5','B+'),
        ('6','B-'),
        ('7','O+'),
        ('8','O-')
    )
    blood_group             = models.CharField(max_length=1, default=1, choices=blood_list)
    help_type               = models.ForeignKey('HelpCategory', on_delete=models.CASCADE)
    amount                  = models.IntegerField()
    amount_received         = models.IntegerField(default=0) 
    require_date            = models.DateField()
    city_name               = models.ForeignKey(CityList, on_delete= models.CASCADE)
    district_name           = models.ForeignKey(DistrictList, on_delete= models.CASCADE)
    post_code               = models.CharField(max_length=20)
    address                 = models.TextField(max_length=500)
    payment_type            = models.ForeignKey('PaymentType', on_delete=models.CASCADE)
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
    document_file_two       = models.ImageField(upload_to='uploads/', blank=True)
    document_file_three     = models.ImageField(upload_to='uploads/', blank=True)
    problem_description     = RichTextField(blank=True,null=True)
    status                  = models.BooleanField(default=False)
    complete_status         = models.BooleanField(default=False)
    timestamp               = models.DateField(auto_now_add=True, auto_now=False)
    update                  = models.DateField(auto_now=True, auto_now_add=False)
    

    def __str__(self):
        return self.name

class PermessionCheck(models.Model):
    user = models.ForeignKey(PoorPeople, on_delete=models.CASCADE)
    view_action = models.BooleanField(default=False)
    delete_action = models.BooleanField(default = False)
    update_action = models.BooleanField(default = False)
    insert_action = models.BooleanField(default = False)


class Doner(models.Model):
    doner_name      = models.CharField(max_length = 120)
    blood_groups     = models.ForeignKey(BlodGroup, on_delete=models.CASCADE) 
    gender_list = (
        ('F','Female'),
        ('M','Male'),
        ('O','Other')
    )
    doner_gender   = models.CharField(max_length=1,choices=gender_list, null=True)
    doner_age       = models.IntegerField(null=True,blank=True)
    doner_phone     = models.CharField(max_length=15)
    doner_email     = models.EmailField(max_length=50,blank=True)
    doner_pass      = models.CharField(max_length = 300)
    doner_image     = models.ImageField(upload_to='uploads/',blank = True)
    joining_date    = models.DateField(auto_now=False, auto_now_add=True) 
    district_name   = models.ForeignKey(DistrictList, on_delete= models.CASCADE)
    city_name       = models.ForeignKey(CityList, on_delete= models.CASCADE)
    status          = models.BooleanField(default=True)
    
    def __str__(self):
        return self.doner_name
    
class DonerLoginHisoty(models.Model):
    doner_name = models.ForeignKey(Doner, on_delete= models.CASCADE)
    doner_ip   = models.CharField(max_length=20)
    login_date = models.DateField(auto_now_add=True)
    login_status = models.BooleanField(default=True)


class PaymentProcess(models.Model):
    payment_type    = models.ForeignKey(PaymentType, on_delete=models.CASCADE) 
    payment_to      = models.ForeignKey(PoorPeople, on_delete=models.CASCADE)
    payment_by      = models.ForeignKey(Doner, on_delete=models.CASCADE)
    payment_amount  = models.IntegerField()
    bank_account    = models.IntegerField(blank=True, null=True)
    bkash_account   = models.IntegerField(blank=True,null=True)
    transaction_num = models.CharField(default='1234',max_length=10)
    payment_date    = models.DateField(auto_now_add= True, auto_now=False)
    status          = models.BooleanField(default= False)

    def __str__(self):
        return "total"

class BloodDoner(models.Model):
    bdoner_name     = models.CharField(max_length=200)
    blood_group     = models.ForeignKey(BlodGroup, on_delete=models.CASCADE)
    last_donate_date = models.DateField()
    bdoner_phone    = models.CharField(max_length=20)
    bdoner_pass     = models.CharField(max_length=20)
    bdoner_district = models.ForeignKey(DistrictList, on_delete=models.CASCADE)
    bdoner_city     = models.ForeignKey(CityList, on_delete= models.CASCADE)
    gender_list = (
        ('F','Female'),
        ('M','Male'),
        ('O','Other')
    )
    bdoner_gender   = models.CharField(max_length=1,choices=gender_list, null=True)
    bdoner_age      = models.IntegerField(null=True)
    status          = models.BooleanField(default=True)

    def __str__(self):
        return self.bdoner_name
    

    
# class DonerLoginHistory(models.Model):
#     ip_address = models.