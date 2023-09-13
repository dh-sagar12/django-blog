
from typing import Any
from django import forms

from blog.models import *
from ckeditor.widgets  import CKEditorWidget

class CustomManyToManyFormField(forms.ModelMultipleChoiceField):
    def label_from_instance(self, category):
         return category.category_name


class BlogForm(forms.ModelForm):

    

    def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            for visible in self.visible_fields():
                visible.field.widget.attrs['class'] = 'block  px-4 py-2 mt-2 text-black w-full tex-sm  border rounded-md focus:border-purple-400 focus:ring-purple-300 focus:outline-none focus:ring focus:ring-opacity-40'
    
    content = forms.CharField(widget=CKEditorWidget())

    category =  CustomManyToManyFormField(
        queryset=Category.objects.all(), 
        widget=forms.CheckboxSelectMultiple

    )

    class Meta:
        model = Blog
        fields = ("title", 'slug', 'content',  'category', 'thumbnail', 'is_published')

    def save(self, commit = True, *args, **kwargs ):
        blog =  super().save(commit=False)
        context =  kwargs.get('request_context')
        print(context)
        if context is not None:
            author_instance  =  Author.objects.filter(user_id =  context.user).first()
            blog.author_id =  author_instance
            blog.uploaded_by =  context.user
        super().save(commit=True)
        super()._save_m2m()



class   AuthorForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'block  px-4 py-2 mt-2 text-black w-full tex-sm  border rounded-md focus:border-purple-400 focus:ring-purple-300 focus:outline-none focus:ring focus:ring-opacity-40'


    class Meta:
        model =  Author
        fields  =  ("name" , 'address', 'contact_number', 'about_you')



class ContactForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'block  px-4 py-2 mt-2 text-black w-full tex-sm  border rounded-md focus:border-purple-400 focus:ring-purple-300 focus:outline-none focus:ring focus:ring-opacity-40'
    
    class Meta:
        model  = Contact
        fields =  ['full_name', 'email', 'message']