from bs4 import BeautifulSoup



def relation():
    descriptions=[]
    ids = [] 
    with open('relation.html', "r") as inf:
        for line in inf:
            # enlever le retour ligne
            line = line.strip()
            if not line:
                # ligne vide
                continue
            elif "rel_id" in line :
                line = line.split('>')
                ids.append(line[1])
            elif "rel_name" in line :
                line = line.split('>')
                #line[1] = line[1].split('-')
                #line[1] = line[1][0]
                descriptions.append(line[1])

    relations=[]
    for i in range (len(descriptions)):
        tuple = (ids[i], descriptions[i])
        relations.append(tuple)
    #print(relations)
    return relations
        

if __name__ == "__main__":
    relation()