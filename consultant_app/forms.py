from django import forms
from . models import User
from django.contrib.auth.forms import UserCreationForm

class MyRegistrationForm(UserCreationForm):
    email = forms.EmailField(required = True)
    first_name = forms.CharField(required = False)
    last_name = forms.CharField(required = False)
    # gender= forms.CharField(choices=GENDER, max_length=10, null=True, blank=True)
    # role= forms.CharField(choices=ROLE_CHOICE, max_length=15, null=True, blank=True)
    employee_id = forms.CharField(max_length=20, default=None, null=True)
    skype_username = forms.CharField(max_length=50, default=None, null=True)
    mobile_no = forms.CharField(max_length=10, null=True, blank=True, )
    company_name = forms.CharField(max_length=50, default=None, null=True)
    experience = forms.CharField(max_length=5, default=None, null=True)
    # status = forms.CharField(choices=RATING_CHOICES, max_length=15,null=True, blank=True)
    current_location = forms.CharField(max_length=30, default=None, null=True)


    class Meta:
        model = User

    def save(self,commit = True):
        user = super(MyRegistrationForm, self).save(commit = False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['First name']
        user.last_name = self.cleaned_data['Last name']
        user.employee_id = self.cleaned_data['employee_id']
        user.skype_username = self.cleaned_data['skype_username']
        user.mobile_no = self.cleaned_data['mobile_no']
        user.company_name = self.cleaned_data['company_name']



        if commit:
            user.save()

        return user
