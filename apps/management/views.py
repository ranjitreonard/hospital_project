import datetime

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView, RedirectView, TemplateView
from apps.management.forms import UserForm, LeavePeriodForm
from apps.pharmacy.models import Expenditure, Medicine
from apps.portal.models import DefaultBill
from apps.staff.models import Staff
from apps.user.models import User
from .models import *


@login_required()
def dashboard(request):
    return render(request=request, template_name='management/dashboard.html')


@login_required()
def staff_list(request):
    staff = User.objects.all()

    context = {
        'object_list': staff
    }

    return render(request=request, template_name='management/staff_list.html', context=context)


class AddStaff(LoginRequiredMixin, CreateView):
    template_name = 'management/staff_new.html'
    form_class = UserForm
    success_url = reverse_lazy('management:staff')
    queryset = User.objects.all()

    def form_valid(self, form):
        valid = super(AddStaff, self).form_valid(form)

        form.instance.set_password(form.instance.password)

        form.save()

        return valid


class StaffDetails(LoginRequiredMixin, DetailView):
    template_name = 'management/staff_details.html'
    model = User
    queryset = User.objects.all()
    pk_url_kwarg = 'id'


# class HumanResourceView(LoginRequiredMixin, TemplateView):
#     template_name = 'management/hr_page.html'
#
#     def get_context_data(self, **kwargs):
#         context = super(HumanResourceView, self).get_context_data(**kwargs)
#         context['complaint'] = Complaint.objects.all()
#         context['leave'] = Leave.objects.all()
#         return context


@login_required()
def complaint_resolve(request, id):
    complaint = Complaint.objects.get(id=id)
    context = {
        'complaint': complaint
    }
    if request.method == "POST":
        complaint.status = 'Resolved'
        complaint.save()

    return HttpResponseRedirect(reverse_lazy('management:hr'))


class ManagerView(LoginRequiredMixin, TemplateView):
    template_name = 'management/ward.html'

    def get_context_data(self, **kwargs):
        context = super(ManagerView, self).get_context_data(**kwargs)
        context['wards'] = Ward.objects.all()
        context['beds'] = Bed.objects.all()
        context['patients'] = Patient.objects.all()
        context['bills'] = DefaultBill.objects.all()
        context['requests'] = Request.objects.all()
        return context


class AddWard(LoginRequiredMixin, RedirectView):
    url = reverse_lazy('management:wards')

    def post(self, request, *args, **kwargs):
        label = request.POST.get('label')

        Ward.objects.create(
            label=label,
            created_by=request.user
        )
        return super(AddWard, self).post(self, request, *args, **kwargs)


@login_required()
def ward_details(request, id):
    ward = Ward.objects.get(id=id)
    bed_number = request.POST.get('bed')

    errors = ' '

    context = {
        'object': ward,
        'errors': errors
    }
    if request.method == 'POST':
        try:
            Bed.objects.get(number__iexact=bed_number, ward=ward)
            errors = 'Bed has already been added'
            context = {
                'object': ward,
                'errors': errors
            }
            return render(request, template_name='management/ward_details.html', context=context)
        except Bed.DoesNotExist:
            new_bed = Bed.objects.create(
                number=bed_number,
                ward=ward,
                status='Unassigned',
                created_by=request.user,
            )
            ward.beds.add(new_bed)

            ward.save()

            return HttpResponseRedirect(reverse_lazy('management:ward-details', kwargs={'id': ward.id}))

    return render(request=request, template_name='management/ward_details.html', context=context)


class AddBill(LoginRequiredMixin, RedirectView):
    url = reverse_lazy('management:wards')

    def post(self, request, *args, **kwargs):
        bill_type = request.POST.get('bill_type')
        service = request.POST.get('service')
        amount = request.POST.get('amount')

        new_default_bill = DefaultBill.objects.create(
            bill_type=bill_type,
            service=service if service else '',
            amount=amount,
            created_by=self.request.user
        )

        return super(AddBill, self).post(self, request, *args, **kwargs)


class DeleteBill(LoginRequiredMixin, RedirectView):
    url = reverse_lazy('management:wards')

    def post(self, request, *args, **kwargs):
        bill_id = kwargs.get('bill_id')

        bill = DefaultBill.objects.get(id=bill_id)

        bill.delete()

        return super(DeleteBill, self).post(self, request, *args, **kwargs)


