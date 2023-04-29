from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
from web_app.models import Doctor


class Blog(models.Model):
    STATUS_CHOICE = (
        ("draft", "Draft"), 
        ("published", "Published")
    )
    meta_title = models.CharField(max_length=500)
    meta_desc = models.CharField(max_length=500)
    url_slug = models.SlugField(max_length=500, unique=True)
    content = RichTextUploadingField()
    featured_image = models.ImageField(upload_to="guides_featured_image/%Y/%m/%d/",null=True,blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICE, default="Draft")
    # publisher = models.OneToOneField(organisation, on_delete=models.CASCADE,null=True,blank=True)
    created_by = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name="blog_created_by")
    reviewed_by = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name="blog_reviewed_by")
    reviewed_at = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.url_slug

