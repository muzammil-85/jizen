
from django.shortcuts import render,redirect
from django.http import HttpResponse, JsonResponse
import datetime,csv
import hashlib
from django.http import HttpResponse 
from django.db.models import Count
from django.utils import timezone
import datetime
from django.conf import settings
from django.core.files.storage import FileSystemStorage  
from django.contrib import messages  
from poorapp import models
from django.views.generic import View
from .utils import render_to_pdf
from django.template.loader import get_template
from django.db.models import Q



def Homepage(request): 
    help_category = models.HelpCategory.objects.all()
    district_list = models.DistrictList.objects.all()
    poor_item = models.PoorPeople.objects.filter(status=True).order_by('-timestamp')
    context = {
        'help_category':help_category,
        'district_list':district_list,
        'poor_item':poor_item
    }

    return render(request, 'commonapp/home_page.html',context)

def Userlog(request):
    return render(request, 'commonapp/user_login.html')

def blood_doner_login(request):
    return render(request, 'commonapp/blood_doner_login.html')

def single_poor_people(request,poor_id):
    poor = models.PoorPeople.objects.filter(id=poor_id).first()
    help_category = models.HelpCategory.objects.all()  
    context = {
        'help_category':help_category, 
        'poor':poor
    }
    return render(request,'commonapp/single_poor_people.html',context)

def application_form(request):
    if request.method == 'POST':
         
        applicant_files = FileSystemStorage()

        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        aplicant_proffession = int(request.POST['aplicant_proffession'])
        gender = request.POST['gender']
        age = request.POST['age']
        blood_group = request.POST['blood_group'] 
        applicant_image = request.FILES['applicant_image']
        fname = applicant_files.save(applicant_image.name, applicant_image)
        upload_file_url = applicant_files.url(fname)   

        father_name = request.POST['father_name']
        father_proffession = int(request.POST['father_proffession'])
        father_mobile = request.POST['father_mobile']
        mother_name = request.POST['mother_name']
        help_type = int(request.POST['help_type'])
        amount = request.POST['amount']
        require_date = request.POST['require_date']
        district_list = int(request.POST['district_list'])
        city_list = request.POST['city_list']
        post_code = request.POST['post_code']
        address = request.POST['address']
        payment_type = int(request.POST['payment_type'])
        account_number = request.POST['account_number']
        itendity_type = request.POST['itendity_type'] 
        identity_file = request.FILES['identity_file']
        fname_doc = applicant_files.save(identity_file.name, identity_file)
        upload_file_url = applicant_files.url(fname_doc)  

        identity_number = request.POST['identity_number']
        doc_file_one = request.FILES['doc_file_one']
        fname1 = applicant_files.save(doc_file_one.name, doc_file_one)
        upload_file_url = applicant_files.url(fname1)  

        doc_file_two = request.FILES['doc_file_two']
        fname2 = applicant_files.save(doc_file_two.name, doc_file_two)
        upload_file_url = applicant_files.url(fname2)  

        doc_file_three = request.FILES['doc_file_three']
        fname3 = applicant_files.save(doc_file_three.name, doc_file_three)
        upload_file_url = applicant_files.url(fname3) 

        problem_description = request.POST['problem_description'] 
        
        models.PoorPeople.objects.create(name=name,email=email,mobile_number=phone, aplicant_proffessions_id=aplicant_proffession, aplicant_gender=gender, aplicant_age=age, image=applicant_image, father_name=father_name, father_proffession_id=father_proffession, father_contact_number=father_mobile, mother_name=mother_name, blood_group=blood_group, help_type_id=help_type, amount=amount, require_date=require_date, city_name_id=city_list, district_name_id=district_list, post_code=post_code, address=address, payment_type_id=payment_type, payment_type_account=account_number, identity_doc_type=itendity_type, identity_doc=identity_file, identity_doc_number=identity_number, document_file_one=doc_file_one, document_file_two=doc_file_two, document_file_three=doc_file_three, problem_description=problem_description)
        messages.success(request,'Thank you {} for your registration, login using your contact Number and password is "123456"'.format(name))
        return redirect('commonapp:thank_you_register')
    else:
        blood_group         = models.BlodGroup.objects.all()
        my_proffession      = models.ApplicantProffession.objects.all()
        father_proffession  = models.FatherProffession.objects.all()
        help_type           = models.HelpCategory.objects.all()
        district_list       = models.DistrictList.objects.all()
        payment_type       = models.PaymentType.objects.filter(status=True)
        context = {
            'my_proffession':my_proffession,
            'blood_group':blood_group,
            'father_proffession':father_proffession,
            'help_type':help_type,
            'district_list':district_list,
            'payment_type':payment_type,
        }
 
    return render(request,'commonapp/application_form.html',context)

def thank_you_register(request): 
    return render(request,'commonapp/thank_you_register.html')