class UpdateBill(LoginRequiredMixin, RedirectView):
    url = reverse_lazy('management:wards')

    def post(self, request, *args, **kwargs):
        bill_id = kwargs.get('bill_id')
        amount = request.POST.get('amount')
        service = request.POST.get('service')
        bill_type = request.POST.get('bill_type')

        bill = DefaultBill.objects.get(id=bill_id)

        bill.amount = amount
        bill.service = service
        bill.bill_type = bill_type
        bill.save()

        return super(UpdateBill, self).post(self, request, *args, **kwargs)


@login_required()
def hr(request):
    all_complaint = Complaint.objects.all().exclude(status=2)
    leave_period = LeavePeriod.objects.all()
    context = {
        'complaints': all_complaint,
        'leave_period': leave_period,
    }

    return render(request,template_name='management/hr_page.html', context=context)


class LeavePeriodDetails(LoginRequiredMixin, DetailView):
    template_name = 'management/leave_period_details.html'
    queryset = LeavePeriod.objects.all()
    model = LeavePeriod
    pk_url_kwarg = 'id'



@login_required()
def complaint_details(request, id):
    complaint = Complaint.objects.get(id=id)
    context = {
        ' complaint': complaint
    }
    review = request.POST.get('review')

    if not complaint.seen:
        complaint.seen = "True"
        complaint.seen_at = timezone.now()
        complaint.seen_by = request.user
        complaint.save()

    if request.method == "POST":
        review = request.POST.get('review')
        complaint.review_by = request.user
        complaint.review_at = timezone.now()
        complaint.response = review
        complaint.status = 'Resolved'
        complaint.save()

    return render(request, template_name='management/complaint_details.html', context=context)


class MakeRequest(LoginRequiredMixin, RedirectView):
    url = reverse_lazy('management:wards')

    def post(self, request, *args, **kwargs):
        department = request.POST.get('department')
        description = request.POST.get('description')

        new_request = Request.objects.create(
            department=department,
            description=description,
            status=0,
            created_by=self.request.user
        )

        return super(MakeRequest, self).post(self, request, *args, **kwargs)


class Requests(LoginRequiredMixin, ListView):
    template_name = 'management/request.html'
    queryset = Request.objects.all()
    model = Request


