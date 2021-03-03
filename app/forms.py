from django import forms
from .models import ChoreInstance, ChoreStatus


class InstanceSubmissionForm(forms.Form):
    def __init__(self, user, *args, **kwargs):
        self.instance = forms.ModelChoiceField(
            queryset=ChoreInstance.objects.filter(
                user=user, status=ChoreStatus.ASSIGNED
            )
        )

        super(forms.Form, self).__init__(*args, **kwargs)

        self.fields["instance"] = self.instance

    instance = forms.ModelChoiceField(
        queryset=ChoreInstance.objects.filter(status=ChoreStatus.ASSIGNED),
        required=True,
    )
    notes = forms.CharField(max_length=5000, required=False)
    image = forms.ImageField(
        label="Select an image",
        required=False,
        widget=forms.ClearableFileInput(attrs={"multiple": True}),
    )
