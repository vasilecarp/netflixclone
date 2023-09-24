from django.db import models

class PublishStateOptions(models.TextChoices):
        # CONSTANT = 'DB_VALUE', 'Human Readable Value'
        PUBLISH = 'PU', 'Publish'
        DRAFT = 'DR', 'Draft'
        # UNLISTED = 'UN', 'Unlisted'
        # PRIVATE = 'PR', 'Private'