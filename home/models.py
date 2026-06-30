from django.db import models
import re

class Registration(models.Model):
    EXPERIENCE_CHOICES = [
        ('beginner', 'Beginner (No prior experience)'),
        ('intermediate', 'Intermediate (1-3 years experience)'),
        ('advanced', 'Advanced (3+ years experience)'),
    ]

    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    experience_level = models.CharField(max_length=20, choices=EXPERIENCE_CHOICES, default='beginner')
    message = models.TextField(blank=True, help_text="Any message or questions for the instructor")
    created_at = models.DateTimeField(auto_now_add=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def __str__(self):
        return f"{self.name} - {self.get_experience_level_display()}"


class GalleryImage(models.Model):
    title = models.CharField(max_length=100)
    caption = models.CharField(max_length=200, blank=True, help_text="Optional description of the image")
    image = models.ImageField(upload_to='gallery/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class AcademyVideo(models.Model):
    title = models.CharField(max_length=150)
    description = models.TextField(blank=True, help_text="Optional description of the video")
    youtube_url = models.URLField(help_text="Paste standard YouTube link: https://www.youtube.com/watch?v=...")
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def youtube_id(self):
        pattern = r'(?:https?://)?(?:www\.)?(?:youtube\.com/watch\?v=|youtu\.be/|youtube\.com/embed/|youtube\.com/shorts/)([a-zA-Z0-9_-]{11})'
        match = re.search(pattern, self.youtube_url)
        return match.group(1) if match else None

    @property
    def thumbnail_url(self):
        if self.youtube_id:
            return f"https://img.youtube.com/vi/{self.youtube_id}/hqdefault.jpg"
        return ""

    def __str__(self):
        return self.title
