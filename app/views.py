from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .models import Chore, ChoreInstance, ChoreStatus


@login_required
def home(request):
    open_instances = ChoreInstance.objects.filter(status=ChoreStatus.ASSIGNED)
    chores = request.user.chore_set.all()
    recent_submissions = ChoreInstance.objects.filter(user=request.user).order_by(
        "-id"
    )[:10]

    context = {
        "user": request.user,
        "open_instances": open_instances,
        "chores": chores,
        "recent_submissions": recent_submissions,
    }

    return render(request, "home.html", context)


@login_required
def submit_chore_instance(request):
    response = HttpResponseRedirect(reverse("home"))
    if not request.POST:
        return response

    if not ("instance" in request.POST):
        messages.error(request, "Failed to update chore!")
        return response

    instance = get_object_or_404(ChoreInstance, pk=request.POST["instance"])
    instance.status = ChoreStatus.SUBMITTED
    instance.save()

    messages.success(
        request, f"{instance.chore.name} successfully submitted for review"
    )

    return response
