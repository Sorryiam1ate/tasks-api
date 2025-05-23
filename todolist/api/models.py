from django.db import models


class Task(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class AstanaHubParticipant(models.Model):
    certificate_number = models.IntegerField(unique=True, null=True)
    issue_date = models.DateField(null=True)
    expiration_date = models.DateField(null=True)
    bin = models.CharField(max_length=12, unique=True, null=True)
    status = models.BooleanField(default=False)
    company_name = models.CharField(max_length=255, null=True)

    def __str__(self):
        return self.company_name
