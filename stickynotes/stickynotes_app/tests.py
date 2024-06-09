from django.test import TestCase
from django.urls import reverse
from stickynotes_app.models import StickyNote, Profile

class PostModelTest(TestCase):
    def setUp(self):
        # Create an author object
        author = Profile.objects.create(user='Test Author')  # Assuming 'username' field in Profile model
        # Create a note object for testing
        StickyNote.objects.create(
            title='Test note', 
            body='This is a test note',
            user=author)
        
    def test_note_has_title(self):
        # Test that a StickyNote object has the expected title
        note = StickyNote.objects.get(id=1)
        self.assertEqual(note.title, 'Test note')
        
    def test_note_has_body(self):
        # Test that a StickyNote object has the expected body
        note = StickyNote.objects.get(id=1)
        self.assertEqual(note.body, 'This is a test note')

class NoteViewTest(TestCase):
    def setUp(self):
        # Create an author object
        author = Profile.objects.create(username='Test Author')  # Assuming 'username' field in Profile model
        # Create a StickyNote object for testing views
        StickyNote.objects.create(
            title='Test Note', 
            body='This is a test note', 
            user=author)

    def test_note_list_view(self):
        # Test the note-list view
        response = self.client.get(reverse('main_board'))  # Ensure the URL name is correct
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Note')
    
    def test_note_detail_view(self):
        # Test the note-detail view
        note = StickyNote.objects.get(id=1)
        response = self.client.get(reverse('view_note', args=[note.id]))  # Ensure the URL name is correct
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Note')
        self.assertContains(response, 'This is a test note')
