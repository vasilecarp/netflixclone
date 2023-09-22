from django.test import TestCase

from .models import Video   

class VideoModelTestCase(TestCase):
    def setUp(self):
        Video.objects.create(title="This is my title")

    def test_valid_title(self):
        title = "This is my title"
        qs = Video.objects.filter(title=title)
        self.assertTrue(qs.exists())

    def test_created_count(self):
        title = "This is my title"
        qs = Video.objects.all()
        self.assertEqual(qs.count(), 1)

    def test_draft_case(self):
        qs = Video.objects.filter(state=Video.VideoStateOptions.DRAFT)
        self.assertEqual(qs.count(), 1)