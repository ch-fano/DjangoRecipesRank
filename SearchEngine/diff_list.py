def gpt_intersections():
    bm25 = [290839, 191643, 265530, 140868, 150879, 138326, 445325, 62205, 518217, 455868, 67627, 167757, 181188, 410720, 155699, 247522, 51336, 45537, 22981, 133516]
    sentiment = [290839, 191643, 265530, 140868, 445325, 150879, 138326, 455868, 167757, 28850, 518217, 247522, 424382, 199160, 465655, 187861, 13577, 346661, 350009, 325401]
    w2v = [265530, 191643, 67627, 280175, 14331, 465655, 13577, 167757, 133516, 209859, 336497, 108821, 92682, 292393, 66229, 76768, 102817, 59511, 190382, 116150]
    review_sentiment = [190382, 299527, 135753, 182629, 110505, 140868, 152116, 123522, 47656, 290839, 12709, 76645, 99992, 191643, 12369, 17073, 55672, 19666, 155699, 53730]

    l= [bm25, sentiment, w2v, review_sentiment]

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
    print()
    print("Solo bm25: ", set(bm25) - (set(sentiment) | set(w2v) | set(review_sentiment)))
    print("Solo sentiment: ", set(sentiment) - (set(w2v) | set(review_sentiment) | set(bm25)))
    print("Solo w2v: ", set(w2v) - (set(review_sentiment) | set(bm25) | set(sentiment)))
    print("Solo review sentiment: ", set(review_sentiment) - (set(w2v) | set(sentiment) | set(bm25)))
    
# Esegui la funzione
gpt_intersections()
