from django.contrib import admin

from .models import Category, Post


@admin.register(Category)
class AdopterAdmin(admin.ModelAdmin):
    list_display = ("name", "description")
    list_filter = ("name", "description")
    search_fields = ("name",)
    readonly_fields = ("id",)


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "category",
        "title",
        "author",
        "created_at",
        "updated_at",
    )
    list_filter = ("title", "created_at", "author", "updated_at")
    search_fields = ("title", "text", "author")
    readonly_fields = ("id", "author")

    def save_model(self, request, obj, form, change):
        if hasattr(obj, "author"):
            if not obj.author:
                obj.author = request.user
        obj.save()
