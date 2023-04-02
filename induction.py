import requests
from bs4 import BeautifulSoup
import json
import re
from relations import relation
# URL de la page web contenant les données à extraire
url = "https://www.jeuxdemots.org/rezo-dump.php"


def recupere(mot, relation):
    # Paramètres de la requête
    params = {
        "gotermsubmit": "Chercher",
        "gotermrel": mot,
        "gotermrel2": "syn",
        "rel": relation,
        "rel2": "",
        "typeinfo": "word",
        "gotermzone": "0",
    }
    
    # Envoi de la requête et récupération de la réponse
    response = requests.post(url, data=params)

    # Utilise BeautifulSoup pour analyser le code HTML de la page web
    soup = BeautifulSoup(response.content, 'html.parser')

    # Récupère le contenu entre les balises <CODE> et </CODE>
    code_source = soup.find('code').text

    
    return code_source
    

def main():
    # Demande à l'utilisateur d'entrer un mot à chercher
    mot = input("Entrez le mot à chercher : ")

    # Appelle la fonction pour trouver les entrées sortantes pour le mot donné
    resultats=recupere(mot,'6')
    #print(resultats)


    # Crée un fichier JSON pour sauvegarder les résultats
    nom_fichier = f"{mot}.json"
    with open(nom_fichier, 'w') as f:
        content=json.dumps(resultats)
        f.write(content)

    print(f"Les résultats ont été sauvegardés dans le fichier '{nom_fichier}'.")
    
    motspecifiques = re.findall(r"r;\d+;(\d+);\d+",resultats)
    #print(motspecifiques)

    liste_label=[]
    for id in motspecifiques:
            for ligne in resultats.split("\n"):
                if ligne.startswith("e;" + id + ";"):
                    chaine = ligne.split(";")[2].strip("'")
                    if chaine not in liste_label and chaine != mot :
                        liste_label.append(chaine)
    #print(liste_label)

    relations = []
    relations = relation()
    dictionnaire_listes = {}
    for label in liste_label :
        resultat = recupere(label,"")
        nom_liste = "liste_"+label
        dictionnaire_listes[nom_liste]=[]
        motsgeneriques_et_specifiques = re.findall(r"r;\d+;\d+;(\d+);(\d+);(\d+)",resultat)
        for id in motsgeneriques_et_specifiques:
            for ligne in resultat.split("\n"):
                if ligne.startswith("e;" + id[0] + ";"):
                    chaine = ligne.split(";")[2].strip("'")
                    if chaine not in liste_label and chaine != mot and chaine.isalpha():
                        for rel in relations :
                            if id[1] == rel[0] :
                                dictionnaire_listes[nom_liste].append((label,rel[1],chaine, id[2]))  
        #print("\nle mot label est\n", label,"\nses mots génériques et les relations avec eux sont :\n", dictionnaire_listes[nom_liste])
    #print(dictionnaire_listes)

    for liste in dictionnaire_listes.values():
        for i, element in enumerate(liste):
            if element[0] != mot:
                liste[i] = (mot, element[1], element[2], element[3])

    print(dictionnaire_listes)

if __name__ == "__main__":
    main()