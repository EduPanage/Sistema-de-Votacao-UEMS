from django.db import models

# Tipo de eleição: único ou múltiplo
ELECTION_TYPE_CHOICES = (
    ('single', 'Voto Único'),
    ('multiple', 'Voto Múltiplo'),
)

class Election(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    type = models.CharField(max_length=10, choices=ELECTION_TYPE_CHOICES, default='single')
    is_published = models.BooleanField(default=False)

    def __str__(self):
        return self.title


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
    vote_token = models.CharField(max_length=128, blank=True)  # para autenticação via link

    class Meta:
        unique_together = ('election', 'email')  # um eleitor pode participar de várias eleições

    def __str__(self):
        return f"{self.name} ({self.email})"


class Vote(models.Model):
    election = models.ForeignKey(Election, on_delete=models.CASCADE, related_name="votes")
    voter = models.ForeignKey(Voter, on_delete=models.CASCADE, related_name="votes")
    option = models.ForeignKey(Option, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    vote_hash = models.CharField(max_length=128, blank=True)

    class Meta:
        unique_together = ('election', 'voter')  # só um voto válido por eleitor por eleição

    def __str__(self):
        return f"Voto de {self.voter.name} em {self.option.name}"
