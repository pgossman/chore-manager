import datetime
import logging

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage

from .forms import InstanceSubmissionForm
from .models import Chore, ChoreInstance, ChoreStatus, Photo


logger = logging.getLogger(__name__)


@login_required
def home(request):
    open_instances = ChoreInstance.objects.filter(
        user=request.user, status=ChoreStatus.ASSIGNED
    )
    assignments = request.user.choreassignment_set.all()
    recent_submissions = (
        ChoreInstance.objects.filter(user=request.user)
        .exclude(status=ChoreStatus.ASSIGNED)
        .order_by("-id")[:10]
    )

    f = InstanceSubmissionForm(request.user)

    context = {
        "user": request.user,
        "f": f,
        "open_instances": open_instances,
        "assignments": assignments,
        "recent_submissions": recent_submissions,
    }

    return render(request, "home.html", context)


@login_required
def submit_chore_instance(request):
    response = HttpResponseRedirect(reverse("home"))
    if request.method != "POST":
        return response

    form = InstanceSubmissionForm(request.user, request.POST)
    if not form.is_valid():
        logger.error("Failed to update chore, InstanceSubmissionForm object not valid")
        messages.error(request, "Failed to update chore, form not valid!")
        return response

    data = form.cleaned_data
    instance = data["instance"]
    instance.notes = data["notes"] or ""
    instance.status = ChoreStatus.SUBMITTED
    instance.submission_date = timezone.now()

    fs = FileSystemStorage()
    for f in request.FILES.getlist("image"):
        now = int(datetime.datetime.utcnow().timestamp())
        filename = f"{instance.id}__{now}__{f.name}"
        photo = Photo()
        photo.instance = instance
        photo.image.save(filename, f, True)

    instance.save()

    messages.success(
        request, f"{instance.assignment} successfully submitted for review"
    )

    return response


@login_required
def worm_review(request):
    unreviewed_instances = ChoreInstance.objects.filter(
        status=ChoreStatus.SUBMITTED
    ).all()

    context = {"unreviewed_instances": unreviewed_instances}
    response = render(request, "worm/review.html", context)

    return response


@login_required
def submit_worm_verdict(request):
    response = HttpResponseRedirect(reverse("home"))

    if not request.POST:
        return response

    verdicts = {
        int(k.replace("verdict", "")): v
        for k, v in request.POST.items()
        if k.startswith("verdict")
    }

    instances = ChoreInstance.objects.filter(id__in=verdicts.keys()).all()

    for instance, verdict in zip(instances, verdicts.values()):
        # TODO let's not use these magic strings
        if verdict == "approve":
            instance.status = ChoreStatus.COMPLETE
        elif verdict == "reject":
            instance.status = ChoreStatus.INCOMPLETE

        instance.save()

    messages.success(request, "Submitted successfully!")

    return response
