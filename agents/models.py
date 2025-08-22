from django.db import models

# Create your models here.

class Agent(models.Model):
    MODEL_CHOICES = [
        ('transformer', 'Transformer'),
        ('gpt', 'GPT'),
        ('llama', 'LLaMA'),
        ('bert', 'BERT'),
        ('other', 'Other'),
    ]

    model_architecture = models.CharField(
        max_length=50,
        choices=MODEL_CHOICES,
        default='transformer',
        verbose_name='Model Architecture'
    )
    checkpoint = models.CharField(
        max_length=200,
        help_text='Hugging Face model path',
        verbose_name='Checkpoint (Hugging Face Model)'
    )
    parameters_in_billions = models.FloatField(
        verbose_name='Parameters (Billions)'
    )
    fine_tuning = models.TextField(
        blank=True,
        verbose_name='Fine-Tuning Details'
    )
    context_of_behavior = models.TextField(
        verbose_name='Context of Behavior'
    )
    name = models.CharField(
        max_length=100,
        verbose_name='Agent Name'
    )
    description = models.TextField(
        blank=True,
        verbose_name='Description'
    )

    def __str__(self):
        return self.name
