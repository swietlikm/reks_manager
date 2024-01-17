from ckeditor.fields import RichTextField
from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext as _

User = get_user_model()


class Category(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")

class Post(models.Model):
    category = models.ForeignKey(
        Category, on_delete=models.DO_NOTHING, related_name="categories", verbose_name=_("Category")
    )

    title = models.CharField(max_length=255, verbose_name=_("Title"))
    text = RichTextField()
    author = models.ForeignKey(
        User, related_name="posts", on_delete=models.DO_NOTHING, verbose_name=_("Author"), null=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} ({self.category})"

    class Meta:
        verbose_name = _("Post")
        verbose_name_plural = _("Posts")
