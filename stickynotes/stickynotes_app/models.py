'''Models for the Sticky Notes app.

This file contains two models: 
Profile and StickyNote.

Classes:
    Profile: Represents the user profile, which includes 
    fields for bio, location, and birth date.
    StickyNote: Represents a sticky note, which includes 
    fields for title, body, creation timestamp, and user reference.
'''
from django.db import models
from django.contrib.auth.models import User
# Create your models here.

# Model representing the user profile - will use this to customise user info in the future updates
class Profile(models.Model):
    '''Model representing the user profile.

    Attributes:
        user (OneToOneField): A reference to the User model, representing the user associated with the profile.
        bio (TextField): A field for the user's biography.
        location (CharField): A field for the user's location.
        birth_date (DateField): A field for the user's birth date.'''
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=30, blank=True)
    birth_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.user.username
    

# Model representing the sticky note
class StickyNote(models.Model):
    '''Model representing a sticky note.

    Attributes:
        title (CharField): A field for the title of the sticky note.
        body (TextField): A field for the body/content of the sticky note.
        created_at (DateTimeField): A field for the creation timestamp of the sticky note.
        user (ForeignKey): A reference to the User model,
        representing the user who created the sticky note.    '''
    # Allow user to customize note color
    COLOR_CHOICES = (
        ('#FFB3BA', 'Soft Pink'),
        ('#FFDFBA', 'Peach'),
        ('#FFFFBA', 'Light Yellow'),
        ('#BAFFC9', 'Light Green'),
        ('#BAE1FF', 'Light Blue'),
        ('#D3C4E3', 'Lavender')
    )
    title = models.CharField(max_length=100)
    body = models.TextField(max_length=300)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    color = models.CharField(max_length=20, choices=COLOR_CHOICES, default='#FFFFBA')
    
    def __str__(self):
        return self.title
