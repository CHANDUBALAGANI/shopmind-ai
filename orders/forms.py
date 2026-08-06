from django import forms


class CheckoutForm(forms.Form):

    full_name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            "class": "form-control"
        })
    )

    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            "class": "form-control"
        })
    )

    phone = forms.CharField(
        max_length=15,
        widget=forms.TextInput(attrs={
            "class": "form-control"
        })
    )

    address = forms.CharField(
        widget=forms.Textarea(attrs={
            "class": "form-control",
            "rows": 3
        })
    )

    city = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            "class": "form-control"
        })
    )

    state = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            "class": "form-control"
        })
    )

    pincode = forms.CharField(
        max_length=10,
        widget=forms.TextInput(attrs={
            "class": "form-control"
        })
    )