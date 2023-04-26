import warnings
from bs4 import BeautifulSoup
warnings.filterwarnings("ignore", category=FutureWarning)
import os
from bs4 import BeautifulSoup as bs
import requests
import json


# envoyer une requête HTTP GET à l'URL
def getHtml(mot,entrant,rel):
    with requests.Session() as s:
        url = 'http://www.jeuxdemots.org/rezo-dump.php?'
        if entrant:
            #les params de la requête
            payload = {'gotermsubmit': 'Chercher', 'gotermrel': mot,'rel' : rel, 'relout': 'norelin'}
        else:
            payload = {'gotermsubmit': 'Chercher', 'gotermrel': mot, 'rel':rel ,'relin': 'norelout'}
        #l'envoi de la requête
        r = s.get(url, params=payload)
        soup = bs(r.text, 'html.parser')
        #chercher ce qu'il y a entre <CODE>
        prod = soup.find_all('code')
        #si on a erreur on rééssaye
        while("MUTED_PLEASE_RESEND" in str(prod)):
            #print("ERREUR")
            r = s.get(url, params=payload)
            soup = bs(r.text, 'html.parser')
            prod = soup.find_all('code')

    return prod



def createTxt(mot,entrant,rel):
    prod = getHtml(mot,entrant,rel)
    # Remplacement des espaces et apostrophes dans le mot pour éviter des problèmes de formatage dans le nom du fichier
    mot = mot.replace(" ", "_")
    mot = mot.replace("'", "")
    # Création du nom de fichier en fonction des paramètres entrant et rel
    if entrant :
        fileTxtName = mot.replace(" ", "_") +rel+ "_e.txt"
    else :
        fileTxtName = mot.replace(" ", "_") +rel+ "_s.txt"

    try:
        filesize = os.path.getsize(fileTxtName)
        # print("Ce fichier existe ")
    except OSError:
        # print("Ce fichier n'existe pas")
        filesize = 0
    
    # Si le fichier n'existe pas ou s'il est vide, création d'un nouveau fichier
    if filesize == 0:

        if entrant:
            fileTxtName = mot.replace(" ", "_") +rel+"_e.txt"
        else:
            fileTxtName = mot.replace(" ", "_") +rel+"_s.txt"
        # Ouverture du fichier en mode écriture
        fileTxt = open(fileTxtName, "w", encoding="utf-8")
        # Écriture des données HTML dans le fichier
        fileTxt.write(str(prod))
        #on ferme le fichier
        fileTxt.close()

    return fileTxtName


#Convertir le txt en JSON 

def mySplit(expression):
    resultat = [] # Liste vide pour stocker les résultats
    tmp = "" # Chaîne temporaire pour stocker chaque élément de la liste
    cond = False
    # Boucle sur les caractères de la chaîne d'entrée
    for i in range(len(expression)):
        # Si on est sur le dernier caractère de la chaîne, on ajoute la chaîne temporaire à la liste des résultats
        if i + 1 == len(expression):
            tmp += expression[i]
            resultat.append(tmp)
        else:
            # Si le caractère actuel est une apostrophe simple et que le caractère suivant n'est pas un point-virgule, on entre dans une chaîne de caractères
            if expression[i] == "\'" and expression[i + 1] != ";":
                cond = True
            # Si le caractère actuel est une apostrophe simple et que le caractère suivant est un point-virgule, on sort de la chaîne de caractères
            elif expression[i] == "\'" and expression[i + 1] == ";":
                cond = False
            # Si on est dans une chaîne de caractères, on ajoute le caractère actuel à la chaîne temporaire
            if cond == True:
                tmp += expression[i]
            # Si on n'est pas dans une chaîne de caractères et que le caractère actuel n'est pas un point-virgule, on ajoute le caractère actuel à la chaîne temporaire
            if cond == False and expression[i] != ";":
                tmp += expression[i]
            # Si on n'est pas dans une chaîne de caractères et que le caractère actuel est un point-virgule, on ajoute la chaîne temporaire à la liste des résultats et on réinitialise la chaîne temporaire
            elif cond == False and expression[i] == ";":
                resultat.append(tmp)
                tmp = ""
    return resultat


