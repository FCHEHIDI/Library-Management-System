[← Library](06-class-library.md) | [Index](README.md) | [Business Rules →](08-business-rules.md)

---

# 📋 Catalogue Complet des Événements

## 🎯 Introduction

Cette documentation présente une approche **event-driven** (pilotée par les événements) pour modéliser le système de gestion de bibliothèque. Chaque événement représente une action ou un changement d'état dans le système, permettant de :

- **Identifier les responsabilités** de chaque classe
- **Définir les méthodes publiques et privées**
- **Comprendre les interactions** entre acteurs (LIBRARIAN, USER, SYSTEM)
- **Tracer les flux de données** et les dépendances

L'approche event-driven facilite la conception orientée objet en partant des **cas d'usage réels** plutôt que d'une structure technique abstraite.

---

## 🔐 1. Événements d'Authentification

| # | Événement | Acteur | Méthode Associée |
|---|-----------|--------|------------------|
| 1 | Le LIBRARIAN se connecte au système | LIBRARIAN | `login()` |
| 2 | Le LIBRARIAN se déconnecte du système | LIBRARIAN | `logout()` |
| 3 | Le USER se connecte au système | USER | `login()` |
| 4 | Le USER se déconnecte du système | USER | `logout()` |
| 5 | Le SYSTEM enregistre la dernière connexion | SYSTEM | `recordLastLogin()` |
| 6 | Le SYSTEM vérifie les credentials | SYSTEM | `verifyCredentials()` |
| 7 | Le SYSTEM génère un token de session | SYSTEM | `generateSessionToken()` |
| 8 | Le SYSTEM révoque un token de session | SYSTEM | `revokeSessionToken()` |

**Total**: 8 événements

---

## 👥 2. Gestion des Utilisateurs (LIBRARIAN)

| # | Événement | Méthode Associée |
|---|-----------|------------------|
| 1 | Le LIBRARIAN enregistre un nouveau compte utilisateur | `register_User()` |
| 2 | Le LIBRARIAN active un compte utilisateur | `activate_User_Account()` |
| 3 | Le LIBRARIAN désactive un compte pour non-respect | `deactivate_User_Account()` |
| 4 | Le LIBRARIAN suspend temporairement un compte | `suspend_User()` |
| 5 | Le LIBRARIAN lève la suspension | `unsuspend_User()` |
| 6 | Le LIBRARIAN autorise un utilisateur à emprunter | `authorize_User_To_Borrow()` |
| 7 | Le LIBRARIAN révoque l'autorisation d'emprunt | `revoke_Borrowing_Permission()` |
| 8 | Le LIBRARIAN supprime définitivement un compte | `delete_User_Account()` |
| 9 | Le LIBRARIAN consulte les infos d'un utilisateur | `get_User_Details()` |
| 10 | Le LIBRARIAN consulte tous les utilisateurs | `get_All_Users()` |
| 11 | Le LIBRARIAN filtre les utilisateurs par statut | `filter_Users_By_Status()` |
| 12 | Le LIBRARIAN consulte l'historique d'emprunts | `get_User_Borrowing_History()` |
| 13 | Le LIBRARIAN modifie les droits d'un utilisateur | `update_User_Permissions()` |
| 14 | Le LIBRARIAN bannit définitivement un utilisateur | `ban_User()` |

**Total**: 14 événements

---

## 📚 3. Gestion des Livres (LIBRARIAN)

| # | Événement | Méthode Associée |
|---|-----------|------------------|
| 1 | Le LIBRARIAN ajoute un nouveau livre | `add_Book()` |
| 2 | Le LIBRARIAN supprime un livre | `remove_Book()` |
| 3 | Le LIBRARIAN modifie les informations d'un livre | `update_Book_Details()` |
| 4 | Le LIBRARIAN modifie l'état physique d'un livre | `update_Book_Physical_State()` |
| 5 | Le LIBRARIAN consulte les détails d'un livre | `get_Book_By_Id()` |
| 6 | Le LIBRARIAN consulte tous les livres | `get_All_Books()` |
| 7 | Le LIBRARIAN vérifie la disponibilité | `check_Books_Availability()` |
| 8 | Le LIBRARIAN modifie manuellement la disponibilité | `set_Book_Availability()` |
| 9 | Le LIBRARIAN restreint un livre | `restrict_Book()` |
| 10 | Le LIBRARIAN lève la restriction | `unrestrict_Book()` |
| 11 | Le LIBRARIAN marque un livre comme perdu | `mark_Book_As_Lost()` |
| 12 | Le LIBRARIAN marque un livre en réparation | `mark_Book_As_In_Repair()` |
| 13 | Le LIBRARIAN consulte l'historique d'emprunts | `get_Book_Borrowing_History()` |
| 14 | Le LIBRARIAN filtre les livres par catégorie | `filter_Books_By_Category()` |
| 15 | Le LIBRARIAN filtre par état physique | `filter_Books_By_Physical_State()` |
| 16 | Le LIBRARIAN consulte les statistiques d'emprunts | `get_Book_Statistics()` |

