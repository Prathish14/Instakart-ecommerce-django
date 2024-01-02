from users_app.models import Profile
from django import forms

class EditProfileSupport(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['name','image','email','phone','address','website','facebook','twitter','linkedin']
        labels={
            'website': "Website Url",
            'facebook':"Facebook Url",
            'twitter':'Twitter Url',
            'linkedin':'Linkedin Url'
        }
    
