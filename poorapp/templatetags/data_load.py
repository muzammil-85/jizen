from django import template 
register = template.Library()
from ..models import PoorPeople,Doner,PaymentProcess,CityList

@register.filter(name='doner_info')
def intactive_counts(request,id):
    doner_info = Doner.objects.filter(id=id)
    return doner_info

@register.filter(name='my_paymenbt')
def my_paymenbt(request,id):
    my_paymenbt = PaymentProcess.objects.filter(payment_by_id=id)[:5]
    return my_paymenbt

@register.filter(name='county_wise_city')
def county_wise_city(id):
    city_list = CityList.objects.filter(district_id=id)
    return city_list

@register.filter(name='make_payment')
def make_payment(request,poor):
    deue_amount = poor.amount - poor.amount_received 
    return deue_amount 
 
@register.filter(name='total_payment')
def total_payment(request,id):
    my_paymenbt = PaymentProcess.objects.filter(payment_by_id=id)
    total = 0
    for payment in my_paymenbt:
        total = total + payment.payment_amount 
    return total

 
@register.filter(name='amount_require')
def transaction(request,transaction):
    amount_require = transaction.payment_to.amount - transaction.payment_to.amount_received   
    return amount_require

 
@register.filter(name='doner_transaction')
def doner_transactions(request,doner_id):
    transaction = PaymentProcess.objects.filter(payment_by_id=doner_id).distinct() 
    return transaction

