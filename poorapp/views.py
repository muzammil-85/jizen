from django.shortcuts import render,redirect
from django.http import HttpResponse ,JsonResponse
from . import models
import datetime,csv
import hashlib
from django.db.models import Q, Sum, Max, Avg, Min, Avg, F
from django.db.models import Count
from django.utils import timezone
import datetime
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.contrib.auth import authenticate
from django.contrib import messages  
from dotenv import load_dotenv

load_dotenv() 
# Create your views here.
# def user_login(request):
#     if request.method == 'POST':
#         usermobile = request.POST[]
#         username = request.POST[]


def get_client_ip(request): 
    remote_address = request.META.get('REMOTE_ADDR') 
    ip = remote_address 
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        proxies = x_forwarded_for.split(',') 
        while (len(proxies) > 0 and
                proxies[0].startswith(PRIVATE_IPS_PREFIX)):
            proxies.pop(0) 
        if len(proxies) > 0:
            ip = proxies[0]
    print(ip)
    return ip
def Dashboard(request): 
    if request.session['userid'] == None:
        return redirect('poorapp:doner_login')
    return render(request,'dashboard/admin_dashboard.html')

def add_poor_list(request):
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
        
        models.Receivers.objects.create(name=name,email=email,mobile_number=phone, aplicant_proffessions_id=aplicant_proffession, aplicant_gender=gender, aplicant_age=age, image=applicant_image, father_name=father_name, father_proffession_id=father_proffession, father_contact_number=father_mobile, mother_name=mother_name, help_type_id=help_type, amount=amount, require_date=require_date, city_name_id=city_list, district_name_id=district_list, post_code=post_code, address=address, payment_type_id=payment_type, payment_type_account=account_number, identity_doc_type=itendity_type, identity_doc=identity_file, identity_doc_number=identity_number, document_file_one=doc_file_one, document_file_two=doc_file_two, document_file_three=doc_file_three, problem_description=problem_description)
        messages.success(request,'Thank you {} for your registration, We will Review your application and contact you soon!!"'.format(name))
        return redirect('commonapp:thank_you_register')
    else:
        my_proffession      = models.ApplicantProffession.objects.all()
        father_proffession  = models.FatherProffession.objects.all()
        help_type           = models.HelpCategory.objects.all()
        district_list       = models.DistrictList.objects.all()
        payment_type       = models.PaymentType.objects.filter(status=True)
        city_list = models.CityList.objects.all()
        context = {
            'my_proffession':my_proffession,
            'father_proffession':father_proffession,
            'help_type':help_type,
            'district_list':district_list,
            'city_list':city_list,
            'payment_type':payment_type,
        }
 
    return render(request,'poorapp/add_new_poor.html',context)

def add_father_proffession(request):
    if request.method == 'POST':
        proffesion = request.POST.get('father_prof')
        ob = models.FatherProffession()
        ob.proffession_type = proffesion
        ob.save()
        messages.success(request,"Proffession Added Successfully")
    template = 'poorapp/add_father_prof.html'
    return render(request,template)

def father_proffession_list(request): 
    father_proffession_list = models.FatherProffession.objects.all().order_by('proffession_type')
    context = {
        'father_proffession_list':father_proffession_list
    }
    template = 'poorapp/father_prof_list.html'
    return render(request,template,context)

def delete_father_proffession(request,prof_id):
    ob = models.FatherProffession.objects.get(id=prof_id)
    ob.delete()
    messages.success(request,"Item Deleted successfully ")
    return redirect('/poor/dashboard/father-proffession-list')

def edit_father_proffession(request,prof_id):
    ob = models.FatherProffession.objects.get(id=prof_id)
    if request.method == 'POST':
        proffesion = request.POST.get('father_prof')
        new_ob = ob
        new_ob.proffession_type = proffesion
        new_ob.save()
        messages.success(request,"Prffession Updated Successfully ")
        return redirect('/poor/dashboard/father-proffession-list')
    context = {
        'proffession_list':ob
    }
    template = 'poorapp/update_father_prof.html'
    return render(request, template,context)

