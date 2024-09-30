# restaurants/forms.py
from django import forms
from django.contrib.auth.models import User
from .models import UserProfile
from .models import RestaurantReview

class UserRegistrationForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    email = forms.EmailField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput())
    favorite_cuisine = forms.CharField(max_length=255)
    favorite_dish = forms.CharField(max_length=255)
    dietary_restrictions = forms.CharField(max_length=255, required=False)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'password']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        user.username = self.cleaned_data['email']  # Use email as username
        if commit:
            user.save()
            # Create a related UserProfile instance
            UserProfile.objects.create(
                user=user,
                favorite_cuisine=self.cleaned_data['favorite_cuisine'],
                favorite_dish=self.cleaned_data['favorite_dish'],
                dietary_restrictions=self.cleaned_data.get('dietary_restrictions', '')
            )
        return user

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['favorite_cuisine', 'favorite_dish', 'dietary_restrictions']

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']


class ReviewForm(forms.ModelForm):
    RATING_CHOICES = [(i, i) for i in range(1, 6)]  # 1 to 5

    rating = forms.ChoiceField(
        choices=RATING_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Rating'
    )
    comment = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        label='Your Review'
    )

    class Meta:
        model = RestaurantReview
        fields = ['rating', 'comment']
