# 2- Compte Bancaire

## 📋 Contexte métier

Vous êtes stagiaire dans une fintech. Votre mentor vous dit :

*"Pour commencer, on va faire un mini-système de compte bancaire. Nos clients ont des comptes avec un solde, ils peuvent déposer et retirer de l'argent. Important : on ne peut pas avoir un solde négatif, c'est la règle métier numéro 1 ! Et il faut garder un historique des opérations pour la conformité."*

### User Story

**En tant que** client de la banque\n**Je veux** gérer mon compte bancaire (dépôts, retraits)\n**Afin de** suivre mes finances en toute sécurité

### Critères d'acceptation

* ✅ Je peux créer un compte avec un solde initial
* ✅ Je peux déposer de l'argent (montant positif uniquement)
* ✅ Je peux retirer de l'argent si j'ai suffisamment de fonds
* ✅ Je ne peux pas avoir un solde négatif
* ✅ Je peux consulter mon solde et l'historique des opérations


## 🎯 Travail à faire

### Étape 1 : Modélisation

**Questions à se poser :**

* Quelle est l'entité principale ?
* Quelles données doit-elle stocker ?
* Quelles validations métier implémenter ?
* Comment modéliser l'historique ?

### Étape 2 : Implémentation


Ouvrez VS code et codez-moi tout ça ! 😎


### Étape 3 : Tests avancés

* Test des validations (montants négatifs)
* Test de l'historique des opérations
* Test des cas limites (solde exact)


```typescript
// exemple simple :
const compte = new CompteBancaire("12345", "Jean Martin", 100);

console.log(compte.getSolde()); // 100

compte.deposer(50);
console.log(compte.getSolde()); // 150

const reussit = compte.retirer(30);
console.log(reussit); // true
console.log(compte.getSolde()); // 120

const echec = compte.retirer(200);
console.log(echec); // false (solde insuffisant)
console.log(compte.getSolde()); // 120 (inchangé)
```