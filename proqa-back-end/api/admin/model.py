from django.contrib.admin import ModelAdmin
from django.http import HttpResponseRedirect
from django.urls import reverse


def handle_change_button(self, request, obj):
    """
    Activates this model instance and deactivates all others.
    """
    if "_activate" in request.POST:
        obj._meta.model.objects.exclude(pk=obj.pk).update(active=False)
        obj.active = True
        obj.save()
        self.message_user(request,
                         f"{obj.name} was activated successfully.")
    else:
        self.message_user(request,
                         f"{obj.name} was changed successfully.")
    return HttpResponseRedirect(request.path_info)

def handle_save_button(self, request, obj):
    """
    Returns back to newly created model after saving to allow activation right after.
    """
    self.message_user(request,
                      f"{obj.name} was added successfully.")
    return HttpResponseRedirect(reverse(f'admin:api_{obj.__class__.__name__}_change'.lower(), args=[obj.pk]))

class PromptTemplateAdmin(ModelAdmin):
    """
    Model admin for prompt template model.
    """
    readonly_fields = ["active"]

    def response_change(self, request, obj):
        """
        Handles PromptTemplate instance change
        """
        return handle_change_button(self, request, obj)

    def response_add(self, request, obj):
        """
        Handles PromptTemplate instance creation
        """
        return handle_save_button(self, request, obj)

class LLMAdmin(ModelAdmin):
    """
    Model admin for LLM model.
    """
    readonly_fields = ["active"]

    def response_change(self, request, obj):
        """
        Handles LLM instance change
        """
        return handle_change_button(self, request, obj)

    def response_add(self, request, obj):
        """
        Handles LLM instance creation
        """
        return handle_save_button(self, request, obj)
