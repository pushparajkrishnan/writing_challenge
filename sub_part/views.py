from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt

from .models import Submission, Feedback, UserProfile
from .services.ai_feedback import generate_feedback

from django.contrib.auth.models import User
from django.contrib import messages

import os

def landing(request):
    return render(request, "sub_part/landing.html")


@login_required
def dashboard(request):
    subs = Submission.objects.filter(user=request.user).order_by("-created_at")[:10]
    return render(request, "sub_part/dashboard.html", {"subs": subs})


@login_required
def topics(request):
    tones = ["creative", "opinion", "reflective", "narrative"]
    prompts = [f"{t.title()} prompt #{i+1}" for i, t in enumerate(tones[:3])]
    return render(request, "sub_part/topics.html", {"prompts": prompts})


@login_required
def editor(request, slug):
    return render(request, "sub_part/editor.html", {"topic": slug})


@login_required
def submit_writing(request):
    if request.method != "POST":
        return HttpResponseBadRequest("POST only")

    topic = request.POST.get("topic", "").strip()
    content = request.POST.get("content", "").strip()
    wc = len(content.split())

    sub = Submission.objects.create(
        user=request.user,
        topic=topic,
        content=content,
        word_count=wc,
    )

    fb = generate_feedback(content, topic)

    if fb and fb.get("feedback"):
        f = fb["feedback"]
        Feedback.objects.create(
            submission=sub,
            clarity_score=f["clarity_score"],
            depth_score=f["depth_score"],
            structure_score=f["structure_score"],
            originality_score=f["originality_score"],
            overall_score=f["overall_score"],
            strengths=f["strengths"],
            improvements=f["improvements"],
            specific_suggestions=f["specific_suggestions"],
            tokens_used=fb.get("tokens_used"),
            cost=fb.get("cost")
        )

    return redirect("history")


@login_required
def history(request):
    subs = Submission.objects.filter(user=request.user)
    return render(request, "sub_part/history.html", {"subs": subs})


def pricing(request):
    return render(request, "sub_part/pricing.html")


def leaderboard(request):
    # simple ranking — no Challenge model needed
    top = Feedback.objects.select_related("submission__user").order_by("-overall_score")[:20]
    return render(request, "sub_part/leaderboard.html", {"rows": top})

@login_required
def upgrade(request):
    profile, _ = UserProfile.objects.get_or_create(user=request.user)
    profile.is_premium = True
    profile.save()
    return render(request, "sub_part/upgrade.html", {"profile": profile})

def signup(request):
    if request.method == "POST":
        name = request.POST.get("name").strip()
        email = request.POST.get("email").strip()
        password = request.POST.get("password")
        confirm = request.POST.get("confirm")
        country = request.POST.get("country")
        user_type = request.POST.get("user_type")
        referral = request.POST.get("referral")

        if password != confirm:
            messages.error(request, "Passwords do not match.")
            return redirect("signup")

        if User.objects.filter(username=email).exists():
            messages.error(request, "Email already registered.")
            return redirect("signup")

        user = User.objects.create_user(
            username=email,
            email=email,
            password=password,
            first_name=name
        )

        # create profile
        UserProfile.objects.create(
            user=user,
            country=country,
            user_type=user_type,
            referral_info=referral,
        )

        messages.success(request, "Account created successfully. Please log in.")
        return redirect("login")

    return render(request, "sub_part/signup.html")


@login_required
def topics(request):
    profile, _ = UserProfile.objects.get_or_create(user=request.user)

    # Simple fallback
    tone = profile.tone_preference if profile.tone_preference else "general"

    EASY_TOPICS = {
        "creative": [
            "Write about a journey that changed your perspective.",
            "Describe a perfect morning in your own words.",
            "Imagine a world where people never used smartphones."
        ],
        "reflective": [
            "Write about a lesson you learned recently.",
            "Describe a moment that made you rethink something important.",
            "Write about a mistake that taught you something valuable."
        ],
        "opinion": [
            "Should schools teach financial literacy from a young age?",
            "Is social media helping or harming relationships?",
            "Should work-from-home become a permanent option?"
        ],
        "narrative": [
            "Tell the story of your most unusual day.",
            "Describe a memorable experience from childhood.",
            "Write about a time you helped someone unexpectedly."
        ],
        "general": [
            "Write about a hobby you enjoy.",
            "Describe your daily routine.",
            "Write about something new you learned recently."
        ],
    }

    prompts = EASY_TOPICS.get(tone, EASY_TOPICS["general"])

    return render(request, "sub_part/topics.html", {"prompts": prompts})
