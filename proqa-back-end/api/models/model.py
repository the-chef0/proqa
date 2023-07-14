from django.db import models
from django.core.exceptions import ValidationError

class PromptTemplate(models.Model):
    """
    Represents a template for generating prompts in the application
    """
    name = models.CharField(max_length=100, unique=True)
    active = models.BooleanField(default=False)
    instruction = models.TextField()
    question_format = models.TextField()
    answer_format = models.TextField()
    separator = models.CharField(max_length=16, default="", blank=True)

    def clean(self):
        """
        Checks if the prompt template is correctly made.
        """
        if r'{context}' not in self.question_format:
            raise ValidationError(r"Prompt template must contain a slot for the context in the \
                                    form {context}.")
        if r'{question}' not in self.question_format:
            raise ValidationError(r"Prompt template must contain a slot for the question in the \
                                    form {question}.")
        if r'{answer}' not in self.answer_format:
            raise ValidationError(r"Prompt template must contain a slot for the answer in the \
                                    form {answer}.")

    class Meta:
        """
        Meta class for prompt template.
        There can only be one active prompt template.
        """
        constraints = [
            models.UniqueConstraint(
                fields=['name'],
                condition=models.Q(active=True),
                name='current_template')
        ]

    def __str__(self):
        return f'{self.name}'

class LLM(models.Model):
    """
    Identifier model for a Large Language model weights file.
    """
    name = models.CharField(max_length=100, unique=True)
    context_size = models.PositiveIntegerField(default=2048)
    description = models.TextField(blank=True, null=True)
    temperature = models.FloatField(default=0.8)
    gpu_layers = models.PositiveIntegerField(default=0)
    batch_size = models.PositiveIntegerField(default=1024)
    active = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        """
        Meta class for large language model
        There can only be one active model. 
        """
        constraints = [
            models.UniqueConstraint(
                fields=['active'],
                condition=models.Q(active=True),
                name='current_model')
        ]
