from django.urls import path
from . import views
app_name = "commonapp"
urlpatterns = [ 
    path("", views.Homepage, name='home'),
    path("login-user", views.Userlog, name='login'),
    path('application-form', views.application_form, name='application_form'),
    path('bind-districtwise-city/', views.bind_districtwise_city, name='bind_districtwise_city'),
    path('bind-identity-type/', views.bind_identity_type, name='bind_identity_type'),
    path('bind-district-city/', views.bind_district_city, name='bind_district_city'),
    path('pdf-application-form/', views.GeneratePDF.as_view(), name='pdf_application_form'),
    path('single-poor-people/<int:poor_id>', views.single_poor_people, name='single_poor_people'),
    path('thank-you-register', views.thank_you_register, name='thank_you_register'),
    path('thank-you-cloth/<int:donor_id>', views.thank_you_cloth, name='thank_you_cloth'),
    path('thank-you-food/<int:donor_id>', views.thank_you_food, name='thank_you_food'),
    path('thank-you-edu/<int:donor_id>', views.thank_you_edu, name='thank_you_edu'),
    path('districtwise-city-search/', views.districtwise_city_search, name='districtwise_city_search'),
    path('contact-support/', views.contact_support, name='contact_support'),
    path('search-poor/', views.search_poor, name='search_poor'),
    path('search-poor-admin/', views.search_poor_admin, name='search_poor_admin'),
]
