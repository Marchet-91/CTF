from hashlib import md5

def search(lista, trovare):
    for pos, i in enumerate(lista):
        if i == trovare:
            return pos

def all_pos(pos, t, change, original):
    for k in t:
        change[pos] = k
        # print(" ".join(change))
        print(md5((" ".join(change)).encode()).hexdigest()[:6])
        if md5(original.encode()).hexdigest()[:6] == md5((" ".join(change)).encode()).hexdigest()[:6]:
            return change

original = "Oggetto: determinazione del voto di CyberChallenge per lo studente Davide Maiorca, anno accademico 2021 2022. Il sottoscritto Giorgio Giacinto, VISTO lo scarso impegno nello studio di CyberChallenge; VISTO il numero di persone che ha risolto la challenge 3; VISTO il numero di assenze dello studente; DETERMINA che, nel corrente anno accademico, lo studente deve avere il voto 7/30."

change = "Oggetto: determinazione del voto di CyberChallenge per lo studente Davide Maiorca, anno accademico 2021 2022. Il sottoscritto Giorgio Giacinto, VISTO lo scarso impegno nello studio di CyberChallenge; VISTO il numero di persone che ha risolto la challenge 3; VISTO il numero di assenze dello studente; DETERMINA che, nel corrente anno accademico, lo studente deve avere il voto 7/30."
change = change.split(" ")
# print(change[48])

pos = [-1,48,1, 33,21,44, 31]
voto = [
    "30/30.", 
    "30L/30."]

tempo = [
    "attuale", 
    "in corso", 
    "corrente"
]

determina = [
    "determinazione",
    "assegnazione del voto",
    "attribuzione del voto", 
    "valutazione", 
    "delibera del voto", 
    "definizione del voto",
    "stabilire il voto"]

ha = [
    "ha",
    "hanno"
]

scarso = [
    "notevole",
    "grande",
    "forte",
    "elevato",
    "straordinario"
]

studente = [""
    "studente;",
    "partecipante;"
    "alunno;",
    "concorrente"
]

persone = [
    "persone",
    "partecipanti",
    "concorrenti",
    "sfidanti",
    "candidati",
    "iscritti",
    "utenti", 
    "soggetti"
]

voto1 = [
    "valutazione",
    "punteggio",
    "giudizio",
    "esito",
    "livello"
]

accademico = [
    "accademico",
    "scolastico",
    "universitario",
    "didattico",
    "formativo"
]

assenze = [""
    "assenze",
    "presenze", 
    "partecipazione"
]

change[search(change, "scarso")] = "grande"
change[search(change, "7/30.")] = "30L/30."
print(change)
TMP = change
# print(change)
# print(search(change, "persone"))
win = all_pos(-1, voto, change, original)
if win == None:
    # print("1")
    # print(TMP)
    win = all_pos(48 , tempo, change, original)
if win == None:
    change = TMP
    win = all_pos(1 , determina, change, original)
if win == None:
    change = TMP
    print(TMP)
    print(change)
    win = all_pos(33 , ha, change, original)
if win == None:
    change = TMP
    win = all_pos(21, scarso, change, original)
if win == None:
    change = TMP
    win = all_pos(search(change, "studente;") , studente, change, original)
if win == None:
    change = TMP
    win = all_pos(search(change, "persone") , persone, change, original)
if win == None:
    change = TMP
    win = all_pos(search(change, "accademico") , accademico, change, original)
if win == None:
    change = TMP
    win = all_pos(search(change, "voto") , voto1, change, original)
if win == None:
    change = TMP
    win = all_pos(search(change, "assenze") , assenze, change, original)


if win == None:
    change = TMP
    for a in voto:
        for b in tempo:
            for c in determina:
                for d in ha:
                    for e in scarso:
                        for f in studente:
                            for g in persone:
                                for h in voto1:
                                    for i in accademico:
                                        for l in assenze:
                                            change = f"Oggetto: {c} del {h} di CyberChallenge per lo studente Davide Maiorca, anno {i} 2021 2022. Il sottoscritto Giorgio Giacinto, VISTO lo {e} impegno nello studio di CyberChallenge; VISTO il numero di {g} che {d} risolto la challenge 3; VISTO il numero di {l} dello {f} DETERMINA che, nel {b} anno accademico, lo studente deve avere il voto {a}"
                                            if md5(original.encode()).hexdigest()[:6] == md5((" ".join(change)).encode()).hexdigest()[:6]:
                                                win = change

print(win)
print(md5(original.encode()).hexdigest()[:6])

