from django.db import models
from django.contrib.auth.models import User
import os
from django.dispatch import receiver
from django.db.models.signals import post_delete

class UploadedFile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='uploads')
    file = models.FileField(upload_to='uploads/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    summary = models.JSONField(default=dict)  # Stores calculated stats
    processed_data = models.JSONField(default=list)  # Stores the parsed CSV rows
    user_upload_index = models.PositiveIntegerField(blank=True, null=True, editable=False)

    def save(self, *args, **kwargs):
        if not self.user_upload_index:
            # simple auto-increment logic scoped to the user
            max_index = UploadedFile.objects.filter(user=self.user).aggregate(models.Max('user_upload_index'))['user_upload_index__max']
            self.user_upload_index = (max_index or 0) + 1
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Upload {self.user_upload_index} by {self.user.username} - {self.uploaded_at}"

    class Meta:
        ordering = ['-uploaded_at']

@receiver(post_delete, sender=UploadedFile)
def submission_delete(sender, instance, **kwargs):
    """
    Deletes file from filesystem when corresponding `UploadedFile` object is deleted.
    """
    if instance.file:
        if os.path.isfile(instance.file.path):
            os.remove(instance.file.path)
