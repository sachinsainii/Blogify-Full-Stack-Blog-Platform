from django import forms

from.models import Post, Category, Comment

# class CategoryForm(forms.ModelForm):
#     class Meta:
#         model = Category
#         fields = ['name','slug']

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title','text','image', 'category','tags']
        
    # tags = forms.CharField(
    #     required=False,
    #     help_text = "Enter tags separated by commas",
    #     widget=forms.TextInput(attrs={'placeholder':'e.g. django, python, webdev'})
    # )

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Add a comment...'})
        }