def poor_lists_all(request):
    all_poor_list = models.Receivers.objects.all()  
    poor_list_active = models.Receivers.objects.filter(status=True,complete_status=False).order_by('timestamp').count()
    poor_list_inactive = models.Receivers.objects.filter(status=False).order_by('timestamp').count()
    poor_list_pending = models.Receivers.objects.filter(complete_status=False,status=False).order_by('timestamp').count()
    poor_list_complete = models.Receivers.objects.filter(complete_status=True).order_by('timestamp').count()
    total_poor = all_poor_list.count()
    poor_people = models.Receivers.objects.all()
    for i in poor_people:
        if i.complete_status == False:
            if i.help_type==3:
                need = i.amount-i.amount_received
                if need <= 0:
                    i.complete_status = True
                    i.save()
           
        
    context = {
        'poor_list_active':poor_list_active,
        'poor_list_inactive':poor_list_inactive,
        'poor_list_pending':poor_list_pending,
        'poor_list_complete':poor_list_complete,
        'all_poor_list':all_poor_list,
        'total_poor':total_poor
    }
    return render(request,'poorapp/poor_list_all.html',context)
    

def poor_lists_active(request):
    all_poor_list = models.Receivers.objects.all().count()
    poor_list_active = models.Receivers.objects.filter(status=True,complete_status=False).order_by('timestamp')
    poor_list_inactive = models.Receivers.objects.filter(status=False).order_by('timestamp').count()
    poor_list_pending = models.Receivers.objects.filter(complete_status=False,status=False).order_by('timestamp').count()
    poor_list_complete = models.Receivers.objects.filter(complete_status=True).order_by('timestamp').count()
    total_active = poor_list_active.count()
    context = {
        'poor_list':poor_list_active,
        'poor_list_inactive':poor_list_inactive,
        'poor_list_pending':poor_list_pending,
        'poor_list_complete':poor_list_complete,
        'all_poor_list':all_poor_list,
        'total':total_active
    }
    return render(request,'poorapp/poor_list_active.html',context) 

def poor_lists_inactive(request): 
    total = models.Receivers.objects.all().count()
    poor_list_active = models.Receivers.objects.filter(status=True,complete_status=False).order_by('timestamp').count()
    poor_list_inactive = models.Receivers.objects.filter(status=False).order_by('timestamp')
    poor_list_pending = models.Receivers.objects.filter(complete_status=False,status=False).order_by('timestamp').count()
    poor_list_complete = models.Receivers.objects.filter(complete_status=True).order_by('timestamp').count()
    total_inactive = poor_list_inactive.count()
    context = {
        'poor_list':poor_list_inactive,
        'poor_list_active':poor_list_active,
        'poor_list_pending':poor_list_pending,
        'poor_list_complete':poor_list_complete,
        'total_inactive':total_inactive,
        'total':total
    }
    return render(request,'poorapp/poor_list_inactive.html',context)

def poor_lists_pending(request):
    total = models.Receivers.objects.all().count()
    poor_list_active = models.Receivers.objects.filter(status=True,complete_status=False).order_by('timestamp').count()
    poor_list_inactive = models.Receivers.objects.filter(status=False).order_by('timestamp').count()
    poor_list_pending = models.Receivers.objects.filter(complete_status=False,status=False).order_by('timestamp')
    poor_list_complete = models.Receivers.objects.filter(complete_status=True).order_by('timestamp').count()
    total_pending = poor_list_pending.count()
    context = {
        'poor_list_inactive':poor_list_inactive,
        'poor_list_active':poor_list_active,
        'poor_list_pending':poor_list_pending,
        'poor_list_complete':poor_list_complete,
        'total_pending':total_pending,
        'total':total
    }
    return render(request,'poorapp/poor_list_pending.html',context)

def poor_lists_approve(request,poor_id):
    ob = models.Receivers.objects.get(id = poor_id)
    ob.status = True
    ob.save()
    return redirect('poorapp:poor_list_pending')


def donor_lists_approve(request,donor_id):
    ob = models.Doner.objects.get(id = donor_id)
    ob.status = True
    ob.save()
    return redirect('poorapp:doner_list')
