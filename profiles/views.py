from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from django.http import HttpResponseForbidden

from .models import Profile
from .forms import ProfileForm

def profile_detail(request, username):
    """
    Display a user's profile.

    Args:
        request: The HTTP request
        username: The username of the user whose profile to display

    Returns:
        Rendered profile detail page
    """
    user = get_object_or_404(User, username=username)

    # Get or create profile for the user
    profile, created = Profile.objects.get_or_create(
        user=user,
        defaults={'bio': ''}
    )

    context = {
        'profile': profile,
        'user_profile': user,
    }

    return render(request, 'profiles/detail.html', context)

@login_required
def profile_edit(request):
    """
    Allow a logged-in user to edit their profile.

    Args:
        request: The HTTP request

    Returns:
        Rendered profile edit form or redirect to profile detail page
    """
    # Get or create profile for the current user
    profile, created = Profile.objects.get_or_create(
        user=request.user,
        defaults={'bio': ''}
    )

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, _('Your profile has been updated successfully.'))
            return redirect('profiles:profile_detail', username=request.user.username)
    else:
        form = ProfileForm(instance=profile)

    context = {
        'form': form,
        'profile': profile,
    }

    return render(request, 'profiles/edit.html', context)
