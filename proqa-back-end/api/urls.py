from django.urls import path
from api import views

urlpatterns = [
    path('question/', views.question),
    path('answer/', views.answer),
    path('sources/', views.sources),
    path('chat/creation/', views.creation),
    path('chat/deletion/', views.deletion),
    path('chat/hiding/', views.hiding),
    path('chat/pinning/', views.pinning),
    path('chat/history/', views.history),
    path('chat/messages/', views.messages),
    path('chat/saving/', views.saving),
    path('answer/rating/', views.rating),
    path('faq/entries/', views.faq_entries),
]
