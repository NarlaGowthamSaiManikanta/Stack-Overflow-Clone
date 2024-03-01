from django import forms
from .models import User


class UserCreationForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput,
                               help_text='Must contain 8+ characters, including at least 1 letter and 1 number.')

    class Meta:
        model = User
        fields = ('email', 'password')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user


class AlmostDoneForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['profile_pic', 'name']
