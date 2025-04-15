import pandas as pd
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv

# Charger les variables d'environnement depuis le fichier .env
load_dotenv()

# Configuration de l'email
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
EMAIL_USERNAME = os.getenv("EMAIL_USERNAME")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")

# Données des centres de santé au Bénin
HEALTHCARE_FACILITIES = {
    # Cotonou
    "CNHU-HKM": {
        "name": "Centre National Hospitalier et Universitaire Hubert K. Maga",
        "location": "Cotonou",
        "quartier": "Akpakpa",
        "coordinates": {"lat": 6.3667, "lng": 2.4333},
        "type": "Public",
        "specialties": ["Général", "Cardiologie", "Pédiatrie", "Chirurgie", "Urgences", "Maternité"],
        "contact": "+229 21 30 30 31",
        "services": ["Consultation", "Hospitalisation", "Urgences 24/7", "Laboratoire", "Radiologie"],
        "equipements": ["Scanner", "IRM", "Bloc opératoire", "Laboratoire d'analyses"]
    },
    "Hôpital de la Mère et de l'Enfant": {
        "name": "Hôpital de la Mère et de l'Enfant Lagune",
        "location": "Cotonou",
        "quartier": "Cadjèhoun",
        "coordinates": {"lat": 6.3667, "lng": 2.4333},
        "type": "Public",
        "specialties": ["Pédiatrie", "Gynécologie", "Obstétrique", "Maternité"],
        "contact": "+229 21 30 30 32",
        "services": ["Consultation", "Hospitalisation", "Accouchement", "Vaccination"],
        "equipements": ["Échographe", "Salle d'accouchement", "Couveuse"]
    },
    "Clinique la Croix": {
        "name": "Clinique la Croix",
        "location": "Cotonou",
        "quartier": "Ganhi",
        "coordinates": {"lat": 6.3667, "lng": 2.4333},
        "type": "Privé",
        "specialties": ["Général", "Maternité", "Pédiatrie"],
        "contact": "+229 21 31 31 31",
        "services": ["Consultation", "Hospitalisation", "Accouchement"],
        "equipements": ["Échographe", "Laboratoire"]
    },

    # Porto-Novo
    "Hôpital de Zone de Porto-Novo": {
        "name": "Hôpital de Zone de Porto-Novo",
        "location": "Porto-Novo",
        "quartier": "Centre",
        "coordinates": {"lat": 6.4969, "lng": 2.6289},
        "type": "Public",
        "specialties": ["Général", "Maternité", "Pédiatrie", "Chirurgie"],
        "contact": "+229 20 21 21 21",
        "services": ["Consultation", "Hospitalisation", "Urgences"],
        "equipements": ["Bloc opératoire", "Laboratoire"]
    },

    # Parakou
    "Hôpital de Zone de Parakou": {
        "name": "Hôpital de Zone de Parakou",
        "location": "Parakou",
        "quartier": "Centre",
        "coordinates": {"lat": 9.3500, "lng": 2.6167},
        "type": "Public",
        "specialties": ["Général", "Maternité", "Pédiatrie", "Chirurgie"],
        "contact": "+229 23 61 11 11",
        "services": ["Consultation", "Hospitalisation", "Urgences"],
        "equipements": ["Bloc opératoire", "Laboratoire"]
    },

    # Natitingou
    "Hôpital Saint Jean de Dieu": {
        "name": "Hôpital Saint Jean de Dieu",
        "location": "Natitingou",
        "quartier": "Centre",
        "coordinates": {"lat": 10.3000, "lng": 1.3667},
        "type": "Public",
        "specialties": ["Général", "Pédiatrie", "Chirurgie", "Maternité"],
        "contact": "+229 23 84 00 00",
        "services": ["Consultation", "Hospitalisation", "Urgences"],
        "equipements": ["Bloc opératoire", "Laboratoire"]
    },

    # Abomey-Calavi
    "Centre de Santé d'Abomey-Calavi": {
        "name": "Centre de Santé d'Abomey-Calavi",
        "location": "Abomey-Calavi",
        "quartier": "Centre",
        "coordinates": {"lat": 6.4500, "lng": 2.3500},
        "type": "Public",
        "specialties": ["Général", "Maternité", "Pédiatrie"],
        "contact": "+229 21 36 00 00",
        "services": ["Consultation", "Vaccination", "Planning familial"],
        "equipements": ["Laboratoire de base"]
    }
}