def createJSON(mot,entrant,rel):
    mot = mot.replace(" ", "_")
    mot = mot.replace("'", "")
    if entrant:
        fileJSONName = mot +rel+"_e.json"
    else:
        fileJSONName = mot +rel+"_s.json"
    try:
        filesize = os.path.getsize(fileJSONName)
        # print("Ce fichier existe ")
    except OSError:
        # print("Ce fichier n'existe pas")
        filesize = 0

    if True:
        # Ouvrir le fichier txt en lecture
        if entrant :
            fileTxt = open(mot +rel+ "_e.txt", "r", encoding="utf-8")
        else :
            fileTxt = open(mot +rel+ "_s.txt", "r", encoding="utf-8")
        lines = fileTxt.readlines()

        # Ouvrir le fichierJSON en écriture
        fileJSON = open(fileJSONName, "w", encoding="utf-8")

        # Initialisation des champs pour chaque type de données
        fields_nt = ['ntname']
        fields_e = ["name", "type", "w", "formated name"]
        fields_rt = ['trname', 'trgpname', 'rthelp']
        fields_r = ["node1", "node2", "type", "w"]

        # Initialisation des dictionnaires pour chaque type de données avec dict0 le dictionnaire final
        dict0 = {}
        dict_e = {}
        dict_rt = {}
        dict_r = {}
        dict_nt = {}

        # Boucle sur chaque ligne du fichier txt pour extraire les données
        for i in range(len(lines)):
            description = list(mySplit(lines[i].strip()))
            # print(description)
            if (len(description) > 0):
                #si le premier element de la liste c'est nt
                if description[0] == "nt":
                    # Création d'un nouveau dictionnaire pour chaque relation "nt"
                    dict2 = {}
                    id = description[1]
                    for i in range(1):
                        dict2[fields_nt[i]] = description[i + 2]
                    #On met le dict2 dans le dictionnaire de notre ID dans le dict dict_nt
                    dict_nt[id] = dict2
                #si le premier element de la liste c'est e
                elif description[0] == "e":
                    # Création d'un nouveau dictionnaire pour chaque relation "e"
                    dict2 = {}
                    id = description[1]
                    for i in range(3):
                        dict2[fields_e[i]] = description[i + 2]
                    dict_e[id]=dict2
                    #si il a un formated name et donc c'est un raffinement ou un terme agrégé, on l'enlève du dictionnaire
                    if len(description) > 5:
                        if id in dict_e:
                            del dict_e[id]
                        else:
                            pass
                #si le premier element de la liste c'est rt
                elif description[0] == "rt":
                    dict2 = {}
                    id = description[1]
                    for i in range(2):
                        dict2[fields_rt[i]] = description[i + 2]

                    if len(description) > 4:
                        dict2[fields_rt[2]] = description[4]

                    dict_rt[id] = dict2
                #si le premier element de la liste c'est r
                elif (description[0] == "r") :
                    dict2 = {}
                    id = description[1]
                    for i in range(4):
                        dict2[fields_r[i]] = description[i + 2]
                    dict_r[id] = dict2


        #on associe chaque dictionnaire de dict0 à son dictionnaire associé
        dict0["nt"] = dict_nt
        dict0["e"] = dict_e
        dict0["r"] = dict_r
        dict0["rt"] = dict_rt
        json.dump(dict0, fileJSON, indent=4) #on écrit dans le fichier json

        fileJSON.close()
        fileTxt.close()
    return fileJSONName


def getData(mot,entrant,rel):
    createTxt(mot,entrant,rel)
    createJSON(mot,entrant,rel)
    mot = mot.replace(" ", "_")
    # Ouvrir le fichier  Json en lecture
    if entrant :
        fileJSONName = mot +rel+ "_e.json"
    else:
        fileJSONName = mot +rel+ "_s.json"
    fileJSON = open(fileJSONName, "r")
    data = json.load(fileJSON) #pour récupérer les informations de notre fichier json
    fileJSON.close()
    return data


