from django.urls import path
from shoes.views import *

urlpatterns = [
    path('', index_template, name='index_shoes'),
    path('list/', shoes_template, name='list_shoes'),
    path('httpresponse/', index),
    path('add/', shoes_add, name='add_shoes'),
    path('list/<int:shoes_id>/', shoes_detail, name='one_shoes'),
    #     Supplier ----------------------------------------------
    path('supplier/list/', supplier_list, name='list_supp'),
    path('supplier/add/', supplier_form, name='add_supp'),
    # Supplier class VIEW ---------------------------------------
    # LISTVIEW
    path('supplier/view/list/', SupplierListView.as_view(), name='list_supp_view'),
    path('supplier/view/<int:supplier_id>', SupplierDetailView.as_view(), name='info_supp_view'),
    #  CREATEVIEW
    path('supplier/view/add/', SupplierCreateView.as_view(), name='add_supp_view'),

    # UPDATEVIEW
    path('supplier/view/edit/<int:pk>', SupplierUpdateView.as_view(), name='edit_supp_view'),
    # DELETE
    path('supplier/view/del/<int:pk>', SupplierDeleteView.as_view(), name='del_supp_view'),
    path('registration/', user_registration, name='regis'),
    path('login/', user_login, name='log in'),
    path('logout/', user_logout, name='log out'),
    path('email/', contact_email, name='contact_email'),

    path('api/list/', shoes_api_list, name='shoes_api_list'),
    path('api/detail/<int:pk>', shoes_api_detail, name='shoes_api_detail'),
]
