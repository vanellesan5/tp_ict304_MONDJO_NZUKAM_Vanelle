from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Compte, Transaction
from .serializers import CompteSerializer, CompteListSerializer, TransactionSerializer

class CompteViewSet(viewsets.ModelViewSet):
    queryset = Compte.objects.all()
    serializer_class = CompteSerializer
    
    def get_serializer_class(self):
        if self.action == 'list':
            return CompteListSerializer
        return CompteSerializer
    
    @action(detail=True, methods=['post'])
    def depot(self, request, pk=None):
        """Effectuer un dépôt sur le compte"""
        compte = self.get_object()
        montant = request.data.get('montant')
        
        if not montant or float(montant) <= 0:
            return Response(
                {'erreur': 'Le montant doit être positif'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Créer la transaction
        transaction = Transaction.objects.create(
            compte=compte,
            type='depot',
            montant=montant,
            statut='reussi',
            description=request.data.get('description', 'Dépôt')
        )
        
        # Mettre à jour le solde
        compte.solde += float(montant)
        compte.save()
        
        return Response({
            'message': 'Dépôt effectué avec succès',
            'solde': compte.solde,
            'transaction': TransactionSerializer(transaction).data
        }, status=status.HTTP_200_OK)
    
    @action(detail=True, methods=['post'])
    def retrait(self, request, pk=None):
        """Effectuer un retrait sur le compte"""
        compte = self.get_object()
        montant = request.data.get('montant')
        
        if not montant or float(montant) <= 0:
            return Response(
                {'erreur': 'Le montant doit être positif'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if float(montant) > float(compte.solde):
            return Response(
                {'erreur': 'Solde insuffisant'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Créer la transaction
        transaction = Transaction.objects.create(
            compte=compte,
            type='retrait',
            montant=montant,
            statut='reussi',
            description=request.data.get('description', 'Retrait')
        )
        
        # Mettre à jour le solde
        compte.solde -= float(montant)
        compte.save()
        
        return Response({
            'message': 'Retrait effectué avec succès',
            'solde': compte.solde,
            'transaction': TransactionSerializer(transaction).data
        }, status=status.HTTP_200_OK)
    
    @action(detail=True, methods=['get'])
    def historique(self, request, pk=None):
        """Obtenir l'historique des transactions"""
        compte = self.get_object()
        transactions = compte.transactions.all()
        serializer = TransactionSerializer(transactions, many=True)
        return Response(serializer.data)