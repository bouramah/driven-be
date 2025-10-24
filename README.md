# driven-be

Application backend pour le projet Driven.

## Installation des dépendances

```bash
pip install -r requirements.txt
```

## Configuration de l'environnement

1. Copiez le fichier `.env.exemple` en `.env`
```bash
cp .env.exemple .env
```

2. Modifiez le fichier `.env` selon votre environnement

3. Créez les répertoires nécessaires pour le stockage des fichiers
```bash
mkdir -p uploads/icons
```

## Structure des réponses API

Toutes les réponses API suivent la structure suivante :

```json
{
    "error": false,          // booléen indiquant s'il y a une erreur
    "message": {
        "en": "Message in English",
        "fr": "Message en Français"
    },
    "data": {}              // données de la réponse (optionnel)
}
```

En cas d'erreur :
```json
{
    "error": true,
    "message": {
        "en": "Error message in English",
        "fr": "Message d'erreur en Français"
    },
    "details": "Détails techniques de l'erreur" 
}
```

## Gestion des fichiers

Les fichiers uploadés sont stockés dans les répertoires suivants :
- Icons des applications : `uploads/icons/`
- Icons des pages : `uploads/pages/`

Formats acceptés pour les icônes :
- PNG
- JPG/JPEG
- GIF
- SVG

## Validations importantes

- Lors de la création ou de la mise à jour d'une page, si un `app_id` est fourni, l'application correspondante doit exister.
- Lors de l'ajout de pages à une application, l'application doit exister.

## Gestion de la base de données

### Migrations récentes

- **49eb56c0f603** : Les champs `app_icon` dans la table `application` et `app_id` dans la table `page` sont maintenant optionnels (nullable).

### Pour un nouveau développeur

Pour créer les tables dans la base de données lors de la première utilisation du projet :

1. Assurez-vous que le fichier `.env` est correctement configuré avec les paramètres de votre base de données
2. Exécutez les commandes suivantes :

```bash
# Définir la variable d'environnement FLASK_APP
export FLASK_APP=run.py

# Appliquer les migrations existantes pour créer les tables
flask db upgrade
```

Les tables seront créées dans le répertoire `instance/app.db` pour SQLite ou dans la base de données MySQL configurée dans votre fichier `.env`.

### Pour mettre à jour une table existante

Si vous avez modifié un modèle (ajout/suppression de champs, modification de contraintes, etc.) et que vous souhaitez mettre à jour la structure de la base de données :

1. Modifiez le modèle dans les fichiers correspondants (`app/common/models.py` ou `app/apps/*/models.py`)
2. Générez une nouvelle migration :

```bash
# Définir la variable d'environnement FLASK_APP
export FLASK_APP=run.py

# Générer une migration automatique basée sur les changements détectés
flask db migrate -m "Description de votre modification"

# Vérifiez le fichier de migration généré dans le dossier migrations/versions
# pour vous assurer que les modifications sont correctes

# Appliquez la migration
flask db upgrade
```

### Commandes utiles pour la gestion des migrations

```bash
# Voir l'état actuel des migrations
flask db current

# Revenir à une version précédente
flask db downgrade

# Voir l'historique des migrations
flask db history
```

## Lancement de l'application

```bash
python run.py
```

