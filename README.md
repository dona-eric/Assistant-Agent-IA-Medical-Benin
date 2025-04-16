# Assistant IA en Santé - Bénin

Une application d'assistant IA spécialisé en santé au Bénin utilisant LangChain, LangGraph, Ollama et Streamlit, avec intégration de Google Maps pour la localisation des hôpitaux et la prise de rendez-vous.

## Architecture Détaillée

### 1. Contexte Médical et Infrastructure
- **Données maladies prévalentes** :
  - Intégration des bases de données (OMS, Ministère de la Santé)
  - Modules d'information et de prévention par maladie
- **Cartographie des structures de santé** :
  - Collecte via open data et API gouvernementales
  - Stockage des coordonnées GPS et informations des établissements
- **Accès rural** :
  - Version offline avec cache local
  - Backend SMS/USSD pour zones non connectées

### 2. Fonctionnalités Techniques
- **Gestion de rendez-vous** :
  - API RESTful pour synchronisation des créneaux
  - Interface mobile/web + passerelle SMS/USSD
  - Système de notifications (Twilio/Nexmo)
- **Recherche d'hôpitaux** :
  - Intégration Google Maps/OpenStreetMap
  - Algorithme de tri par distance et disponibilité
  - Mise à jour continue des statuts

### 3. Adaptation Culturelle et Linguistique
- **Langues supportées** :
  - Français, Fon, Yoruba, Bariba
  - Interface multilingue
- **Sensibilité culturelle** :
  - Base de connaissances sur pratiques traditionnelles
  - Conseils contextualisés

### 4. Sécurité et Conformité
- **RGPD/lois locales** :
  - Chiffrement (AES, TLS)
  - Anonymisation des données
- **Consentement** :
  - Pop-up explicatif
  - Gestion des droits d'accès

### 5. Interface Utilisateur
- **Design inclusif** :
  - Navigation simplifiée
  - Tutoriels vidéo/audio
- **Accessibilité** :
  - Synthèse vocale
  - Mode contraste élevé

### 6. Partnerships et Écosystème
- **Collaborations** :
  - API pour échanges de données
  - Plateforme d'administration partenaires
- **Financement** :
  - Système d'abonnement pour cliniques

### 7. Gestion des Urgences
- **Détection symptômes** :
  - Questionnaire intelligent
  - Scoring de gravité
- **Coordination** :
  - API/SMS vers services d'urgence

### 8. Optimisation Technique
- **Modèle Mistral** :
  - Fine-tuning sur données locales
  - Disclaimers pour incertitudes
- **Infrastructure** :
  - Cloud scalable
  - Backup local

### 9. Validation et Amélioration
- **Tests utilisateurs** :
  - Pilotes en ville et zones rurales
- **Feedback loop** :
  - Formulaire intégré
  - Validation médicale

### 10. Aspects Juridico-Éthiques
- **Limites de responsabilité** :
  - Mentions légales
- **Comité d'éthique** :
  - Validation des fonctionnalités

## Architecture API et Base de Données

### 1. Architecture API
- **API Gateway** :
  - Gestion des authentifications
  - Rate limiting
  - Logging des requêtes
  - Cache des réponses fréquentes

- **Endpoints Principaux** :
  ```
  /api/v1/
  ├── /auth/           # Authentification et autorisation
  ├── /hospitals/      # Gestion des hôpitaux
  ├── /appointments/   # Prise de rendez-vous
  ├── /medical-info/   # Informations médicales
  ├── /emergency/      # Gestion des urgences
  └── /user/           # Gestion des utilisateurs
  ```

- **Sécurité** :
  - JWT pour l'authentification
  - HTTPS obligatoire
  - Validation des entrées
  - Protection contre les attaques CSRF

### 2. Architecture Base de Données
- **Système de Gestion** :
  - PostgreSQL pour les données relationnelles
  - MongoDB pour les données non-structurées
  - Redis pour le cache

- **Schéma Principal** :
  ```sql
  -- Table des utilisateurs
  CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    phone_number VARCHAR(20) UNIQUE,
    email VARCHAR(255),
    language_preference VARCHAR(10),
    created_at TIMESTAMP,
    last_login TIMESTAMP
  );

  -- Table des hôpitaux
  CREATE TABLE hospitals (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255),
    address TEXT,
    latitude DECIMAL(10,8),
    longitude DECIMAL(11,8),
    phone_number VARCHAR(20),
    type VARCHAR(50),
    specialties JSONB,
    working_hours JSONB
  );

  -- Table des rendez-vous
  CREATE TABLE appointments (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    hospital_id INTEGER REFERENCES hospitals(id),
    doctor_id INTEGER,
    date_time TIMESTAMP,
    status VARCHAR(20),
    symptoms TEXT,
    created_at TIMESTAMP
  );

  -- Table des informations médicales
  CREATE TABLE medical_info (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255),
    content TEXT,
    language VARCHAR(10),
    category VARCHAR(50),
    created_at TIMESTAMP,
    updated_at TIMESTAMP
  );
  ```

