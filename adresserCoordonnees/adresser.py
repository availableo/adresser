# -*- coding: utf-8 -*-
import requests, json

exempleProperties = {
                'label': '1 Lieu Dit le Puy Montbault 49310 Lys-Haut-Layon',
                'score': 0.9999546206872928,
                'housenumber': '1',
                'id': '49373_c133_00001',
                'name': '1 Lieu Dit le Puy Montbault',
                'postcode': '49310',
                'citycode': '49373',
                'oldcitycode': '49286',
                'x': 427367.43,
                'y': 6673856.11,
                'city': 'Lys-Haut-Layon',
                'oldcity': 'Saint-Hilaire-du-Bois',
                'context': '49, Maine-et-Loire, Pays de la Loire',
                'type': 'housenumber',
                'importance': 0.46302,
                'street': 'Lieu Dit le Puy Montbault',
                'distance': 336,
                'population': None  # rarement présent
                }

def chercherAdresse(xWgs84, yWgs84):
    xRequete = round(xWgs84, 6)
    yRequete = round(yWgs84, 6)
    #print(xRequete, yRequete)
    requeteGeoportail = 'https://api-adresse.data.gouv.fr/reverse/?lon={}&lat={}'.format(str(xRequete), str(yRequete))
    r = requests.get(requeteGeoportail)
    if not r.ok:
        return None
    dicoRetour = json.loads(r.text.encode('latin-1').decode('unicode-escape'))
    """
    exemple de réponse:
        {'type': 'FeatureCollection', 'version': 'draft',
        'features': [{
            'type': 'Feature',
            'geometry': {
                'type': 'Point', 'coordinates': [-0.596411, 47.109079]},
            'properties': {
                'label': '1 Lieu Dit le Puy Montbault 49310 Lys-Haut-Layon',
                'score': 0.9999546206872928,
                'housenumber': '1',
                'id': '49373_c133_00001',
                'name': '1 Lieu Dit le Puy Montbault',
                'postcode': '49310',
                'citycode': '49373',
                'oldcitycode': '49286',
                'x': 427367.43,
                'y': 6673856.11,
                'city': 'Lys-Haut-Layon',
                'oldcity': 'Saint-Hilaire-du-Bois',
                'context': '49, Maine-et-Loire, Pays de la Loire',
                'type': 'housenumber',
                'importance': 0.46302,
                'street': 'Lieu Dit le Puy Montbault',
                'distance': 336}
                    }],
        'attribution': 'BAN',
        'licence': 'ETALAB-2.0',
        'limit': 1}
    """
    featuresAdresse = dicoRetour.get('features', [])

    adresseProperties = featuresAdresse[0].get('properties', {}) if featuresAdresse else {}
    print(xWgs84, yWgs84, '\n', adresseProperties)
    return adresseProperties

def chercherAdresses(coordoneesWgs84):
    """
    input: coordoneesWgs84: liste de tupples ou listes: (x, y); en WGS84
    returns dict with tuples as keys
    """
    adressesProperties = {}  # {(x,y): {adresse}, ...}
    for xy in coordoneesWgs84:
        adressesProperties[xy] = chercherAdresse(xy[0], xy[1])
    return adressesProperties
