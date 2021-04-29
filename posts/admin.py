from django.contrib import admin
from .models import Post, Category, Metric
from .forms import PostForm


# Register your models here.


class PostAdmin(admin.ModelAdmin):
    form = PostForm
    list_display = ("title", "author")
    list_filter = ("category",)
    search_fields = ("title",)
    readonly_fields = ("author",)


class PostInline(admin.TabularInline):
    model = Post
    max_num = 3
    extra = 1


class TagAdmin(admin.ModelAdmin):
    inlines = [PostInline]


admin.site.register(Post, PostAdmin)
admin.site.register(Category)
admin.site.register(Metric)
