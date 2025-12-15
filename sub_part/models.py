from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    plan = models.CharField(max_length=20, default="free")  # free / pro
    writing_level = models.CharField(max_length=30, blank=True)
    country = models.CharField(max_length=50, blank=True)
    role = models.CharField(max_length=30, blank=True)  # student, working, business

    def __str__(self):
        return self.user.username


class Submission(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    topic = models.CharField(max_length=300)
    content = models.TextField()
    word_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.topic}"



class Feedback(models.Model):
    submission = models.OneToOneField(Submission, on_delete=models.CASCADE)
    clarity_score = models.IntegerField()
    depth_score = models.IntegerField()
    structure_score = models.IntegerField()
    originality_score = models.IntegerField()
    overall_score = models.IntegerField()
    strengths = models.TextField()
    improvements = models.TextField()
    specific_suggestions = models.TextField()
    raw_json = models.JSONField()  # full JSON

    def __str__(self):
        return f"Feedback for {self.submission.id}"



class Challenge(models.Model):
    CHALLENGE_TYPES = [
        ("creative", "Creative"),
        ("opinion", "Opinion"),
        ("reflective", "Reflective"),
        ("narrative", "Narrative"),
    ]

    name = models.CharField(max_length=100)
    challenge_type = models.CharField(max_length=20, choices=CHALLENGE_TYPES)
    days = models.IntegerField(default=7)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.days} days)"

country = models.CharField(max_length=100, blank=True)
user_type = models.CharField(max_length=50, blank=True)  # student / business / professional
referral_info = models.CharField(max_length=255, blank=True)

from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    country = models.CharField(max_length=120, blank=True)
    user_type = models.CharField(max_length=50, blank=True)  # student / working professional / business
    writing_level = models.CharField(max_length=50, blank=True)  # beginner / professional / expert
    tone_preference = models.CharField(max_length=30, blank=True)  # creative / reflective / narrative / opinion
    referral_info = models.CharField(max_length=200, blank=True)
    is_premium = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username
