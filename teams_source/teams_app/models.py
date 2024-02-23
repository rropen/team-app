from django.db import models
from django.contrib.auth.models import User

#JC - Teams model
class Team(models.Model):

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=128, unique=True, null=False)
    description = models.CharField(max_length=512)
    notes = models.CharField(max_length=512, null=False, default="")
    private = models.BooleanField(default=False)
    creator_application = models.CharField(max_length=128, null=False, default="unknown") # application that created team

    def __str__(self):
        return f"{self.name}"

    @property
    def count(self):
        return Relationship.objects.filter(team=self, status=1).count()
    
    @property
    def members(self):
        return Relationship.objects.filter(team=self, status=1).all()

#JC - Role model
class Role(models.Model):

    id = models.AutoField(primary_key=True)
    role = models.CharField(max_length=65, null=False, unique=True)

    def __str__(self):
        return f"{self.role}"

#JC - Status model
class Status(models.Model):

    id = models.AutoField(primary_key=True)
    status = models.CharField(max_length=65, null=False, unique=True)

    def __str__(self):
        return f"{self.status}"

#JC - Relationship model which links the user to their team and role
class Relationship(models.Model):

    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    status = models.ForeignKey(Status, on_delete=models.CASCADE)

    class Meta:
        unique_together = (
            "user",
            "team"
        )

    def __str__(self):
        return f"User: {self.user.username}({self.user.id}) -> {self.team.name}({self.team.id}) as {self.role}"
    
    @property
    def user_profile(self):
        return UserProfile.objects.get(user=self.user)
    
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    accepted_policy = models.BooleanField()

    region = models.CharField(max_length=60, default="GB")

    def __str__(self):
        return f'{self.user.username}'
    
    @property
    def role(self):
        return Relationship.objects.filter(user=self.user, status=1)