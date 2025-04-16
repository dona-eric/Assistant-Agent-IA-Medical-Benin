import json
import os
from typing import Dict, List, Optional
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

class HealthcareCenters:
    def __init__(self):
        self.centers = self._load_centers()
    
    def _load_centers(self) -> Dict:
        """Charge les données des centres de santé depuis un fichier JSON"""
        centers = {
            "public": {
                "CNHU": {
                    "name": "Centre National Hospitalier et Universitaire (CNHU)",
                    "type": "Public",
                    "location": "Cotonou",
                    "address": "Avenue Jean-Paul II, Cotonou",
                    "coordinates": {"lat": 6.3667, "lng": 2.4333},
                    "specialties": ["Général", "Urgences", "Maternité", "Pédiatrie", "Chirurgie"],
                    "contact": "+229 21 30 06 56",
                    "opening_hours": "24/7",
                    "website": "https://cnhu.bj"
                },
                "Hôpital Saint-Jean-de-Dieu": {
                    "name": "Hôpital Saint-Jean-de-Dieu",
                    "type": "Public",
                    "location": "Tanguiéta",
                    "address": "Tanguiéta",
                    "coordinates": {"lat": 10.6214, "lng": 1.2644},
                    "specialties": ["Général", "Urgences", "Maternité"],
                    "contact": "+229 23 83 00 11",
                    "opening_hours": "24/7"
                },
                "Hôpital d'Avougon": {
                    "name": "Hôpital d'Avougon",
                    "type": "Public",
                    "location": "Abomey",
                    "address": "A 5 km d'Abomey, sur la route de Lokossa",
                    "coordinates": {"lat": 7.1833, "lng": 1.9833},
                    "specialties": ["Général", "Urgences", "Maternité"],
                    "contact": "+229 22 50 00 61",
                    "opening_hours": "24/7"
                },
                "Hôpital Modulaire": {
                    "name": "Hôpital Modulaire",
                    "type": "Public",
                    "location": "Natitingou",
                    "address": "A l'entrée sud de la ville, après l'ENI",
                    "coordinates": {"lat": 10.3000, "lng": 1.3667},
                    "specialties": ["Général", "Urgences", "Maternité"],
                    "contact": "+229 23 82 13 32",
                    "opening_hours": "24/7"
                },
                "Centre Hospitalier Départemental Porto-Novo": {
                    "name": "Centre Hospitalier Départemental",
                    "type": "Public",
                    "location": "Porto-Novo",
                    "address": "Porto-Novo",
                    "coordinates": {"lat": 6.4965, "lng": 2.6036},
                    "specialties": ["Général", "Urgences", "Maternité"],
                    "contact": "+229 20 21 35 90",
                    "opening_hours": "24/7"
                },
                "Centre Hospitalier Départemental Parakou": {
                    "name": "Centre Hospitalier Départemental",
                    "type": "Public",
                    "location": "Parakou",
                    "address": "Quartier Titirou, Parakou",
                    "coordinates": {"lat": 9.3400, "lng": 2.6200},
                    "specialties": ["Général", "Urgences", "Maternité"],
                    "contact": "+229 23 61 07 21",
                    "opening_hours": "24/7"
                },
                "Centre Hospitalier Départemental Natitingou": {
                    "name": "Centre Hospitalier Départemental",
                    "type": "Public",
                    "location": "Natitingou",
                    "address": "Natitingou",
                    "coordinates": {"lat": 10.3000, "lng": 1.3667},
                    "specialties": ["Général", "Urgences", "Maternité"],
                    "contact": "+229 23 82 14 17",
                    "opening_hours": "24/7"
                },
                "Hôpital de Djougou": {
                    "name": "Hôpital de Djougou",
                    "type": "Public",
                    "location": "Djougou",
                    "address": "Sur la route de N'dali",
                    "coordinates": {"lat": 9.7000, "lng": 1.6667},
                    "specialties": ["Général", "Urgences", "Maternité"],
                    "contact": "+229 23 80 01 40",
                    "opening_hours": "24/7"
                },
                "Hôpital de Dassa-Zoumé": {
                    "name": "Hôpital",
                    "type": "Public",
                    "location": "Dassa-Zoumé",
                    "address": "Dassa-Zoumé",
                    "coordinates": {"lat": 7.7500, "lng": 2.1833},
                    "specialties": ["Général", "Urgences", "Maternité"],
                    "contact": "+229 22 53 00 31",
                    "opening_hours": "24/7"
                }
            },
            "private": {
                "Clinique Mahouna": {
                    "name": "Clinique Mahouna",
                    "type": "Privé",
                    "location": "Cotonou",
                    "address": "Rue 395 et place du Souvenir, Cotonou",
                    "coordinates": {"lat": 6.3667, "lng": 2.4333},
                    "specialties": ["Général", "Urgences", "Maternité"],
                    "contact": "+229 21 30 14 35",
                    "opening_hours": "24/7"
                },
                "Polyclinique La Roseraie": {
                    "name": "Polyclinique La Roseraie",
                    "type": "Privé",
                    "location": "Cotonou",
                    "address": "Sodjèatimè, Cotonou",
                    "coordinates": {"lat": 6.3667, "lng": 2.4333},
                    "specialties": ["Général", "Urgences", "Maternité"],
                    "contact": "+229 21 33 14 66",
                    "opening_hours": "24/7"
                },
                "Clinique Louis-Pasteur": {
                    "name": "Clinique Louis-Pasteur",
                    "type": "Privé",
                    "location": "Porto-Novo",
                    "address": "Sur la route d'Aguégué",
                    "coordinates": {"lat": 6.4965, "lng": 2.6036},
                    "specialties": ["Général", "Urgences", "Maternité"],
                    "contact": "+229 20 21 50 00",
                    "opening_hours": "24/7"
                },
                "Cabinet Dentaire Dr Bouhoun": {
                    "name": "Cabinet Dentaire Dr Bouhoun",
                    "type": "Privé",
                    "location": "Cotonou",
                    "address": "Cotonou",
                    "coordinates": {"lat": 6.3667, "lng": 2.4333},
                    "specialties": ["Dentaire"],
                    "contact": "+229 21 32 16 56",
                    "opening_hours": "8:00-18:00"
                }
            }
        }
        return centers
    
    def get_all_centers(self) -> Dict:
        """Retourne tous les centres de santé"""
        return self.centers
    
    def search_centers(self, 
                      location: Optional[str] = None,
                      center_type: Optional[str] = None,
                      specialty: Optional[str] = None) -> List[Dict]:
        """Recherche des centres selon les critères"""
        results = []
        
        for type_key, centers in self.centers.items():
            if center_type and type_key != center_type.lower():
                continue
                
            for center_id, center in centers.items():
                if location and location.lower() not in center['location'].lower():
                    continue
                    
                if specialty and specialty.lower() not in [s.lower() for s in center['specialties']]:
                    continue
                    
                results.append({
                    'id': center_id,
                    **center
                })
        
        return results
    
    def get_center_details(self, center_id: str) -> Optional[Dict]:
        """Récupère les détails d'un centre spécifique"""
        for centers in self.centers.values():
            if center_id in centers:
                return centers[center_id]
        return None
    
    def get_center_coordinates(self, center_id: str) -> Optional[Dict]:
        """Récupère les coordonnées d'un centre"""
        center = self.get_center_details(center_id)
        return center['coordinates'] if center else None
    
    def get_center_map_url(self, center_id: str) -> Optional[str]:
        """Génère l'URL OpenStreetMap pour un centre"""
        center = self.get_center_details(center_id)
        if not center:
            return None
            
        coords = center['coordinates']
        return f"https://www.openstreetmap.org/?mlat={coords['lat']}&mlon={coords['lng']}&zoom=15"
    
    def get_centers_by_location(self, location: str) -> List[Dict]:
        """Récupère tous les centres d'une localité"""
        return self.search_centers(location=location)
    
    def get_centers_by_type(self, center_type: str) -> List[Dict]:
        """Récupère tous les centres d'un type donné"""
        return self.search_centers(center_type=center_type)
    
    def get_centers_by_specialty(self, specialty: str) -> List[Dict]:
        """Récupère tous les centres ayant une spécialité donnée"""
        return self.search_centers(specialty=specialty) 