**Total**: 16 événements

---

## 📖 4. Emprunts (LIBRARIAN & SYSTEM)

| # | Événement | Acteur | Méthode Associée |
|---|-----------|--------|------------------|
| 1 | Le SYSTEM traite une demande d'emprunt | SYSTEM | `process_Borrowing()` |
| 2 | Le SYSTEM valide les conditions d'emprunt | SYSTEM | `validate_Borrowing_Conditions()` |
| 3 | Le SYSTEM crée un enregistrement d'emprunt | SYSTEM | `create_Borrowing_Record()` |
| 4 | Le SYSTEM calcule la date de retour | SYSTEM | `calculate_Due_Date()` |
| 5 | Le SYSTEM traite un retour de livre | SYSTEM | `process_Return()` |
| 6 | Le SYSTEM vérifie l'état du livre au retour | SYSTEM | `check_Book_Condition_On_Return()` |
| 7 | Le SYSTEM clôture un enregistrement | SYSTEM | `close_Borrowing_Record()` |
| 8 | Le SYSTEM détecte les emprunts en retard | SYSTEM | `detect_Overdue_Borrowings()` |
| 9 | Le SYSTEM consulte tous les emprunts en retard | SYSTEM | `get_Overdue_Borrowings()` |
| 10 | Le LIBRARIAN prolonge manuellement un emprunt | LIBRARIAN | `extend_Borrowing()` |
| 11 | Le LIBRARIAN annule un emprunt | LIBRARIAN | `cancel_Borrowing()` |

**Total**: 11 événements

---

## 📧 5. Communication (LIBRARIAN)

| # | Événement | Méthode Associée |
|---|-----------|------------------|
| 1 | Le LIBRARIAN envoie un email à un utilisateur | `send_Email_To_User()` |
| 2 | Le LIBRARIAN envoie un email groupé | `send_Bulk_Email()` |
| 3 | Le LIBRARIAN envoie un email à l'admin | `send_Email_To_Admin()` |
| 4 | Le LIBRARIAN publie une information générale | `publish_General_Info()` |
| 5 | Le LIBRARIAN envoie une notification | `send_Notification()` |
| 6 | Le LIBRARIAN consulte ses notifications | `receive_Notification()` |
| 7 | Le LIBRARIAN marque une notification comme lue | `mark_Notification_As_Read()` |

**Total**: 7 événements

---

## 🔔 6. Notifications (SYSTEM → LIBRARIAN)

| # | Événement | Méthode Associée |
|---|-----------|------------------|
| 1 | Le SYSTEM notifie la fin imminente d'un emprunt | `notify_Due_Date_Approaching()` |
| 2 | Le SYSTEM notifie d'une demande de prolongation | `notify_Extension_Request()` |
| 3 | Le SYSTEM notifie d'un retard d'emprunt | `notify_Overdue_Borrowing()` |
| 4 | Le SYSTEM notifie d'un nouveau commentaire | `notify_New_Comment()` |
| 5 | Le SYSTEM notifie d'une nouvelle réclamation | `notify_New_Claim()` |
| 6 | Le SYSTEM notifie d'un livre retourné endommagé | `notify_Damaged_Book_Return()` |

**Total**: 6 événements

---

## 💬 7. Gestion des Commentaires (LIBRARIAN)

| # | Événement | Méthode Associée |
|---|-----------|------------------|
| 1 | Le LIBRARIAN consulte les commentaires en attente | `get_Pending_Comments()` |
| 2 | Le LIBRARIAN approuve un commentaire | `approve_Comment()` |
| 3 | Le LIBRARIAN rejette un commentaire | `reject_Comment()` |
| 4 | Le LIBRARIAN supprime un commentaire inapproprié | `delete_Comment()` |
| 5 | Le LIBRARIAN consulte tous les commentaires d'un livre | `get_Comments_By_Book()` |

**Total**: 5 événements

---

## 📖 8. Consultation des Livres (USER)

