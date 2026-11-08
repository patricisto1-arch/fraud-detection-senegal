# Détection de fraude bancaire par Machine Learning

> Prototype de détection automatique des transactions suspectes, avec application interactive et simulateur de gain, conçu pour être **réentraîné sur les données de votre structure** (banque, fintech, opérateur de mobile money).

Projet réalisé au **Dakar Institute of Technology (DIT)** par **Patrice Dione** et **Mame Faty Dieng**. Présenté au Demo Day DIT 2026.

---

## Le problème

La fraude sur les paiements électroniques coûte cher aux institutions financières et aux opérateurs de paiement mobile, en argent comme en confiance client. Les règles manuelles ne suivent pas l'évolution des schémas frauduleux, et la fraude est **extrêmement rare** par rapport aux transactions normales : un système qui ne détecterait rien paraîtrait pourtant exact à plus de 99 %.

## La solution

Une chaîne complète, de la donnée brute au score de risque :

1. **Analyse exploratoire** des transactions (distributions, corrélations, valeurs extrêmes).
2. **Prétraitement** : standardisation du montant et du temps, séparation entraînement/test stratifiée (80/20).
3. **Gestion du déséquilibre** avec SMOTE (appliqué uniquement sur l'entraînement) ou pondération des classes.
4. **Comparaison de 4 modèles** : Régression Logistique, Random Forest, XGBoost, Isolation Forest.
5. **Évaluation adaptée** : précision, rappel, F1, AUC-ROC et matrice de confusion, plutôt que l'accuracy.
6. **Application Streamlit** pour explorer, comparer, prédire et chiffrer le gain.

## Données

Jeu de données public *Credit Card Fraud Detection* (ULB / Kaggle) : 284 807 transactions de cartes bancaires européennes sur deux jours, dont 492 fraudes (0,17 %). Les variables V1 à V28 sont issues d'une ACP (anonymisation) ; `Time`, `Amount` et `Class` sont conservées telles quelles.

## Résultats

Jeu de test de 56 962 transactions dont 98 fraudes, seuil de décision 0,5 (résultats du notebook) :

| Modèle | Précision | Rappel | F1 | AUC-ROC |
|---|---|---|---|---|
| Random Forest (SMOTE) | 0,82 | 0,82 | 0,82 | 0,969 |
| XGBoost (SMOTE) | 0,72 | 0,87 | 0,79 | 0,981 |
| XGBoost (pondération `scale_pos_weight`, sans SMOTE) | 0,89 | 0,85 | 0,87 | 0,967 |
| Régression Logistique (SMOTE) | 0,06 | 0,92 | 0,11 | 0,970 |
| Isolation Forest (non supervisé) | 0,30 | 0,33 | 0,32 | 0,954 |

**Lecture pour un décideur** : avec le Random Forest, 80 fraudes sur 98 sont détectées pour seulement 17 fausses alertes sur près de 57 000 transactions légitimes. Le seuil de décision se règle selon votre appétit au risque : plus bas, on détecte plus de fraudes mais on génère plus d'alertes à vérifier.

## L'application

| Page | Rôle |
|---|---|
| Accueil | Présentation du projet et des résultats clés |
| EDA | Exploration du jeu de données |
| Comparaison | Métriques, matrices de confusion et courbes ROC des modèles |
| Prédiction | Saisie d'une transaction, score de risque, seuil réglable |
| Simulateur | Estimation du gain en FCFA selon votre volume, vos pertes et vos coûts |

## Lancer l'application

```bash
git clone https://github.com/patricisto1-arch/fraud-detection-senegal.git
cd fraud-detection-senegal
python -m venv .venv
.venv\Scripts\activate          # Windows (Linux/macOS : source .venv/bin/activate)
python -m pip install -r requirements.txt
python -m streamlit run appli/accueil.py
```

L'application s'ouvre sur http://localhost:8501. Les modèles entraînés sont fournis dans `appli/models/`. La page EDA a besoin du fichier `creditcard.csv` (non versionné, car trop volumineux) : à télécharger sur Kaggle (*Credit Card Fraud Detection*, ULB) et à placer dans le dossier `data/`.

## Structure du dépôt

```
appli/            Application Streamlit (accueil.py, pages/, models/)
appli/notebook_PF.ipynb   Notebook complet : EDA, prétraitement, modélisation
notebooks/        Figures générées par le notebook
docs/             Documentation complémentaire
requirements.txt  Dépendances Python
```

## Limites

- Le jeu de données est **européen et date de 2013** : c'est la méthode qui est transférable, pas le modèle tel quel. Un déploiement réel exige un réentraînement sur des données locales.
- Le modèle repère les **comportements transactionnels anormaux**. Les fraudes par manipulation (faux agent, usurpation par appel téléphonique), où la victime valide elle-même l'opération, restent difficiles à voir au niveau de la transaction et doivent être complétées par la sensibilisation et des règles métier.
- Le simulateur de gain est **illustratif** : ses montants par défaut sont des hypothèses, et le rappel et le taux de fausses alertes sont supposés constants.
- Les performances ont été mesurées sur un seul découpage entraînement/test.

## Pilote proposé

Nous proposons un pilote simple avec votre structure :

1. **Échantillon anonymisé** de vos transactions (ou exécution sur site, sans que les données ne quittent votre système).
2. **Réentraînement** des modèles et réglage du seuil sur vos données.
3. **Mesure comparée** des fraudes détectées et du coût des fausses alertes avec et sans le modèle, sur une période test.
4. **Restitution** chiffrée du gain via le simulateur, avec vos vrais paramètres.

## Pistes d'évolution

- Pipeline de réentraînement automatique pour suivre l'évolution des fraudes.
- Scoring en temps réel via une API REST.
- Explicabilité des décisions (SHAP, LIME).
- Variables propres aux paiements mobiles (fréquence, horaires, nouveaux bénéficiaires).
- Modèles séquentiels (LSTM, autoencodeurs).

## Références

- Dal Pozzolo, A., et al. (2015). *Calibrating Probability with Undersampling for Unbalanced Classification*. IEEE SSCI.
- Chawla, N. V., et al. (2002). *SMOTE: Synthetic Minority Over-sampling Technique*. JAIR, 16, 321-357.
- Chen, T., & Guestrin, C. (2016). *XGBoost: A Scalable Tree Boosting System*. KDD.
- Liu, F. T., et al. (2008). *Isolation Forest*. ICDM.
- Breiman, L. (2001). *Random Forests*. Machine Learning, 45(1), 5-32.

## Contact

**Patrice Dione** — Dakar Institute of Technology — [e-mail: patrice.dione.ia@gmail.com 
LinkedIn: linkedin.com/in/patrice
dione-450486340 
GitHub: github.com/patricisto1-arch 
Address: Dakar, Senegal]