#C'est pour récupérer les ID des 2 mots qu'on entre au terminal
def getIdEnt(mot, ent, data):
    jsonData = data["e"]

    idEnt = -1
    idMot = -1
    # print(jsonData)
    for entity in jsonData:
        name = jsonData[entity]['name']
        x = name.replace("'", "", 2)
        if x == ent:
            idEnt = entity
        if x == mot:
            idMot = entity

    result = {"idEnt": idEnt, "idMot": idMot}
    return result

#C'est pour récupérer l'ID de la relation parmi le dictionnaire des relations
def getIdRel(rel):
    url = "https://www.jeuxdemots.org/jdm-about-detail-relations.php" #le site où on récupère les relations + leurs IDs
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    table_rows = soup.find_all('tr')

    relations_dict = {}
    for row in table_rows:
        rel_id = row.find('td', attrs={'info': 'rel_id'}) #dans la balise td rel_id
        rel_name = row.find('td', attrs={'info': 'rel_name'}) #dans la balise td rel_name
        if rel_id and rel_name:
            cleaned_rel_id = int(rel_id.text.strip().split()[0])
            cleaned_rel_name = rel_name['title'].split(' ')[0]
            relations_dict[cleaned_rel_id] = cleaned_rel_name

    for rel_id, name in relations_dict.items():
        if name == rel:
            return str(rel_id)
    return None

#Pour voir si la relation est entrante ou pas, ça renvoie oui ou non + le poids de la relation
def isRelEntrante(idEnt, idRt, data):
    jsonDataR = data["r"] #là où on a la clé = "r"
    resultat = False
    w = ""
    # Boucle sur chaque relation dans jsonDataR
    for entity in jsonDataR:
        # Récupération de l'ID de l'entité et du type de la relation pour chaque relation, l'ID de l'entité c'est ['node1'] psq c'est les relations entrantes
        id_entite = jsonDataR[entity]['node1']
        x = id_entite.replace("'", "", 2)
        type = jsonDataR[entity]['type']
        y = type.replace("'", "", 2)
        w = jsonDataR[entity]["w"]
        # Vérification si l'entité correspond à l'ID d'entrée (le mot qu'on cherche à savoir si c'est une rel entrante ou pas) et si le type de relation correspond à l'ID de relation
        if x == idEnt and y == idRt :
            resultat = True

            break
    return [resultat,w]

#récupérer le poids de la liste resultat que getEntTrans et getEntGenSpec renvoient pour pouvoir classer la liste resultat par poids
def poids(resultat):
    return int(resultat[2])


#celle c'est pour récupérer les mots "transitifs" aka les mots qui avec lesquels on a une relation "rel" la même qu'on cherche au terminal pour le mots d'arrivée 
#pour essayer de trouver des transitivité après
def getEntTrans(data, idRt, idMot,mot,rel):
    jsonDataE = data["e"] #on recupère les données dans la clé "e"
    jsonDataR = data["r"]#on recupère les données dans la clé "r"
    
    #la liste des relations transitives
    relationTransitive = ["r_lieu","r_lieu-1","r_isa","r_holo","r_hypo", "r_has_part","r_own","r_own-1","r_product_of","r_similar"]
    #si notre rel est une relation transitive
    resultat = []
    if rel in relationTransitive :
        #pour chaque relation dans jsonDataR
        for relation in jsonDataR: 
            #si elle a le même id et que c'est pas une relation négative (fausse)
            if (jsonDataR[relation]['type'] == idRt and ("-") not in jsonDataR[relation]['w']):
                node2 = jsonDataR[relation]['node2']
                x = node2.replace("'", "", 2)
                # type = 1 ça veut dire c'est un terme (n_term)
                #si le x est dans jsonDataE donc pas un raffinement ou un mot agrégé, et que c'est un terme et que c'est pas le mot qu'on a 
                if x in jsonDataE and jsonDataE[x]['type'] == '1' and x != idMot:
                    #on l'ajoute à la liste comme [id, nom, poids]
                    resultat.append([x, jsonDataE[x]['name'], jsonDataR[relation]['w']])
        resultat = sorted(resultat,key=poids,reverse = True) #on trie la liste par poids
        
        if len(resultat) == 0: #si on trouve pas dans le fichier mot_s.json on essaye d'aller chercher dans le site plutôt mot = mot et rel = rel uniquement
            dataRel = getData(mot,False,rel)
            jsonDataE = dataRel["e"]
            jsonDataR = dataRel["r"]
            for relation in jsonDataR:
                if (jsonDataR[relation]['type'] == idRt and ("-") not in jsonDataR[relation]['w']):
                    node2 = jsonDataR[relation]['node2']
                    x = node2.replace("'", "", 2)
                    if x in jsonDataE and jsonDataE[x]['type'] == '1' and x != idMot:
                        resultat.append([x, jsonDataE[x]['name'], jsonDataR[relation]['w']])
            resultat = sorted(resultat, key=poids, reverse=True)
    else :
        print("La relation n'est pas transitive")
    return resultat

