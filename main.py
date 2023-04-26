from fonctions import *
import requests
from bs4 import BeautifulSoup

inverse = {"r_agent": "r_agent-1","r_agent-1": "r_agent", "r_patient": "r_patient-1", "r_patient": "r_patient-1" ,"r_isa": "r_hypo","r_hypo": "r_isa" ,"r_holo": "r_has_part", "r_has_part": "r_holo","r_lieu": "r_lieu-1", "r_lieu-1": "r_lieu"}


mot = input("Allez, balance une entité cool : ")
rel = input("Donne-moi une relation géniale à explorer : ")
ent = input("Ok, maintenant une autre entité qui déchire : ")
cpt_val = int(input("Allez, combien tu veux ? Fais-nous rêver : "))

print("On va peut-être découvrir des choses surprenantes. Accroche-toi bien !")



createTxt(mot,False,"") #je cherche les mots sortants du mot de départ
createJSON(mot,False,"")
data = getData(mot,False,"")

#recuperation des entitées
infos = getIdEnt(mot,ent,data)
idEnt = infos["idEnt"]
idMot = infos["idMot"]

#Recuperer la relation
if idEnt != "null":
    idRt = getIdRel(rel)
    
# Traiter le cas ou la relation n'est pas directe
if True:
    createTxt(ent,True,"") #je cherche les mots entrants du mot cible
    createJSON(ent,True,"")
    dataEnt = getData(ent,True,"")
    #idCommuns = getIdCommuns(data,dataEnt,idEnt,idMot)
    
    #Voir si la relation existe entre les 2 entités
    #relation directe
    print("********************************************************")
    if idRt is not None:
        resultat = isRelEntrante(idMot,idRt,dataEnt)
        if resultat[0] == True :
            print("Oui c'est une relation directe et son poids est : ",resultat[1])
        else : 
            print("Non c'est pas une relation directe!\n")


    affichageAnswers(data, dataEnt, idMot, idEnt, idRt, mot, rel, ent, cpt_val)

    #si ma relation c'est une relation inversible, je fais tout à l'envers
    if rel in inverse:
        print("*********************************************Prouver l'inverse*********************************************")
        rel_1 = inverse[rel] #la relation devient l'inverse de ma relation de départ 
        print("Prouvons : " + ent + " " + rel_1 + " " + mot) #mot devient ent et ent devient mot

        createTxt(ent, False, "") #je cherche plutot les mots sortants du mot cible
        createJSON(ent, False, "")
        dataEnt = getData(ent, False, "")

        idRt_1 = getIdRel(rel_1)

        createTxt(mot, True, "") #et les mots entrants du mot de dpéart
        createJSON(mot, True, "")
        data = getData(mot, True, "")
        
        if idRt_1 is not None:
            resultat = isRelEntrante(idEnt,idRt_1,data)
            if resultat[0] == True :
                print("Oui c'est une relation directe et son poids est : ",resultat[1])
            else : 
                print("Non c'est pas une relation directe!\n")

        affichageAnswers(dataEnt, data, idEnt, idMot, idRt_1, ent, rel_1, mot, cpt_val)
