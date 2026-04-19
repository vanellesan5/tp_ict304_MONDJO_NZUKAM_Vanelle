from django.db import models
import uuid

class Compte(models.Model):
    TYPE_CHOICES = [
        ('courant', 'Compte Courant'),
        ('epargne', 'Compte Épargne'),
        ('professionnel', 'Compte Professionnel'),
    ]
    STATUT_CHOICES = [
        ('actif', 'Actif'),
        ('suspendu', 'Suspendu'),
        ('ferme', 'Fermé'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    titulaire = models.CharField(max_length=200)
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    solde = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    devise = models.CharField(max_length=3, default='XAF')
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='actif')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.titulaire} — {self.solde} {self.devise}"
    
    class Meta:
        ordering = ['-created_at']

class Transaction(models.Model):
    TYPE_CHOICES = [
        ('depot', 'Dépôt'),
        ('retrait', 'Retrait'),
        ('transfert', 'Transfert'),
    ]
    STATUT_CHOICES = [
        ('en_attente', 'En Attente'),
        ('reussi', 'Réussi'),
        ('echoue', 'Échoué'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    compte = models.ForeignKey(Compte, on_delete=models.CASCADE, related_name='transactions')
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    montant = models.DecimalField(max_digits=15, decimal_places=2)
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='en_attente')
    description = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.type.upper()} — {self.montant} — {self.statut}"
    
    class Meta:
        ordering = ['-created_at']