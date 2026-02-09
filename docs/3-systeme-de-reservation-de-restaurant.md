# 3- Système de réservation de restaurant

## 📋 Contexte métier

Vous aidez un restaurateur, Pierre, qui explique :

*"Mon restaurant a 15 tables de différentes tailles. Les clients réservent par téléphone et je note tout sur un carnet ! J'aimerais un système simple : créer une réservation avec le nom du client, le nombre de personnes, la date et l'heure. Et surtout, pouvoir vérifier rapidement si j'ai une table libre."*

### User Story

**En tant que** restaurateur\n**Je veux** gérer les réservations de tables\n**Afin d'** optimiser le service et éviter les doublons

### Critères d'acceptation

* ✅ Je peux créer une réservation avec nom, nombre de personnes, date/heure
* ✅ Je peux confirmer ou annuler une réservation
* ✅ Je peux voir le statut d'une réservation
* ✅ Je peux lister toutes les réservations d'une date


### Étape 1 : Modélisation

**Réflexion :**

* Quelles sont les entités ? (Réservation, Table ?)
* Quels états peut avoir une réservation ?
* Quelles informations sont indispensables ?

### Étape 2 : Implémentation

Go, go go !

### Étape 3 : Tests complets

* Test de tous les changements de statut
* Test du format de la date dans getResume()
* Test qu'on ne peut pas confirmer une réservation annulée