- **Indexes et Optimisations** :
  - Index géospatial pour la recherche d'hôpitaux
  - Index sur les champs fréquemment recherchés
  - Partitionnement des tables par date

### 3. Synchronisation et Réplication
- **Stratégie de Réplication** :
  - Master-slave pour la haute disponibilité
  - Réplication géographique pour la réduction de latence
  - Backup automatique quotidien

- **Synchronisation Hors-ligne** :
  - Queue de synchronisation pour les zones rurales
  - Compression des données pour les connexions lentes
  - Gestion des conflits de données

### 4. Monitoring et Maintenance
- **Outils de Monitoring** :
  - Prometheus pour les métriques
  - Grafana pour la visualisation
  - Alertes automatiques

- **Maintenance** :
  - Scripts de migration automatiques
  - Nettoyage périodique des données
  - Optimisation des performances

## Prérequis

- Python 3.12
- Ollama installé et configuré sur votre machine
- Le modèle Llama2 téléchargé dans Ollama
- Une clé API Google Maps (pour les fonctionnalités de cartographie)

## Installation

1. Clonez ce dépôt :
```bash
git clone [URL_DU_REPO]
cd [NOM_DU_REPO]
```

2. Installez les dépendances :
```bash
pip install -r requirements.txt
```

3. Configurez votre clé API Google Maps :
```bash
echo "GOOGLE_MAPS_API_KEY=votre_clé_api" > .env
```

4. Assurez-vous qu'Ollama est en cours d'exécution :
```bash
ollama serve
```

5. Téléchargez le modèle Llama2 si ce n'est pas déjà fait :
```bash
ollama pull llama2
```

## Fonctionnalités

### 1. Assistant de Questions Santé
- Posez des questions sur la santé
- Obtenez des réponses basées sur le modèle Llama2
- Recommandations d'hôpitaux appropriés au Bénin

### 2. Recherche d'Hôpitaux
- Trouvez des hôpitaux par ville
- Filtrez par spécialité médicale
- Visualisez les hôpitaux sur une carte interactive
- Informations détaillées sur chaque établissement

### 3. Prise de Rendez-vous
- Prenez rendez-vous dans les hôpitaux listés
- Sélectionnez la date et l'heure
- Confirmation immédiate du rendez-vous
- Rappels et informations pratiques

## Workflow de Fine-Tuning NLP Multilingue

### 1. Collecte des Données
- **Corpus médicaux** : 
  - Dossiers médicaux anonymisés
  - FAQs de médecins béninois
  - Guides de santé publique
- **Langues cibles** :
  - Français (langue officielle)
  - Fon (langue locale majeure)
  - Yoruba (langue régionale)
  - Bariba (langue régionale)

### 2. Préparation des Données
- **Nettoyage** :
  - Suppression des informations personnelles
  - Normalisation du texte
  - Traduction parallèle pour les corpus multilingues
- **Annotation** :
  - Étiquetage des entités médicales
  - Classification des intents (questions, réponses, symptômes)
  - Marqueurs culturels et contextuels

### 3. Fine-Tuning du Modèle
- **Configuration** :
  - Utilisation de Mistral comme modèle de base
  - Adaptation des paramètres pour les langues locales
  - Optimisation pour le contexte médical béninois
- **Entraînement** :
  - Phases d'entraînement progressif
  - Validation croisée multilingue
  - Tests de performance par langue

### 4. Évaluation et Validation
- **Métriques** :
  - Précision par langue
  - Compréhension contextuelle
  - Pertinence des réponses
- **Tests** :
  - Validation par des médecins locaux
  - Tests utilisateurs en conditions réelles
  - Vérification de la sensibilité culturelle

### 5. Déploiement et Maintenance
- **Intégration** :
  - Mise en production progressive
  - Monitoring des performances
  - Collecte de feedback
- **Amélioration continue** :
  - Mise à jour régulière des corpus
  - Ajustement des paramètres
  - Ajout de nouvelles langues si nécessaire

### Ressources Nécessaires
- Serveurs GPU pour l'entraînement
- Stockage sécurisé pour les données médicales
- Expertise en NLP et en langues locales
- Collaboration avec des professionnels de santé

## Utilisation

1. Lancez l'application Streamlit :
```bash
streamlit run app.py
```

2. Ouvrez votre navigateur à l'adresse indiquée (généralement http://localhost:8501)

3. Utilisez les différents onglets pour :
   - Poser des questions sur la santé
   - Trouver des hôpitaux près de chez vous
   - Prendre rendez-vous avec un médecin

## Avertissement

Cet assistant IA fournit des informations générales sur la santé et ne remplace pas l'avis d'un professionnel de santé qualifié. Consultez toujours un médecin pour des problèmes de santé spécifiques.

## Contribution

Les données des hôpitaux sont stockées dans `benin_healthcare_data.py`. N'hésitez pas à contribuer en ajoutant de nouveaux établissements ou en mettant à jour les informations existantes.

## Licence

MIT 