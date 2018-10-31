from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class ApplicationStatus(models.Model):
  value = models.CharField(max_length=20)
  def __str__(self):
    return self.value

class JobApplication(models.Model):
  user = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True, blank=True)
  applicationStatus = models.ForeignKey(ApplicationStatus, on_delete=models.DO_NOTHING, null=True, blank=True)
  jobTitle = models.CharField(max_length=200)
  company = models.CharField(max_length=200)
  applyDate = models.CharField(max_length=200)
  msgId = models.CharField(max_length=200)
  source = models.CharField(max_length=200, default='')
  def __str__(self):
    return self.jobTitle + '@' + self.company
