from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser,Postt
from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User 

User = get_user_model()
class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required= True)
    # native_name = forms.CharField(max_length=5, required=False)
    phone_no = forms.CharField(max_length=10, required=False)
    class Meta:
        model = CustomUser
        fields = ('username','email', 'location', 'birth_date', 'phone_no','profile_picture', 'password1', 'password2')
    
    def clean_email(self):
        email=self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("A user with this email aleready exists.")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Postt
        fields = ['username','first_name', 'last_name', 'location', 'birth_date','profile_picture']


