# 3- Exercice code à refacto

## 📋 Contexte

Vous venez d'être embauché(e) comme développeur(euse) dans une banque. Votre premier mission ? Reprendre le code d'un ancien stagiaire qui a développé le logiciel de gestion des distributeurs automatiques de billets (DAB).

Le problème ? Le code fonctionne... mais c'est un vrai plat de spaghettis 🍝 ! Votre chef de projet vous demande de **refactoriser ce code en utilisant la Programmation Orientée Objet** pour le rendre maintenable, extensible et professionnel.


## 🛠️ Votre mission

### **Phase 1 : Analyser le code existant** 🔍

### **Phase 2 : Concevoir votre architecture POO** 📐

### **Phase 3 : Coder votre solution** 💻

### **Phase 4 : Tester votre code** 🧪


\

Le code : 

```typescript
// ========================================
// DISTRIBUTEUR DE BILLETS - CODE PROCÉDURAL DÉGUEULASSE
// ========================================

// Les comptes dans un tableau d'objets littéraux
let comptes = [
  {numero: "FR001", nom: "Dupont", prenom: "Alice", solde: 1500, pin: "1234", bloque: false, tentatives: 0},
  {numero: "FR002", nom: "Martin", prenom: "Bob", solde: 500, pin: "5678", bloque: false, tentatives: 0},
  {numero: "FR003", nom: "Durand", prenom: "Claire", solde: 2000, pin: "9999", bloque: false, tentatives: 0},
  {numero: "FR004", nom: "Leroy", prenom: "David", solde: 300, pin: "0000", bloque: false, tentatives: 0}
];

// Les billets du distributeur 
let billets = [10, 20, 30];

// Historique des opérations (tableau de strings)
let historique: string[] = [];

// ========================================
// FONCTIONS
// ========================================

function trouverCompte(numero: string) {
  for (let i = 0; i < comptes.length; i++) {
    if (comptes[i].numero === numero) {
      return i; // retourne l'index
    }
  }
  return -1;
}

function verifierPin(numero: string, pin: string): boolean {
  let index = trouverCompte(numero);
  
  if (index === -1) {
    console.log("Compte introuvable");
    return false;
  }
  
  let compte = comptes[index];
  
  if (compte.bloque) {
    console.log("❌ Compte bloqué. Contactez votre banque.");
    historique.push(numero + " - Tentative sur compte bloqué");
    return false;
  }
  
  if (pin === compte.pin) {
    compte.tentatives = 0;
    console.log("✅ Code PIN correct");
    historique.push(numero + " - Authentification réussie - " + compte.prenom + " " + compte.nom);
    return true;
  } else {
    compte.tentatives = compte.tentatives + 1;
    console.log("❌ PIN incorrect, tentative " + compte.tentatives + "/3");
    historique.push(numero + " - PIN incorrect (tentative " + compte.tentatives + ")");
    
    if (compte.tentatives >= 3) {
      compte.bloque = true;
      console.log("🔒 COMPTE BLOQUÉ après 3 tentatives !");
      historique.push(numero + " - COMPTE BLOQUÉ");
    }
    return false;
  }
}

function afficherSolde(numero: string) {
  let index = trouverCompte(numero);
  
  if (index === -1) {
    console.log("Compte introuvable");
    return;
  }
  
  let compte = comptes[index];
  
  console.log("━━━━━━━━━━━━━━━━━━━━━━━━━━━");
  console.log("💰 SOLDE DU COMPTE");
  console.log("   Titulaire: " + compte.prenom + " " + compte.nom);
  console.log("   Numéro: " + compte.numero);
  console.log("   Solde: " + compte.solde + "€");
  console.log("   Statut: " + (compte.bloque ? "BLOQUÉ" : "Actif"));
  console.log("━━━━━━━━━━━━━━━━━━━━━━━━━━━");
  
  historique.push(numero + " - Consultation solde - " + compte.solde + "€");
}

function deposer(numero: string, montant: number) {
  let index = trouverCompte(numero);
  
  if (index === -1) {
    console.log("Compte introuvable");
    return;
  }
  
  if (montant <= 0) {
    console.log("❌ Montant invalide");
    return;
  }
  
  let compte = comptes[index];
  compte.solde = compte.solde + montant;
  
  console.log("✅ Dépôt de " + montant + "€ effectué");
  console.log("   Nouveau solde: " + compte.solde + "€");
  
  historique.push(numero + " - Dépôt " + montant + "€ - Nouveau solde: " + compte.solde + "€");
}

function retirer(numero: string, montant: number): boolean {
  let index = trouverCompte(numero);
  
  if (index === -1) {
    console.log("Compte introuvable");
    return false;
  }
  
  let compte = comptes[index];
  
  // Vérifications
  if (montant <= 0) {
    console.log("❌ Montant invalide");
    return false;
  }
  
  if (montant % 10 !== 0) {
    console.log("❌ Le montant doit être un multiple de 10€");
    historique.push(numero + " - Retrait refusé (pas multiple de 10)");
    return false;
  }
  
  if (compte.solde < montant) {
    console.log("❌ Solde insuffisant");
    console.log("   Solde disponible: " + compte.solde + "€");
    console.log("   Montant demandé: " + montant + "€");
    historique.push(numero + " - Retrait refusé (solde insuffisant)");
    return false;
  }
  
  // Calculer les billets nécessaires
  let reste = montant;
  let distribution = [0, 0, 0]; // [nb50, nb20, nb10]
  
  // Billets de 50€
  let max50 = Math.floor(reste / 50);
  if (max50 > billets[0]) {
    max50 = billets[0];
  }
  distribution[0] = max50;
  reste = reste - (max50 * 50);
  
  // Billets de 20€
  let max20 = Math.floor(reste / 20);
  if (max20 > billets[1]) {
    max20 = billets[1];
  }
  distribution[1] = max20;
  reste = reste - (max20 * 20);
  
  // Billets de 10€
  let max10 = Math.floor(reste / 10);
  if (max10 > billets[2]) {
    max10 = billets[2];
  }
  distribution[2] = max10;
  reste = reste - (max10 * 10);
  
  // Vérifier si on peut distribuer le montant
  if (reste > 0) {
    console.log("❌ Distributeur: pas assez de billets disponibles");
    console.log("   Stock actuel: " + billets[0] + "x50€, " + billets[1] + "x20€, " + billets[2] + "x10€");
    historique.push(numero + " - Retrait refusé (distributeur vide)");
    return false;
  }
  
  // Effectuer le retrait
  compte.solde = compte.solde - montant;
  billets[0] = billets[0] - distribution[0];
  billets[1] = billets[1] - distribution[1];
  billets[2] = billets[2] - distribution[2];
  
  console.log("✅ Retrait effectué: " + montant + "€");
  if (distribution[0] > 0) {
    console.log("   " + distribution[0] + " billet(s) de 50€");
  }
  if (distribution[1] > 0) {
    console.log("   " + distribution[1] + " billet(s) de 20€");
  }
  if (distribution[2] > 0) {
    console.log("   " + distribution[2] + " billet(s) de 10€");
  }
  console.log("   Nouveau solde: " + compte.solde + "€");
  
  historique.push(numero + " - Retrait " + montant + "€ (" + distribution[0] + "x50 + " + distribution[1] + "x20 + " + distribution[2] + "x10) - Solde: " + compte.solde + "€");
  
  return true;
}

function afficherStock() {
  console.log("╔════════════════════════════════╗");
  console.log("║   STOCK DU DISTRIBUTEUR        ║");
  console.log("╠════════════════════════════════╣");
  console.log("║ Billets de 50€: " + billets[0] + "             ║");
  console.log("║ Billets de 20€: " + billets[1] + "             ║");
  console.log("║ Billets de 10€: " + billets[2] + "             ║");
  console.log("╠════════════════════════════════╣");
  let total = (billets[0] * 50) + (billets[1] * 20) + (billets[2] * 10);
  console.log("║ TOTAL: " + total + "€                  ║");
  console.log("╚════════════════════════════════╝");
}

function reapprovisionner(nb50: number, nb20: number, nb10: number) {
  billets[0] = billets[0] + nb50;
  billets[1] = billets[1] + nb20;
  billets[2] = billets[2] + nb10;
  
  console.log("🔧 Réapprovisionnement effectué:");
  console.log("   +" + nb50 + " billets de 50€");
  console.log("   +" + nb20 + " billets de 20€");
  console.log("   +" + nb10 + " billets de 10€");
  
  historique.push("ADMIN - Réapprovisionnement: +" + nb50 + "x50€, +" + nb20 + "x20€, +" + nb10 + "x10€");
}

function afficherHistorique() {
  console.log("\n╔════════════════════════════════════════════════════════╗");
  console.log("║              HISTORIQUE DES OPÉRATIONS                 ║");
  console.log("╠════════════════════════════════════════════════════════╣");
  
  if (historique.length === 0) {
    console.log("║  Aucune opération enregistrée                          ║");
  } else {
    for (let i = 0; i < historique.length; i++) {
      console.log("║ " + (i + 1) + ". " + historique[i]);
    }
  }
  
  console.log("╚════════════════════════════════════════════════════════╝\n");
}

function afficherTousLesComptes() {
  console.log("\n╔════════════════════════════════════════════════════════╗");
  console.log("║              LISTE DES COMPTES                         ║");
  console.log("╠════════════════════════════════════════════════════════╣");
  
  for (let i = 0; i < comptes.length; i++) {
    let c = comptes[i];
    console.log("║ " + c.numero + " - " + c.prenom + " " + c.nom);
    console.log("║   Solde: " + c.solde + "€ - " + (c.bloque ? "BLOQUÉ" : "Actif"));
    console.log("╠════════════════════════════════════════════════════════╣");
  }
  
  console.log("╚════════════════════════════════════════════════════════╝\n");
}

function debloquerCompte(numero: string, pinAdmin: string): boolean {
  if (pinAdmin !== "ADMIN2024") {
    console.log("❌ Code admin incorrect");
    return false;
  }
  
  let index = trouverCompte(numero);
  
  if (index === -1) {
    console.log("Compte introuvable");
    return false;
  }
  
  comptes[index].bloque = false;
  comptes[index].tentatives = 0;
  console.log("🔓 Compte " + numero + " débloqué");
  historique.push("ADMIN - Déblocage compte " + numero);
  
  return true;
}


// ========================================
// SIMULATION D'UTILISATION
// ========================================

console.log("╔════════════════════════════════════════════════════════╗");
console.log("║          BIENVENUE AU DISTRIBUTEUR AUTOMATIQUE         ║");
console.log("╚════════════════════════════════════════════════════════╝\n");

// Afficher tous les comptes
afficherTousLesComptes();

// Alice se connecte
console.log("\n=== Alice Dupont (FR001) ===");
verifierPin("FR001", "1234");
afficherSolde("FR001");
retirer("FR001", 100);
afficherSolde("FR001");

// Bob se connecte
console.log("\n=== Bob Martin (FR002) ===");
verifierPin("FR002", "5678");
afficherSolde("FR002");
retirer("FR002", 200);
deposer("FR002", 50);
afficherSolde("FR002");

// Claire se connecte
console.log("\n=== Claire Durand (FR003) ===");
verifierPin("FR003", "9999");
afficherSolde("FR003");
retirer("FR003", 500);

// David tente de se connecter avec mauvais PIN
console.log("\n=== David Leroy (FR004) - Tentatives incorrectes ===");
verifierPin("FR004", "1111");
verifierPin("FR004", "2222");
verifierPin("FR004", "3333");
verifierPin("FR004", "0000"); // Le bon code mais compte bloqué

// Afficher l'état du distributeur
console.log("\n");
afficherStock();

// Admin débloque le compte de David
console.log("\n=== Intervention administrateur ===");
debloquerCompte("FR004", "ADMIN2024");

// David peut maintenant se connecter
console.log("\n=== David réessaie ===");
verifierPin("FR004", "0000");
afficherSolde("FR004");

// Réapprovisionner le distributeur
console.log("\n=== Réapprovisionnement ===");
reapprovisionner(5, 10, 15);
afficherStock();

// Afficher l'historique complet
afficherHistorique();

// État final des comptes
afficherTousLesComptes();
```