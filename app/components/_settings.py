import streamlit as st
from services.auth_api import auth_update
import time

# ------------------------------------------------------------
# SETTINGS (Modification Identifiants)
# ------------------------------------------------------------

def settings():
    # On affiche directement le formulaire 
    st.subheader("Modifier les identifiants")
    
    with st.form("Settings_form"):
        st.info("Saisissez vos identifiants actuels pour valider.")
        old_user = st.text_input("Identifiant actuel")
        old_pass = st.text_input("Mot de passe actuel", type="password")
        st.divider()
        new_user = st.text_input("Nouvel identifiant")
        new_pass = st.text_input("Nouveau mot de passe", type="password")
        
        col_btn1, col_btn2 = st.columns(2)
        with col_btn1:
            submit = st.form_submit_button("Mettre à jour", use_container_width=True)
        with col_btn2:
            cancel = st.form_submit_button("Annuler", use_container_width=True)

    if cancel:
        st.session_state.bdd_mode = "list"
        st.rerun()

    if submit:
        if not (old_user and old_pass and new_user and new_pass):
            st.error("Tous les champs sont obligatoires.")
        else:
            # Appel de la fonction avec arguments définis dans auth.py
            success_data, err = auth_update(
                current_username=old_user, 
                current_password=old_pass, 
                new_username=new_user, 
                new_password=new_pass
            )
            
            # Dans votre service request, le succès est confirmé si success_data n'est pas None
            if success_data is not None:
                st.success("Identifiants mis à jour !")
                time.sleep(2)
                st.session_state.clear()
                st.switch_page("main.py")
            else:
                # On cherche d'abord 'detail' (standard API), puis 'message'
                if err:
                    msg = err.get("detail") or err.get("message") or "Erreur inconnue"
                else:
                    msg = "Le serveur ne répond pas"
                
                st.error(f"❌ {msg}")