import streamlit as st

# Configuration de la page Streamlit (DOIT être la première commande Streamlit)
st.set_page_config(
    page_title="Assistant Médical Bénin",
    page_icon="🏥",
    layout="wide"
)

import pandas as pd
import folium
from streamlit_folium import folium_static
import benin_healthcare_data as bhd
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv
import requests
import json
from typing import Dict, Optional
import time

# Charger les variables d'environnement
load_dotenv()

# Configuration de l'API Hugging Face
HF_API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.2"
HF_API_TOKEN = os.getenv("HUGGINGFACE_API_TOKEN")

# Cache pour stocker les réponses
response_cache: Dict[str, Dict] = {}

def query_huggingface(prompt: str) -> Optional[str]:
    headers = {"Authorization": f"Bearer {HF_API_TOKEN}"}
    
    try:
        response = requests.post(
            HF_API_URL,
            headers=headers,
            json={"inputs": prompt}
        )
        
        if response.status_code == 200:
            return response.json()[0]['generated_text']
        elif response.status_code == 503:
            # Le modèle est en cours de chargement, attendre et réessayer
            time.sleep(20)
            return query_huggingface(prompt)
        else:
            st.error(f"Erreur API: {response.status_code}")
            return None
    except Exception as e:
        st.error(f"Erreur de connexion: {str(e)}")
        return None

def generate_response(question: str) -> str:
    # Vérifier le cache
    cache_key = question.lower().strip()
    if cache_key in response_cache:
        cached_response = response_cache[cache_key]
        if time.time() - cached_response['timestamp'] < 3600:  # Cache valide pendant 1 heure
            return cached_response['response']
    
    # Préparer le prompt
    prompt = f"""
    Tu es un assistant médical professionnel au Bénin avec une expertise approfondie en santé publique.
    Réponds à la question suivante de manière claire, précise et adaptée au contexte béninois.
    
    Question: {question}
    
    Pour les questions sur les maladies :
    - Décris les symptômes principaux
    - Explique les causes possibles
    - Donne des conseils de prévention adaptés au contexte béninois
    - Recommande quand consulter un médecin
    - Mentionne les centres de santé appropriés au Bénin
    
    Pour les questions sur les traitements :
    - Explique les options disponibles au Bénin
    - Mentionne les précautions à prendre
    - Indique les centres spécialisés au Bénin
    
    Réponse:
    """
    
    # Obtenir la réponse de l'API
    response = query_huggingface(prompt)
    
    if response:
        # Nettoyer la réponse
        response = response.replace(prompt, "").strip()
        
        # Mettre en cache
        response_cache[cache_key] = {
            'response': response,
            'timestamp': time.time()
        }
        
        return response
    else:
        return """
        Je suis désolé, je ne peux pas répondre à cette question pour le moment.
        Veuillez réessayer plus tard ou consulter un professionnel de santé.
        """

# Base de connaissances médicales
MEDICAL_KNOWLEDGE = {
    "paludisme": {
        "symptômes": [
            "Fièvre élevée et irrégulière (jusqu'à 40°C)",
            "Frissons et sueurs froides",
            "Douleurs musculaires",
            "Fatigue intense",
            "Maux de tête",
            "Nausées et vomissements",
            "Dans les cas graves : confusion, convulsions, coma"
        ],
        "causes": [
            "Piqûre de moustique Anophèle infecté",
            "Parasite Plasmodium (principalement P. falciparum au Bénin)",
            "Transmission par le sang (rare)"
        ],
        "prévention": [
            "Utilisation de moustiquaires imprégnées",
            "Pulvérisation d'insecticide dans les maisons",
            "Élimination des eaux stagnantes",
            "Port de vêtements couvrants le soir",
            "Utilisation de répulsifs anti-moustiques"
        ],
        "centres": [
            "CNHU-HKM (Cotonou)",
            "Hôpital de la Mère et de l'Enfant (Cotonou)",
            "Hôpital de Zone de Porto-Novo",
            "Hôpital de Zone de Parakou",
            "Hôpital Saint Jean de Dieu (Natitingou)"
        ]
    },
    "grippe": {
        "symptômes": [
            "Fièvre soudaine",
            "Toux sèche",
            "Maux de gorge",
            "Écoulement nasal",
            "Fatigue",
            "Douleurs musculaires"
        ],
        "causes": [
            "Virus influenza",
            "Transmission par gouttelettes",
            "Contact avec des surfaces contaminées"
        ],
        "prévention": [
            "Vaccination annuelle",
            "Lavage fréquent des mains",
            "Port du masque en période d'épidémie",
            "Éviter les contacts avec les personnes malades"
        ],
        "centres": [
            "Tous les centres de santé primaires",
            "CNHU-HKM (Cotonou)",
            "Hôpital de Zone de Porto-Novo"
        ]
    }
}

