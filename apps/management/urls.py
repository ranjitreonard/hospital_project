from django.urls import path
from .views import *

app_name = 'management'


urlpatterns = [
    path('dashboard/', dashboard, name='dashboard'),
    path('staff/', staff_list, name='staff'),
    path('staff/add/', AddStaff.as_view(), name='staff-add'),
    path('staff/<id>/', StaffDetails.as_view(), name='staff-details'),
    path('ward/', ManagerView.as_view(), name='wards'),
    path('ward/add/', AddWard.as_view(), name='ward-add'),
    path('ward/<id>/', ward_details, name='ward-details'),
    path('bill/add/', AddBill.as_view(), name='bill-add'),
    path('bill/delete/<bill_id>/', DeleteBill.as_view(), name='bill-delete'),
    path('bill/update/<bill_id>/', UpdateBill.as_view(), name='bill-update'),
    path('hr/', hr, name='hr'),
    path('complaint/details/<id>/', complaint_details, name='complaint-details'),
    path('request/add/', MakeRequest.as_view(), name='request-add'),
    path('requests/', Requests.as_view(), name='requests'),
    path('request/<request_id>/', ChangeRequestStatus.as_view(), name='change-request-status'),
    path('expenditure/', Expenditures.as_view(), name='expenditures'),
    path('medicine/add', AddMedicine.as_view(), name='medicine-add'),
    path('complaint/resolve/', complaint_resolve, name='complaint-resolve'),
    path('leave/period/new/', NewLeavePeriod.as_view(), name='new-leave-period'),
    path('leave/period/details/<id>', LeavePeriodDetails.as_view(), name='leave-period-details')

]