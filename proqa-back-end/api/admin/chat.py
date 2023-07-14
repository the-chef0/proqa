from django.contrib.admin import TabularInline, ModelAdmin

from api.models import Answer


class QAInline(TabularInline):
    """Inline model to show Q&A pairs."""
    extra = 0
    fields = ["question", "content", "rating"]
    model = Answer
    readonly_fields = fields


class SessionAdmin(ModelAdmin):
    """Model admin for chat session model."""
    readonly_fields = ["title", "author", "hidden", "upvotes", "downvotes"]
    inlines = [QAInline]


class AnswerAdmin(ModelAdmin):
    """Model admin for answer model."""
    readonly_fields = ["question", "session", "context", "model", "template", "content", "rating"]


class QuestionAdmin(ModelAdmin):
    """Model admin for question model."""
    readonly_fields = ["summary", "session", "content"]
