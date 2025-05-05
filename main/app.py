import streamlit as st
import folium, os,sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.agent.agent import MedicalAgent
from healthcare_centers import HealthcareCenters
from streamlit_folium import folium_static



# Configuration de la page
st.set_page_config(
    page_title="Assistant Médical Bénin",
    page_icon="🏥",
    layout="wide"
)

# Titre de l'application
st.title("🤖 Assistant IA en Santé - Bénin")
st.markdown("""
    Bienvenue dans votre assistant IA spécialisé en santé au Bénin. 
    Posez vos questions sur la santé et trouvez les centres de santé près de chez vous.
""")

# Initialisation des services
@st.cache_resource
def get_medical_agent():
    return MedicalAgent()

@st.cache_resource
def get_healthcare_centers():
    return HealthcareCenters()

# Création des onglets
tab1, tab2, tab3= st.tabs(["Assistant Médical", "Centres de Santé", "Prendre Rendez-vous"])

with tab1:
    st.header("Assistant Médical")
    
    # Zone de texte pour la question
    question = st.text_area(
        "Posez votre question sur la santé :",
        placeholder="Exemple: Quels sont les symptômes du paludisme ? Comment prévenir le paludisme ?",
        height=100
    )
        
    # Bouton pour obtenir une réponse
    if st.button("Obtenir une réponse"):
        if question:
            with st.spinner("Analyse en cours..."):
                try:
                    agent = get_medical_agent()
                    response = agent.chat(question)
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
    st.header("Recherche de Centres de Santé")
    
    # Filtres de recherche
    col1, col2, col3 = st.columns(3)
        
    with col1:
        location = st.text_input("Ville", placeholder="Ex: Cotonou")
    
    with col2:
        center_type = st.selectbox(
            "Type d'établissement",
            ["Hopital", "Clinique", "Pharmarcie", "Centre de santé", "Laboratoire", "Cabinet Médical"],
        )
        
    with col3:
        specialty = st.selectbox(
            "Spécialité",
            ["", "Général", "Cardiologie", "Pédiatrie", "Chirurgie", "Gynécologie", 
             "Obstétrique", "Maternité", "Urgences"]
        )
        
    # Bouton de recherche
    if st.button("Rechercher"):
        healthcare_centers = get_healthcare_centers()
        results = healthcare_centers.search_centers(
            location=location if location else None,
            center_type=center_type if center_type else None,
            specialty=specialty if specialty else None
        )
        
        if not results:
            st.warning("Aucun centre de santé trouvé avec ces critères.")
        else:
            # Afficher les résultats
            for center in results:
                with st.expander(f"🏥 {center['name']}"):
                    st.write(f"**Type:** {center['type']}")
                    st.write(f"**Localisation:** {center['location']}")
                    st.write(f"**Adresse:** {center['address']}")
                    st.write(f"**Spécialités:** {', '.join(center['specialties'])}")
                    st.write(f"**Contact:** {center['contact']}")
                    if 'website' in center:
                        st.write(f"**Site web:** {center['website']}")
                    
                    # Afficher la carte
                    map_url = healthcare_centers.get_center_map_url(center['id'])
                    if map_url:
                        st.markdown(f"[Voir sur Google Maps]({map_url})")
                        
                        # Créer une carte Folium
                        m = folium.Map(
                            location=[center['coordinates']['lat'], center['coordinates']['lng']],
                            zoom_start=15
                        )
                        folium.Marker(
                            [center['coordinates']['lat'], center['coordinates']['lng']],
                            popup=center['name'],
                            tooltip=center['name']
                        ).add_to(m)
                        folium_static(m) 