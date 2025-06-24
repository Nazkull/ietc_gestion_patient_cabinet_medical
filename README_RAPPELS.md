# Système de Rappels par Email

Ce système permet d'envoyer automatiquement des rappels par email aux patients qui ont un rendez-vous le lendemain.

## Fonctionnalités

- ✅ Rappels automatiques pour les rendez-vous du lendemain
- ✅ Envoi manuel de rappels via l'interface secrétaire
- ✅ Configuration Gmail avec authentification sécurisée
- ✅ Emails HTML formatés avec les détails du rendez-vous
- ✅ Gestion des doublons pour éviter les rappels multiples

## Configuration

### 1. Configuration Gmail

Pour utiliser le système de rappels, vous devez configurer un compte Gmail :

1. **Activez l'authentification à 2 facteurs** sur votre compte Google
2. **Générez un mot de passe d'application** :
   - Allez dans les paramètres de votre compte Google
   - Sécurité → Authentification à 2 facteurs
   - Mots de passe d'application → Générer un nouveau mot de passe
   - Utilisez ce mot de passe dans l'application

### 2. Configuration dans l'Application

1. Connectez-vous en tant que **Secrétaire**
2. Cliquez sur l'onglet **"Rappel"** dans la barre latérale
3. Entrez votre email Gmail et le mot de passe d'application
4. Cliquez sur **"Tester la connexion"** pour vérifier
5. Cliquez sur **"Sauvegarder la configuration"**

## Utilisation

### Envoi Automatique

Le système peut envoyer automatiquement des rappels :

1. Configurez l'email comme décrit ci-dessus
2. Cliquez sur **"Démarrer le service de rappels"**
3. Le système vérifiera toutes les heures les rendez-vous du lendemain
4. Les rappels seront envoyés automatiquement

### Envoi Manuel

Pour envoyer manuellement les rappels :

1. Configurez l'email
2. Cliquez sur **"Envoyer les rappels pour demain"**
3. Le système enverra immédiatement les rappels pour tous les rendez-vous confirmés de demain

## Format des Emails

Les emails de rappel contiennent :
- Nom du patient
- Date et heure du rendez-vous
- Nom du médecin
- Raison de la consultation
- Instructions pour se présenter 10 minutes avant

## Statuts des Rendez-vous

Seuls les rendez-vous avec le statut **"planned"** (confirmé) sont éligibles aux rappels.

Les statuts possibles :
- `pending` : En attente de confirmation
- `planned` : Confirmé (éligible aux rappels)
- `cancelled` : Annulé
- `completed` : Terminé

## Test du Système

Vous pouvez tester le système avec le script `test_reminders.py` :

```bash
python test_reminders.py
```

Ce script vous permettra de :
1. Vérifier les rendez-vous de demain
2. Tester la configuration email
3. Envoyer des rappels de test

## Dépannage

### Problèmes Courants

1. **"Email manager non configuré"**
   - Configurez d'abord l'email dans l'interface secrétaire

2. **"Échec de l'envoi de l'email"**
   - Vérifiez que l'authentification à 2 facteurs est activée
   - Utilisez un mot de passe d'application, pas votre mot de passe principal
   - Vérifiez que l'email et le mot de passe sont corrects

3. **"Aucun rendez-vous confirmé pour demain"**
   - Vérifiez qu'il y a des rendez-vous avec le statut "planned" pour demain
   - Les rendez-vous "pending" ne reçoivent pas de rappels

### Logs

Les logs d'activité sont affichés dans la console et dans le fichier `app.log`.

## Sécurité

- Les mots de passe d'application sont plus sécurisés que les mots de passe principaux
- L'authentification à 2 facteurs est obligatoire
- Les emails sont envoyés via SMTP sécurisé (TLS)
- Aucun mot de passe n'est stocké en clair dans les fichiers

## Support

Pour toute question ou problème, consultez les logs ou contactez l'administrateur système. 