def donor_lists_completed(request,donor_id):
    ob = models.Doner.objects.get(id = donor_id)
    
    ob.complete= True
    ob.save()
    return redirect('poorapp:doner_list')

def poor_lists_disapprove(request,poor_id):
    ob = models.Receivers.objects.get(id = poor_id)
    ob.status = False
    ob.save()
    return redirect('poorapp:poor_list_pending')

def poor_lists_completed(request,poor_id):
    ob = models.Receivers.objects.get(id = poor_id)
    ob.complete_status = True
    ob.save()
    return redirect('poorapp:poor_list_pending')

def poor_lists_complete(request):
    poor_list_all = models.Receivers.objects.all().count()
    poor_list_active = models.Receivers.objects.filter(status=True,complete_status=False).order_by('timestamp').count()
    poor_list_inactive = models.Receivers.objects.filter(status=False).order_by('timestamp').count()
    poor_list_pending = models.Receivers.objects.filter(complete_status=False,status=False).order_by('timestamp').count()
    poor_list_complete = models.Receivers.objects.filter(complete_status=True).order_by('timestamp') 
    total_complete = poor_list_complete.count()
    
    context = {
        'poor_list_inactive':poor_list_inactive,
        'poor_list_all':poor_list_all,
        'poor_list_active':poor_list_active,
        'poor_list_pending':poor_list_pending,
        'poor_list_complete':poor_list_complete,
        'total_complete':total_complete
    }
    return render(request,'poorapp/poor_list_complete.html',context)

def doner_dashboard(request):
    return render(request,'dashboard/dashboard-doner.html')

def doner_login(request):
    if request.method == 'POST':
        email_phone = request.POST['email_phone'] 
        donner_password = request.POST['donner_password']
        # Encrypting the password
        enc_pass = hashlib.md5(donner_password.encode())
        doner_pass = enc_pass.hexdigest()
        chk_user = models.Doner.objects.filter(Q(doner_pass = doner_pass) & (Q(doner_phone = email_phone) | Q(doner_email = email_phone))).first()
        print(chk_user)
        if chk_user and chk_user.status:
            request.session['userid'] = chk_user.id
            models.DonerLoginHisoty.objects.create(doner_name_id = request.session['userid'], doner_ip=get_client_ip(request))
            return redirect('poorapp:doner_dashboard') 
            
        elif chk_user and chk_user.status == False:
            messages.warning(request,"Your Account is temporarly Suspended")
            return redirect('poorapp:doner_login')
        else:
            messages.error(request, "Oops!! something went wrong")
    return render(request,'commonapp/doner_login.html')


def admin_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['admin_password']
        user = authenticate(username=username,password=password)
        if user is not None:
            request.session['admin'] = 'admin'
            return redirect('poorapp:poor_list_all') 
        else:
            messages.error(request,"Username or password is not Correct")
    context = {

    }

    return render(request,'dashboard/admin_login.html',context)
def admin_logout(request):
    request.session['admin'] = None
    return redirect('poorapp:admin_login')

def admin_dashboard(request):
    return render(request,'dashboard/admin_dashboard.html')
def doner_login_history(request,doner_id):
    login_history = models.DonerLoginHisoty.objects.filter(doner_name_id = doner_id)
    context = {
        'login_history':login_history
    }
    return render(request,'dashboard/doner_login_history.html',context)
def doner_logout(request):
    request.session['userid'] = None
    return redirect('poorapp:doner_login')