| # | Événement | Méthode Associée |
|---|-----------|------------------|
| 1 | Le USER consulte tous les livres | `get_All_Books()` |
| 2 | Le USER consulte uniquement les livres disponibles | `get_Available_Books()` |
| 3 | Le USER recherche un livre par titre | `search_By_Title()` |
| 4 | Le USER recherche un livre par auteur | `search_By_Author()` |
| 5 | Le USER recherche un livre par ISBN | `search_By_ISBN()` |
| 6 | Le USER filtre les livres par catégorie | `filter_By_Category()` |
| 7 | Le USER filtre par année de publication | `filter_By_Year()` |
| 8 | Le USER filtre par note moyenne | `filter_By_Rating()` |
| 9 | Le USER consulte les détails d'un livre | `get_Book_Details()` |
| 10 | Le USER consulte les commentaires | `get_Book_Comments()` |
| 11 | Le USER consulte la disponibilité | `check_Book_Availability()` |

**Total**: 11 événements

---

## 📚 9. Emprunts (USER)

| # | Événement | Méthode Associée |
|---|-----------|------------------|
| 1 | Le USER emprunte un livre | `borrow_Book()` |
| 2 | Le USER consulte ses livres empruntés | `get_My_Borrowed_Books()` |
| 3 | Le USER consulte son historique complet | `get_My_Borrowing_History()` |
| 4 | Le USER demande une prolongation | `request_Extension()` |
| 5 | Le USER retourne un livre | `return_Book()` |
| 6 | Le USER vérifie combien il peut emprunter | `get_Available_Borrowing_Slots()` |

**Total**: 6 événements

---

## 🔔 10. Notifications (USER)

| # | Événement | Méthode Associée |
|---|-----------|------------------|
| 1 | Le USER s'abonne aux notifications de disponibilité | `subscribe_To_Book_Availability()` |
| 2 | Le USER se désabonne | `unsubscribe_From_Book_Availability()` |
| 3 | Le USER reçoit une notification de retour imminent | `receive_Due_Date_Reminder()` |
| 4 | Le USER reçoit une notification de retard | `receive_Overdue_Notification()` |
| 5 | Le USER reçoit notification de prolongation approuvée | `receive_Extension_Approved()` |
| 6 | Le USER reçoit notification de prolongation refusée | `receive_Extension_Rejected()` |
| 7 | Le USER reçoit notification de disponibilité | `receive_Book_Available()` |
| 8 | Le USER reçoit notification de suspension | `receive_Suspension_Notice()` |
| 9 | Le USER reçoit notification d'activation | `receive_Activation_Notice()` |
| 10 | Le USER consulte toutes ses notifications | `receive_Notification()` |
| 11 | Le USER marque une notification comme lue | `mark_Notification_As_Read()` |
| 12 | Le USER active/désactive les notifications | `toggle_Notifications()` |

**Total**: 12 événements

---

## 💬 11. Commentaires & Avis (USER)

| # | Événement | Méthode Associée |
|---|-----------|------------------|
| 1 | Le USER ajoute un commentaire | `add_Comment()` |
| 2 | Le USER ajoute une note (1-5 étoiles) | `add_Rating()` |
| 3 | Le USER modifie son commentaire | `edit_Comment()` |
| 4 | Le USER supprime son commentaire | `delete_Comment()` |
| 5 | Le USER consulte ses propres commentaires | `get_My_Comments()` |
| 6 | Le USER reçoit notification d'approbation | `receive_Comment_Approved()` |
| 7 | Le USER reçoit notification de rejet | `receive_Comment_Rejected()` |

**Total**: 7 événements

---

## 👤 12. Gestion de Profil (USER)

| # | Événement | Méthode Associée |
|---|-----------|------------------|
| 1 | Le USER consulte son profil | `get_Profile()` |
| 2 | Le USER modifie ses informations personnelles | `update_Profile()` |
| 3 | Le USER modifie ses préférences de notification | `update_Notification_Preferences()` |
| 4 | Le USER consulte les règles de la bibliothèque | `get_Library_Rules()` |

**Total**: 4 événements

---

## 🆘 13. Réclamations (USER)

| # | Événement | Méthode Associée |
|---|-----------|------------------|
| 1 | Le USER soumet une réclamation (livre endommagé) | `send_Claim()` |
| 2 | Le USER soumet une réclamation (livre perdu) | `send_Claim()` |
| 3 | Le USER soumet une réclamation (frais incorrects) | `send_Claim()` |
| 4 | Le USER soumet une réclamation (problème de compte) | `send_Claim()` |
| 5 | Le USER soumet une réclamation (problème de service) | `send_Claim()` |
| 6 | Le USER soumet une réclamation (problème technique) | `send_Claim()` |
| 7 | Le USER consulte ses réclamations | `get_My_Claims()` |
| 8 | Le USER reçoit notification (réclamation reçue) | `receive_Claim_Received()` |
| 9 | Le USER reçoit notification (en cours de traitement) | `receive_Claim_InProgress()` |
| 10 | Le USER reçoit notification (réclamation résolue) | `receive_Claim_Resolved()` |
| 11 | Le USER reçoit notification (réclamation rejetée) | `receive_Claim_Rejected()` |

