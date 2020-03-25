from django.urls import path
from . import views 
app_name="poorapp"
urlpatterns = [
    path('', views.Dashboard, name='dashboard'), 
    path('doner/doner-register', views.doner_register, name='doner_register'),
    path('get-city/', views.get_city_by_ajax),
    path('doner/doner-login', views.doner_login, name='doner_login'), 
    path('doner/', views.doner_dashboard, name='doner_dashboard'), 
    path('doner/doner-logout', views.doner_logout, name='doner_logout'),  
    path('doner/profile/<int:doner_id>', views.doner_profile, name='doner_profile'),
    path('doner/search-payment/<int:doner_id>', views.doner_payment_search, name='doner_payment_search'),
    path('doner/make-payment/<int:poor_id>', views.make_payment, name='make_payment'),
    path('doner/doner-profile-update/<int:doner_id>', views.doner_profile_update, name='doner_profile_update'),
    path('doner/view-transactions/<int:doner_id>', views.view_transactions, name='view_transactions'),
    path('doner/csv-doner-transaction-import/<int:doner_id>', views.csv_doner_transaction_import, name='csv_doner_transaction_import'),
    path('bind-country-wise-city/', views.bind_country_wise_city, name='bind_country_wise_city'),
    path('doner-login-history/<int:doner_id>', views.doner_login_history, name='doner_login_history'),
    path('doner-password-change/<int:doner_id>', views.doner_password_change, name='doner_password_change'),

    path('poor/add-poor-item', views.add_poor_list, name='add_poor'),
    path('poor/add-father-proffession', views.add_father_proffession, name='father_prof'),
    path('poor/father-proffession-list', views.father_proffession_list, name='father_prof_list'),
    path('poor/delete-father-proffession/<int:prof_id>', views.delete_father_proffession, name='del_father_prof'),
    path('poor/edit-father-proffession/<int:prof_id>', views.edit_father_proffession, name='edit_father_prof'),
    path('poor/poor-list-all', views.poor_lists_all, name='poor_list_all'),
    path('poor/poor-list-active', views.poor_lists_active, name='poor_list'),
    path('poor/poor-list-inactive', views.poor_lists_inactive, name='poor_list_inactive'),
    path('poor/poor-list-pending', views.poor_lists_pending, name='poor_list_pending'),
    path('poor/list-approve/<int:poor_id>', views.poor_lists_approve, name='approveed'),
    path('poor/poor-list-complete', views.poor_lists_complete, name='poor_list_complete'),  
    path('admin-login/', views.admin_login, name='admin_login'),  
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'), 
    path("doner-list/", views.doner_list, name="doner_list"),
    

]