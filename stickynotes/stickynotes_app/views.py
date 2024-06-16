"""This is the file where I defined the views for my sticky notes app.
There is a home view which is the welcome page, a login view
where the user can enter their details to login,
a logout view to log out of the profile, registration view
to create a new user profile, a main board which is the page
the user is redirected after logging in,
and a view, edit and delete views to interact with the notes."""

from django.contrib.auth import authenticate, login
from django.shortcuts import (
    render,
    redirect,
    get_object_or_404,
)
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from .forms import RegistrationForm
from .models import StickyNote, Profile
from .forms import StickyNoteForm, UserForm, ProfileForm


# Create your views here.
def _get_queryset(klass):
    """
    Return a QuerySet or a Manager.
    Duck typing in action: any class with a `get()` method (for
    get_object_or_404) or a `filter()` method (for get_list_or_404) might do
    the job.
    """
    # If it is a model class or anything else with ._default_manager
    if hasattr(klass, "_default_manager"):
        return klass._default_manager.all()
    return klass


def get_object_or_return_false(klass, *args, **kwargs):
    """
    Use get() to return an object, or return false if the object
    does not exist.

    klass may be a Model, Manager, or QuerySet object. All other passed
    arguments and keyword arguments are used in the get() query.

    Like with QuerySet.get(), MultipleObjectsReturned is raised if more than
    one object is found.
    """
    queryset = _get_queryset(klass)
    if not hasattr(queryset, "get"):
        klass__name = (
            klass.__name__ if isinstance(klass, type) else klass.__class__.__name__
        )
        raise ValueError(
            "First argument to get_object_or_404() must be a Model, Manager, "
            "or QuerySet, not '%s'." % klass__name
        )
    try:
        return queryset.get(*args, **kwargs)
    except queryset.model.DoesNotExist:
        return False


def home_view(request):
    '''Home view - this is the landing page.

        Args:
            request (HttpRequest): The HTTP request object.

        Returns:
            HttpResponse: The rendered home page.'''
    return render(request, "home.html")


def login_view(request):
    '''Login view. The AuthenticationForm allows user to login.

        Args:
            request (HttpRequest): The HTTP request object.

        Returns:
            HttpResponse: The rendered login page with a login form.'''
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("main_board")       # Redirect to main board URL
            else:
                messages.error(
                    request, "Invalid username or password"     # A message is displayed if username or password is incorrect.
                )
        else:
            messages.error(request, "Invalid username or password")

    else:
        form = AuthenticationForm()
    return render(request, "login.html", {"form": form})


# Logout view
def logout_view(request):
    '''Logout view. Logs out the user and redirects to the login page.

        Args:
            request (HttpRequest): The HTTP request object.

        Returns:
            HttpResponse: Redirects to the login page.'''
    logout(request)
    return redirect("login")  # Redirects to login page URL


# Registration view
def register_view(request):
    '''Registration view. Handles user registration.

        Args:
            request (HttpRequest): The HTTP request object.

        Returns:
            HttpResponse: The rendered registration page with a registration form.'''
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            messages.success(
                request, f"Account created for {username}!"
            )  # Message for successful creation of account
            return redirect("login")
    else:
        form = RegistrationForm()
    return render(request, "registration/register.html", {"form": form})


@login_required
def profile_view(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile was successfully updated!')
            return redirect('profile')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)
    
    return render(request, 'profile.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })

# Main sticky notes page
@login_required
def main_board(request):
    '''Sticky notes main board view. Displays all sticky notes.
        
        Args:
            request (HttpRequest): The HTTP request object.

        Returns:
            HttpResponse: The rendered main board page with all sticky notes.'''
    notes = StickyNote.objects.all().order_by('-created_at')  # Order by created_at in descending order
    return render(request, "main_board.html", {"notes": notes})


# Sticky note creation view - allows creation of a new note
@login_required
def create_note(request):
    '''Sticky note creation view. Allows creation of a new note.

        Args:
            request (HttpRequest): The HTTP request object.

        Returns:
            HttpResponse: The rendered create note page with a note form.'''
    if request.method == "POST":
        form = StickyNoteForm(request.POST)
        if form.is_valid():
            note = form.save(commit=False)
            note.user = request.user
            note.save()
            messages.success(request, "Sticky note created successfully!")
            return redirect("main_board")
    else:
        form = StickyNoteForm()
        return render(request, "create_note.html", {"form": form})


# Sticky note view - allows the user to visualize the note
@login_required
def view_note(request, note_id):
    '''Sticky note view. Allows the user to visualize the note.

    Args:
        request (HttpRequest): The HTTP request object.
        note_id (int): The ID of the note to be viewed.

    Returns:
        HttpResponse: The rendered view note page with the specified note'''
    note = get_object_or_404(StickyNote, id=note_id)
    return render(request, "view_note.html", {"note": note})


# Edit sticky note view - allows the user to edit the note title and description
@login_required
def edit_note(request, note_id):
    '''Edit sticky note view. Allows the user to edit the note title and description.

    Args:
        request (HttpRequest): The HTTP request object.
        note_id (int): The ID of the note to be edited.

    Returns:
        HttpResponse: The rendered edit note page with a note form.'''
    note = get_object_or_return_false(StickyNote, id=note_id, user=request.user)
    if note is False:
        messages.error(request, "You don't have permission to edit this note")
        return redirect("main_board")
    else:
        if request.method == "POST":
            form = StickyNoteForm(request.POST, instance=note)
            if form.is_valid():
                note = form.save(
                    commit=False
                )  # Fixed code, now this allows user to update note.
                note.user = request.user
                note.save()
                messages.success(request, "Sticky note updated successfully!")
                return redirect("main_board")
        else:
            form = StickyNoteForm(instance=note)
        return render(request, "edit_note.html", {"form": form, "note": note})


# Delete sticky note view - allows user to delete note from main board.
@login_required
def delete_note(request, note_id):
    '''Delete sticky note view. Allows user to delete a note from the main board.

    Args:
        request (HttpRequest): The HTTP request object.
        note_id (int): The ID of the note to be deleted.

    Returns:
        HttpResponse: The rendered delete note page or redirect to main board.'''
    note = get_object_or_return_false(StickyNote, id=note_id, user=request.user)
    if note is False:
        messages.error(request, "You don't have permission to delete this note")
        return redirect("main_board")
    else:
        if request.method == "POST":
            note.delete()
            messages.success(request, "Sticky note deleted successfully!")
            return redirect("main_board")
        return render(request, "delete_note.html", {"note": note})
