# Exercice 1 : Modélisation

# Système de Gestion d'Atelier Mécanique

## Contexte

Vous devez concevoir un système de gestion pour un atelier de réparation qui prend en charge des motos et des automobiles. Le système doit permettre de suivre les véhicules et leurs interventions.

## Spécifications Techniques

### Caractéristiques Communes des Véhicules

Chaque véhicule en atelier doit être caractérisé par :

* Un numéro d'immatriculation
* Un kilométrage
* Une date de mise en circulation
* Un état diagnostic ("En attente", "En réparation", "Prêt")

### Gestion des Automobiles

Fonctionnalités spécifiques :

* Nombre de portes
* Type de carburant
* Calcul du coût de révision (base 200€ + 50€ par année d'ancienneté)

### Gestion des Motos

Fonctionnalités spécifiques :

* Cylindrée
* Type de permis requis
* Calcul du coût de révision (base 150€ + 30€ par année d'ancienneté)

## Implémentation Requise


1. Modélisez les structures de données pour gérer les véhicules
2. Implémentez les fonctionnalités suivantes :
   * Enregistrement d'un nouveau véhicule
   * Calcul des coûts de révision
   * Affichage des caractéristiques techniques
   * Mise à jour de l'état du véhicule

## Points d'Attention

* Le système doit pouvoir accueillir facilement de nouveaux types de véhicules
* La logique commune doit être centralisée (fichier index.ts avec tous les tests)
* Le code doit être maintenable et évolutif

## Extension Possible

Ajoutez une classe Client avec les propriétés suivantes :

* Nom
* Prénom
* Liste des véhicules possédés
* Méthode pour calculer le coût total des révisions de ses véhicules