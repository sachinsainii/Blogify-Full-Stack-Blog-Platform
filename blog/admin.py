from django.contrib import admin
from .models import Post, Category,Tag,Comment
from django.apps import apps
from django.contrib.contenttypes.models import ContentType
from taggit.models import Tag
from django.http import HttpResponse
import csv
# from .views import BaseAdmin
# Register your models here.
class TagsListFilter(admin.SimpleListFilter):
    title = "Tags"
    parameter_name = "tags"

    def lookups(self, request, model_admin):
        # return [(tag.id, tag.name) for tag in Tag.objects.all()]
        # return (
        #     Tag.objects.filter(
        #         taggeditem_items__content_type__model=model_admin.model._meta.model_name
        #     )
        #     .distinct()
        #     .values_list("id","name","slug")
        # )
        ct = ContentType.objects.get_for_model(model_admin.model)

        tags = Tag.objects.filter(taggit_taggeditem_items__content_type=ct).distinct()
        return [(tag.id, tag.name) for tag in tags]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(tags__id=self.value())
        return queryset

def export_as_csv(modeladmin, request, queryset):
    meta = modeladmin.model._meta
    field_names = [field.name for field in meta.fields]

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename={meta}.csv'
    writer = csv.writer(response)

    writer.writerow(field_names)
    for obj in queryset:
        writer.writerow([getattr(obj,field) for field in field_names])
    return response

export_as_csv.short_description = "Export Selected as CSV"


class BaseAdmin(admin.ModelAdmin):
    actions = [export_as_csv]
    
    def __init__(self, model, admin_site):
      self.search_fields = [f.name for f in model._meta.fields]
      self.autocomplete_fields = [f.name for f in model._meta.fields if f.many_to_one]
      self.filter_horizontal = [
        f.name for f in model._meta.many_to_many
        if f.remote_field.through._meta.auto_created
        ]
      self.list_filter = [f.name for f in model._meta.fields if f.get_internal_type() not in ['TextField']]
      
      if any(f.name == "tags" for f in model._meta.many_to_many):
        self.list_filter += (TagsListFilter,)
      super().__init__(model, admin_site)

app_models = apps.get_app_config('blog').get_models()

for model in app_models:
    if admin.site.is_registered(model):
        continue
    try:
        admin.site.unregister(model)
    except admin.sites.NotRegistered:
        pass
    admin.site.register(model, BaseAdmin)

# @admin.register(Category)
# class CategoryAdmin(admin.ModelAdmin):
#     prepopulated_fields = {"slug":("name",)}

# @admin.register(Post)
# class PostAdmin(admin.ModelAdmin):
#     list_display = ("title","author","category","published_date")
#     list_filter = ("category","published_date")    

# @admin.register(Comment)
# class CommentAdmin(admin.ModelAdmin):
#     list_display = ('post','user','created_date')
#     search_fields = ('text','user_username','post_title')

# admin.site.register(Post)
# admin.site.register(Category)
# admin.site.register(Tag)
#hello

