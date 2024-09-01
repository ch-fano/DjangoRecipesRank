

from itertools import combinations

def trova_comuni(dict_di_liste):
    if not dict_di_liste:
        return []

    # Prendi tutte le liste del dizionario
    liste = list(dict_di_liste.values())

    # Inizia con gli elementi della prima lista
    comuni = set(liste[0])

    # Interseca con gli elementi delle altre liste
    for sottolista in liste[1:]:
        comuni.intersection_update(sottolista)

    # Ritorna i comuni come lista
    return list(comuni)

def intersezioni_a_due_a_due(dict_di_liste):
    intersezioni = []

    # Intersezione di tutte le liste insieme
    tutte_liste = list(dict_di_liste.values())
    intersezione_tutte = set(tutte_liste[0])
    for sottolista in tutte_liste[1:]:
        intersezione_tutte.intersection_update(sottolista)
    intersezioni.append(("Intersezione tra tutte le liste", list(intersezione_tutte)))

    # Intersezioni a due a due per tutte le combinazioni possibili
    for (nome1, lista1), (nome2, lista2) in combinations(dict_di_liste.items(), 2):
        set1 = set(lista1)
        set2 = set(lista2)
        intersezione = set1.intersection(set2)
        intersezioni.append((f"Intersezione tra {nome1} e {nome2}", list(intersezione)))

    return intersezioni

def intersections():

    bm25 = ['46183', '140034', '61231', '185498', '117293', '30756', '90808', '132920', '87461', '184769', '494016', '179638', '68124', '317308', '28419', '457007', '131648', '61131', '76248', '55531']
    sentiment = ['46183', '140034', '61231', '117293', '185498', '30756', '132920', '90808', '68124', '87461', '184769', '179638', '317308', '494016', '457007', '28419', '131648', '55531', '76248', '17095']
    w2v = ['46183', '185498', '17095', '68124', '90693', '370289', '130025', '517410', '132920', '76248', '189655', '82337', '117293', '76710', '373009', '308361', '227756', '55531', '91560', '90808']
    review_sentiment = ['29172', '125897', '46479', '52289', '325571', '48013', '81284', '29977', '99247', '98844', '38607', '411045', '51803', '154576', '192282', '9108', '94989', '283936', '40882', '95988']

    l = [bm25, sentiment, w2v, review_sentiment]
    intersection = set(l[0])

    for ll in l[1:]:
        intersection.intersection_update(ll)

    print("Intersezione tra tutte le liste: ", intersection)

    intersection = set(l[0])
    intersection.intersection_update(l[1])
    intersection.intersection_update(l[2])
    print("Intersezione esclusa review_sentiment: ", intersection)
    print()

    intersection = set(l[0])
    intersection.intersection_update(l[1])
    print("Intersezione bm25-sentiment: ", intersection)

    intersection = set(l[0])
    intersection.intersection_update(l[2])
    print("Intersezione bm25-w2v: ", intersection)

    intersection = set(l[1])
    intersection.intersection_update(l[2])
    print("Intersezione sentiment-w2v: ", intersection)

    print()
    intersection = set(l[0])
    intersection.intersection_update(l[3])
    print("Intersezione bm25-review_sentiment: ", intersection)

    intersection = set(l[1])
    intersection.intersection_update(l[3])
    print("Intersezione sentiment-review_sentiment: ", intersection)

    intersection = set(l[2])
    intersection.intersection_update(l[3])
    print("Intersezione w2v-review_sentiment: ", intersection)


# Trova l'intersezione di tutte le liste
#stringhe_comuni = trova_comuni(relevant_dict)
#print("Intersezione tra tutte le liste:", stringhe_comuni)

# Trova tutte le intersezioni a due a due
#intersezioni = intersezioni_a_due_a_due(relevant_dict)
#for descrizione, intersezione in intersezioni:
 #   print(descrizione, ":", intersezione)

def gpt_intersections():
    bm25 = [98985, 78892, 375810, 214088, 371970, 86105, 278278, 90135, 66436, 170250, 99333, 166025, 125735, 13923, 290078, 9206, 120971, 148231, 213306, 65163]
    sentiment = [98985, 78892, 371970, 375810, 214088, 86105, 90135, 124075, 66436, 278278, 170250, 125735, 13923, 99333, 166025, 290078, 120971, 148231, 65163, 254570]
    w2v = [86105, 98985, 78892, 170250, 214088, 290078, 292007, 166025, 9206, 99333, 13923, 184879, 254570, 121721, 371970, 318626, 37014, 65163, 12706, 66436]
    review_sentiment = [98985, 278278, 78892, 227257, 371970, 42038, 125735, 375810, 86105, 37861, 94528, 40832, 214088, 124075, 90135, 91020, 29765, 106262, 53594, 13923]

    l = [bm25, sentiment, w2v, review_sentiment]

    # Intersezione tra tutte le liste
    intersection_all = set(bm25)
    for ll in l[1:]:
        intersection_all.intersection_update(ll)
    print("Intersezione tra tutte le liste: ", intersection_all)

    # Intersezione tra bm25, sentiment e w2v (esclusa review_sentiment)
    intersection_excluded_review = set(bm25)
    intersection_excluded_review.intersection_update(sentiment)
    intersection_excluded_review.intersection_update(w2v)
    print("Intersezione esclusa review_sentiment: ", intersection_excluded_review)
    print()

    # Intersezioni a due a due
    intersection_bm25_sentiment = set(bm25).intersection(sentiment)
    print("Intersezione bm25-sentiment: ", intersection_bm25_sentiment)

    intersection_bm25_w2v = set(bm25).intersection(w2v)
    print("Intersezione bm25-w2v: ", intersection_bm25_w2v)

    intersection_sentiment_w2v = set(sentiment).intersection(w2v)
    print("Intersezione sentiment-w2v: ", intersection_sentiment_w2v)

    print()
    intersection_bm25_review_sentiment = set(bm25).intersection(review_sentiment)
    print("Intersezione bm25-review_sentiment: ", intersection_bm25_review_sentiment)

    intersection_sentiment_review_sentiment = set(sentiment).intersection(review_sentiment)
    print("Intersezione sentiment-review_sentiment: ", intersection_sentiment_review_sentiment)

    intersection_w2v_review_sentiment = set(w2v).intersection(review_sentiment)
    print("Intersezione w2v-review_sentiment: ", intersection_w2v_review_sentiment)


# Esegui la funzione
gpt_intersections()