# Titre de l'application
st.title("🤖 Assistant IA en Santé - Bénin")
st.markdown("""
    Bienvenue dans votre assistant IA spécialisé en santé au Bénin. Posez vos questions sur la santé,
    trouvez des hôpitaux près de chez vous, et prenez rendez-vous avec des médecins.
""")

# Initialisation de Google Maps
@st.cache_resource
def init_gmaps():
    return googlemaps.Client(key=os.getenv('GOOGLE_MAPS_API_KEY'))

# Création de la carte des hôpitaux
def create_hospitals_map():
    m = folium.Map(location=[9.3077, 2.3158], zoom_start=7)  # Centre sur le Bénin
    
    for hospital_id, data in bhd.get_all_hospitals().items():
        folium.Marker(
            location=[data['coordinates']['lat'], data['coordinates']['lng']],
            popup=f"{data['name']}<br>Spécialités: {', '.join(data['specialties'])}<br>Contact: {data['contact']}",
            tooltip=data['name']
        ).add_to(m)
    
    return m

def main():
    # Onglets pour différentes fonctionnalités
    tab1, tab2, tab3, tab4 = st.tabs(["Questions Santé", "Trouver un Centre de Santé", "Prendre Rendez-vous", "Assistant Médical"])
    
    with tab1:
        st.header("Posez vos questions sur la santé")
        user_question = st.text_area(
            "Votre question :",
            placeholder="Ex: Quels sont les symptômes du paludisme ? Comment prévenir le paludisme ?",
            height=100
        )
        
        if st.button("Obtenir une réponse"):
            if user_question:
                with st.spinner("Analyse en cours..."):
                    try:
                        response = generate_response(user_question)
                        
                        st.markdown("### Réponse :")
                        st.write(response)
                        st.warning("""
                            ⚠️ Important : Les informations fournies par cet assistant ne remplacent pas 
                            l'avis d'un professionnel de santé. Consultez toujours un médecin pour des 
                            problèmes de santé spécifiques.
                        """)
                    except Exception as e:
                        st.error(f"Une erreur est survenue : {str(e)}")
            else:
                st.warning("Veuillez poser une question.")
    
    with tab2:
        st.header("Trouver un centre de santé")
        col1, col2 = st.columns(2)
        
        with col1:
            city = st.text_input("Ville", placeholder="Ex: Cotonou")
            quartier = st.text_input("Quartier (optionnel)", placeholder="Ex: Akpakpa")
            facility_type = st.selectbox(
                "Type d'établissement",
                ["", "Public", "Privé"]
            )
        
        with col2:
            specialty = st.selectbox(
                "Spécialité (optionnel)",
                ["", "Général", "Cardiologie", "Pédiatrie", "Chirurgie", "Gynécologie", 
                 "Obstétrique", "Maternité", "Urgences"]
            )
        
        if st.button("Rechercher"):
            if city:
                try:
                    # Recherche des centres avec les critères spécifiés
                    facilities = bhd.search_facilities(
                        city=city,
                        quartier=quartier if quartier else None,
                        facility_type=facility_type if facility_type else None,
                        specialty=specialty if specialty else None
                    )
                    
                    if not facilities:
                        st.warning(f"Aucun centre de santé trouvé à {city}" + 
                                 (f" dans le quartier {quartier}" if quartier else "") +
                                 (f" de type {facility_type}" if facility_type else "") +
                                 (f" avec la spécialité {specialty}" if specialty else ""))
                    else:
                        st.write(f"Centres de santé trouvés :")
                        for name, data in facilities.items():
                            st.write(f"### {data['name']}")
                            st.write(f"- **Type:** {data['type']}")
                            st.write(f"- **Localisation:** {data['location']}, {data['quartier']}")
                            st.write(f"- **Spécialités:** {', '.join(data['specialties'])}")
                            st.write(f"- **Services:** {', '.join(data['services'])}")
                            st.write(f"- **Équipements:** {', '.join(data['equipements'])}")
                            st.write(f"- **Contact:** {data['contact']}")
                            st.write("")
                        
                        # Afficher la carte
                        st.header("Carte des centres de santé")
                        folium_static(create_hospitals_map())
                except Exception as e:
                    st.error(f"Une erreur est survenue : {str(e)}")
            else:
                st.warning("Veuillez entrer au moins une ville.")
    
    with tab3:
        st.header("Prendre un rendez-vous")
        
        # Sélection du centre de santé
        facilities = bhd.get_all_facilities()
        facility_id = st.selectbox(
            "Centre de santé",
            options=list(facilities.keys()),
            format_func=lambda x: facilities[x]['name']
        )
        
        if facility_id:
            # Sélection de la spécialité
            specialties = set()
            for doctor in bhd.get_doctors_by_facility(facility_id).values():
                specialties.add(doctor['specialty'])
            
            specialty = st.selectbox(
                "Spécialité",
                options=sorted(list(specialties))
            )
            
            # Sélection du médecin
            doctors = {
                name: data for name, data in bhd.get_doctors_by_facility(facility_id).items()
                if data['specialty'] == specialty
            }
            
            doctor_name = st.selectbox(
                "Médecin",
                options=list(doctors.keys())
            )
            
            # Sélection de la date
            min_date = datetime.now().date()
            max_date = min_date + timedelta(days=30)
            date = st.date_input(
                "Date du rendez-vous",
                min_value=min_date,
                max_value=max_date
            )
            
            # Sélection de l'heure
            if doctor_name and date:
                available_slots = bhd.get_available_slots(facility_id, doctor_name, date)
                time = st.selectbox(
                    "Heure du rendez-vous",
                    options=available_slots
                )
            
            # Informations du patient
            st.subheader("Informations du patient")
            patient_name = st.text_input("Nom complet")
            patient_phone = st.text_input("Numéro de téléphone")
            patient_email = st.text_input("Email (optionnel)")
            patient_birthdate = st.date_input("Date de naissance")
            patient_gender = st.selectbox("Genre", ["Homme", "Femme", "Autre"])
            
            # Motif de la consultation
            consultation_reason = st.text_area(
                "Motif de la consultation",
                placeholder="Décrivez brièvement la raison de votre consultation"
            )
            
            # Bouton de confirmation
            if st.button("Confirmer le rendez-vous"):
                if not all([patient_name, patient_phone, patient_birthdate, patient_gender]):
                    st.error("Veuillez remplir tous les champs obligatoires")
                else:
                    patient_info = {
                        "name": patient_name,
                        "phone": patient_phone,
                        "email": patient_email,
                        "birthdate": patient_birthdate,
                        "gender": patient_gender,
                        "reason": consultation_reason
                    }
                    
                    success, message = bhd.book_slot(
                        facility_id,
                        doctor_name,
                        date,
                        time,
                        patient_info
                    )
                    
                    if success:
                        st.success(f"""
                            Rendez-vous confirmé !
                            
                            Détails du rendez-vous :
                            - Centre : {facilities[facility_id]['name']}
                            - Médecin : {doctor_name} ({specialty})
                            - Date : {date.strftime('%d/%m/%Y')}
                            - Heure : {time}
                            
                            Informations patient :
                            - Nom : {patient_name}
                            - Contact : {patient_phone}
                            {f'- Email : {patient_email}' if patient_email else ''}
                            
                            Important :
                            - Veuillez arriver 15 minutes avant l'heure du rendez-vous
                            - Apportez votre carte d'identité et votre carnet de santé
                            - En cas d'annulation, merci de nous prévenir au moins 24h à l'avance
                        """)
                        
                        # Envoi de la confirmation par email si fourni
                        if patient_email:
                            # Ici, on pourrait ajouter la logique d'envoi d'email
                            st.info("Un email de confirmation vous a été envoyé")
                    else:
                        st.error(message)
    
    with tab4:
        st.header("Assistant Médical")
        
        # Zone de texte pour la question
        question = st.text_area(
            "Posez votre question sur la santé",
            placeholder="Exemple: Quels sont les symptômes du paludisme ?"
        )
        
        if question:
            # Générer la réponse avec le modèle
            response = generate_response(question)
            
            # Afficher la réponse
            st.markdown("### Réponse")
            st.markdown(response)
            
            # Avertissement standard
            st.warning("""
                ⚠️ Important : Les informations fournies par cet assistant ne remplacent pas l'avis d'un professionnel de santé. 
                Consultez toujours un médecin pour des problèmes de santé spécifiques.
            """)

if __name__ == "__main__":
    main() 