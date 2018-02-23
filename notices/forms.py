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

    tags = forms.CharField(
        required=False,
        help_text='Enter tags separated by commas. Enter comma after every tag (even the last one). No spaces.')


    class Meta:
        model = Notice
        fields = ['title', 'message', 'tags']