#On récupère les mots qui ont avec le mot de départ une relation de type (rel) pour l'utiliser dans GetGenerique et GetSpecifique pour chaque relation de généralisation ou spécification
#la seule différence avec getEntTrans c'est que on vérifie si notre relation est dans la liste des relations transitives
def getEntGenSpec(data, idRt, idMot,mot,rel):
    jsonDataE = data["e"]
    jsonDataR = data["r"]
    #len(jsonDataR[idRt])
    resultat = []
    for relation in jsonDataR: 
        if (jsonDataR[relation]['type'] == idRt and ("-") not in jsonDataR[relation]['w']  ): # si (-) très peu probable voire faux
            node2 = jsonDataR[relation]['node2']
            x = node2.replace("'", "", 2)
            # type = 1 ça veut dire c'est un terme (n_term)
            if x in jsonDataE and jsonDataE[x]['type'] == '1' and x != idMot:
                resultat.append([x, jsonDataE[x]['name'], jsonDataR[relation]['w']])
    resultat = sorted(resultat,key=poids,reverse = True) #on les trie par poids
    
    if len(resultat) == 0: #si on trouve pas dans le fichier mot_s.json on essaye d'aller chercher dans le site plutôt mot = mot et rel = rel uniquement
        dataRel = getData(mot,False,rel)
        jsonDataE = dataRel["e"]
        jsonDataR = dataRel["r"]
        for relation in jsonDataR:
            if (jsonDataR[relation]['type'] == idRt and ("-") not in jsonDataR[relation]['w']):
                node2 = jsonDataR[relation]['node2']
                x = node2.replace("'", "", 2)
                if x in jsonDataE and jsonDataE[x]['type'] == '1' and x != idMot:
                    resultat.append([x, jsonDataE[x]['name'], jsonDataR[relation]['w']])
        resultat = sorted(resultat, key=poids, reverse=True)
    return resultat


#on appelle getEntGenSpec pour toute relation de généralisation
def getGenerique(data, idMot,mot,rel):
    dico_generalisation = {"r_isa": "6", "r_holo": "10"}
    if rel in dico_generalisation:
        del dico_generalisation[rel] #on delete psq c'est redondant avec la transitivité
    resultat = {}
    for key in dico_generalisation:
        resultat[key] = getEntGenSpec(data, dico_generalisation[key], idMot,mot,key)
    return resultat

#on appelle getEntGenSpec pour toute relation de spécification
def getSpecifique(data, idMot,mot,rel):
    dico_specialisation = {"r_hypo": "8", "r_has_part": "9"}
    if rel in dico_specialisation:
        del dico_specialisation[rel] #on delete psq c'est redondant avec la transitivité
    resultat = {}
    for key in dico_specialisation:
        resultat[key] = getEntGenSpec(data, dico_specialisation[key], idMot,mot,key)

    return resultat