def search_poor(request):
    
    qs = models.PoorPeople.objects.all()
    qs = qs.filter(status=True)
    name = request.POST.get('search')
    district = request.POST.get('district')
    city = request.POST.get('city')
    help_cat = request.POST.get('help_cat')
    if help_cat:
        int_help_cat = int(help_cat)
    else:
        int_help_cat = None;

    if name !="" and name != None:
        qs = qs.filter(name__icontains=name)
        
    if district != "" and district != None:
        qs = qs.filter(district_name=district)

    if city != "" and city != None:
        qs = qs.filter(city_name=city)
    
    if help_cat != "" and help_cat != None:
        qs = qs.filter(help_type=help_cat) 

    help_category = models.HelpCategory.objects.all()   
    district_list = models.DistrictList.objects.all() 

    context = { 
        'poor_search':qs,
        'help_category':help_category,
        'district_list':district_list, 
        'help_cat':int_help_cat, 

    }
    return render(request, 'commonapp/search_poor.html',context)








class GeneratePDF(View):
    def get(self, request, *args, **kwargs):
        template = get_template('commonapp/application_form_pdf.html')
        context = {
             
        }
        html = template.render(context)
        pdf = render_to_pdf('commonapp/application_form_pdf.html', context)
        if pdf:
            response = HttpResponse(pdf, content_type='application/pdf')
            filename = "application_form.pdf"
            content = "inline; filename='%s'" %(filename)
            download = request.GET.get("download")
            if download:
                content = "attachment; filename='%s'" %(filename)
            response['Content-Disposition'] = content
            return response
        return HttpResponse("Not found")




def bind_districtwise_city(request): 
    district_id    = int(request.GET.get('district_list'))
    city_list   = models.CityList.objects.filter(district_id = district_id) 
    context = {
        'city_list':city_list
    }
    return render(request, 'commonapp/bind_districtwise_city.html',context) 

def districtwise_city_search(request): 
    district_id    = int(request.GET.get('district_list'))
    city_list   = models.CityList.objects.filter(district_id = district_id) 
    context = {
        'city_list':city_list
    }
    return render(request, 'commonapp/districtwise_city_search.html',context) 

def bind_identity_type(request):  
    itendity_type = request.GET.get('itendity_type')
    doct_type   = models.PoorPeople.objects.filter(identity_doc_type = itendity_type).first()
    print(doct_type)
    context = {
        'doct_type':doct_type
    }
    return render(request, 'commonapp/bind_identity_type.html',context) 

def bind_district_city(request):
    return render(request, 'commonapp/bind_identity_type.html')

def register_blood_doner(request): 
    blood_doner = models.BlodGroup.objects.all()
    disttrict_list = models.DistrictList.objects.all()
    if request.method=="POST":
        name = request.POST['doner_name']
        bdoner_phone = request.POST['bdoner_phone']
        bdoner_pass = request.POST['bdoner_pass']
        bdoner_age = request.POST['bdoner_age']
        gender = request.POST['gender']
        blood_group = int(request.POST['blood_group'])
        donate_date = request.POST['donate_date']
        district = int(request.POST['district'])
        city_id = int(request.POST['city'])

        models.BloodDoner.objects.create(bdoner_name=name, blood_group_id=blood_group, last_donate_date=donate_date, bdoner_phone=bdoner_phone, bdoner_pass=bdoner_pass, bdoner_district_id=district, bdoner_city_id=city_id, bdoner_gender=gender, bdoner_age=bdoner_age)
        messages.success(request,"Register as blood doner successfully")
        return redirect('commonapp:blood_doner_login')
    context = {
        'blood_doner':blood_doner,
        'disttrict_list':disttrict_list
    }
    return render(request,'commonapp/register_blood_doner.html',context)

def blood_doner_list(request):  
    name = request.GET.get('doner_name',False) 
    district = request.GET.get('district',False) 
    city = request.GET.get('city',False) 
    blood_type = request.GET.get('blood_type',False) 
    if name:
        if district:
            if city:
                if blood_type:
                    search_result = models.BloodDoner.objects.filter(bdoner_name__icontains=name,bdoner_district=district,bdoner_city=city,blood_group=blood_type) 
                else:
                    search_result = models.BloodDoner.objects.filter(bdoner_name__icontains=name,bdoner_district=district,bdoner_city=city) 
            else:
                search_result = models.BloodDoner.objects.filter(bdoner_name__icontains=name,bdoner_district=district) 
        else:
            search_result = models.BloodDoner.objects.filter(bdoner_name__icontains=name)

        blood_group = models.BlodGroup.objects.all()
        district_list = models.DistrictList.objects.all()
        counts = search_result.count()
        if counts > 0:  
            message = '1'
        else:
            message = '0'
        if district:
            district = int(district)
        context = {
            'blood_search':search_result,
            'search_result':search_result,
            'blood_group':blood_group,
            'district_list':district_list,
            'message':message,
            'name':name,
            'district':district
        }
    else:
        blood_group = models.BlodGroup.objects.all()
        district_list = models.DistrictList.objects.all()
        blood_search = models.BloodDoner.objects.all()
        context = {
            'blood_search':blood_search,
            'blood_group':blood_group,
            'district_list':district_list,
        } 
    return render(request,'commonapp/blood_doner_list.html',context)