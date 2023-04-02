import requests
from bs4 import BeautifulSoup
import json
import re

# URL de la page web contenant les données à extraire
url = "https://www.jeuxdemots.org/rezo-dump.php"


def recupere(mot):
    # Paramètres de la requête
    params = {
        "gotermsubmit": "Chercher",
        "gotermrel": "rel",
        "gotermrel2": "syn",
        "rel": "",
        "rel2": "",
        "typeinfo": "word",
        "gotermzone": "0",
        "gotermterme": mot
    }

    # Envoi de la requête et récupération de la réponse
    response = requests.post(url, data=params)

    # Utilise BeautifulSoup pour analyser le code HTML de la page web
    soup = BeautifulSoup(response.content, 'html.parser')

    # Récupère le contenu entre les balises <CODE> et </CODE>
    code_source = soup.find('code').text

    # Affiche le code source de la page
    #print(code_source)

    # Récupère les entrées sortantes pour le terme donné
    entrees_sortantes = []
    for lien in soup.find_all('a', href=True):
        if lien['href'].startswith('?gotermrel='):
            entree_sortante = lien.text
            entrees_sortantes.append(entree_sortante,"\n")

    # Affiche les entrées sortantes
    print("Entrées sortantes pour le terme 'troupe d'artistes' :")
    liste_resultats=[]
    for entree_sortante in entrees_sortantes:
        print(entree_sortante)
        liste_resultats.append(entree_sortante,"\n")
                
    

    #avoir acces a ce fichier , chercher les termes generiques les is-a , expressions regulieres
    #creer des fichiers pour chaque terme generique recupere avec tous les relations 
    #trouver du coup toutes les relations transitives propres a ce fichier
    
    return code_source

    

def main():
    # Demande à l'utilisateur d'entrer un mot à chercher
    mot = input("Entrez le mot à chercher le sang : ")

    # Appelle la fonction pour trouver les entrées sortantes pour le mot donné
    resultats=recupere(mot)
    #print(resultats)


    # Crée un fichier JSON pour sauvegarder les résultats
    nom_fichier = f"{mot}.json"
    with open(nom_fichier, 'w') as f:
        content=json.dumps(resultats)
        f.write(content)

    print(f"Les résultats ont été sauvegardés dans le fichier '{nom_fichier}'.")
    
    #m=[]
    #p=[]
    texte="11;25\nr;304601874;287382;6388301;11;25\nr;485770571;287382;13765567;11;25\nr;545791576;287382;276096;36;25\nr;527622328;287382;2563049;71;25\nr;5692467;287382;131306;777;10\nr;5692476;287382;98704;777;10\nr;5692484;287382;145172;777;10\nr;5692493;287382;272289;777;10\nr;5692495;287382;252722;777;10\nr;5692498;287382;96916;777;10\nr;5692505;287382;12860;777;10\nr;5692514;287382;149242;777;10\nr;5692523;287382;34677;777;10\nr;5692524;287382;57875;777;10\nr;5692534;287382;87736;777;10\nr;5692542;287382;82873;777;10\nr;5692558;287382;48338;777;10\nr;5692561;287382;243489;777;10\nr;5692562;287382;65203;777;10\nr;5692563;287382;115155;777;10\nr;5692569;287382;110367;777;10\nr;5692574;287382;18481;777;10\nr;5692575;287382;155304;777;10\nr;5692581;287382;101938;777;10\nr;5692586;287382;43739;777;10\nr;5692587;287382;100736;777;10\nr;5692590;287382;141231;777;10\nr;5692593;287382;100520;777;10\nr;5692594;287382;108041;777;10\nr;5692600;287382;89390;777;10\nr;5692605;287382;103057;777;10\nr;6273269;287382;287741;777;10\nr;18467652;287382;413123;777;10\nr;18467660;287382;418092;777;10\nr;18467662;287382;428313;777;10\nr;"
    motsgeneriques = re.findall(r"r;\d+;\d+;(\d+)",resultats)

    #print("les mots generiques sont",motsgeneriques)
    
    #for ligne in resultats.split('\n'):
     #   if ligne:
      #      troisieme_nombre = ligne.split(';')[2]
       #     print(troisieme_nombre)
    #for ligne in texte.split('\n'):
     #   parties = ligne.split(';')
        #partiesliste =" ".join(parties)
        #lignes=lignes+partiesliste
      #  p.append(parties)
       # for partie in parties:
        #    if partie[0][0] == "r":
         #       if len(parties[0]) > 0 & len(partie) > 2:
            #if partie.startswith("r;"):
          #       troisieme_nombre = partie.split(';')[2]
           #      print(troisieme_nombre)
            #     m.append(troisieme_nombre)
             #   else:
              #      continue
                # vérifier si la sous-liste contient suffisamment d'éléments

    
    #print("parties",parties)

    # parcourir chaque liste dans la liste principale
    #for sous_liste in ma_liste:
    # vérifier si le premier élément de chaque liste commence par "r"
    #if sous_liste[0][0] == "r":
        # afficher la sous-liste si la condition est vraie
        #print(sous_liste)       

    #motsgeneriques=[]
    #pattern = r'^r;\d+;(\d+);'

    #with open(mot+".json", "r") as file:
        #contents = file.read()
        #matches = re.findall(pattern, contents)
   
    
    
        #for line in f:
            #line = line.replace('\r', '').replace('\n', '')
            #elements = line.strip().split(";")
            #print(elements)
        #for i in range(len(elements)):
            #if elements[i] == "r":
                #number = int(elements[i+2])
                #motsgeneriques.append(number)
                #print(number)

    

    #print(motsgeneriques)

    # la liste des éléments à rechercher après le "e"
    #liste_elements = ["51970", "32456"]

    # on récupère le premier élément après le "e"
    #premier_element = resultats.split(";")[1]

    # si cet élément est dans la liste, on récupère le deuxième élément après le "e"
    #if premier_element in motsgeneriques:
        #index_element = resultats.split(";").index(premier_element)
        #deuxieme_element = resultats.split(";")[index_element + 2]

    # sinon, on retourne None
    #else:
        #deuxieme_element = None

    #print(deuxieme_element)

    chaine = "e;51970;'représentation';1;3243"
    

    for element in motsgeneriques:
        if "e;" + str(element) in resultats:
            liste_mots = resultats.split(";")
            print(liste_mots)
            index_element = liste_mots.index("e;" + str(element))
            if index_element < len(liste_mots) - 2:
                mot = liste_mots[index_element + 2]
                print(mot)
    
    



if __name__ == "__main__":
    main()
