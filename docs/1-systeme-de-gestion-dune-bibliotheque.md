# 1- Système de gestion d'une bibliothèque

## Contexte métier

Vous travaillez pour une petite bibliothèque municipale à Saint Pavace. Le bibliothécaire vous explique :

*"Actuellement, on gère tout sur papier ! J'aimerais un petit système pour enregistrer nos livres et suivre les emprunts. On a environ 500 livres, et nos adhérents peuvent emprunter jusqu'à 3 livres à la fois. J'ai besoin de savoir rapidement si un livre est disponible et qui l'a emprunté."*

### User Story

**En tant que** bibliothécaire\n**Je veux** pouvoir enregistrer les livres et gérer les emprunts\n**Afin de** suivre efficacement l'état de ma collection

### Critères d'acceptation

* ✅ Je peux créer un livre avec titre, auteur, ISBN
* ✅ Je peux marquer un livre comme emprunté ou disponible
* ✅ Je peux voir qui a emprunté un livre
* ✅ Un livre emprunté ne peut pas être emprunté par quelqu'un d'autre


## 💡Méthodo :

### Étape 1 : Modélisation

**Identifiez les entités** dans le contexte ci-dessus :

* Quels sont les "objets" métier ?
* Quelles sont leurs propriétés ? Accès ?
* Quelles sont leurs actions/méthodes ? Accès ?

**=> Dessinez un diagramme de classe simple** 


### Étape 2 : Implémentation 


Ouvrez VS code et codez-moi tout ça ! 😎


### Étape 3 : Tests à implémenter

Écrivez des tests qui vérifient :

* Création d'un livre
* Emprunt d'un livre disponible
* Impossibilité d'emprunter un livre déjà emprunté
* Retour d'un livre


```typescript
// Exemple de test super simple avec 1 seule classe :) (more is less ! ! !)

// Tests à faire passer :
const livre1 = new Livre("1984", "George Orwell", "978-0451524935");
console.log(livre1.getStatut()); // "Disponible"

livre1.emprunter("Alice Dubois");
console.log(livre1.getStatut()); // "Emprunté par Alice Dubois"

livre1.rendre();
console.log(livre1.getStatut()); // "Disponible"
```