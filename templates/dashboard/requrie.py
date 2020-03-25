from django.shortcuts import render,redirect
from django.contrib import messages
from . import models
import hashlib
from django.db.models import Q

# Create your views here.

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
        return ip
    else:
        ip = request.META.get('REMOTE_ADDR')
        return ip

def index(request):
    user_list = models.ProfileList.objects.filter(status = True).order_by("ranking") 
    context = {
        'user_list': user_list,
    }
    return render(request, "profileapp/index.html", context)

def user_signup(request):
    if request.method == 'POST':
        country_name = request.POST['country_name']
        first_name   = request.POST['first_name']
        last_name    = request.POST['last_name']
        phone_number = request.POST['phone_number']
        password     = request.POST['password'] 

        encripted_pass = hashlib.md5(password.encode())
        user_pass_encr = encripted_pass.hexdigest()

        models.ProfileList.objects.create(country_name_id = country_name, first_name = first_name, last_name = last_name, phone_number = phone_number, user_pass = user_pass_encr, user_type = "1", ip_address = get_client_ip(request))
        messages.success(request, "Your Profile is created Successfully")
        return redirect('/')

def dashboard(request):
    return render(request, "profileapp/dashboard.html")

def user_logout(request):
    request.session['userid'] = None
    return redirect("/") 

def user_login(request):
    if request.method == 'POST':
        user_mobile     = request.POST['user_mobile']
        user_pass       = request.POST['user_pass']

        encripted_pass = hashlib.md5(user_pass.encode())
        user_pass_encr = encripted_pass.hexdigest()

        chk_user = models.ProfileList.objects.filter(phone_number = user_mobile, user_pass = user_pass_encr).first()
        if chk_user and chk_user.status:
            request.session['userid'] = chk_user.id
            models.UserLoginHistory.objects.create(worker_name_id = chk_user.id, ip_address = get_client_ip(request))
            return redirect('/user-dashboard/')
        elif chk_user and chk_user.status == False:
            models.UserLoginHistory.objects.create(worker_name_id = chk_user.id, ip_address = get_client_ip(request), status = False)
            messages.warning(request, "Your Account Temporarily Suspended")
            return render(request, "profileapp/user_login.html")
        else:     
            messages.error(request ,"Phone number or password is not correct") 
            return render(request, "profileapp/user_login.html")
    else:        
        return render(request, "profileapp/user_login.html")

def worker_profile(request, id):
    profile = models.ProfileList.objects.filter(id = id)
    education_quality = models.EducationalQualification.objects.filter(worker_name_id = id) 
    language_list = models.UserLanguages.objects.filter(worker_name_id = id) 
    context = {
        'profile': profile,
        'education_quality': education_quality,
        'language_list': language_list,
    }
    return render(request, "profileapp/worker_profile.html", context)

def ready_product(request):
    product_list = models.ReadyProduct.objects.filter(status = True) 
    context = {
        'product_list': product_list,
    }
    return render(request, "profileapp/ready_product.html", context)

def software_development(request):
    return render(request, "profileapp/software_development.html")

def mobile_app_development(request):
    return render(request, "profileapp/mobile_app_development.html")

def web_development(request):
    return render(request, "profileapp/web_development.html")

#------------------------User Admin---------------------------#
def chk_authentication(request, userid):
    valid_user = models.ProfileList.objects.filter(id = userid).first()
    if valid_user and valid_user.status:
        return True
    elif valid_user and valid_user.status == False:
        messages.warning(request, "Your Account Temporarily Suspended")
        return False   
    else:
        return False       


def user_dashboard(request):
    if request.session['userid'] and chk_authentication(request, request.session['userid']):
        return render(request, "profileapp/user_dashboard.html")
    else:
        return redirect("/")       

def user_profile(request):
    if request.session['userid'] and chk_authentication(request, request.session['userid']):
        profile = models.ProfileList.objects.filter(id = request.session['userid']).first()
        edu_quality = models.EducationalQualification.objects.filter(worker_name_id = request.session['userid']) 
        context = {
            'profile': profile,
            'edu_quality': edu_quality
        }
        return render(request, "profileapp/user_profile.html", context)
    else:
        return redirect("/")    

def user_ready_product(request):
    if request.session['userid'] and chk_authentication(request, request.session['userid']):
        product_list = models.ReadyProduct.objects.filter(owner_name_id = request.session['userid'], status = True)
        context = {
            'product_list': product_list
        }
        return render(request, "profileapp/user_ready_product.html", context)
    else:
        return redirect("/")   

def user_settings(request):
    if request.session['userid'] and chk_authentication(request, request.session['userid']):
        product_list = models.ReadyProduct.objects.filter(owner_name_id = request.session['userid'], status = True)
        context = {
            'product_list': product_list
        }
        return render(request, "profileapp/user_settings.html", context)
    else:
        return redirect("/")   

def user_inbox(request, sender_id):
    if request.session['userid'] and chk_authentication(request, request.session['userid']):
        messages_list = models.UserMessages.objects.filter(Q(receiver_user = request.session['userid'], sender_user_id = sender_id) | Q(receiver_user = sender_id, sender_user_id = request.session['userid'])).order_by('-id')
   
        user_list = models.UserMessages.objects.filter(receiver_user = request.session['userid']).values('sender_user','sender_user_id__first_name','sender_user_id__last_name').distinct()  
        user_chat = models.UserMessages.objects.filter(receiver_user = request.session['userid'], sender_user = sender_id)

        context = {
            'user_list': user_list,
            'user_chat': user_chat,
        }
        return render(request, "profileapp/user_inbox.html", context)
    else:
        return redirect("/")   

def change_password(request):
    if request.session['userid'] and chk_authentication(request, request.session['userid']):
        product_list = models.ReadyProduct.objects.filter(owner_name_id = request.session['userid'], status = True)
        context = {
            'product_list': product_list
        }
        return render(request, "profileapp/change_password.html", context)
    else:
        return redirect("/")   

def billing_information(request):
    if request.session['userid'] and chk_authentication(request, request.session['userid']):
        product_list = models.ReadyProduct.objects.filter(owner_name_id = request.session['userid'], status = True)
        context = {
            'product_list': product_list
        }
        return render(request, "profileapp/change_password.html", context)
    else:
        return redirect("/")   

def user_login_history(request):
    if request.session['userid'] and chk_authentication(request, request.session['userid']):
        login_history = models.UserLoginHistory.objects.filter(worker_name_id = request.session['userid']).order_by("-id")
        context = {
            'login_history': login_history
        }
        return render(request, "profileapp/user_login_history.html", context)
    else:
        return redirect("/")   