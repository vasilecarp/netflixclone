from django.db import models
from django.db.models.signals import pre_save
from django.utils import timezone
from django.utils.text import slugify

class PublishStateOptions(models.TextChoices):
        # CONSTANT = 'DB_VALUE', 'Human Readable Value'
        PUBLISH = 'PU', 'Publish'
        DRAFT = 'DR', 'Draft'
        # UNLISTED = 'UN', 'Unlisted'
        # PRIVATE = 'PR', 'Private'

class VideoQuerySet(models.QuerySet):
    def published(self):
        now = timezone.now()
        return self.filter(state=Video.VideoStateOptions.PUBLISH, publish_timestamp__lte=timezone.now())

class VideoManager(models.Manager):
    def get_queryset(self):
        return VideoQuerySet(self.model, using=self._db)
    
    def published(self):
        return self.get_queryset().published()  


class Video(models.Model):  
    VideoStateOptions = PublishStateOptions
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    slug = models.SlugField(blank=True, null=True)
    video_id = models.CharField(max_length=100, unique=True)
    active = models.BooleanField(default=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    state = models.CharField(max_length=2, choices=VideoStateOptions.choices, default=VideoStateOptions.DRAFT)
    publish_timestamp = models.DateTimeField(auto_now_add=False, auto_now=False, null=True, blank=True)

    objects = VideoManager()

    @property
    def is_published(self):
        return self.active
    
    def save(self, *args, **kwargs):        
        if self.slug is None:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

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

def publish_state_pre_save(sender, instance, *args, **kwargs):
    is_publish = instance.state == PublishStateOptions.PUBLISH
    is_draft = instance.state == PublishStateOptions.DRAFT
    if is_publish and instance.publish_timestamp is None:        
        instance.publish_timestamp = timezone.now()
    elif is_draft:
        instance.publish_timestamp = None

pre_save.connect(publish_state_pre_save, sender=Video)