def doner_register(request):
    if request.method == 'POST':
        doner_name = request.POST['doner_name']
        doner_gender = request.POST.get('doner_gender')
        doner_age = request.POST.get('doner_age')
        doner_email = request.POST['doner_email']
        doner_phone = request.POST['doner_phone']
        doner_pass = request.POST['doner_pass']
        doner_image = request.FILES.get('doner_image')
        district_id = int(request.POST['district'])
        city_id = int(request.POST['city_list'])
        status = request.POST.get('status', False)

        # Encrypting the password
        enc_pass = hashlib.md5(doner_pass.encode())
        doner_pass = enc_pass.hexdigest()

        # Checking for existing phone number or email
        chk_doner_phone = models.Doner.objects.filter(doner_phone=doner_phone).count()
        chk_doner_email = models.Doner.objects.filter(doner_email=doner_email).count()

        if chk_doner_phone:
            messages.warning(request, "This phone number is already used")
        elif chk_doner_email:
            messages.warning(request, "This Email is already used")
        else:
            # Creating new doner entry
            try:
                doner = models.Doner.objects.create(
                    doner_name=doner_name,
                    doner_gender=doner_gender,
                    doner_age=doner_age,
                    doner_phone=doner_phone,
                    doner_email=doner_email,
                    doner_pass=doner_pass,
                    doner_image=doner_image,
                    district_name_id=district_id,
                    city_name_id=city_id,
                    status=True,
                )
            except Exception as e:
                print(e)
                messages.error(request, "Oops!! something went wrong")
                return redirect('poorapp:doner_register')
            messages.success(request, "Hi {}, You have successfully registered".format(doner_name))
            return redirect('poorapp:doner_login')

    # Fetching district and city lists for the form
    doner_district = models.DistrictList.objects.all()
    doner_city = models.CityList.objects.all()
    context = {
        'doner_district': doner_district,
        'doner_city': doner_city
    }

    return render(request, 'commonapp/doner_register.html', context)

def get_city_by_ajax(request):
    print("Data founded")
    if request.is_ajax(): 
        dist_id = request.GET['district']
        print(dist_id)
        city_list = models.CityList.objects.filter(district_id = dist_id)
        context = {
            'city_list':city_list
        }
        return JsonResponse(context, safe = False)

def doner_profile(request,doner_id):
    doner = models.Doner.objects.filter(id=doner_id).first()
    payment = models.PaymentProcess.objects.filter(payment_by_id = doner_id)
    people = models.PaymentProcess.objects.filter(payment_by_id = doner_id).count()
    total = 0
    for item in payment:
        total = total + item.payment_amount 
    context ={
        'doner'  :doner,
        'payment':payment,
        'total'  :total,
        'people' :people
    }
    return render(request,'dashboard/doner_profile.html',context)


def doner_payment_search(request, doner_id):
    if request.method == 'POST':
        payment_type = int(request.POST['payment_type'])
        payment_to = int(request.POST['payment_to'])
        payment_amount = int(request.POST['payment_amount'])
        transaction_num = int(request.POST['transaction_num'])
        payment_by = request.session.userid

    poor_item = models.Receivers.objects.all().order_by('require_date')
    
    context = {
        'poor_item':poor_item, 
        'doner_id':doner_id
    }
    return render(request,'dashboard/doner_payment.html',context)
        

def make_payment(request,poor_id):
    if request.method == 'POST':
        payment_type = request.POST['payment_type']
        payment_amount = int(request.POST['payment_amount'])
        payment_by = int(request.session['userid'])

        # if request.POST['bank_account']:
        #     bank_account = request.POST['bank_account']
        #     models.PaymentProcess.objects.create(payment_type_id = payment_type, payment_to_id=poor_id, payment_by_id = payment_by, payment_amount = payment_amount,bank_account = bank_account)
        # elif request.POST['bkash_account']:
        #     bkash_account = request.POST['bkash_account']
        #     models.PaymentProcess.objects.create(payment_type_id = payment_type, payment_to_id=poor_id, payment_by_id = payment_by, payment_amount = payment_amount, bkash_account = bkash_account)
        # else:
        ob = models.PaymentProcess.objects.create(payment_type_id = payment_type, payment_to_id=poor_id, payment_by_id = payment_by, payment_amount = payment_amount)
        ob.payment_to.amount_received = ob.payment_to.amount_received + payment_amount
        ob.payment_to.save()
        messages.success(request, "You have successfully Paid!!")
        payment_type = models.PaymentType.objects.filter(status=True)
        context = {
        'payment_type':payment_type
        }
        return render(request,'dashboard/make_payment.html',context)
    payment_type = models.PaymentType.objects.filter(status=True)
    context = {
        'payment_type':payment_type
    }   
    return render(request,'dashboard/make_payment.html',context)

