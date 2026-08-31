
import json
import random
import time
from datetime import datetime, timedelta

maintenant = int(time.time())

# ============================================================
# 1. eau_semaine.json - 7 jours a resolution 5 min (2016 points)
# ============================================================
eau_semaine = []
debut = maintenant - (7 * 24 * 3600)
for i in range(7 * 24 * 12):  # 2016 creneaux de 5 min
    ts = debut + i * 300
    heure = datetime.fromtimestamp(ts).hour
    # Simulation d'un profil realiste : pics matin/soir, creux la nuit
    if 6 <= heure <= 9 or 18 <= heure <= 22:
        base = random.randint(5, 25)
    elif 0 <= heure <= 5:
        base = random.randint(0, 2)
    else:
        base = random.randint(1, 8)
    # Simulation occasionnelle d'une regeneration (pic important)
    if random.random() < 0.002:
        base += random.randint(30, 60)
    eau_semaine.append({"timestamp": ts, "litres": base})

with open("eau_semaine.json", "w") as f:
    json.dump(eau_semaine, f)
print(f"eau_semaine.json genere: {len(eau_semaine)} points")

# ============================================================
# 2. eau_mois.json - 30 jours a resolution horaire (720 points)
# ============================================================
eau_mois = []
debut = maintenant - (30 * 24 * 3600)
for i in range(30 * 24):
    ts = debut + i * 3600
    heure = datetime.fromtimestamp(ts).hour
    if 6 <= heure <= 9 or 18 <= heure <= 22:
        base = random.randint(80, 250)
    elif 0 <= heure <= 5:
        base = random.randint(0, 20)
    else:
        base = random.randint(20, 100)
    if random.random() < 0.03:
        base += random.randint(150, 300)
    eau_mois.append({"timestamp": ts, "litres": base})

with open("eau_mois.json", "w") as f:
    json.dump(eau_mois, f)
print(f"eau_mois.json genere: {len(eau_mois)} points")

# ============================================================
# 3. eau_annees.json - 3 annees de donnees mensuelles
# ============================================================
mois_labels = ["Jan", "Fev", "Mar", "Avr", "Mai", "Jun",
               "Jul", "Aou", "Sep", "Oct", "Nov", "Dec"]

eau_annees = {}
annee_courante = datetime.now().year
for annee in range(annee_courante - 2, annee_courante + 1):
    donnees_annee = []
    for m in mois_labels:
        # Consommation mensuelle realiste avec variation saisonniere
        base = random.randint(2800, 4200)
        donnees_annee.append({"mois": m, "litres": base})
    eau_annees[str(annee)] = donnees_annee

with open("eau_annees.json", "w") as f:
    json.dump(eau_annees, f)
print(f"eau_annees.json genere: {len(eau_annees)} annees")

# ============================================================
# 4. regenerations.json - 10 dernieres regenerations
# ============================================================
regenerations = []
ts_courant = maintenant - (60 * 24 * 3600)  # etale sur ~2 mois
for i in range(10):
    ts_courant += random.randint(4 * 24 * 3600, 8 * 24 * 3600)  # tous les 4-8 jours
    duree = random.randint(300, 900)  # 5 a 15 min
    litres = random.randint(35, 65)
    regenerations.append({
        "timestamp": ts_courant,
        "duree_secondes": duree,
        "litres_consommes": litres
    })

with open("regenerations.json", "w") as f:
    json.dump(regenerations, f)
print(f"regenerations.json genere: {len(regenerations)} evenements")

# ============================================================
# 5. statut.json
# ============================================================
statut = {
    "etat": "SERVICE",
    "sel_pourcentage": 72,
    "distance_mm": 184,
    "last_regen_date": datetime.fromtimestamp(regenerations[-1]["timestamp"]).strftime("%d/%m/%Y"),
    "autonomie_jours_estimee": 14.5,
    "rendement_pourcent": 96.3,
    "ratio_litres_par_kg_sel": 145.2,
    "capteur_sel_hs": False,
    "anomalie_conso_eau_active": False,
    "watchdog_ok": True,
    "derniere_maj": datetime.now().strftime("%d/%m/%Y %H:%M"),
    "debit_instantane_lmin": round(random.uniform(0, 8), 2)
}

with open("statut.json", "w") as f:
    json.dump(statut, f)
print("statut.json genere")

# ============================================================
# 6. config.json
# ============================================================
config = {
    "eauActif": True,
    "eauOffsetLitres": 1250.5,
    "distPleinMM": 80,
    "distVideMM": 650,
    "distanceMaxPlausibleMM": 1000,
    "seuilAlarmePourcent": 0,
    "capaciteSelKg": 25,
    "seuilAnomalieEauLitres": 200,
    "fenetreAnomalieEauMinutes": 60,
    "multiplicateurAnomalieRegen": 1.5
}

with open("config.json", "w") as f:
    json.dump(config, f)
print("config.json genere")

print("\n=== TOUS LES FICHIERS DE TEST ONT ETE GENERES ===")
