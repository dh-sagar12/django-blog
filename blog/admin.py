from django.contrib import admin

from .models import *

# Register your models here.


# Register your models here.

class CategoryBlogInline(admin.TabularInline):
    model = CategoryBlog
    extra = 1


class BlogAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'author_id', 'upload_date', 'view_count', 'uploaded_by')
    inlines =  (CategoryBlogInline,)


class CateogryAdmin(admin.ModelAdmin):
    inlines = (CategoryBlogInline,)



admin.site.register(Author)
admin.site.register(Category, CateogryAdmin)
admin.site.register(Blog, BlogAdmin)
admin.site.register(BlogComment)
admin.site.register(CategoryBlog)
admin.site.register(Contact)