#cette méthode teste la relation sur l'outil Hélix, regarde s'il y a parmi les mots affichés (annotations) un des mots dans notre dictionnaire, s'il y en a plusiers ça récupère la liste des coefficients de chaque annotation 
def annotation(mot,rel,ent):
    coeff = 1
    coeffs = []
    # Liste des mots avec leur poids respectif
    poids_dict = {
        "toujours vrai": 3,
        "Pertinent": 2,
        "Fréquent": 1.5,
        "Probable": 1.25,
        "Possible": 1,
        "Non spécifique": 0.75,
        "Contrastif": 0.75,
        "Rare": 0.5,
        "Improbable": 0.25,
        "Pas fréquent" : 0.25,
        "Peu pertinent" : 0.25,
        "Non pertinent": 0.1,
        "Ne sait pas": 0,
        "Contradictoire": -1
    }

    # Construire l'URL avec les variables
    url = f"https://www.jeuxdemots.org/rezo-ask.php?gotermsubmit=Demander&term1={mot}&rel={rel}&term2={ent}"
    #print("url",url)
    # Faire une requête HTTP pour obtenir le contenu de la page
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Trouver les balises <RESULT> et </RESULT>
    results = soup.find_all('result')
    for result in results:
        anot_text = result.find('anot').text.strip()
        # Vérifier si un mot de la liste est présent dans le texte de la balise ANOT
        for key, value in poids_dict.items():
            if key.lower() in anot_text.lower():
                coeffs.append(value)
    return coeffs


#récupérer la moyenne de la liste resultats de la méthode classification pour pouvoir la trier selon la moyenne
def moyennes(resultat):
    return int(resultat[5])