**Total**: 11 événements

---

## 🔧 14. Système Automatique

| # | Événement | Méthode/Processus Associé |
|---|-----------|---------------------------|
| 1 | Vérification quotidienne des retards | `checkOverdueBorrowings()` (cron) |
| 2 | Envoi rappels automatiques (J-3, J-1) | `sendDueDateReminders()` (cron) |
| 3 | Envoi notifications de retard (J+1, J+7, J+14) | `sendOverdueNotifications()` (cron) |
| 4 | Mise à jour statut emprunts (active → overdue) | `updateBorrowingStatuses()` |
| 5 | Génération des statistiques d'utilisation | `generateUsageStatistics()` |
| 6 | Archivage des anciens emprunts | `archiveOldBorrowings()` |
| 7 | Nettoyage des notifications lues (> 30j) | `cleanupOldNotifications()` |
| 8 | Sauvegarde des données | `backupSystemData()` |
| 9 | Détection comptes inactifs (> 1 an) | `detectInactiveAccounts()` |
| 10 | Notification admin (livres perdus > 60j) | `notifyAdminLostBooks()` |
| 11 | Calcul des notes moyennes des livres | `calculateAverageRatings()` |
| 12 | Mise à jour nombre total d'emprunts par livre | `updateBookBorrowingCounts()` |

**Total**: 12 événements

---

## 📊 Tableau Récapitulatif

| Catégorie | Nombre d'Événements |
|-----------|---------------------|
| 🔐 Authentification | 8 |
| 👥 Gestion utilisateurs (LIBRARIAN) | 14 |
| 📚 Gestion livres (LIBRARIAN) | 16 |
| 📖 Emprunts (LIBRARIAN & SYSTEM) | 11 |
| 📧 Communication (LIBRARIAN) | 7 |
| 🔔 Notifications (SYSTEM → LIBRARIAN) | 6 |
| 💬 Gestion commentaires (LIBRARIAN) | 5 |
| 📖 Consultation livres (USER) | 11 |
| 📚 Emprunts (USER) | 6 |
| 🔔 Notifications (USER) | 12 |
| 💬 Commentaires & avis (USER) | 7 |
| 👤 Profil (USER) | 4 |
| 🆘 Réclamations (USER) | 11 |
| 🔧 Système automatique | 12 |
| **TOTAL** | **130 événements** |

---

## 🗺️ Mapping Événements → Méthodes des Classes

### Classe `Librarian`

- **Gestion utilisateurs**: `register_User()`, `activate_User_Account()`, `suspend_User()`, `ban_User()`, etc.
- **Gestion livres**: `add_Book()`, `remove_Book()`, `update_Book_Details()`, `mark_Book_As_Lost()`, etc.
- **Emprunts**: `extend_Borrowing()`, `cancel_Borrowing()`, `get_Overdue_Borrowings()`
- **Communication**: `send_Email_To_User()`, `send_Bulk_Email()`, `send_Notification()`
- **Commentaires**: `get_Pending_Comments()`, `approve_Comment()`, `reject_Comment()`

### Classe `Borrower` (USER)

- **Consultation**: `get_All_Books()`, `search_By_Title()`, `search_By_Author()`, `filter_By_Category()`
- **Emprunts**: `borrow_Book()`, `return_Book()`, `request_Extension()`, `get_My_Borrowed_Books()`
- **Notifications**: `subscribe_To_Book_Availability()`, `receive_Notification()`, `mark_Notification_As_Read()`
- **Commentaires**: `add_Comment()`, `add_Rating()`, `edit_Comment()`, `get_My_Comments()`
- **Profil**: `get_Profile()`, `update_Profile()`
- **Réclamations**: `send_Claim()`, `get_My_Claims()`

### Classe `Library` (SYSTEM)

- **Gestion centrale**: `add_Book()`, `remove_Book()`, `register_User()`, `get_All_Users()`
- **Emprunts**: `process_Borrowing()`, `process_Return()`, `get_Overdue_Borrowings()`
- **Automatisations**: `send_Due_Date_Reminders()`, `detect_Overdue_Borrowings()`, `archive_Old_Borrowings()`

---

## 🎓 Conclusion

Ce catalogue exhaustif des événements permet de :

✅ **Modéliser les 3 classes principales** avec précision  
✅ **Définir les interfaces** (`IBorrowable`, `INotifiable`, `ISearchable`, `IUser`)  
✅ **Identifier les responsabilités** de chaque acteur  
✅ **Structurer les méthodes publiques et privées**  
✅ **Garantir la cohérence** entre les cas d'usage et l'implémentation

---

[← Library](06-class-library.md) | [Index](README.md) | [Business Rules →](08-business-rules.md)
