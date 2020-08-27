import logging

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .models import Chore, ChoreInstance, ChoreStatus


logger = logging.getLogger(__name__)


@login_required
def home(request):
    open_instances = ChoreInstance.objects.filter(status=ChoreStatus.ASSIGNED)
    assignments = request.user.choreassignment_set.all()
    recent_submissions = ChoreInstance.objects.filter(user=request.user).order_by(
        "-id"
    )[:10]

    context = {
        "user": request.user,
        "open_instances": open_instances,
        "assignments": assignments,
        "recent_submissions": recent_submissions,
    }

    return render(request, "home.html", context)


@login_required
def submit_chore_instance(request):
    response = HttpResponseRedirect(reverse("home"))
    if not request.POST:
        return response

    if not ("instance" in request.POST):
        logger.error("Failed to update chore, no instance id in POST")
        messages.error(request, "Failed to update chore!")
        return response

    instance = get_object_or_404(ChoreInstance, pk=request.POST["instance"])
    instance.notes = request.POST["notes"] or ""
    instance.status = ChoreStatus.SUBMITTED
    instance.submission_date = timezone.now()
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

    import pdb

    pdb.set_trace()

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
