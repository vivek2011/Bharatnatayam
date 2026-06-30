from django.shortcuts import render, redirect
from django.contrib import messages
from django.conf import settings
from .models import Registration, GalleryImage, AcademyVideo
import os

def home_view(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        experience_level = request.POST.get('experience_level')
        message = request.POST.get('message', '')

        if name and email and phone:
            Registration.objects.create(
                name=name,
                email=email,
                phone=phone,
                experience_level=experience_level,
                message=message
            )
            messages.success(request, f"Thank you, {name}! Your registration has been successfully received.")
            return redirect('home')
        else:
            messages.error(request, "Please fill in all required fields.")

    # Check if the hero image exists
    hero_image_path = os.path.join(settings.BASE_DIR, 'static', 'images', 'hero_dance.png')
    hero_image_exists = os.path.exists(hero_image_path)
    
    context = {
        'hero_image_exists': hero_image_exists,
    }
    
    return render(request, 'home/index.html', context)


def gallery_view(request):
    images = GalleryImage.objects.all().order_by('-uploaded_at')
    videos = AcademyVideo.objects.all().order_by('-created_at')
    context = {
        'images': images,
        'videos': videos,
    }
    return render(request, 'home/gallery.html', context)
