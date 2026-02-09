# ---------------------------------------------------------------------------------
### Options de filtrage
# ---------------------------------------------------------------------------------
            # Options de filtrage 
            # Je créé un container avec un contour pour les filtres
            with st.container(border=True):
                st.subheader("Filtres de recherche")
                # Filtres principaux (nom, type, région, dpt)
                # Pour toutes mes colonnes de filtres je me suis mit sur une base 10 pour faciliter les ratios en faisant en sorte que les champs soit en base 1
                Fil1, F1, Fil2, F2, Fil3, F3, Fil4, F4, Fil5 = st.columns([1.2,1,1.2,1,1.2,1,1.2,1,1.2])
                with F1:
                    # Il nous faudra créer une liste des prospects à partir de la BDD
                    prospects_list = ["Tout"] + data["Nom"].unique().tolist()
                    nom_prospect = st.selectbox("Nom du prospect", options=prospects_list, key="filtre_nom")
                    st.write("<br>", unsafe_allow_html=True)
                with F2:
                    # Il nous faudra créer une liste des types de prospects à partir de la BDD
                    type_list = ["Tout"] + data["Type"].unique().tolist()
                    type_prospect = st.selectbox("Type de prospect", options=type_list, key="filtre_type")
                    st.write("<br>", unsafe_allow_html=True)
                with F3:
                    # Il nous faudra créer une liste des régions à partir de la BDD
                    region_list = ["Tout"] + data["Region"].unique().tolist()
                    region_prospect = st.selectbox("Region", options=region_list, key="filtre_region")
                    st.write("<br>", unsafe_allow_html=True)
                with F4:
                    # Il nous faudra créer une liste des départements à partir de la BDD
                    dpt_list = ["Tout"] + data["Departement"].unique().tolist()
                    dpt_prospect = st.selectbox("Departement", options=dpt_list, key="filtre_dpt")
                    st.write("<br>", unsafe_allow_html=True)
                
                
                st.write("<br>", unsafe_allow_html=True)
                st.write("---", unsafe_allow_html=True) # ligne de séparation interfiltres
                
                
                # Filtres de rang 2 : adhérents
                # Sur une première ligne on ajoute les filtres nb adhérents et nb followers
                Fill1, FAd1, Fill2, FAd2, Fill3 = st.columns([3.5,1,1,1,3.5])
                # J'ai créé de manière arbitraire les intervalles de sélection pour les adhérents et followers, on peut le changer
                with FAd1:
                    nb_adh_prospect = st.selectbox("Nombre d'adhérents", options=["0-100", "100-500", "500-1.000", "1000+"], key="filtre_nb_adh")
                    st.write("<br>", unsafe_allow_html=True)
                with FAd2:
                    nb_followers_total_prospect = st.selectbox("Nombre de followers", options=["0-100", "100-500", "500-1.000", "1.000-10.000", "10.000+"], key="filtre_nb_followers")
                    st.write("<br>", unsafe_allow_html=True)
                
                #Sur une deuxième ligne on ajoute les filtres par réseaux sociaux
                # Adh FB, adh Twitter, adh Insta, adh YT, adh TikTok
                Fill2_1, FAd2_1, Fill2_2, FAd2_2, Fill2_3, FAd2_3, Fill2_4, FAd2_4, Fill2_5, FAd2_5, Fill2_6 = st.columns([1.5,1,0.5,1,0.5,1,0.5,1,0.5,1,1.5])
                with FAd2_1:
                    adhérents_fb = st.number_input("Adhérents Facebook (mini)", key="filtre_adh_fb")
                    st.write("<br>", unsafe_allow_html=True)
                with FAd2_2:
                    adhérents_twitter = st.number_input("Adhérents Twitter (mini)", key="filtre_adh_twitter")
                    st.write("<br>", unsafe_allow_html=True)
                with FAd2_3:
                    adhérents_insta = st.number_input("Adhérents Instagram (mini)", key="filtre_adh_insta")
                    st.write("<br>", unsafe_allow_html=True)
                with FAd2_4:
                    adhérents_yt = st.number_input("Adhérents YouTube (mini)", key="filtre_adh_yt")
                    st.write("<br>", unsafe_allow_html=True)
                with FAd2_5:
                    adhérents_tiktok = st.number_input("Adhérents TikTok (mini)", key="filtre_adh_tiktok")
                    st.write("<br>", unsafe_allow_html=True)


                st.write("<br>", unsafe_allow_html=True)
                st.write("---", unsafe_allow_html=True) # ligne de séparation interfiltres


                # Filtres de rang 3 : sélection sur les prospects ayant les champs remplis :
                # Sur une première ligne : Mail, Tel, Website
                Filler1, FSub1, Filler2, FSub2, Filler3, FSub3, Filler4 = st.columns([1.75,1,1.75,1,1.75,1,1.75])
                with FSub1:
                    mail_prospect = st.selectbox("Email", options=["Oui", "Non", "Tout"], key="filtre_mail")
                    st.write("<br>", unsafe_allow_html=True)
                with FSub2:
                    tel_prospect = st.selectbox("Téléphone", options=["Oui", "Non", "Tout"], key="filtre_tel")
                    st.write("<br>", unsafe_allow_html=True)
                with FSub3:
                    website_prospect = st.selectbox("Site Web", options=["Oui", "Non", "Tout"], key="filtre_website")
                    st.write("<br>", unsafe_allow_html=True)
                
                # Sur une deuxième ligne : Status, Accepte com 
                Filler2_1, FSub2_1, Filler2_2, FSub2_2, Filler2_3 = st.columns([3.5,1,1,1,3.5])
                with FSub2_1:
                    # On créé la liste des statuts à partir de la BDD
                    statut_list = ["Tout"] + data["Statut"].unique().tolist()
                    status_propect = st.selectbox("Status", options=statut_list, key="filtre_status", ) # Il faudra créer status list avec status.unique_values()
                    st.write("<br>", unsafe_allow_html=True)
                with FSub2_2:
                    prospect_accepte_com = st.selectbox("Accepte com", options=["Oui", "Non", "Tout"], key="filtre_accepte_com")
                    st.write("<br>", unsafe_allow_html=True)
                
                st.write("<br><br>", unsafe_allow_html=True) # Espacement avant boutons valider / reset

                # Boutons de filtrage et réinitialisation
                filter_col1, filer, filter_col2 = st.columns([2,6,2])
                with filter_col1: # Bouton de filtrage
                    if st.button("Filtrer", width='stretch', key="filter_but"):
                        # On intègrera ici la fonction de filtrage de la BDD en fonction des key plus haut
                        # ex : if filtre_nom != "Tout":
                            # temp_bdd_filtre = temp_bdd_filtre[temp_bdd_filtre["nom"].astype(str).str.contains(filtre_nom, case=False, na=False, regex=False)]
                        # peut être qu'on aura besoin de faire du st.session_state pour garder les valeurs des filtres, mais pas sûr
                        st.rerun() # Pour appliquer les filtres dès le clic
                
                with filter_col2: # Bouton de reset
                    if st.button("Réinitialiser les filtres", width='stretch', key="reset_but"):
                        # On utilise une variable session_state pour indiquer le reset des filtres
                        # Il faudra par la suite intégrer en haut de la fonction que les valeurs se remettent par défaut si session_state.reset_triggered est True
                        st.session_state.reset_triggered = True 
                        st.rerun() # On recharge la page pour appliquer le reset