from django import forms

from .models import Blogs as BlogsModel


class BlogsForm(forms.ModelForm):
    class Meta:
        model = BlogsModel
        fields = ['user', 'content', 'image']

    # Custom validation for content field
    def clean_content(self, *args, **kwargs):
        content = self.cleaned_data.get('content')
        if len(content) > 240:
            raise forms.ValidationError("Content too long!")
        return content

    # Overriding clean() - validate that no item in formset violate unique constraints on model
    def clean(self, *args, **kwargs):
        data = self.cleaned_data
        content = data.get('content', None)
        if content == "":
            content = None
        image = data.get("image", None)
        if content is None and image is None:
            raise forms.ValidationError('Content OR image required!')
        return super().clean(*args, **kwargs)