# Données des médecins et leurs disponibilités
DOCTORS_DATA = {
    "CNHU-HKM": {
        "Dr. Koffi": {
            "specialty": "Cardiologie",
            "schedule": {
                "lundi": ["09:00", "10:00", "11:00", "14:00", "15:00"],
                "mercredi": ["09:00", "10:00", "11:00", "14:00", "15:00"],
                "vendredi": ["09:00", "10:00", "11:00", "14:00", "15:00"]
            }
        },
        "Dr. Adjo": {
            "specialty": "Pédiatrie",
            "schedule": {
                "mardi": ["09:00", "10:00", "11:00", "14:00", "15:00"],
                "jeudi": ["09:00", "10:00", "11:00", "14:00", "15:00"]
            }
        }
    },
    "Hôpital de la Mère et de l'Enfant": {
        "Dr. Yawa": {
            "specialty": "Gynécologie",
            "schedule": {
                "lundi": ["09:00", "10:00", "11:00", "14:00", "15:00"],
                "mercredi": ["09:00", "10:00", "11:00", "14:00", "15:00"]
            }
        }
    }
}

# Dictionnaire pour stocker les rendez-vous pris
APPOINTMENTS = {}

# Mapping des jours de la semaine
DAY_MAPPING = {
    "Monday": "lundi",
    "Tuesday": "mardi",
    "Wednesday": "mercredi",
    "Thursday": "jeudi",
    "Friday": "vendredi",
    "Saturday": "samedi",
    "Sunday": "dimanche"
}

def send_confirmation_email(patient_email, appointment_details):
    if not patient_email:
        return False, "Email non fourni"
    
    try:
        # Création du message
        msg = MIMEMultipart()
        msg['From'] = EMAIL_USERNAME
        msg['To'] = patient_email
        msg['Subject'] = "Confirmation de votre rendez-vous médical"
        
        # Corps du message
        body = f"""
        Bonjour {appointment_details['patient_info']['name']},
        
        Votre rendez-vous a été confirmé avec succès.
        
        Détails du rendez-vous :
        - Centre : {HEALTHCARE_FACILITIES[appointment_details['facility_id']]['name']}
        - Médecin : {appointment_details['doctor_name']}
        - Date : {appointment_details['date'].strftime('%d/%m/%Y')}
        - Heure : {appointment_details['time']}
        
        Important :
        - Veuillez arriver 15 minutes avant l'heure du rendez-vous
        - Apportez votre carte d'identité et votre carnet de santé
        - En cas d'annulation, merci de nous prévenir au moins 24h à l'avance
        
        Cordialement,
        L'équipe de gestion des rendez-vous
        """
        
        msg.attach(MIMEText(body, 'plain'))
        
        # Connexion au serveur SMTP
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(EMAIL_USERNAME, EMAIL_PASSWORD)
        
        # Envoi de l'email
        server.send_message(msg)
        server.quit()
        
        return True, "Email de confirmation envoyé avec succès"
    except Exception as e:
        return False, f"Erreur lors de l'envoi de l'email : {str(e)}"

# Fonction pour obtenir les centres par ville
def get_facilities_by_city(city):
    return {name: data for name, data in HEALTHCARE_FACILITIES.items() 
            if city.lower() in data['location'].lower()}

# Fonction pour obtenir les centres par quartier
def get_facilities_by_quartier(quartier):
    return {name: data for name, data in HEALTHCARE_FACILITIES.items() 
            if quartier.lower() in data['quartier'].lower()}