#On va mettre toutes les inférences dans un paquet, faire la moyenne de leurs poids * coeffs des annots, et les classer par moyenne pour les utiliser dans la méthod afficheAnswers
def classificationInferences(data,dataEnt,idMot,idEnt,idRt,mot,rel,ent):
    resultats = []
    coeffs = []
    coeffs_2 = []
    trouve = False

    X = getEntTrans(data, idRt, idMot,mot,rel) #je récupère les mots qui ont une relation "rel" avec le mot de départ (mot) pour pouvoir faire la transitivité en bas

    Y = getGenerique(data, idMot,mot,rel) #je récupère les mots génériques pour pouvoir faire la deduction et voir s'il y a une relation entrante dans le mot cible de type motGénérique rel motCible

    Z = getSpecifique(data, idMot,mot,rel) #je récupère les mots spécifiques pour pouvoir faire l'induction et voir s'il y a une relation entrante dans le mot cible de type motGénérique rel motCible
    
    
    #************************************************************** TRANSITIVITE ***************************************************************************************************
    for idCommun in X: # pour chaque petite liste de ma grande liste resultat :
        teste = isRelEntrante(idCommun[0], idRt, dataEnt)
        isRelE = teste[0] #true or false
        if isRelE: #c'est true
            trouve = True
            coeffs = annotation(mot,rel,idCommun[1].replace("'", "")) #on cherche les coeffs de la première relation d'inférence de l'outil Hélix (s'il y en a)
            poids_1 = int(idCommun[2].replace("'", ""))
            coeffs_2 = annotation(idCommun[1].replace("'", ""),rel,ent) #on cherche les coeffs de la deuxième relation d'inférence de l'outil Hélix (s'il y en a)
            poids_2 = int(teste[1].replace("'", ""))
            if "-" not in str(poids_1) and "-" not in str(poids_2): #si c'est pas négatif
                for coeff in coeffs :
                    poids_1 = poids_1 * float(coeff) #on multiplie * le coefficient si on trouve une annotation parmi les nôtres entre mon mot et le mot "transitif"
                for coeff_2 in coeffs_2 :
                    poids_2 = poids_2 * float(coeff_2) #on multiplie * le coefficient si on trouve une annotation parmi les nôtres entre le mot transitif et le mot d'arrivée(ent)
                moyenne = (poids_1 + poids_2)/2
                resultats.append([idCommun[0],idCommun[1],rel,poids_1, poids_2,moyenne,"PREUVE TRANSITIVE"])
    
     #************************************************************** DEDUCTION ****************************************************************************************************
    for idCommun in Y:
        for entity in Y[idCommun]:
            teste = isRelEntrante(entity[0], idRt, dataEnt)
            isRelE = teste[0]
            if isRelE:
                trouve = True
                coeffs = annotation(mot,idCommun,entity[1].replace("'", "")) #on cherche les coeffs de la première relation d'inférence de l'outil Hélix (s'il y en a)
                poids_1 = int(entity[2].replace("'", ""))
                coeffs_2 = annotation(entity[1].replace("'", ""),rel,ent) #on cherche les coeffs de la deuxieme relation d'inférence de l'outil Hélix (s'il y en a)
                poids_2 = int(teste[1].replace("'", ""))
                if "-" not in str(poids_1) and "-" not in str(poids_2):
                    for coeff in coeffs :
                        poids_1 = poids_1 * coeff #on multiplie * le coefficient si on trouve une annotation parmi les nôtres entre mon mot et le mot "generique"
                    for coeff_2 in coeffs_2 :
                        poids_2 = poids_2 * coeff_2 #on multiplie * le coefficient si on trouve une annotation parmi les nôtres entre le mot générique et le mot cible
                    moyenne = (poids_1 + poids_2)/2
                    resultats.append([entity[0],entity[1],idCommun,poids_1,poids_2,moyenne,"PREUVE DEDUCTIVE"])
    
    #************************************************************** INDUCTION ******************************************************************************************************
    for idCommun in Z:
        for entity in Z[idCommun]:
            teste = isRelEntrante(entity[0], idRt, dataEnt)
            isRelE = teste[0]
            if isRelE:
                trouve = True
                coeffs = annotation(mot,idCommun,entity[1].replace("'", "")) #on cherche les coeffs de la première relation d'inférence de l'outil Hélix (s'il y en a)
                poids_1 = int(entity[2].replace("'", ""))
                coeffs_2 = annotation(entity[1].replace("'", ""),rel,ent) #on cherche les coeffs de la deuxieme relation d'inférence de l'outil Hélix (s'il y en a)
                poids_2 = int(teste[1].replace("'", ""))
                if "-" not in str(poids_1) and "-" not in str(poids_2):
                    for coeff in coeffs :
                        poids_1 = poids_1 * coeff #on multiplie * le coefficient si on trouve une annotation parmi les nôtres entre mon mot et le mot "spécifique"
                    for coeff_2 in coeffs_2 :
                        poids_2 = poids_2 * coeff_2 #on multiplie * le coefficient si on trouve une annotation parmi les nôtres entre le mot spécifique et le mot cible
                    moyenne = (poids_1 + poids_2)/2
                    resultats.append([entity[0],entity[1],idCommun,poids_1,poids_2,moyenne,"PREUVE INDUCTIVE"])
    resultats = sorted(resultats, key=moyennes, reverse=True) #je trie par moyenne
    return [resultats,trouve]


#Affichage des résultats
def affichageAnswers(data, dataEnt, idMot, idEnt, idRt, mot, rel, ent, cpt):
    result = classificationInferences(data,dataEnt,idMot,idEnt,idRt,mot,rel,ent)
    if result[1] == False : #si on a trouvé aucune preuve
        print("Pas de preuve")
    else :
        for resultat in result[0] : #je récupère la liste triée de mes inférences et pour chaque inférence j'affiche
            if  cpt > 0:
                if "-" not in str(resultat[3]) and "-" not in str(resultat[4]):
                    print("==============="+resultat[6]+"================================")
                    print("OUI car : " + mot + " " + str(resultat[2]) + " " + str(resultat[1]) + " (Poids : "+str(resultat[3])+")")
                    print("et " + str(resultat[1]) + " " + rel + " " + ent + "(Poids : "+str(resultat[4])+")")
                    cpt = cpt - 1