# Lexique POO TypeScript

### 🔷 Classe

**Définition :** Modèle (blueprint) pour créer des objets avec propriétés et comportements.

**Analogie :** La classe est le plan d'une voiture, l'objet est la voiture construite.

```typescript
class Voiture {
  // Propriétés (données/état)
  marque: string;
  annee: number;
  
  // Constructeur (initialisation)
  constructor(marque: string, annee: number) {
    this.marque = marque;
    this.annee = annee;
  }
  
  // Méthode (comportement/action)
  demarrer(): void {
    console.log(`${this.marque} de ${this.annee} démarre`);
  }
  
  // Méthode avec retour
  getAge(): number {
    return new Date().getFullYear() - this.annee;
  }
}
```

**Points clés :**

* Une classe = structure + comportements
* Mot-clé `class` suivi du nom (PascalCase)
* Contient propriétés, constructeur, méthodes


---

### 🔷 Objet / Instance

**Définition :** Réalisation concrète d'une classe. Chaque instance a ses propres valeurs.

```typescript
const maVoiture = new Voiture("Peugeot", 2020);
const taVoiture = new Voiture("Renault", 2022);

maVoiture.demarrer(); // "Peugeot de 2020 démarre"
taVoiture.demarrer(); // "Renault de 2022 démarre"

console.log(maVoiture.getAge()); // 5
console.log(taVoiture.getAge()); // 3
```

**Points clés :**

* Mot-clé `new` pour instancier
* Chaque instance = espace mémoire distinct
* Même classe, données différentes


---

### 🔷 Constructeur

**Définition :** Méthode spéciale appelée automatiquement lors de l'instanciation avec `new`.

```typescript
// contructeur V1 (débutant)
class Personne {
  nom: string;
  age: number;
  
  constructor(nom: string, age: number) {
    console.log("Création d'une personne");
    this.nom = nom;
    this.age = age;
  }
}

// contructeur V2 (avancé)
class PersonneV2 {
  constructor(
    public nom: string,      // public automatiquement
    private age: number,      // private automatiquement
    readonly id: string = crypto.randomUUID() // avec valeur par défaut + readonly = empêche de modifier l'attribut après son initialisation
  ) {
    // this.nom et this.age créés automatiquement
  }
}

const p = new PersonneV2("Alice", 30);
console.log(p.nom); // "Alice" ✅
console.log(p.age); // Erreur : private ❌
```

**Points clés :**

* Un seul constructeur par classe
* Paramètres du constructeur = valeurs d'initialisation
* Raccourci TS avec modificateurs dans les paramètres
* `this` = référence à l'instance courante


---

### 🔷 Encapsulation

**Définition :** Principe de cacher les détails internes et d'exposer uniquement une interface publique contrôlée.

```typescript
class CompteBancaire {
  private solde: number = 0;        // Privé : invisible de l'extérieur
  readonly numeroCompte: string;    // Public mais non modifiable
  
  constructor(numero: string) {
    this.numeroCompte = numero;
  }
  
  // Interface publique contrôlée (public par défaut)
  deposer(montant: number): void {
    if (montant <= 0) {
      throw new Error("Montant invalide");
    }
    this.solde += montant;
  }
  
  retirer(montant: number): boolean {
    if (montant > this.solde) {
      return false; // Solde insuffisant
    }
    this.solde -= montant;
    return true;
  }
  
  // Getter pour lecture seule
  getSolde(): number {
    return this.solde;
  }
}

const compte = new CompteBancaire("FR123456");
compte.deposer(100);
console.log(compte.getSolde()); // 100 ✅
console.log(compte.solde); // Erreur : private ❌
compte.solde = 99999; // Erreur : private ❌
```

**Avantages :**

* Protection des données sensibles
* Validation centralisée
* Flexibilité de modification interne sans casser l'interface publique


---

### 🔷 Modificateurs d'accès

**Définition :** Contrôlent la visibilité et l'accès aux membres d'une classe.

| Modificateur | Classe | Enfants | Extérieur |
|--------------|--------|---------|-----------|
| `public` (défaut) | ✅      | ✅       | ✅         |
| `protected`  | ✅      | ✅       | ❌         |
| `private`    | ✅      | ❌       | ❌         |

```typescript
class Vehicule {
  public marque: string;           // Accessible partout / par défaut
  protected vitesseMax: number;    // Classe + enfants
  private numeroSerie: string;     // Classe uniquement
  
  constructor(marque: string, vitesseMax: number, serie: string) {
    this.marque = marque;
    this.vitesseMax = vitesseMax;
    this.numeroSerie = serie;
  }
  
  private verifierSerie(): boolean {
    return this.numeroSerie.length === 10;
  }
}

class Voiture extends Vehicule {
  afficherVitesseMax(): void {
    console.log(this.vitesseMax);    // ✅ protected accessible
    console.log(this.numeroSerie);   // ❌ private non accessible
  }
}

const v = new Vehicule("Tesla", 250, "ABC1234567");
console.log(v.marque);          // ✅ public
console.log(v.vitesseMax);      // ❌ protected
console.log(v.numeroSerie);     // ❌ private
```

**Convention :** Préfixer les propriétés privées avec `_` (optionnel)

```typescript
class User {
  private _password: string;
  
  constructor(password: string) {
    this._password = password;
  }
}
```
