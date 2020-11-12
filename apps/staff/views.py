from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import CreateView
from pip._vendor.urllib3.util import request

from apps.management.forms import LeavePeriodForm
from apps.management.models import Complaint
from apps.staff.models import Leave


@login_required()
def dashboard(request):
    return render(request=request, template_name='staff/dashboard.html')



@login_required()
def add_complaint(request):
    complaints = request.POST.get('complaints')
    all_complaints = Complaint.objects.all()

    context = {
        'all_complaints': all_complaints
    }
    if request.method == 'POST':

        my_complaint = Complaint.objects.create(
            complaint=complaints,
            created_by=request.user,
            status='Pending',
            # created_at=timezone.now(),
        )
        # complaints.complaint.add(my_complaint)
        my_complaint.save()
    return render(request, 'staff/complaint.html', context=context)


def cancel_complaint(request, id):
    complaint = Complaint.objects.get(id=id)
    if complaint.status == 'Pending':
        complaint.status = 'Canceled'
        complaint.save()

    return redirect(reverse_lazy('staff:add-complaint'))


