from django.test import TestCase
from django.urls import reverse
from .models import StickyNote, Profile
# Create your tests here.

class PostModelTest(TestCase):
    def setUP(self):
        # Create an author object
        author = Profile.objects.create(name='Test Author')
        # Create a note object for testing
        StickyNote.objects.create(
            title='Test note', 
            body='This is a test note',
            user=author)
        
    def test_note_has_title(self):
        #Test that a Stickynote object has the expected title
        note = StickyNote.objects.get(id=1)
        self.assertEqual(note.title, 'Test note')
        
    def test_note_has_body(self):
        # Test that Stickynote object has expected body
        note = StickyNote.objects.get(id=1)
        self.assertEqual(note.body, 'This is a test note')
        
    # def test_note_delete(self):
    #     note = StickyNote.objects.get(id=1)
    #     note.delete()
    #     self.assertEqual(??)
    
class NoteViewTest(TestCase):
    def setUp(self):
        # Create an author object
        author = Profile.objects.create(name='Test Author')
        # Create a Stickynote object for testing views
        StickyNote.objects.create(
            title='Test Note', 
            body='This is a test note', 
            user=author)

    def test_note_list_view(self):
        # Test the note-list view
        response = self.client.get(reverse('post_list'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response, 'Test Note')
    
    def test_note_detail_view(self):
        # Test the note-detail view
        note = StickyNote.objects.get(id=1)
        response = self.client.get(reverse('note_detail', args=[str(note.id)]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Note')
        
    def test_note_detail_view(self):
        # Test the note detail view
        note = StickyNote.objects.get(id=1)
        response = self.client.get(reverse('note_detail', args=[str(note.id)]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Note')
        self.assertContains(response, 'This is a Test Note')