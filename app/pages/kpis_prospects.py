import os
from warnings import filters
from services.kpis_api import get_prospects_kpis
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

st.set_page_config(page_title="KPIs prospects", layout="wide")

from components.prospects_filters import render_prospects_filters
from services.prospects_api import list_prospects, search_prospects
from components.kpis import (
    pie_prospect, histo_adhérents, histo_followers, map_prospects,
    treemap_followers, bar_statuts, website_pie_chart, gauge_accepte_com,
    gauge_tel_manquants, gauge_mail_manquants, gauge_non_contactés
)

if not st.session_state.get("authenticated"):
    st.switch_page("main.py")

# ---------------------------------------------------------------------------------
### Petit CSS pour les titres et les valeurs des KPIs
# ---------------------------------------------------------------------------------
st.markdown("""
<style>
.kpi-title { font-size: 18px; font-weight: 600; }
.kpi-value { font-size: 34px; font-weight: 700; }
.block-container { padding-top: 1.5rem; }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------------------------------
### On charge les données de la BDD prospects via l'API
# ---------------------------------------------------------------------------------


placeholder_map = Path(__file__).parent.parent / 'components' / 'map_placeholder.jpg'



# ---------------------------------------------------------------------------------
def interface_bdd():
    
    st.title("KPIs des prospects")
    # Ici on va créer l'interface de la BDD avec les différents filtres
    # On créé pour commencer deux containers afin de centrer le contenu de la page et le rendre dézoomable au besoin
    # Le premier container est stretch pour prendre toute la largeur de l'écran et mettre le second au centre
    with st.container(border=False, width='stretch', horizontal_alignment="center", vertical_alignment="center"):
        # Le second container est centré avec une largeur fixe
        with st.container(border=False, width=1485, horizontal_alignment="center", vertical_alignment="center"):
            # Titre principal de la page
            st.markdown("<h2>Filtres</h2>", unsafe_allow_html=True) ## Créer un CSS center pour les titles

# Ajout des filtres de la BDD

            filters = render_prospects_filters(
                key="bdd", 
                fields=["nom", "type_prospect", "region", "departement", "nb_aderents", "followers_total", "email", "telephone", "sit_web", "statut", "accepte_contact"],
                show_sort=False,
            )
            
            if filters:
                data, err = search_prospects(**filters)
            else:
                data, err = list_prospects()

            if err:
                st.error(err.get("message", "Erreur chargement prospects"))
                st.stop()

            data = pd.DataFrame(data or [])

            if data.empty:
                st.warning("Aucune donnée de prospects disponible.")
                return
            kpis, err = get_prospects_kpis(**filters)

            if err:
                st.error(err)
                st.stop()
# ---------------------------------------------------------------------------------
### KPIS BDD
# ---------------------------------------------------------------------------------
            # On sort du container des filtres pour passer aux KPIs de la BDD
            # On va découper les KPIs en trois containers :
            # 1 = prospects/adhérents/followers
            # 2 = statuts/website
            # 3 = Com, contactés, tel
            
            # 1er container KPIs : prospects/adhérents/followers
            with st.container(height='stretch', vertical_alignment="center"):
                # Afin de centrer au mieux le contenu conformément aux maquettes on utilise deux colonnes dont la première sera split en deux
                numeric_values_and_graphs, map_tree = st.columns([6,4])
                with numeric_values_and_graphs:
                    # Dans cette colonne on va faire 3 containers avec deux colonnes chacun (ratio 1/2)
                    # Cela nous permet de centrer les valeurs numériques et les graphes associés
                    
                    # premier num/graph : nb prospects subset + camembert prospects
                    with st.container(height='stretch', vertical_alignment="center"):
                        num1, graph1 = st.columns([1,2]) # pas de base 10 ici car division par 3
                        with num1: # Nombre de prospects (en assignant des classes css)
                            with st.container(height='stretch', vertical_alignment="center"):
                                st.markdown("<h3 class='kpi-title' style='text-align: center;'>Nombre de prospects</h3>", unsafe_allow_html=True)
                                total_prospects =  len(data)
                                st.markdown(f"<h3 class='kpi-value' style='text-align: center;'>{total_prospects}</h3>", unsafe_allow_html=True)
                        with graph1: # Camembert répartition types de prospects
                            pie_prospect(kpis)
                    
                    # deuxième num/graph : nb adhérents subset + histo répartition du nb d'adhérents
                    with st.container(height='stretch', vertical_alignment="center"):
                        num2, graph2 = st.columns([1,2]) # pas de base 10 ici car division par 3
                        with num2: # Nombre d'adhérents (en assignant des classes css)
                            with st.container(height='stretch', vertical_alignment="center"):
                                st.markdown("<h3 class='kpi-title' style='text-align: center;'>Nombre d'adhérents</h3>", unsafe_allow_html=True)
                                total_adherents = data['nb_aderents'].sum()
                                st.markdown(f"<h3 class='kpi-value' style='text-align: center;'>{total_adherents}</h3>", unsafe_allow_html=True)
                        with graph2: # Histogramme répartition du nb d'adhérents
                            histo_adhérents(kpis) # On utilise l'histogramme des adhérents qu'on définira dans kpis.py
                    
                    # troisième num/graph : nb followers subset + histo répartition du nb de followers
                    with st.container(height='stretch', vertical_alignment="center"):
                        num3, graph3 = st.columns([1,2]) # pas de base 10 ici car division par 3
                        with num3: # Nombre de followers (en assignant des classes css)
                            with st.container(height='stretch', vertical_alignment="center"):
                                st.markdown("<h3 class='kpi-title' style='text-align: center;'>Nombre de followers</h3>", unsafe_allow_html=True)
                                followers_columns = ['facebook_followers', 'x_followers', 'instagram_followers', 'youtube_followers', 'tictok_followers']
                                data_followers = data[followers_columns].fillna(0)
                                max_followers = data_followers.max(axis=1)
                                total_followers = max_followers.sum()
                                st.markdown(f"<h3 class='kpi-value' style='text-align: center;'>{total_followers}</h3>", unsafe_allow_html=True)
                        with graph3: # Histogramme répartition du nb de followers    
                            histo_followers(kpis) # On utilise l'histogramme des followers qu'on définira dans kpis.py
                
                with map_tree:
                    # Ici on intégrera la carte avec répartition des prospects sur le territoire et le treemap de la répartition des followers par réseaux sociaux
                    # On commence par le container de la map
                    with st.container(height='stretch', width='stretch', vertical_alignment="center"):
                        map_prospects(data) # On utilise la carte des prospects qu'on définira dans kpis.py
                    
                    # Ensuite on crée le container du treemap
                    with st.container(height='stretch', vertical_alignment="center"):
                        treemap_followers(kpis) # On utilise le treemap des followers qu'on définira dans kpis.py
            
            # 2e container KPIs : statuts/nombre site webs
            with st.container(height='stretch', vertical_alignment="center"):
                # Ici on aura également besoin de deux colonnes
                repr_statuts, website_pie = st.columns([6,4])
                with repr_statuts:
                    st.markdown("<h3 class='kpi-title' style='text-align: center;'>Répartition des statuts des prospects</h3>", unsafe_allow_html=True)
                    with st.container(height='stretch', vertical_alignment="center"):
                        
                        bar_statuts(kpis) # On utilise le bar chart des statuts qu'on définira dans kpis.py

                # colonne website_pie 
                with website_pie:
                    st.markdown("<h3 class='kpi-title' style='text-align: center;'>Prospects ayant un site web</h3>", unsafe_allow_html=True)
                    with st.container(height='stretch', vertical_alignment="center"):
                        
                        website_pie_chart(kpis) # On utilise le pie chart du nombre de sites webs qu'on définira dans kpis.py
            
            # 3e container KPIs : Com, contactés, tel, website
            with st.container(height='stretch', vertical_alignment="center"):
                # On créé 4 colonnes de taille égale pour chaque KPI
                com, contactés, tel_manquants, mail_manquants = st.columns(4)
                
                # Première colonne : Nombre prospects qui acceptent la com + jauge du %
                with com :
                    with st.container(height='stretch', vertical_alignment="center"):
                        total_accepte_com = int(data[data['accepte_contact'] == True].shape[0])
                        st.markdown(f"<h3 class='kpi-value' style='text-align: center;'>Total des prospects acceptant la com :<br>{total_accepte_com}</h3>", unsafe_allow_html=True)
                    with st.container(height='stretch', vertical_alignment="center"):
                        gauge_accepte_com(kpis) # On utilise la jauge du taux d'acceptation com qu'on définira dans kpis.py

                # Deuxième colonne : Nombre de prospects jamais contactés + jauge du %
                with contactés:
                    with st.container(height='stretch', vertical_alignment="center"):
                        total_non_contactés = int(data[data['contacte'] == False].shape[0])
                        st.markdown(f"<h3 class='kpi-value' style='text-align: center;'>Total des prospects non contactés :<br>{total_non_contactés}</h3>", unsafe_allow_html=True)
                    with st.container(height='stretch', vertical_alignment="center"):
                        gauge_non_contactés(kpis) # On utilise la jauge du taux de non contactés qu'on définira dans kpis.py

                # Troisième colonne : Nombre de prospects sans téléphone + jauge du %
                with tel_manquants:
                    with st.container(height='stretch', vertical_alignment="center"):
                        total_tel_manquants = int(data['telephone'].isnull().sum())
                        st.markdown(f"<h3 class='kpi-value' style='text-align: center;'>Total des prospects sans téléphone :<br>{total_tel_manquants}</h3>", unsafe_allow_html=True)
                    with st.container(height='stretch', vertical_alignment="center"):
                        gauge_tel_manquants(kpis) # On utilise la jauge du taux de prospects sans téléphone qu'on définira dans kpis.py

                # Quatrième colonne : Nombre de prospects sans email + jauge du %
                with mail_manquants:
                    with st.container(height='stretch', vertical_alignment="center"):
                        total_mail_manquants = int(data['email'].isnull().sum())
                        st.markdown(f"<h3 class='kpi-value' style='text-align: center;'>Total des prospects sans email :<br>{total_mail_manquants}</h3>", unsafe_allow_html=True)
                    with st.container(height='stretch', vertical_alignment="center"):
                        gauge_mail_manquants(kpis) # On utilise la jauge du taux de prospects sans email qu'on définira dans kpis.py
                        
interface_bdd()