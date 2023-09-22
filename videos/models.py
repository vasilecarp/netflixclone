from django.db import models
from django.utils import timezone

class Video(models.Model):
    class VideoStateOptions(models.TextChoices):
        PUBLISHED = 'PU', 'Publish'
        DRAFT = 'DR', 'Draft'
        # PRIVATE = 'PR', 'Private'
        # UNLISTED = 'UN', 'Unlisted'

    title = models.CharField(max_length=100)
    description = models.TextField(max_length=500, blank=True, null=True)
    slug = models.SlugField(blank=True, null=True)
    video_id = models.CharField(max_length=100, blank=True, null=True)
    active = models.BooleanField(default=True)
    # timestamp = models.DateTimeField(auto_now_add=True)
    # updated = models.DateTimeField(auto_now=True)
    state = models.CharField(max_length=2, choices=VideoStateOptions.choices, default=VideoStateOptions.DRAFT)
    publish_timestamp = models.DateTimeField(auto_now=False, auto_now_add=False, null=True, blank=True)
    
    @property
    def is_published(self):
        return self.active
    
    def save(self, *args, **kwargs):
        if self.state == self.VideoStateOptions.PUBLISH and self.publish_timestamp is None:
            print('save as timestamp for published')
            self.publish_timestamp = timezone.now()
        elif self.state == self.VideoStateOptions.DRAFT:            
            self.publish_timestamp = None
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
    
class VideoAllProxy(Video):
    class Meta:
        proxy = True
        verbose_name = 'All video'
        verbose_name_plural = 'All videos'

class VideoPublishedProxy(Video):
    class Meta:
        proxy = True
        verbose_name = 'Published video'
        verbose_name_plural = 'Published videos'