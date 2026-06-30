from django.contrib import admin
from django.utils.html import format_html
from .models import Registration, GalleryImage, AcademyVideo

admin.site.site_header = "Administration"
admin.site.site_title = "Administration"

@admin.register(Registration)
class RegistrationAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'experience_level', 'created_at')
    list_filter = ('experience_level', 'created_at')
    search_fields = ('name', 'email', 'phone')

@admin.register(GalleryImage)
class GalleryImageAdmin(admin.ModelAdmin):
    list_display = ('image_thumbnail', 'title', 'caption', 'uploaded_at')
    search_fields = ('title', 'caption')
    fields = ('title', 'caption', 'image', 'image_preview')
    readonly_fields = ('image_preview',)

    def image_thumbnail(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="width: 50px; height: 50px; object-fit: cover; border-radius: 4px;" />', obj.image.url)
        return "-"
    image_thumbnail.short_description = 'Thumbnail'

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-width: 250px; max-height: 250px; object-fit: contain; border-radius: 4px; border: 1px solid #ccc; display: block;" />', obj.image.url)
        return "No image uploaded yet"
    image_preview.short_description = 'Preview'


@admin.register(AcademyVideo)
class AcademyVideoAdmin(admin.ModelAdmin):
    list_display = ('title', 'youtube_url', 'created_at')
    search_fields = ('title', 'description')
    fields = ('title', 'description', 'youtube_url', 'video_preview')
    readonly_fields = ('video_preview',)

    def video_preview(self, obj):
        if obj.youtube_id:
            return format_html(
                '<iframe width="360" height="202" src="https://www.youtube-nocookie.com/embed/{}" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen referrerpolicy="strict-origin-when-cross-origin" style="border-radius: 4px; border: 1px solid #ccc;"></iframe>',
                obj.youtube_id
            )
        return "Enter a valid YouTube URL first to see the preview."
    video_preview.short_description = 'Video Preview'
