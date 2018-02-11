from django import forms
from .models import Notice

class NewNoticeForm(forms.ModelForm):

    message = forms.CharField(
        widget=forms.Textarea(
            attrs={'rows': 5, 'placeholder': 'Description'}
        ),
        max_length=2000,
        help_text='The max length of the text is 2000.'
    )


    class Meta:
        model = Notice
        fields = ['title', 'message']