from django.urls import path
from . import views

urlpatterns = [
    path("", views.landing, name="landing"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("topics/", views.topics, name="topics"),
    path("editor/<slug:slug>/", views.editor, name="editor"),
    path("submit/", views.submit_writing, name="submit_writing"),
    path("history/", views.history, name="history"),
    path("pricing/", views.pricing, name="pricing"),
    path("leaderboard/", views.leaderboard, name="leaderboard"),
    path("upgrade/", views.upgrade, name="upgrade"),
    path("signup/", views.signup, name="signup"),
]
