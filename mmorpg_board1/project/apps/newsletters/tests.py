from django.test import TestCase
from .models import Newsletter

class NewslettersTest(TestCase):
    def test_newsletter_creation(self):
        nl = Newsletter.objects.create(
            subject='Test Newsletter',
            message='Test message'
        )
        self.assertEqual(nl.subject, 'Test Newsletter')
        self.assertFalse(nl.is_sent)