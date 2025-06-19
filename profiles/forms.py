from django import forms
from django.utils.translation import gettext_lazy as _
from .models import Profile

class ProfileForm(forms.ModelForm):
    """
    Form for editing user profile information.
    Allows users to update their bio and avatar.
    """
    
    class Meta:
        model = Profile
        fields = ['bio', 'avatar']
        widgets = {
            'bio': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': _('Tell something about yourself...')
            }),
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make the avatar field more user-friendly
        self.fields['avatar'].widget.attrs.update({
            'class': 'form-control-file',
            'accept': 'image/*'
        })
        
    def clean_avatar(self):
        """
        Validate that the uploaded file is a valid image and not too large.
        """
        avatar = self.cleaned_data.get('avatar')
        if avatar:
            # Check file size (limit to 2MB)
            if avatar.size > 2 * 1024 * 1024:
                raise forms.ValidationError(_('Image file too large. Please keep it under 2MB.'))
            
            # Check file type
            if not avatar.content_type.startswith('image'):
                raise forms.ValidationError(_('Uploaded file is not a valid image.'))
                
        return avatar