def view_transactions(request,doner_id):
    if request.session['userid']:
        transaction_list = models.PaymentProcess.objects.filter(payment_by_id = doner_id)

        
        # lists = models.PaymentProcess.objects.annotate(newamount = F('payment_to__amount') - F('payment_to__amount_received'))
        # for item in lists:
        #     print(item.newamount)
        # distinct = models.PaymentProcess.objects.values(
        # 'payment_to__name'
        # ).annotate(
        #     name_count=Count('payment_to__name')
        # ).filter(name_count=2)
        # transaction_list = models.PaymentProcess.objects.filter(payment_to__name__in=[item['payment_to__name'] for item in distinct])
        # print(transaction_list)
        context = {
            'transaction_list':transaction_list,
        }
        return render(request,'dashboard/view_transactions.html',context)
    else:
        return redirect('poorapp:doner_login')

 
def doner_password_change(request, doner_id):
    if request.session['userid']:
        if request.method == "POST":
            old_pass = request.POST['old_pass']
            new_pass = request.POST['new_pass']
            conf_pass = request.POST['confirm_pass']
            if new_pass == conf_pass:
                update_model = models.Doner.objects.filter(doner_pass = old_pass)
                if(update_model):
                    update_model.update(doner_pass = new_pass)
                    messages.success(request, "Password Updated Successfully")
                else: 
                    messages.error(request, "Old Password is not correct")
            else:
                messages.error(request,"Password Doesn't Match")
        return render(request,'dashboard/doner_password_change.html')
    else:
        return redirect('poorapp:doner_login') 

def csv_doner_transaction_import(request, doner_id):
    if request.session['userid']:
        transaction_list = models.PaymentProcess.objects.filter(payment_by_id= doner_id)
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition']= 'attachment; filename="transaction_list.csv"'

        writer = csv.writer(response)
        writer.writerow(["SL", "Payment Type", "Transaction Date", "Paid To", "TC Number", "Amount Paid"])
        sl = 1
        for item in transaction_list:
            writer.writerow([sl, item.payment_type, item.payment_date, item.payment_to.name, item.transaction_num, item.payment_amount])
            sl = sl+1
        return response

def doner_profile_update(request, doner_id): 
    if request.session['userid']:
        if request.method == "POST":
            name = request.POST['name']
            email = request.POST['email']
            phone = request.POST['phone']
            district = int(request.POST['country'])
            city_name = int(request.POST['city_name'])
            if bool(request.FILES.get('myfile', False)) == True:
                image = request.FILES['myfile'] 
                fs = FileSystemStorage()
                fname = fs.save(image.name, image)
                upload_file_url = fs.url(fname)  
                models.Doner.objects.filter(id = doner_id).update(doner_name=name,doner_phone=phone, doner_email = email, district_name_id=district,city_name = city_name, doner_image=image)
            else: 
                models.Doner.objects.filter(id = doner_id).update(doner_name=name, doner_phone=phone, doner_email = email, district_name_id=district,city_name = city_name)
            messages.success(request,"Profile Updated Successfully ")        
            return redirect('poorapp:doner_dashboard')           
        profile = models.Doner.objects.filter(id=doner_id).first()
        district_list = models.DistrictList.objects.all()
        city_lists = models.CityList.objects.all()
        context = {
            'profile':profile,
            'district_list':district_list,
            'city_lists':city_lists,
        } 
        return render(request,'dashboard/doner_profile_update.html',context)
    else:
        return redirect('/')

def bind_country_wise_city(request):
    country_id = int(request.GET.get('country_id'))
    city_list =  models.CityList.objects.filter(district_id = country_id) 

    context = {
        'city_list': city_list,
    }
    return render(request, "dashboard/bind_country_wise_city.html", context)

def doner_list(request):
    doner = models.Doner.objects.all()
    context = {
        'doner':doner
    }
    return render(request,'dashboard/doner_list.html',context)
