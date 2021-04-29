from django import forms
from django.core.exceptions import ValidationError
from .models import Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = "__all__"
        exclude = ("metrics",)

    def clean_title(self):
        title = self.cleaned_data.get("title")
        if "test" in title:
            raise ValidationError("title shouldn't has test word!")

        return title

    def clean(self):
        # hna a2dr aktb validation bra7ty 3la kol 7aga
        super(PostForm, self).clean()
        content = self.cleaned_data.get("content")
        title = self.cleaned_data.get("title")
        if len(content) < 10:
            raise ValidationError("content must be bigger than 10 chars")

        return self.cleaned_data
