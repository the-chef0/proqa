from django.contrib import admin
from django.contrib.admin import ModelAdmin

from api.admin.chat import QuestionAdmin, AnswerAdmin, SessionAdmin
from api.admin.collection import CollectionAdmin, SourceAdmin, ChunkAdmin
from api.admin.model import PromptTemplateAdmin, LLMAdmin
from api.models import (
    Question,
    Answer,
    ChatSession,
    Collection,
    Source,
    Chunk,
    PromptTemplate,
    LLM,
    FAQEntry
)

admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer, AnswerAdmin)
admin.site.register(ChatSession, SessionAdmin)
admin.site.register(FAQEntry, ModelAdmin)

admin.site.register(Collection, CollectionAdmin)
admin.site.register(Source, SourceAdmin)
admin.site.register(Chunk, ChunkAdmin)

admin.site.register(PromptTemplate, PromptTemplateAdmin)
admin.site.register(LLM, LLMAdmin)