# Fonction pour obtenir les centres par type (public/privé)
def get_facilities_by_type(facility_type):
    return {name: data for name, data in HEALTHCARE_FACILITIES.items() 
            if facility_type.lower() in data['type'].lower()}

# Fonction pour obtenir les centres par spécialité
def get_facilities_by_specialty(specialty):
    return {name: data for name, data in HEALTHCARE_FACILITIES.items() 
            if specialty.lower() in [s.lower() for s in data['specialties']]}

# Fonction pour obtenir tous les centres
def get_all_facilities():
    return HEALTHCARE_FACILITIES

# Fonction pour rechercher des centres avec plusieurs critères
def search_facilities(city=None, quartier=None, facility_type=None, specialty=None):
    results = HEALTHCARE_FACILITIES
    
    if city:
        results = {k: v for k, v in results.items() 
                  if city.lower() in v['location'].lower()}
    
    if quartier:
        results = {k: v for k, v in results.items() 
                  if quartier.lower() in v['quartier'].lower()}
    
    if facility_type:
        results = {k: v for k, v in results.items() 
                  if facility_type.lower() in v['type'].lower()}
    
    if specialty:
        results = {k: v for k, v in results.items() 
                  if specialty.lower() in [s.lower() for s in v['specialties']]}
    
    return results 

# Fonction pour obtenir les médecins d'un centre
def get_doctors_by_facility(facility_id):
    return DOCTORS_DATA.get(facility_id, {})

# Fonction pour obtenir les créneaux disponibles
def get_available_slots(facility_id, doctor_name, date):
    doctor = DOCTORS_DATA.get(facility_id, {}).get(doctor_name)
    if not doctor:
        return []
    
    # Convertir la date en jour de la semaine en français
    day_name = DAY_MAPPING[date.strftime("%A")]
    
    # Récupérer tous les créneaux du jour
    all_slots = doctor["schedule"].get(day_name, [])
    
    # Filtrer les créneaux déjà pris
    taken_slots = set()
    for appointment in APPOINTMENTS.values():
        if (appointment["facility_id"] == facility_id and 
            appointment["doctor_name"] == doctor_name and 
            appointment["date"] == date):
            taken_slots.add(appointment["time"])
    
    return [slot for slot in all_slots if slot not in taken_slots]

# Fonction pour vérifier la disponibilité d'un créneau
def is_slot_available(facility_id, doctor_name, date, time):
    available_slots = get_available_slots(facility_id, doctor_name, date)
    return time in available_slots

# Fonction pour réserver un créneau
def book_slot(facility_id, doctor_name, date, time, patient_info):
    if not is_slot_available(facility_id, doctor_name, date, time):
        return False, "Créneau non disponible"
    
    # Générer un ID unique pour le rendez-vous
    appointment_id = f"{facility_id}_{doctor_name}_{date}_{time}"
    
    # Enregistrer le rendez-vous
    appointment_details = {
        "facility_id": facility_id,
        "doctor_name": doctor_name,
        "date": date,
        "time": time,
        "patient_info": patient_info
    }
    APPOINTMENTS[appointment_id] = appointment_details
    
    # Envoyer l'email de confirmation si l'email est fourni
    if patient_info.get("email"):
        email_success, email_message = send_confirmation_email(
            patient_info["email"],
            appointment_details
        )
        if not email_success:
            return True, f"Rendez-vous confirmé mais {email_message}"
    
    return True, "Rendez-vous confirmé"

# Fonction pour annuler un rendez-vous
def cancel_appointment(appointment_id):
    if appointment_id in APPOINTMENTS:
        del APPOINTMENTS[appointment_id]
        return True, "Rendez-vous annulé avec succès"
    return False, "Rendez-vous non trouvé"

# Fonction pour obtenir les rendez-vous d'un patient
def get_patient_appointments(patient_phone):
    return {
        id: appointment for id, appointment in APPOINTMENTS.items()
        if appointment["patient_info"]["phone"] == patient_phone
    } 