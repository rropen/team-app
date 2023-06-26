from django.db import models

#JC - Teams model
class Team(models.Model):

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=128, unique=True, null=False)
    description = models.CharField(max_length=512)
    notes = models.CharField(max_length=512, null=False, default="")
    private = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name}"