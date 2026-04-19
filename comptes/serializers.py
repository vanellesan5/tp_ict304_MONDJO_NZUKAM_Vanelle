from rest_framework import serializers
from .models import Compte, Transaction

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ['id', 'type', 'montant', 'statut', 'description', 'created_at']

class CompteSerializer(serializers.ModelSerializer):
    transactions = TransactionSerializer(many=True, read_only=True)
    
    class Meta:
        model = Compte
        fields = ['id', 'titulaire', 'type', 'solde', 'devise', 'statut', 'created_at', 'updated_at', 'transactions']
        read_only_fields = ['id', 'created_at', 'updated_at']

class CompteListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Compte
        fields = ['id', 'titulaire', 'type', 'solde', 'devise', 'statut', 'created_at']