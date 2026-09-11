# Classes AMNS Physique — laboratoire interactif

Application Streamlit interactive pour les classes AMNS Physique, avec un
laboratoire d'optique géométrique et une page de cercle trigonométrique.
Le dépôt inclut une page indépendante de cercle trigonométrique accessible
depuis la navigation multi-pages de Streamlit.

## Lancer en local

```bash
pip install -r requirements.txt
streamlit run app.py
```

Ensuite, ouvrez la barre latérale Streamlit pour naviguer entre :
- la page principale d'optique géométrique ;
- la page **Cercle Trigonométrique Réactif**.

## Déployer sur Streamlit Community Cloud

1. Poussez ce dépôt sur GitHub.
2. Dans [Streamlit Community Cloud](https://share.streamlit.io/), sélectionnez le dépôt.
3. Choisissez la branche `main` et le fichier d'entrée `app.py`.
4. Cliquez sur **Deploy**.

Les dépendances sont installées automatiquement depuis `requirements.txt`.