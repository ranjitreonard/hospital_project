from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView, RedirectView, TemplateView

from apps.management.forms import UserForm
from apps.portal.models import DefaultBill
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


class ManagerView(LoginRequiredMixin, TemplateView):
    template_name= 'management/ward.html'

    def get_context_data(self, **kwargs):
       context = super(ManagerView, self).get_context_data(**kwargs)
       context['wards'] = Ward.objects.all()
       context['beds'] = Bed.objects.all()
       context['patients'] = Patient.objects.all()
       context['bills'] = DefaultBill.objects.all()
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
             return render(request, template_name='management/ward_details.html', context= context)
        except Bed.DoesNotExist:
            new_bed = Bed.objects.create(
                number=bed_number,
                ward=ward,
                status='Unassigned',
                created_by=request.user,
            )
            ward.beds.add(new_bed)

            ward.save()

            return HttpResponseRedirect(reverse_lazy('management:ward-details', kwargs={'id':ward.id}))

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

        return super(AddBill, self).post(self,request,*args, **kwargs)


class DeleteBill(LoginRequiredMixin, RedirectView):
    url = reverse_lazy('management:wards')

    def post(self,request, *args, **kwargs):
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

        return super(UpdateBill, self). post(self, request, *args, **kwargs)