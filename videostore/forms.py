from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Store

class StaffUserCreationForm(UserCreationForm):
    store = forms.ModelChoiceField(queryset=Store.objects.all(), required=True)
    
    class Meta:
        model = User
        fields = ['username', 'store', 'password1', 'password2']
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = 'staff'
        user.store = self.cleaned_data['store']
        if commit:
            user.save()
        return user