class ChangeRequestStatus(LoginRequiredMixin, RedirectView):
    url = reverse_lazy('management:requests')

    def get(self, request, *args, **kwargs):
        status_type = kwargs.get('type')
        request_id = kwargs.get('request_id')

        my_request = Request.objects.get(id=request_id)

        if my_request.status == 0:
            my_request.status = 1
            my_request.save()

        return super(ChangeRequestStatus, self).get(self, request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        request_id = kwargs.get('request_id')
        comment = request.POST.get('comment')

        my_request = Request.objects.get(id=request_id)

        if my_request.status == 0:
            my_request.comment = comment
            my_request.status = 2
            my_request.save()

        return super(ChangeRequestStatus, self).post(self, request, *args, **kwargs)


class Expenditures(LoginRequiredMixin, ListView):
    template_name = 'management/expenditure.html'
    queryset = Expenditure.objects.all()
    model = Expenditure


class AddMedicine(LoginRequiredMixin, RedirectView):
    url = reverse_lazy('management:expenditures')

    def post(self, request, *args, **kwargs):
        name = request.POST.get('name')
        medicine_type = request.POST.get('medicine_type')
        boxes_bought = request.POST.get('boxes_bought')
        no_in_box = request.POST.get('no_in_box')
        manufacturer = request.POST.get('manufacturer')
        manufacture_date = request.POST.get('manufacture_date')
        expiry_date = request.POST.get('expiry_date')
        selling_price_per_unit = request.POST.get('selling_price_per_unit')
        cost_price_per_box = request.POST.get('cost_price_per_box')

        try:
            medicine = Medicine.objects.get(name__exact=name)
            medicine.boxes_bought = boxes_bought
            medicine.accumulated_boxes_bought += int(boxes_bought)
            medicine.boxes_left += int(boxes_bought),
            medicine.no_in_box +=int(no_in_box)
            medicine.total_no_units_accumulated += int(no_in_box)* int(boxes_bought)
            medicine.units_left += int(no_in_box) * int(boxes_bought)
            medicine.total_cost += cost_price_per_box * boxes_bought
            medicine.accumlated_total_cost += int(cost_price_per_box) * int(boxes_bought)

            # medicine.pieces_per_box += pieces_per_box
            # medicine.pieces += pieces_per_box * boxes_bought
            # medicine.pieces_left += pieces_per_box * boxes_bought
            medicine.save()

        except Medicine.DoesNotExist:
            new_medicine = Medicine.objects.create(
                name=name,
                medicine_type=medicine_type,
                boxes_bought=boxes_bought,
                accumulated_boxes_bought=boxes_bought,
                boxes_left=boxes_bought,
                no_in_box=no_in_box,
                total_no_units_accumulated=int(no_in_box) * int(boxes_bought),
                units_left=int(no_in_box) * int(boxes_bought),
                selling_price_per_unit=selling_price_per_unit,
                cost_price_per_box=cost_price_per_box,
                cost_price_per_unit=int(cost_price_per_box) / int(no_in_box),
                selling_price_per_box=int(selling_price_per_unit) * int(no_in_box),
                accumulated_total_cost=int(cost_price_per_box) * int(boxes_bought),
                total_cost=int(cost_price_per_box) * int(boxes_bought),
                # pieces_per_box=pieces_per_box,
                # pieces=pieces_per_box * boxes_bought,
                # pieces_left=pieces_per_box * boxes_bought,
                # boxes_left=boxes_bought,
                # pieces_selling_price=pieces_selling_price,
                manufacturer=manufacturer,
                manufacture_date=manufacture_date,
                expiry_date=expiry_date,
                created_by=self.request.user
            )
        new_exp = Expenditure.objects.create(
            category='Medicine',
            item=name,
            cost=int(cost_price_per_box) * int(boxes_bought),
            created_by=self.request.user,
        )

        return super(AddMedicine, self).post(self, request, *args, **kwargs)


class NewLeavePeriod(LoginRequiredMixin, CreateView):
    template_name = 'management/leave_period_new.html'
    success_url = reverse_lazy('management:hr')
    form_class = LeavePeriodForm
    queryset = LeavePeriod.objects.all()

    def form_valid(self, form):
        valid = super(NewLeavePeriod, self).form_valid(form)

        # get number of days
        nod = (form.instance.end_date - form.instance.start_date).days
        form.instance.number_of_days = nod

        # get all user objects
        users = User.objects.all()
        # convert end_date to a datetime type without the time data
        # Import datetime at the top
        # date1 = datetime.datetime.strptime(form.instance.end_date, "%Y-%m-%d")

        # leave_period = LeavePeriod.objects.get(end_date__year=date1.year)
        # looping through all the users
        for user in users:
            # initiate leave days left
            days_left = 0
            try:
                # try to get the latest staff object by excluding this new leave period
                # Add get_latest_by to the class Meta of the Staff model
                latest = Staff.objects.filter(user=user).exclude(leave_period=form.instance).latest()
                # use the latest to get the remaining days of the staff
                days_left = latest.number_of_days_left
            except Staff.DoesNotExist:
                pass
            # create the staff with the user iterator
            staff = Staff.objects.create(

                user=user,
                leave_period=form.instance,
                created_by=self.request.user,
                total_number_of_days= days_left + int(form.instance.days_allowed),
                number_of_days_left= days_left + int(form.instance.days_allowed),
            )

            # staff.save()
            # add the staff instance to the leave period staffs m2m field
            form.instance.staffs.add(staff)
        form.instance.created_by = self.request.user
        form.save()

        return valid


# class LeavePeriod(LoginRequiredMixin, CreateView):
#     template_name = 'management/leave_period_new.html'
#     success_url = reverse_lazy('management:hr')
#     form_class = LeavePeriodForm
#     queryset = Leave.objects.all()
#
#     def get_context_data(self, **kwargs):
#         context = super(LeavePeriod, self).get_context_data(**kwargs)
#         context['leave_period'] = Leave.objects.all()
#
#         return context