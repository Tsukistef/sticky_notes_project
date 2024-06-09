from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from stickynotes_app.models import StickyNote, Profile

class NoteModelTest(TestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(username='test_author', password='testpassword')
        # Create a test note
        self.note = StickyNote.objects.create(
            title='Test note', 
            body='This is a test note',
            user=self.user
        )
        
    def test_note_has_title(self):
        # Test that a StickyNote object has the expected title
        note = StickyNote.objects.get(id=self.note.id)
        self.assertEqual(note.title, 'Test note')
        
    def test_note_has_body(self):
        # Test that a StickyNote object has the expected body
        note = StickyNote.objects.get(id=self.note.id)
        self.assertEqual(note.body, 'This is a test note')

class NoteViewTest(TestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(username='test_author', password='testpassword')

        # Create a test note
        self.note = StickyNote.objects.create(
            title='Test Note',
            body='This is a test note',
            user=self.user
        )

    def test_main_board_view(self):
        # Test the main board view
        self.client.login(username='test_author', password='testpassword')
        response = self.client.get(reverse('main_board'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Note')
    
    def test_view_note_view(self):
        # Test the view note view
        self.client.login(username='test_author', password='testpassword')
        response = self.client.get(reverse('view_note', args=[self.note.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Note')
        self.assertContains(response, 'This is a test note')
