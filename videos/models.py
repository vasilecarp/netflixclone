from django.db import models

class Video(models.Model):
    class VideoStateOptions(models.TextChoices):
        # CONSTANT = 'DB_VALUE', 'Human Readable Value'
        PUBLISH = 'PU', 'Publish'
        DRAFT = 'DR', 'Draft'
        # UNLISTED = 'UN', 'Unlisted'
        # PRIVATE = 'PR', 'Private'

    title = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    slug = models.SlugField(blank=True, null=True)
    video_id = models.CharField(max_length=100, null=True, blank=True)
    active = models.BooleanField(default=True)
    # timestamp = models.DateTimeField(auto_now_add=True)
    # updated = models.DateTimeField(auto_now=True)
    state = models.CharField(max_length=2, choices=VideoStateOptions.choices, default=VideoStateOptions.DRAFT)
    # publish_timestamp = models.DateTimeField(auto_now_add=False, auto_now=False, null=True, blank=True)
    @property
    def is_published(self):
        return self.active

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
