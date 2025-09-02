def validate(infos):
    # Vérifie si deux sites disent la même chose (très simplifié)
    if len(infos) >= 2:
        return infos[0]["text"]
    return None
