from django import forms
# from .models import

# 登入表單
class LoginForm(forms.Form):

    username = forms.CharField(
        label="帳號",
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'id':'username',
                'name':'username'
            })
    )
    password = forms.CharField(
        label="密碼",
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'id':'password',
                'name':'password'
            })
    )


