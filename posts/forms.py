from django import forms
from django.core.exceptions import ValidationError
from Users.models import Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = "__all__"

    def clean(self):
        super(PostForm, self).clean()
        content = self.cleaned_data.get("content")
        if len(content) < 5:
            raise ValidationError("content must be bigger than 5 chars")

        return self.cleaned_data
