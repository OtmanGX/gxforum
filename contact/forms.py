from django import forms


class ContactForm(forms.Form):
    name = forms.CharField(max_length=30, required=True)
    from_email = forms.EmailField(required=False)
    subject = forms.CharField(max_length=30)
    message = forms.CharField(widget=forms.Textarea(attrs={'placeholder':'Your message'}), required=True)