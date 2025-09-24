from django import forms
from .models import Media, Member, Borrow


class MediaForm(forms.ModelForm):
    class Meta:
        model = Media
        fields = ['type', 'title', 'author']

class MemberForm(forms.ModelForm):
    class Meta:
        model = Member
        fields = ['lastname', 'firstname']

class BorrowForm(forms.ModelForm):
    class Meta:
        model = Borrow
        fields = ['member', 'media', 'borrowing_date']