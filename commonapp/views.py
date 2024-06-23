
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
from django.core.mail import send_mail


def Homepage(request): 
    help_category = models.HelpCategory.objects.all()
    district_list = models.DistrictList.objects.all()
    poor_item = models.Receivers.objects.filter(status=True).order_by('-timestamp')
    context = {
        'help_category':help_category,
        'district_list':district_list,
        'poor_item':poor_item 
    }

    return render(request, 'commonapp/home_page.html',context)

def Userlog(request):
    return render(request, 'commonapp/user_login.html')


def single_poor_people(request, poor_id):
    poor = models.Receivers.objects.filter(id=poor_id).first()
    help_category = models.HelpCategory.objects.all()  
    context = {
        'help_category': help_category, 
        'poor': poor
    }
    return render(request, 'commonapp/single_poor_people.html', context)



def application_form(request):
    if request.method == 'POST':
         
        applicant_files = FileSystemStorage()

        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        aplicant_proffession = int(request.POST['aplicant_proffession'])
        gender = request.POST['gender']
        age = request.POST['age']
        applicant_image = request.FILES['applicant_image']
        fname = applicant_files.save(applicant_image.name, applicant_image)
        upload_file_url = applicant_files.url(fname)   
        father_name = request.POST['father_name']
        father_proffession = int(request.POST['father_proffession'])
        father_mobile = request.POST['father_mobile']
        mother_name = request.POST['mother_name']
        help_type = int(request.POST['help_type'])
        print(help_type)
        require_date = request.POST['require_date']
        district_list = int(request.POST['district_list'])
        city_list = request.POST['city_list']
        post_code = request.POST['post_code']
        address = request.POST['address']
        
        itendity_type = request.POST['itendity_type'] 
        identity_file = request.FILES['identity_file']
        fname_doc = applicant_files.save(identity_file.name, identity_file)
        upload_file_url = applicant_files.url(fname_doc)  

        identity_number = request.POST['identity_number']
        doc_file_one = request.FILES['doc_file_one']
        fname1 = applicant_files.save(doc_file_one.name, doc_file_one)
        upload_file_url = applicant_files.url(fname1)  

        problem_description = request.POST['problem_description']
        edu_items = ''
        payment_type = None
        account_number = 0
        amount=0
        cloth_count=0
        cloth_size=''
        food_quantity=0
        food_time=None
        print(help_type)
        if(help_type==3):
            amount = request.POST['amount']
            payment_type = int(request.POST['payment_type'])
            account_number = request.POST['account_number']
        elif(help_type==1):
            edu_items = request.POST['amount']
        elif(help_type==2):
            cloth_count = int(request.POST['amount'])
            cloth_size = request.POST['payment_type']
        elif(help_type==6):
            food_quantity = int(request.POST['amount'])
            food_time = request.POST['food_time']

        models.Receivers.objects.create(name=name,food_time=food_time,food_quantity=food_quantity,cloth_count=cloth_count,cloth_size=cloth_size,edu_items=edu_items,email=email,mobile_number=phone, aplicant_proffessions_id=aplicant_proffession, aplicant_gender=gender, aplicant_age=age, image=applicant_image, father_name=father_name, father_proffession_id=father_proffession, father_contact_number=father_mobile, mother_name=mother_name, help_type_id=help_type, amount=amount, require_date=require_date, city_name_id=city_list, district_name_id=district_list, post_code=post_code, address=address, payment_type_id=payment_type, payment_type_account=account_number, identity_doc_type=itendity_type, identity_doc=identity_file, identity_doc_number=identity_number, document_file_one=doc_file_one, problem_description=problem_description)
        messages.success(request,'Thank you {} for your registration, We will Review your application and contact you soon!!"'.format(name))
        return redirect('commonapp:thank_you_register')
    else:
        my_proffession      = models.ApplicantProffession.objects.all()
        father_proffession  = models.FatherProffession.objects.all()
        district_list       = models.DistrictList.objects.all()
        city_list           = models.CityList.objects.all()
        payment_type        = models.PaymentType.objects.filter(status=True)

        # Check if the required HelpCategory instances exist
        clothes_help, created = models.HelpCategory.objects.get_or_create(category_name='I need Clothes')
        education_help, created = models.HelpCategory.objects.get_or_create(category_name='Educational Help')
        food_help, created = models.HelpCategory.objects.get_or_create(category_name='I need Food')

        # Get the IDs of the required HelpCategory instances
        clothes_help_id = clothes_help.id
        education_help_id = education_help.id
        food_help_id = food_help.id

        help_type = models.HelpCategory.objects.all()

        context = {
            'my_proffession': my_proffession,
            'father_proffession': father_proffession,
            'help_type': help_type,
            'district_list': district_list,
            'payment_type': payment_type,
            'city_list': city_list,
            'clothes_help_id': clothes_help_id,
            'education_help_id': education_help_id,
            'food_help_id': food_help_id,
        }
 
    return render(request, 'commonapp/application_form.html', context)

def thank_you_register(request):
    
    return render(request,'commonapp/thank_you_register.html')
def thank_you_cloth(request,donor_id):
    ob = models.Doner.objects.get(id = donor_id)
    ob.request = True
    ob.save()
    return render(request,'commonapp/thank_you_cloth.html')

def thank_you_edu(request,donor_id): 
    ob = models.Doner.objects.get(id = donor_id)
    ob.request = True
    ob.save()
    return render(request,'commonapp/thank_you_edu.html')

def thank_you_food(request,donor_id): 
    ob = models.Doner.objects.get(id = donor_id)
    ob.request = True
    ob.save()
    return render(request,'commonapp/thank_you_food.html')


def contact_support(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        subject = request.POST['subject']
        message = request.POST['message']

        # Construct the email message
        email_subject = f"Support Request: {subject}"
        email_message = f"Name: {name}\nEmail: {email}\n\nMessage:\n{message}"

        try:
            # Send the email
            send_mail(
                email_subject,
                email_message,
                settings.DEFAULT_FROM_EMAIL,
                [settings.SUPPORT_EMAIL],
            )
            messages.success(request, "Your message has been sent successfully.")
            return JsonResponse(request, messages)
        except Exception as e:
           print(e)

    return render(request, 'commonapp/contact_support.html')

def search_poor(request):
    
    qs = models.Receivers.objects.all()
    qs = qs.filter(complete_status=False,status=True)
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



def search_poor_admin(request):
    
    qs = models.Receivers.objects.all()
    qs = qs.filter(status=True)
    name = request.POST.get('search')
    

    if name !="" and name != None:
        qs = qs.filter(name__icontains=name) 

    context = { 
        'all_poor_list':qs,

    }
    return render(request, 'poorapp/poor_list_all.html',context)






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
    doct_type   = models.Receivers.objects.filter(identity_doc_type = itendity_type).first()
    print(doct_type)
    context = {
        'doct_type':doct_type
    }
    return render(request, 'commonapp/bind_identity_type.html',context) 

def bind_district_city(request):
    return render(request, 'commonapp/bind_identity_type.html')

