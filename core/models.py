from django.db import models
from django.contrib.auth.models import User

# Tipo de eleição: único ou múltiplo
ELECTION_TYPE_CHOICES = (
    ('single', 'Voto Único'),
    ('multiple', 'Voto Múltiplo'),
)

class Election(models.Model):
    theme = models.CharField(max_length=200, verbose_name='Tema')
    description = models.TextField(blank=True, null=True, verbose_name='Descrição')
    start_date = models.DateTimeField(verbose_name='Início')
    end_date = models.DateTimeField(verbose_name='Fim')
    type = models.CharField(max_length=10, choices=ELECTION_TYPE_CHOICES, default='single', verbose_name='Tipo de Voto')
    document = models.FileField(upload_to='election_documents/', blank=True, null=True, verbose_name='Documento')
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name='Criado por')
    is_published = models.BooleanField(default=False)

    def __str__(self):
        return self.theme


class Option(models.Model):
    election = models.ForeignKey(Election, on_delete=models.CASCADE, related_name="options")
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Voter(models.Model):
    election = models.ForeignKey(Election, on_delete=models.CASCADE, related_name="voters")
    name = models.CharField(max_length=100)
    email = models.EmailField()
    has_voted = models.BooleanField(default=False)
    vote_token = models.CharField(max_length=128, blank=True)

    class Meta:
        unique_together = ('election', 'email')

    def __str__(self):
        return f"{self.name} ({self.email})"


class Vote(models.Model):
    election = models.ForeignKey(Election, on_delete=models.CASCADE, related_name="votes")
    voter = models.ForeignKey(Voter, on_delete=models.CASCADE, related_name="votes")
    option = models.ForeignKey(Option, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    vote_hash = models.CharField(max_length=128, blank=True)

    class Meta:
        unique_together = ('election', 'voter')

    def __str__(self):
        return f"Voto de {self.voter.name} em {self.option.name}"