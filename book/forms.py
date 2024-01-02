from django import forms
from book.models import  BookModel, Review

class BooksForm(forms.ModelForm):
    class Meta:
        model = BookModel
        fields= '__all__'
    

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        for field in self.fields:
             self.fields[field].widget.attrs.update({
                 'class':(
                    'appearance-none block w-full bg-gray-200 '
                    'text-gray-700 border border-gray-200 rounded '
                    'py-3 px-4 leading-tight focus:outline-none '
                    'focus:bg-white focus:border-gray-500'
                 )
             })

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['name', 'email', 'body']
    
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        for field in self.fields:
             self.fields[field].widget.attrs.update({
                 'class':(
                    'appearance-none block w-full bg-gray-200 '
                    'text-gray-700 border border-gray-200 rounded '
                    'py-3 px-4 leading-tight focus:outline-none '
                    'focus:bg-white focus:border-gray-500'
                 )
             })