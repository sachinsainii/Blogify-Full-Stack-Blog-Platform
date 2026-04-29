# import django_filters
# from .models import Post, Category, Tag
# from users.models import CustomUser

# class PostFilter(django_filters.FilterSet):
#     category = django_filters.ModelChoiceFilter(queryset=Category.objects.all())
#     tags = django_filters.ModelMultipleChoiceFilter(queryset=Tag.objects.all())
#     author = django_filters.ModelChoiceFilter(queryset=CustomUser.objects.all())
#     created_date = django_filters.DateFilter(field_name='created_date')
#     class Meta:
#         model = Post
#         fields = ['category', 'tags', 'author', 'created_at']