L'application sera accessible à l'adresse configurée dans le fichier `.env` (par défaut : http://localhost:5001).

## Tests avec Postman

### Configuration de l'environnement Postman

1. Créez un nouvel environnement dans Postman
2. Ajoutez la variable `BASE_URL` avec la valeur `http://localhost:5001/api`

### Collection d'exemples

#### Applications

##### 1. Lister toutes les applications
```http
GET {{BASE_URL}}/applications
```

##### 2. Obtenir une application spécifique
```http
GET {{BASE_URL}}/applications/1
```

##### 3. Créer une nouvelle application
```http
POST {{BASE_URL}}/applications
```
Body (form-data):
- `nom` : Nom de l'application
- `description` : Description de l'application
- `app_color` : Couleur de l'application (ex: #FF0000)
- `app_icon` : Fichier image (PNG, JPG, JPEG, GIF, SVG) (optionnel)
- `creer_par` : ID de l'utilisateur créateur
- `modifier_par` : ID de l'utilisateur modificateur

Exemple de réponse réussie :
```json
{
    "error": false,
    "message": {
        "en": "Application created successfully",
        "fr": "Application créée avec succès"
    },
    "data": {
        "app_id": 1,
        "nom": "Mon Application",
        "description": "Description de l'application",
        "app_color": "#FF0000",
        "app_icon": "uploads/icons/mon_icone.png",
        "creer_par": 1,
        "modifier_par": 1,
        "creer_a": "2024-02-25T12:00:00",
        "modifier_a": "2024-02-25T12:00:00"
    }
}
```

##### 4. Mettre à jour une application
```http
PUT {{BASE_URL}}/applications/1
```
Body (form-data) :
- `nom` : Nouveau nom (optionnel)
- `description` : Nouvelle description (optionnel)
- `app_color` : Nouvelle couleur (optionnel)
- `app_icon` : Nouveau fichier image (optionnel)
- `modifier_par` : ID de l'utilisateur modificateur

##### 5. Supprimer une application
```http
DELETE {{BASE_URL}}/applications/1
```

#### Pages

##### 1. Lister toutes les pages
```http
GET {{BASE_URL}}/pages
```

##### 2. Obtenir une page spécifique
```http
GET {{BASE_URL}}/pages/1
```

##### 3. Lister les pages d'une application
```http
GET {{BASE_URL}}/pages/application/1
```

##### 4. Créer une nouvelle page
```http
POST {{BASE_URL}}/pages
```
Body (form-data):
- `nom` : Nom de la page
- `description` : Description de la page
- `lien` : Lien vers la page
- `app_id` : ID de l'application associée (optionnel)
- `icon` : Fichier image (PNG, JPG, JPEG, GIF, SVG) (optionnel)
- `creer_par` : ID de l'utilisateur créateur
- `modifier_par` : ID de l'utilisateur modificateur

Exemple de réponse réussie :
```json
{
    "error": false,
    "message": {
        "en": "Page created successfully",
        "fr": "Page créée avec succès"
    },
    "data": {
        "page_id": 1,
        "nom": "Ma Page",
        "description": "Description de la page",
        "lien": "/ma-page",
        "icon": "uploads/pages/mon_icone.png",
        "app_id": 1,
        "creer_par": 1,
        "modifier_par": 1,
        "creer_a": "2024-02-25T12:00:00",
        "modifier_a": "2024-02-25T12:00:00"
    }
}
```

##### 5. Mettre à jour une page
```http
PUT {{BASE_URL}}/pages/1
```
Body (form-data) :
- `nom` : Nouveau nom (optionnel)
- `description` : Nouvelle description (optionnel)
- `lien` : Nouveau lien (optionnel)
- `app_id` : Nouvelle application associée (optionnel)
- `icon` : Nouveau fichier image (optionnel)
- `modifier_par` : ID de l'utilisateur modificateur

##### 6. Supprimer une page
```http
DELETE {{BASE_URL}}/pages/1
```

##### 7. Ajouter des pages à une application
```http
POST {{BASE_URL}}/pages/application/1/add
```
Body (JSON) :
```json
{
    "page_ids": [1, 2, 3]
}
```

Exemple de réponse réussie :
```json
{
    "error": false,
    "message": {
        "en": "Pages added to application successfully",
        "fr": "Pages ajoutées à l'application avec succès"
    }
}
```

##### 8. Retirer des pages d'une application
```http
POST {{BASE_URL}}/pages/application/1/remove
```
Body (JSON) :
```json
{
    "page_ids": [1, 2, 3]
}
```

Exemple de réponse réussie :
```json
{
    "error": false,
    "message": {
        "en": "Pages removed from application successfully",
        "fr": "Pages retirées de l'application avec succès"
    }
}
```

#### Blacklist

##### 1. Lister toutes les entrées de la liste noire
```http
GET {{BASE_URL}}/blacklist
```

##### 2. Obtenir une entrée spécifique par ID
```http
GET {{BASE_URL}}/blacklist/1
```

##### 3. Obtenir une entrée par numéro
```http
GET {{BASE_URL}}/blacklist/number/123456789
```

##### 4. Vérifier si un numéro est blacklisté
```http
GET {{BASE_URL}}/blacklist/check/123456789
```

Exemple de réponse :
```json
{
    "error": false,
    "message": {
        "en": "Number check completed",
        "fr": "Vérification du numéro terminée"
    },
    "data": {
        "is_blacklisted": true
    }
}
```

##### 5. Créer une nouvelle entrée dans la liste noire
```http
POST {{BASE_URL}}/blacklist
```
Body (JSON):
```json
{
    "numero": "123456789",
    "nom": "Nom du contact",
    "structure": "Structure du contact",
    "creer_par": 1,
    "modifier_par": 1
}
```

Exemple de réponse réussie :
```json
{
    "error": false,
    "message": {
        "en": "Blacklist entry created successfully",
        "fr": "Entrée de la liste noire créée avec succès"
    },
    "data": {
        "id": 1,
        "numero": "123456789",
        "nom": "Nom du contact",
        "structure": "Structure du contact",
        "date_ajout": "2024-05-15T12:00:00",
        "creer_par": 1,
        "modifier_par": 1,
        "creer_a": "2024-05-15T12:00:00",
        "modifier_a": "2024-05-15T12:00:00"
    }
}
```

##### 6. Mettre à jour une entrée de la liste noire
```http
PUT {{BASE_URL}}/blacklist/1
```
Body (JSON):
```json
{
    "numero": "987654321",
    "nom": "Nouveau nom",
    "structure": "Nouvelle structure",
    "modifier_par": 1
}
```

##### 7. Supprimer une entrée de la liste noire
```http
DELETE {{BASE_URL}}/blacklist/1
```
#### Traces

##### 1. Lister toutes les entrées de trace
```http
GET {{BASE_URL}}/traces
```

Paramètres de pagination (optionnels) :
- `page` : Numéro de la page (défaut: 1)
- `per_page` : Nombre d'éléments par page (défaut: 10, max: 50)

Exemple :
```http
GET {{BASE_URL}}/traces?page=2&per_page=15
```

Exemple de réponse avec pagination :
```json
{
    "error": false,
    "message": {
        "en": "Trace entries retrieved successfully",
        "fr": "Entrées de trace récupérées avec succès"
    },
    "data": [
        {
            "id": 11,
            "date": "2024-05-15T12:00:00",
            "action": "LOGIN",
            "detail": "Connexion utilisateur",
            "code": "AUTH_001",
            "param": "user_id=1",
            "code_sql": "SELECT * FROM utilisateur WHERE id_utilisateur = 1",
            "end_point": "/api/auth/login",
            "id_utilisateur": 1
        },
        // ... autres entrées ...
    ],
    "pagination": {
        "page": 2,
        "per_page": 15,
        "total_items": 45,
        "total_pages": 3,
        "has_next": false,
        "has_prev": true,
        "next_page": null,
        "prev_page": 1
    }
}
```

##### 2. Obtenir une entrée de trace spécifique par ID
```http
GET {{BASE_URL}}/traces/1
```

##### 3. Créer une nouvelle entrée de trace
```http
POST {{BASE_URL}}/traces
```
Body (JSON) :
```json
{
    "action": "CREATE_USER",
    "detail": "Création d'un nouvel utilisateur",
    "code": "USER_001",
    "param": "username=johndoe",
    "code_sql": "INSERT INTO utilisateur...",
    "end_point": "/api/utilisateurs",
    "id_utilisateur": 1
}
```

Note: Seuls les champs `action` sont obligatoires. Les autres champs sont optionnels.

##### 4. Mettre à jour une entrée de trace
```http
PUT {{BASE_URL}}/traces/1
```
Body (JSON) :
```json
{
    "action": "UPDATE_USER",
    "detail": "Mise à jour d'un utilisateur"
}
```

##### 5. Supprimer une entrée de trace
```http
DELETE {{BASE_URL}}/traces/1
```

##### 6. Obtenir les traces par utilisateur
```http
GET {{BASE_URL}}/traces/utilisateur/1
```

Supporte également la pagination avec les paramètres `page` et `per_page`.

##### 7. Obtenir les traces par action
```http
GET {{BASE_URL}}/traces/action/LOGIN
```

Supporte également la pagination avec les paramètres `page` et `per_page`.

##### 8. Obtenir les traces par plage de dates
```http
GET {{BASE_URL}}/traces/date-range?start_date=2024-01-01&end_date=2024-12-31
```

Paramètres obligatoires :
- `start_date` : Date de début au format ISO (YYYY-MM-DD)
- `end_date` : Date de fin au format ISO (YYYY-MM-DD)

Supporte également la pagination avec les paramètres `page` et `per_page`.


### Entités

#### Lister toutes les entités
```http
GET {{BASE_URL}}/entites
```

Paramètres optionnels :
- `page` : Numéro de la page (défaut : 1)
- `per_page` : Nombre d'éléments par page (défaut : 10, max : 50)

Exemple avec pagination :
```http
GET {{BASE_URL}}/entites?page=2&per_page=15
```

Exemple de réponse :
```json
{
    "error": false,
    "message": {
        "en": "Entities retrieved successfully",
        "fr": "Entités récupérées avec succès"
    },
    "data": [
        {
            "id": 1,
            "nom": "Entité 1",
            "code": "ENT1",
            "email": "entite1@example.com",
            "creer_par": 1,
            "modifier_par": 1,
            "creer_a": "2024-01-01T00:00:00",
            "modifier_a": "2024-01-01T00:00:00"
        },
        // ... autres entités
    ],
    "pagination": {
        "page": 2,
        "per_page": 15,
        "total_items": 45,
        "total_pages": 3,
        "has_next": false,
        "has_prev": true,
        "next_page": null,
        "prev_page": 1
    }
}
```

#### Obtenir une entité par ID
```http
GET {{BASE_URL}}/entites/1
```

#### Obtenir une entité par code
```http
GET {{BASE_URL}}/entites/code/ENT1
```

#### Créer une entité
```http
POST {{BASE_URL}}/entites
```

Corps de la requête :
```json
{
    "nom": "Nouvelle Entité",
    "code": "NEWENT",
    "email": "nouvelle@example.com",
    "creer_par": 1,
    "modifier_par": 1
}
```

#### Mettre à jour une entité
```http
PUT {{BASE_URL}}/entites/1
```

Corps de la requête :
```json
{
    "nom": "Entité Modifiée",
    "code": "MODENT",
    "email": "modifiee@example.com",
    "modifier_par": 1
}
```

#### Supprimer une entité
```http
DELETE {{BASE_URL}}/entites/1
```

### Objectifs

#### Obtenir tous les objectifs (avec pagination)
```
GET /api/objectifs?page=1&per_page=10
```

Réponse :
```json
{
    "error": false,
    "message": {
        "en": "Objectives retrieved successfully",
        "fr": "Objectifs récupérés avec succès"
    },
    "data": [
        {
            "id": 1,
            "titre": "Objectif CA Q1",
            "id_utilisateur": 1,
            "type": "chiffre_affaires",
            "description": "Atteindre 100K€ de CA",
            "periode": "2024.01-2024.03",
            "date_debut": "2024-01-01T00:00:00",
            "date_fin": "2024-03-31T00:00:00",
            "statut": "En cours",
            "progression": 0.75,
            "valeur": 100000,
            "creer_par": 1,
            "modifier_par": 1,
            "creer_a": "2023-01-01T12:00:00",
            "modifier_a": "2023-01-01T12:00:00"
        },
        {
            "id": 2,
            "titre": "Objectif Marge Février",
            "id_utilisateur": 1,
            "type": "marge",
            "description": "Atteindre 30% de marge",
            "periode": "2024.02",
            "date_debut": "2024-02-01T00:00:00",
            "date_fin": "2024-02-29T00:00:00",
            "statut": "En cours",
            "progression": 0.5,
            "valeur": 30,
            "creer_par": 1,
            "modifier_par": 1,
            "creer_a": "2023-01-01T12:00:00",
            "modifier_a": "2023-01-01T12:00:00"
        }
    ],
    "pagination": {
        "page": 1,
        "per_page": 10,
        "total_pages": 1,
        "total_items": 2,
        "has_next": false,
        "has_prev": false,
        "next_page": null,
        "prev_page": null
    }
}
```

#### Obtenir un objectif par ID
```
GET /api/objectifs/1
```

Réponse :
```json
{
    "error": false,
    "message": {
        "en": "Objective retrieved successfully",
        "fr": "Objectif récupéré avec succès"
    },
    "data": {
        "id": 1,
        "titre": "Objectif CA Q1",
        "id_utilisateur": 1,
        "type": "chiffre_affaires",
        "description": "Atteindre 100K€ de CA",
        "periode": "2024.01-2024.03",
        "date_debut": "2024-01-01T00:00:00",
        "date_fin": "2024-03-31T00:00:00",
        "statut": "En cours",
        "progression": 0.75,
        "valeur": 100000,
        "creer_par": 1,
        "modifier_par": 1,
        "creer_a": "2023-01-01T12:00:00",
        "modifier_a": "2023-01-01T12:00:00"
    }
}
```

#### Obtenir les objectifs d'un utilisateur (avec pagination)
```
GET /api/utilisateurs/1/objectifs?page=1&per_page=10
```

Réponse :
```json
{
    "error": false,
    "message": {
        "en": "User objectives retrieved successfully",
        "fr": "Objectifs de l'utilisateur récupérés avec succès"
    },
    "data": [
        {
            "id": 1,
            "titre": "Objectif CA Q1",
            "id_utilisateur": 1,
            "type": "chiffre_affaires",
            "description": "Atteindre 100K€ de CA",
            "periode": "2024.01-2024.03",
            "date_debut": "2024-01-01T00:00:00",
            "date_fin": "2024-03-31T00:00:00",
            "statut": "En cours",
            "progression": 0.75,
            "valeur": 100000,
            "creer_par": 1,
            "modifier_par": 1,
            "creer_a": "2023-01-01T12:00:00",
            "modifier_a": "2023-01-01T12:00:00"
        },
        {
            "id": 2,
            "titre": "Objectif Marge Février",
            "id_utilisateur": 1,
            "type": "marge",
            "description": "Atteindre 30% de marge",
            "periode": "2024.02",
            "date_debut": "2024-02-01T00:00:00",
            "date_fin": "2024-02-29T00:00:00",
            "statut": "En cours",
            "progression": 0.5,
            "valeur": 30,
            "creer_par": 1,
            "modifier_par": 1,
            "creer_a": "2023-01-01T12:00:00",
            "modifier_a": "2023-01-01T12:00:00"
        }
    ],
    "pagination": {
        "page": 1,
        "per_page": 10,
        "total_pages": 1,
        "total_items": 2,
        "has_next": false,
        "has_prev": false,
        "next_page": null,
        "prev_page": null
    }
}
```

#### Obtenir les objectifs par type (avec pagination)
```
GET /api/objectifs/type/chiffre_affaires?page=1&per_page=10
```

Réponse :
```json
{
    "error": false,
    "message": {
        "en": "Objectives by type retrieved successfully",
        "fr": "Objectifs par type récupérés avec succès"
    },
    "data": [
        {
            "id": 1,
            "titre": "Objectif CA Q1",
            "id_utilisateur": 1,
            "type": "chiffre_affaires",
            "description": "Atteindre 100K€ de CA",
            "periode": "2024.01-2024.03",
            "date_debut": "2024-01-01T00:00:00",
            "date_fin": "2024-03-31T00:00:00",
            "statut": "En cours",
            "progression": 0.75,
            "valeur": 100000,
            "creer_par": 1,
            "modifier_par": 1,
            "creer_a": "2023-01-01T12:00:00",
            "modifier_a": "2023-01-01T12:00:00"
        }
    ],
    "pagination": {
        "page": 1,
        "per_page": 10,
        "total_pages": 1,
        "total_items": 1,
        "has_next": false,
        "has_prev": false,
        "next_page": null,
        "prev_page": null
    }
}
```

#### Obtenir les objectifs par période (avec pagination)
```
GET /api/objectifs/periode/2024.01?page=1&per_page=10
```

**Note**: La recherche par période fonctionne avec des périodes simples (ex: "2024.01") ou des plages (ex: "2024.01-2024.03"). La recherche trouvera les objectifs dont la période correspond exactement ou se trouve dans la plage spécifiée.

Réponse :
```json
{
    "error": false,
    "message": {
        "en": "Objectives by period retrieved successfully",
        "fr": "Objectifs par période récupérés avec succès"
    },
    "data": [
        {
            "id": 1,
            "titre": "Objectif CA Q1",
            "id_utilisateur": 1,
            "type": "chiffre_affaires",
            "description": "Atteindre 100K€ de CA",
            "periode": "2024.01-2024.03",
            "date_debut": "2024-01-01T00:00:00",
            "date_fin": "2024-03-31T00:00:00",
            "statut": "En cours",
            "progression": 0.75,
            "valeur": 100000,
            "creer_par": 1,
            "modifier_par": 1,
            "creer_a": "2023-01-01T12:00:00",
            "modifier_a": "2023-01-01T12:00:00"
        }
    ],
    "pagination": {
        "page": 1,
        "per_page": 10,
        "total_pages": 1,
        "total_items": 1,
        "has_next": false,
        "has_prev": false,
        "next_page": null,
        "prev_page": null
    }
}
```

#### Créer un objectif
```
POST /api/objectifs
```

Corps de la requête :
```json
{
    "titre": "Objectif CA Q1",
    "id_utilisateur": 1,
    "type": "chiffre_affaires",
    "description": "Atteindre 100K€ de CA",
    "periode": "2024.01-2024.03",
    "date_debut": "2024-01-01T00:00:00",
    "date_fin": "2024-03-31T00:00:00",
    "statut": "En cours",
    "progression": 0.0,
    "valeur": 100000,
    "creer_par": 1,
    "modifier_par": 1
}
```

Réponse :
```json
{
    "error": false,
    "message": {
        "en": "Objective created successfully",
        "fr": "Objectif créé avec succès"
    },
    "data": {
        "id": 1,
        "titre": "Objectif CA Q1",
        "id_utilisateur": 1,
        "type": "chiffre_affaires",
        "description": "Atteindre 100K€ de CA",
        "periode": "2024.01-2024.03",
        "date_debut": "2024-01-01T00:00:00",
        "date_fin": "2024-03-31T00:00:00",
        "statut": "En cours",
        "progression": 0.0,
        "valeur": 100000,
        "creer_par": 1,
        "modifier_par": 1,
        "creer_a": "2023-01-01T12:00:00",
        "modifier_a": "2023-01-01T12:00:00"
    }
}
```

#### Mettre à jour un objectif
```
PUT /api/objectifs/1
```

Corps de la requête :
```json
{
    "description": "Atteindre 120K€ de CA",
    "periode": "2024.01-2024.06",
    "valeur": 120000,
    "progression": 0.25,
    "modifier_par": 1
}
```

Réponse :
```json
{
    "error": false,
    "message": {
        "en": "Objective updated successfully",
        "fr": "Objectif mis à jour avec succès"
    },
    "data": {
        "id": 1,
        "titre": "Objectif CA Q1",
        "id_utilisateur": 1,
        "type": "chiffre_affaires",
        "description": "Atteindre 120K€ de CA",
        "periode": "2024.01-2024.06",
        "date_debut": "2024-01-01T00:00:00",
        "date_fin": "2024-03-31T00:00:00",
        "statut": "En cours",
        "progression": 0.25,
        "valeur": 120000,
        "creer_par": 1,
        "modifier_par": 1,
        "creer_a": "2023-01-01T12:00:00",
        "modifier_a": "2023-01-01T12:00:00"
    }
}
```

#### Supprimer un objectif
```
DELETE /api/objectifs/1
```

Réponse :
```json
{
    "error": false,
    "message": {
        "en": "Objective deleted successfully",
        "fr": "Objectif supprimé avec succès"
    }
}
```

### Codifications

#### Obtenir toutes les codifications (avec pagination)
```http
GET /api/codifications?page=1&per_page=10
```

Réponse :
```json
{
    "error": false,
    "message": {
        "en": "Codifications retrieved successfully",
        "fr": "Codifications récupérées avec succès"
    },
    "data": [
        {
            "id": 1,
            "libelle": "Type de demande",
            "param": "TYPE_DEMANDE",
            "description": "Types de demandes possibles",
            "creer_par": 1,
            "modifier_par": 1,
            "creer_a": "2024-01-01T12:00:00",
            "modifier_a": "2024-01-01T12:00:00"
        }
    ],
    "pagination": {
        "page": 1,
        "per_page": 10,
        "total_pages": 1,
        "total_items": 1,
        "has_next": false,
        "has_prev": false,
        "next_page": null,
        "prev_page": null
    }
}
```

#### Obtenir une codification par ID
```http
GET /api/codifications/1
```

Réponse :
```json
{
    "error": false,
    "message": {
        "en": "Codification retrieved successfully",
        "fr": "Codification récupérée avec succès"
    },
    "data": {
        "id": 1,
        "libelle": "Type de demande",
        "param": "TYPE_DEMANDE",
        "description": "Types de demandes possibles",
        "creer_par": 1,
        "modifier_par": 1,
        "creer_a": "2024-01-01T12:00:00",
        "modifier_a": "2024-01-01T12:00:00"
    }
}
```

#### Obtenir une codification par paramètre
```http
GET /api/codifications/param/TYPE_DEMANDE
```

Réponse : même format que la recherche par ID.

#### Rechercher des codifications (avec pagination)
```http
GET /api/codifications/search?q=demande&page=1&per_page=10
```

Réponse :
```json
{
    "error": false,
    "message": {
        "en": "Search results retrieved successfully",
        "fr": "Résultats de recherche récupérés avec succès"
    },
    "data": [
        {
            "id": 1,
            "libelle": "Type de demande",
            "param": "TYPE_DEMANDE",
            "description": "Types de demandes possibles",
            "creer_par": 1,
            "modifier_par": 1,
            "creer_a": "2024-01-01T12:00:00",
            "modifier_a": "2024-01-01T12:00:00"
        }
    ],
    "pagination": {
        "page": 1,
        "per_page": 10,
        "total_pages": 1,
        "total_items": 1,
        "has_next": false,
        "has_prev": false,
        "next_page": null,
        "prev_page": null
    }
}
```

#### Créer une codification
```http
POST /api/codifications
```

Corps de la requête :
```json
{
    "libelle": "Type de demande",
    "param": "TYPE_DEMANDE",
    "description": "Types de demandes possibles",
    "creer_par": 1,
    "modifier_par": 1
}
```

Réponse :
```json
{
    "error": false,
    "message": {
        "en": "Codification created successfully",
        "fr": "Codification créée avec succès"
    },
    "data": {
        "id": 1,
        "libelle": "Type de demande",
        "param": "TYPE_DEMANDE",
        "description": "Types de demandes possibles",
        "creer_par": 1,
        "modifier_par": 1,
        "creer_a": "2024-01-01T12:00:00",
        "modifier_a": "2024-01-01T12:00:00"
    }
}
```

#### Mettre à jour une codification
```http
PUT /api/codifications/1
```

Corps de la requête :
```json
{
    "libelle": "Type de demande modifié",
    "description": "Description mise à jour",
    "modifier_par": 1
}
```

Réponse :
```json
{
    "error": false,
    "message": {
        "en": "Codification updated successfully",
        "fr": "Codification mise à jour avec succès"
    },
    "data": {
        "id": 1,
        "libelle": "Type de demande modifié",
        "param": "TYPE_DEMANDE",
        "description": "Description mise à jour",
        "creer_par": 1,
        "modifier_par": 1,
        "creer_a": "2024-01-01T12:00:00",
        "modifier_a": "2024-01-01T12:00:00"
    }
}
```

#### Supprimer une codification
```http
DELETE /api/codifications/1
```

Réponse :
```json
{
    "error": false,
    "message": {
        "en": "Codification deleted successfully",
        "fr": "Codification supprimée avec succès"
    }
}
```

### Settings (Paramètres)

#### Obtenir tous les paramètres (avec pagination)
```http
GET /api/settings?page=1&per_page=10
```

Réponse :
```json
{
    "error": false,
    "message": {
        "en": "Settings retrieved successfully",
        "fr": "Paramètres récupérés avec succès"
    },
    "data": [
        {
            "id_set": 1,
            "id_utilisateur": 1,
            "id_codification": 1
        }
    ],
    "pagination": {
        "page": 1,
        "per_page": 10,
        "total_pages": 1,
        "total_items": 1,
        "has_next": false,
        "has_prev": false,
        "next_page": null,
        "prev_page": null
    }
}
```

#### Obtenir un paramètre par ID
```http
GET /api/settings/1
```

Réponse :
```json
{
    "error": false,
    "message": {
        "en": "Setting retrieved successfully",
        "fr": "Paramètre récupéré avec succès"
    },
    "data": {
        "id_set": 1,
        "id_utilisateur": 1,
        "id_codification": 1
    }
}
```

#### Obtenir les paramètres d'un utilisateur (avec pagination)
```http
GET /api/settings/utilisateur/1?page=1&per_page=10
```

Réponse :
```json
{
    "error": false,
    "message": {
        "en": "User settings retrieved successfully",
        "fr": "Paramètres de l'utilisateur récupérés avec succès"
    },
    "data": [
        {
            "id_set": 1,
            "id_utilisateur": 1,
            "id_codification": 1
        }
    ],
    "pagination": {
        "page": 1,
        "per_page": 10,
        "total_pages": 1,
        "total_items": 1,
        "has_next": false,
        "has_prev": false,
        "next_page": null,
        "prev_page": null
    }
}
```

#### Créer un paramètre
```http
POST /api/settings
```

Corps de la requête :
```json
{
    "id_utilisateur": 1,
    "id_codification": 1
}
```

Réponse :
```json
{
    "error": false,
    "message": {
        "en": "Setting created successfully",
        "fr": "Paramètre créé avec succès"
    },
    "data": {
        "id_set": 1,
        "id_utilisateur": 1,
        "id_codification": 1
    }
}
```

#### Mettre à jour un paramètre
```http
PUT /api/settings/1
```

Corps de la requête :
```json
{
    "id_codification": 2
}
```

Réponse :
```json
{
    "error": false,
    "message": {
        "en": "Setting updated successfully",
        "fr": "Paramètre mis à jour avec succès"
    },
    "data": {
        "id_set": 1,
        "id_utilisateur": 1,
        "id_codification": 2
    }
}
```

#### Supprimer un paramètre
```http
DELETE /api/settings/1
```

Réponse :
```json
{
    "error": false,
    "message": {
        "en": "Setting deleted successfully",
        "fr": "Paramètre supprimé avec succès"
    }
}
```

### Codes de réponse HTTP

## Gestion des Rôles

### Endpoints

#### Récupérer tous les rôles (avec pagination)
```http
GET /api/roles?page=1&per_page=10
```
**Réponse**
```json
{
    "error": false,
    "message": {
        "fr": "Rôles récupérés avec succès",
        "en": "Roles retrieved successfully"
    },
    "data": {
        "items": [
            {
                "role_id": 1,
                "nom": "Admin",
                "description": "Administrateur",
                "app_id": 1,
                "creer_par": 1,
                "modifier_par": 1,
                "creer_a": "2024-03-14T10:00:00",
                "modifier_a": "2024-03-14T10:00:00"
            }
        ],
        "total": 50,
        "pages": 5,
        "current_page": 1
    }
}
```

#### Récupérer les rôles d'une application (avec pagination)
```http
GET /api/roles/application/1?page=1&per_page=10
```
**Réponse**
```json
{
    "error": false,
    "message": {
        "fr": "Rôles de l'application récupérés avec succès",
        "en": "Application roles retrieved successfully"
    },
    "data": {
        "items": [...],
        "total": 20,
        "pages": 2,
        "current_page": 1
    }
}
```

#### Récupérer un rôle par ID
```http
GET /api/roles/1
```
**Réponse**
```json
{
    "error": false,
    "message": {
        "fr": "Rôle récupéré avec succès",
        "en": "Role retrieved successfully"
    },
    "data": {
        "role_id": 1,
        "nom": "Admin",
        "description": "Administrateur",
        "app_id": 1,
        "creer_par": 1,
        "modifier_par": 1,
        "creer_a": "2024-03-14T10:00:00",
        "modifier_a": "2024-03-14T10:00:00"
    }
}
```

#### Créer un rôle
```http
POST /api/roles
```
**Corps de la requête**
```json
{
    "nom": "Admin",
    "description": "Administrateur",
    "app_id": 1,
    "creer_par": 1,
    "modifier_par": 1
}
```
**Réponse**
```json
{
    "error": false,
    "message": {
        "fr": "Rôle créé avec succès",
        "en": "Role created successfully"
    },
    "data": {
        "role_id": 1,
        "nom": "Admin",
        "description": "Administrateur",
        "app_id": 1,
        "creer_par": 1,
        "modifier_par": 1,
        "creer_a": "2024-03-14T10:00:00",
        "modifier_a": "2024-03-14T10:00:00"
    }
}
```

#### Mettre à jour un rôle
```http
PUT /api/roles/1
```
**Corps de la requête**
```json
{
    "nom": "Super Admin",
    "description": "Super Administrateur",
    "modifier_par": 1
}
```
**Réponse**
```json
{
    "error": false,
    "message": {
        "fr": "Rôle mis à jour avec succès",
        "en": "Role updated successfully"
    },
    "data": {
        "role_id": 1,
        "nom": "Super Admin",
        "description": "Super Administrateur",
        "app_id": 1,
        "creer_par": 1,
        "modifier_par": 1,
        "creer_a": "2024-03-14T10:00:00",
        "modifier_a": "2024-03-14T10:30:00"
    }
}
```

#### Supprimer un rôle
```http
DELETE /api/roles/1
```
**Réponse**
```json
{
    "error": false,
    "message": {
        "fr": "Rôle supprimé avec succès",
        "en": "Role deleted successfully"
    }
}
```

#### Récupérer les permissions d'un rôle
```http
GET /api/roles/1/permissions
```
**Réponse**
```json
{
    "error": false,
    "message": {
        "fr": "Permissions du rôle récupérées avec succès",
        "en": "Role permissions retrieved successfully"
    },
    "data": [
        {
            "permission_id": 1,
            "nom": "CREATE",
            "description": "Créer"
        }
    ]
}
```

#### Affecter des permissions à un rôle
```http
POST /api/roles/1/permissions
```
**Corps de la requête**
```json
{
    "permission_ids": [1, 2, 3]
}
```
**Réponse**
```json
{
    "error": false,
    "message": {
        "fr": "Permissions affectées avec succès",
        "en": "Permissions assigned successfully"
    },
    "data": {
        "role_id": 1,
        "nom": "Admin",
        "description": "Administrateur",
        "app_id": 1
    }
}
```

#### Retirer des permissions d'un rôle
```http
DELETE /api/roles/1/permissions
```
**Corps de la requête**
```json
{
    "permission_ids": [1, 2]
}
```
**Réponse**
```json
{
    "error": false,
    "message": {
        "fr": "Permissions retirées avec succès",
        "en": "Permissions removed successfully"
    },
    "data": {
        "role_id": 1,
        "nom": "Admin",
        "description": "Administrateur",
        "app_id": 1
    }
}
```

### Notes importantes
- Chaque rôle doit être lié à une application (`app_id` requis)
- Le nom du rôle doit être unique par application
- Un rôle ne peut pas être supprimé s'il est associé à des utilisateurs
- Lors de la suppression d'un rôle, toutes ses permissions sont automatiquement retirées

## API de Fonctions

Les API de fonctions permettent de gérer les fonctions API et leurs permissions associées. Ces fonctions remplacent l'ancien système basé sur les endpoints URL et méthodes HTTP.

### Modèle de données

Le modèle de données a été modifié pour passer d'un système basé sur les URL et méthodes HTTP à un système basé sur les noms de fonctions :

- `endpoint` → `fonction_api`
- `endpoint_permission` → `fonction_permission`
- `url_pattern` + `methode` → `nom_fonction`

### Routes disponibles

#### Gestion des fonctions API

| Méthode | Route | Description |
|---------|-------|-------------|
| GET | `/api/fonctions_api` | Liste des fonctions API (paginée) |
| GET | `/api/fonctions_api/application/{app_id}` | Liste des fonctions API pour une application (paginée) |
| GET | `/api/fonctions_api/{id}` | Détails d'une fonction API |
| POST | `/api/fonctions_api` | Créer une nouvelle fonction API |
| PUT | `/api/fonctions_api/{id}` | Mettre à jour une fonction API |
| DELETE | `/api/fonctions_api/{id}` | Supprimer une fonction API |

#### Gestion des permissions des fonctions API

| Méthode | Route | Description |
|---------|-------|-------------|
| GET | `/api/fonctions_api/{id}/permissions` | Liste des permissions d'une fonction API |
| POST | `/api/fonctions_api/{id}/permissions` | Assigner des permissions à une fonction API |
| DELETE | `/api/fonctions_api/{id}/permissions` | Retirer des permissions d'une fonction API |
| POST | `/api/fonctions_api/{fonction_id}/permissions/{permission_id}` | Assigner une permission spécifique à une fonction API |

### Exemples de requêtes

#### Créer une fonction API

```http
POST /api/fonctions_api
Content-Type: application/json

{
    "nom_fonction": "get_utilisateurs",
    "description": "Récupère la liste des utilisateurs",
    "app_id": 1,
    "creer_par": 1,
    "modifier_par": 1
}
```

#### Assigner des permissions à une fonction API

```http
POST /api/fonctions_api/1/permissions
Content-Type: application/json

{
    "permission_ids": [1, 2, 3]
}
```

### Fonctions API

#### 1. Lister toutes les fonctions API
```http
GET {{BASE_URL}}/fonctions_api
```

Paramètres de pagination (optionnels) :
- `page` : Numéro de la page (défaut: 1)
- `per_page` : Nombre d'éléments par page (défaut: 10, max: 50)

Exemple :
```http
GET {{BASE_URL}}/fonctions_api?page=2&per_page=15
```

Exemple de réponse avec pagination :
```json
{
    "error": false,
    "message": {
        "en": "API functions retrieved successfully",
        "fr": "Fonctions API récupérées avec succès"
    },
    "data": [
        {
            "fonction_id": 1,
            "nom_fonction": "get_utilisateurs",
            "description": "Récupère la liste des utilisateurs",
            "app_id": 1,
            "creer_par": 1,
            "modifier_par": 1,
            "creer_a": "2024-05-15T12:00:00",
            "modifier_a": "2024-05-15T12:00:00"
        },
        // ... autres fonctions ...
    ],
    "pagination": {
        "page": 2,
        "per_page": 15,
        "total_items": 45,
        "total_pages": 3,
        "has_next": false,
        "has_prev": true,
        "next_page": null,
        "prev_page": 1
    }
}
```

#### 2. Lister les fonctions API d'une application
```http
GET {{BASE_URL}}/fonctions_api/application/1
```

Supporte également la pagination avec les paramètres `page` et `per_page`.

#### 3. Obtenir une fonction API spécifique
```http
GET {{BASE_URL}}/fonctions_api/1
```

Exemple de réponse :
```json
{
    "error": false,
    "message": {
        "en": "API function retrieved successfully",
        "fr": "Fonction API récupérée avec succès"
    },
    "data": {
        "fonction_id": 1,
        "nom_fonction": "get_utilisateurs",
        "description": "Récupère la liste des utilisateurs",
        "app_id": 1,
        "creer_par": 1,
        "modifier_par": 1,
        "creer_a": "2024-05-15T12:00:00",
        "modifier_a": "2024-05-15T12:00:00"
    }
}
```

#### 4. Créer une nouvelle fonction API
```http
POST {{BASE_URL}}/fonctions_api
```

Body (JSON) :
```json
{
    "nom_fonction": "get_utilisateurs",
    "description": "Récupère la liste des utilisateurs",
    "app_id": 1,
    "creer_par": 1,
    "modifier_par": 1
}
```

Exemple de réponse réussie :
```json
{
    "error": false,
    "message": {
        "en": "API function created successfully",
        "fr": "Fonction API créée avec succès"
    },
    "data": {
        "fonction_id": 1,
        "nom_fonction": "get_utilisateurs",
        "description": "Récupère la liste des utilisateurs",
        "app_id": 1,
        "creer_par": 1,
        "modifier_par": 1,
        "creer_a": "2024-05-15T12:00:00",
        "modifier_a": "2024-05-15T12:00:00"
    }
}
```

#### 5. Mettre à jour une fonction API
```http
PUT {{BASE_URL}}/fonctions_api/1
```

Body (JSON) :
```json
{
    "description": "Récupère la liste complète des utilisateurs",
    "modifier_par": 1
}
```

Exemple de réponse réussie :
```json
{
    "error": false,
    "message": {
        "en": "API function updated successfully",
        "fr": "Fonction API mise à jour avec succès"
    },
    "data": {
        "fonction_id": 1,
        "nom_fonction": "get_utilisateurs",
        "description": "Récupère la liste complète des utilisateurs",
        "app_id": 1,
        "creer_par": 1,
        "modifier_par": 1,
        "creer_a": "2024-05-15T12:00:00",
        "modifier_a": "2024-05-15T12:30:00"
    }
}
```

#### 6. Supprimer une fonction API
```http
DELETE {{BASE_URL}}/fonctions_api/1
```

Exemple de réponse réussie :
```json
{
    "error": false,
    "message": {
        "en": "API function deleted successfully",
        "fr": "Fonction API supprimée avec succès"
    }
}
```

#### 7. Obtenir les permissions d'une fonction API
```http
GET {{BASE_URL}}/fonctions_api/1/permissions
```

Exemple de réponse :
```json
{
    "error": false,
    "message": {
        "en": "API function permissions retrieved successfully",
        "fr": "Permissions de la fonction API récupérées avec succès"
    },
    "data": [
        {
            "permission_id": 1,
            "nom": "READ",
            "description": "Permission de lecture"
        },
        {
            "permission_id": 2,
            "nom": "WRITE",
            "description": "Permission d'écriture"
        }
    ]
}
```

#### 8. Assigner des permissions à une fonction API
```http
POST {{BASE_URL}}/fonctions_api/1/permissions
```

Body (JSON) :
```json
{
    "permission_ids": [1, 2, 3]
}
```

Exemple de réponse réussie :
```json
{
    "error": false,
    "message": {
        "en": "Permissions assigned to API function successfully",
        "fr": "Permissions assignées à la fonction API avec succès"
    },
    "data": {
        "fonction_id": 1,
        "nom_fonction": "get_utilisateurs",
        "description": "Récupère la liste des utilisateurs",
        "app_id": 1
    }
}
```

#### 9. Retirer des permissions d'une fonction API
```http
DELETE {{BASE_URL}}/fonctions_api/1/permissions
```

Body (JSON) :
```json
{
    "permission_ids": [2, 3]
}
```

Exemple de réponse réussie :
```json
{
    "error": false,
    "message": {
        "en": "Permissions removed from API function successfully",
        "fr": "Permissions retirées de la fonction API avec succès"
    },
    "data": {
        "fonction_id": 1,
        "nom_fonction": "get_utilisateurs",
        "description": "Récupère la liste des utilisateurs",
        "app_id": 1
    }
}
```

#### 10. Assigner une permission spécifique à une fonction API
```http
POST {{BASE_URL}}/fonctions_api/1/permissions/4
```

Exemple de réponse réussie :
```json
{
    "error": false,
    "message": {
        "en": "Permission assigned to API function successfully",
        "fr": "Permission assignée à la fonction API avec succès"
    },
    "data": {
        "fonction_id": 1,
        "nom_fonction": "get_utilisateurs",
        "description": "Récupère la liste des utilisateurs",
        "app_id": 1
    }
}
```

### Notes importantes sur les fonctions API
- Chaque fonction API doit être liée à une application (`app_id` requis)
- Le nom de la fonction (`nom_fonction`) doit être unique par application
- Une fonction API ne peut pas être supprimée si elle est associée à des permissions actives
- Lors de la suppression d'une fonction API, toutes ses permissions sont automatiquement retirées

### Utilisateurs

#### 1. Lister tous les utilisateurs
```http
GET {{BASE_URL}}/utilisateurs?page=1&per_page=10
```

Paramètres de pagination (optionnels) :
- `page` : Numéro de la page (défaut: 1)
- `per_page` : Nombre d'éléments par page (défaut: 10, max: 50)

Exemple :
```http
GET {{BASE_URL}}/utilisateurs?page=2&per_page=15
```

Exemple de réponse avec pagination :
```json
{
    "error": false,
    "message": {
        "en": "Users retrieved successfully",
        "fr": "Utilisateurs récupérés avec succès"
    },
    "data": [
        {
            "id_utilisateur": 1,
            "nom": "Dupont",
            "prenom": "Jean",
            "login": "jdupont",
            "email": "jean.dupont@example.com",
            "statut": "Actif",
            "date_expiration": "2025-12-31T00:00:00",
            "profil": "Administrateur",
            "id_entite": 1,
            "creer_par": 1,
            "modifier_par": 1,
            "creer_a": "2024-03-05T12:00:00",
            "modifier_a": "2024-03-05T12:00:00",
            "entite": {
                "id": 1,
                "nom": "Siège",
                "code": "SIEGE",
                "email": "siege@example.com",
                "creer_par": 1,
                "modifier_par": 1,
                "creer_a": "2024-03-05T12:00:00",
                "modifier_a": "2024-03-05T12:00:00"
            },
            "utilisateur_roles": [...]
        }
    ],
    "pagination": {
        "page": 2,
        "per_page": 15,
        "total_items": 45,
        "total_pages": 3,
        "has_next": false,
        "has_prev": true,
        "next_page": null,
        "prev_page": 1
    }
}
```

#### 2. Lister les utilisateurs par entité
```http
GET {{BASE_URL}}/utilisateurs/entite/1
```

Supporte également la pagination avec les paramètres `page` et `per_page`.

#### 3. Lister les utilisateurs par rôle
```http
GET {{BASE_URL}}/utilisateurs/role/1
```

Supporte également la pagination avec les paramètres `page` et `per_page`.

#### 4. Obtenir un utilisateur spécifique
```http
GET {{BASE_URL}}/utilisateurs/1
```

Exemple de réponse :
```json
{
    "error": false,
    "message": {
        "en": "User retrieved successfully",
        "fr": "Utilisateur récupéré avec succès"
    },
    "data": {
        "id_utilisateur": 1,
        "nom": "Dupont",
        "prenom": "Jean",
        "login": "jdupont",
        "email": "jean.dupont@example.com",
        "statut": "Actif",
        "date_expiration": "2025-12-31T00:00:00",
        "profil": "Administrateur",
        "id_entite": 1,
        "creer_par": 1,
        "modifier_par": 1,
        "creer_a": "2024-03-05T12:00:00",
        "modifier_a": "2024-03-05T12:00:00",
        "entite": {
            "id": 1,
            "nom": "Siège",
            "code": "SIEGE",
            "email": "siege@example.com",
            "creer_par": 1,
            "modifier_par": 1,
            "creer_a": "2024-03-05T12:00:00",
            "modifier_a": "2024-03-05T12:00:00"
        },
        "utilisateur_roles": [...]
    }
}
```

#### 5. Rechercher des utilisateurs
```http
GET {{BASE_URL}}/utilisateurs/search?q=dupont
```

Supporte également la pagination avec les paramètres `page` et `per_page`.

#### 6. Obtenir un utilisateur par login
```http
GET {{BASE_URL}}/utilisateurs/login/jdupont
```

#### 7. Obtenir un utilisateur par email
```http
GET {{BASE_URL}}/utilisateurs/email/jean.dupont@example.com
```

#### 8. Créer un nouvel utilisateur
```http
POST {{BASE_URL}}/utilisateurs
```

Body (JSON) :
```json
{
    "nom": "Dupont",
    "prenom": "Jean",
    "login": "jdupont",
    "email": "jean.dupont@example.com",
    "statut": "Actif",
    "date_expiration": "2025-12-31T00:00:00",
    "profil": "Administrateur",
    "id_entite": 1,
    "creer_par": 1,
    "modifier_par": 1
}
```

Exemple de réponse réussie :
```json
{
    "error": false,
    "message": {
        "en": "User created successfully",
        "fr": "Utilisateur créé avec succès"
    },
    "data": {
        "id_utilisateur": 1,
        "nom": "Dupont",
        "prenom": "Jean",
        "login": "jdupont",
        "email": "jean.dupont@example.com",
        "statut": "Actif",
        "date_expiration": "2025-12-31T00:00:00",
        "profil": "Administrateur",
        "id_entite": 1,
        "creer_par": 1,
        "modifier_par": 1,
        "creer_a": "2024-03-05T12:00:00",
        "modifier_a": "2024-03-05T12:00:00",
        "entite": {
            "id": 1,
            "nom": "Siège",
            "code": "SIEGE",
            "email": "siege@example.com",
            "creer_par": 1,
            "modifier_par": 1,
            "creer_a": "2024-03-05T12:00:00",
            "modifier_a": "2024-03-05T12:00:00"
        },
        "utilisateur_roles": []
    }
}
```

#### 9. Mettre à jour un utilisateur
```http
PUT {{BASE_URL}}/utilisateurs/1
```

Body (JSON) :
```json
{
    "nom": "Dupont",
    "prenom": "Jean-Pierre",
    "email": "jean-pierre.dupont@example.com",
    "modifier_par": 1
}
```

Exemple de réponse réussie :
```json
{
    "error": false,
    "message": {
        "en": "User updated successfully",
        "fr": "Utilisateur mis à jour avec succès"
    },
    "data": {
        "id_utilisateur": 1,
        "nom": "Dupont",
        "prenom": "Jean-Pierre",
        "login": "jdupont",
        "email": "jean-pierre.dupont@example.com",
        "statut": "Actif",
        "date_expiration": "2025-12-31T00:00:00",
        "profil": "Administrateur",
        "id_entite": 1,
        "creer_par": 1,
        "modifier_par": 1,
        "creer_a": "2024-03-05T12:00:00",
        "modifier_a": "2024-03-05T12:00:00",
        "entite": {
            "id": 1,
            "nom": "Siège",
            "code": "SIEGE",
            "email": "siege@example.com",
            "creer_par": 1,
            "modifier_par": 1,
            "creer_a": "2024-03-05T12:00:00",
            "modifier_a": "2024-03-05T12:00:00"
        },
        "utilisateur_roles": [...]
    }
}
```

#### 10. Supprimer un utilisateur
```http
DELETE {{BASE_URL}}/utilisateurs/1
```

Exemple de réponse réussie :
```json
{
    "error": false,
    "message": {
        "en": "User deleted successfully",
        "fr": "Utilisateur supprimé avec succès"
    }
}
```

#### 11. Prolonger la date d'expiration d'un utilisateur
```http
PUT {{BASE_URL}}/utilisateurs/1/prolonger
Content-Type: application/json

{
  "date_expiration": "2025-12-31T00:00:00"
}
```

Réponse :

```json
{
  "status": "success",
  "message": "Date d'expiration prolongée avec succès",
  "data": {
    "id": 1,
    "nom": "Dupont",
    "prenom": "Jean",
    "login": "jdupont",
    "email": "jean.dupont@example.com",
    "statut": "Actif",
    "date_expiration": "2025-12-31T00:00:00",
    "profil": "Administrateur",
    "id_entite": 1,
    "entite": {
      "id": 1,
      "nom": "Siège"
    }
  }
}
```

**Note**: Vous pouvez désormais spécifier directement la nouvelle date d'expiration au format ISO 8601 (`YYYY-MM-DDThh:mm:ss`). Si aucune date n'est fournie, la date d'expiration sera automatiquement prolongée de 30 jours à partir de la date actuelle.

#### 12. Mettre à jour le profil d'un utilisateur
```http
PUT {{BASE_URL}}/utilisateurs/1/profil
```

Body (JSON) :
```json
{
    "nom": "Dupont",
    "prenom": "Jean-Pierre",
    "email": "jean-pierre.dupont@example.com"
}
```

Exemple de réponse réussie :
```json
{
    "error": false,
    "message": {
        "en": "Profile updated successfully",
        "fr": "Profil mis à jour avec succès"
    },
    "data": {
        "id_utilisateur": 1,
        "nom": "Dupont",
        "prenom": "Jean-Pierre",
        "email": "jean-pierre.dupont@example.com"
    }
}
```

#### 13. Mettre à jour le statut d'un utilisateur
```http
PUT {{BASE_URL}}/utilisateurs/1/statut
```

Body (JSON) :
```json
{
    "statut": "Inactif"
}
```

Exemple de réponse réussie :
```json
{
    "error": false,
    "message": {
        "en": "Status updated successfully",
        "fr": "Statut mis à jour avec succès"
    },
    "data": {
        "id_utilisateur": 1,
        "nom": "Dupont",
        "prenom": "Jean",
        "statut": "Inactif"
    }
}
```

#### 14. Vérifier l'éligibilité d'un utilisateur
```http
GET {{BASE_URL}}/utilisateurs/1/eligibilite?app_id=1
```

Exemple de réponse :
```json
{
    "error": false,
    "message": {
        "en": "Eligibility checked successfully",
        "fr": "Éligibilité vérifiée avec succès"
    },
    "data": {
        "eligible": true,
        "raison": null
    }
}
```

#### 15. Obtenir les rôles d'un utilisateur
```http
GET {{BASE_URL}}/utilisateurs/1/roles
```

Exemple de réponse :
```json
{
    "error": false,
    "message": {
        "en": "User roles retrieved successfully",
        "fr": "Rôles de l'utilisateur récupérés avec succès"
    },
    "data": [
        {
            "ur_id": 1,
            "id_utilisateur": 1,
            "role_id": 1,
            "app_id": 1,
            "role": {
                "role_id": 1,
                "nom": "Admin",
                "description": "Administrateur"
            },
            "application": {
                "app_id": 1,
                "nom": "Application 1"
            }
        }
    ]
}
```

#### 16. Assigner un rôle à un utilisateur
```http
POST {{BASE_URL}}/utilisateurs/1/roles
```

Body (JSON) :
```json
{
    "role_id": 2,
    "app_id": 1,
    "creer_par": 1,
    "modifier_par": 1
}
```

Exemple de réponse réussie :
```json
{
    "error": false,
    "message": {
        "en": "Role assigned successfully",
        "fr": "Rôle assigné avec succès"
    },
    "data": [
        {
            "ur_id": 2,
            "id_utilisateur": 1,
            "role_id": 2,
            "app_id": 1,
            "role": {
                "role_id": 2,
                "nom": "Éditeur",
                "description": "Éditeur de contenu"
            },
            "application": {
                "app_id": 1,
                "nom": "Application 1"
            }
        }
    ]
}
```

#### 17. Retirer un rôle d'un utilisateur
```http
DELETE {{BASE_URL}}/utilisateurs/1/roles/2/application/1
```

Exemple de réponse réussie :
```json
{
    "error": false,
    "message": {
        "en": "Role removed successfully",
        "fr": "Rôle retiré avec succès"
    }
}
```

### Notes importantes sur les utilisateurs
- Le login et l'email doivent être uniques dans le système
- Les mots de passe ne sont pas gérés dans ce système (authentification externe)
- Un utilisateur peut avoir plusieurs rôles, mais un seul rôle par application
- Lors de la suppression d'un utilisateur, toutes ses associations de rôles sont automatiquement retirées
- Les statuts valides sont : "Actif", "Inactif", "Suspendu", "En attente"

### Authentification

#### Login
```http
POST {{BASE_URL}}/auth/login
Content-Type: application/json

{
  "login": "jdupont",
  "password": "motdepasse"
}
```

Réponse en cas de succès :
```json
{
  "error": false,
  "message": {
    "en": "Authentication successful",
    "fr": "Authentification réussie"
  },
  "data": {
    "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
    "utilisateur": {
      "id_utilisateur": 1,
      "nom": "Dupont",
      "prenom": "Jean",
      "login": "jdupont",
      "email": "jean.dupont@example.com",
      "statut": "Actif",
      "date_expiration": "2025-12-31T00:00:00",
      "profil": "Administrateur",
      "id_entite": 1,
      "creer_par": 1,
      "modifier_par": 1,
      "creer_a": "2024-03-05T12:00:00",
      "modifier_a": "2024-03-05T12:00:00",
      "entite": {
        "id": 1,
        "nom": "Siège",
        "code": "SIEGE",
        "email": "siege@example.com",
        "creer_par": 1,
        "modifier_par": 1,
        "creer_a": "2024-03-05T12:00:00",
        "modifier_a": "2024-03-05T12:00:00"
      },
      "utilisateur_roles": [...]
    }
  }
}
```

Réponse en cas d'échec (exemples) :
```json
{
  "error": true,
  "message": {
    "en": "User not found",
    "fr": "Utilisateur non trouvé"
  }
}
```

```json
{
  "error": true,
  "message": {
    "en": "Account is inactive or expired",
    "fr": "Compte utilisateur inactif ou expiré"
  }
}
```
### Gestion des erreurs d'authentification

Les erreurs d'authentification suivent le format standard suivant :

```json
{
  "error": true,
  "message": {
    "en": "Error message in English",
    "fr": "Message d'erreur en français"
  },
  "details": {
    "en": "Detailed explanation in English",
    "fr": "Explication détaillée en français"
  }
}
```

#### Types d'erreurs possibles

1. Token invalide (401)
```json
{
  "error": true,
  "message": {
    "en": "Invalid token",
    "fr": "Token invalide"
  }
}
```

2. Token expiré (401)
```json
{
  "error": true,
  "message": {
    "en": "Token has expired",
    "fr": "Token expiré"
  },
  "details": {
    "en": "Please login again to get a new token",
    "fr": "Connectez-vous à nouveau pour obtenir un nouveau token"
  }
}
```

3. Accès non autorisé (401)
```json
{
  "error": true,
  "message": {
    "en": "Unauthorized access",
    "fr": "Accès non autorisé"
  }
}
```

4. Token révoqué (401)
```json
{
  "error": true,
  "message": {
    "en": "Token has been revoked",
    "fr": "Token révoqué"
  },
  "details": {
    "en": "The token has been revoked",
    "fr": "Le token a été révoqué"
  }
}
```
```