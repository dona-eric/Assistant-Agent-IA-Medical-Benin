# Assistant IA en Santé - Bénin

Une application d'assistant IA spécialisé en santé au Bénin utilisant LangChain, LangGraph, Ollama et Streamlit, avec intégration de Google Maps pour la localisation des hôpitaux et la prise de rendez-vous.

## Prérequis

- Python 3.12
- Ollama installé et configuré sur votre machine
- Le modèle Llama2 téléchargé dans Ollama
- Une clé API Google Maps (pour les fonctionnalités de cartographie)

## Installation

1. Clonez ce dépôt :
```bash
git clone git@github.com:dona-eric/Assistant-Agent-IA-Medical-Benin.git
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

## Auteur 
Eric KOULODJI D.
**Data Scientist, Developpeur Django & Machine Learning Specialist**
