from crypt import load_text_from_web, gen_key, chiffrer
from collections import Counter

# Liste de symboles fixés
symbols = ['b', 'j', '\r', 'J', '”', ')', 'Â', 'É', 'ê', '5', 't', '9', 'Y', '%', 'N', 'B', 'V', '\ufeff', 'Ê', '?',
           '’', 'i', ':', 's', 'C', 'â', 'ï', 'W', 'y', 'p', 'D', '—', '«', 'º', 'A', '3', 'n', '0', 'q', '4', 'e',
           'T', 'È', '$', 'U', 'v', '»', 'l', 'P', 'X', 'Z', 'À', 'ç', 'u', '…', 'î', 'L', 'k', 'E', 'R', '2', '_',
           '8', 'é', 'O', 'Î', '‘', 'a', 'F', 'H', 'c', '[', '(', "'", 'è', 'I', '/', '!', ' ', '°', 'S', '•', '#',
           'x', 'à', 'g', '*', 'Q', 'w', '1', 'û', '7', 'G', 'm', '™', 'K', 'z', '\n', 'o', 'ù', ',', 'r', ']', '.',
           'M', 'Ç', '“', 'h', '-', 'f', 'ë', '6', ';', 'd', 'ô', 'e ', 's ', 't ', 'es', ' d', '\r\n', 'en', 'qu',
           ' l', 're', ' p', 'de', 'le', 'nt', 'on', ' c', ', ', ' e', 'ou', ' q', ' s', 'n ', 'ue', 'an', 'te', ' a',
           'ai', 'se', 'it', 'me', 'is', 'oi', 'r ', 'er', ' m', 'ce', 'ne', 'et', 'in', 'ns', ' n', 'ur', 'i ', 'a ',
           'eu', 'co', 'tr', 'la', 'ar', 'ie', 'ui', 'us', 'ut', 'il', ' t', 'pa', 'au', 'el', 'ti', 'st', 'un', 'em',
           'ra', 'e,', 'so', 'or', 'l ', ' f', 'll', 'nd', ' j', 'si', 'ir', 'e\r', 'ss', 'u ', 'po', 'ro', 'ri', 'pr',
           's,', 'ma', ' v', ' i', 'di', ' r', 'vo', 'pe', 'to', 'ch', '. ', 've', 'nc', 'om', ' o', 'je', 'no', 'rt',
           'à ', 'lu', "'e", 'mo', 'ta', 'as', 'at', 'io', 's\r', 'sa', "u'", 'av', 'os', ' à', ' u', "l'", "'a", 'rs',
           'pl', 'é ', '; ', 'ho', 'té', 'ét', 'fa', 'da', 'li', 'su', 't\r', 'ée', 'ré', 'dé', 'ec', 'nn', 'mm', "'i",
           'ca', 'uv', '\n\r', 'id', ' b', 'ni', 'bl']

# Liste de symboles paf leurs fréquences dans le corpus
sorted_symbols = [(' ', 130167), ('e ', 73260), ('\r\n', 71838), ('s ', 58451), (', ', 49016), ('t ', 43097),
                  (' d', 40076), ('_', 39834), ('es', 36943), ('le', 33739), ('a', 32315), ('de', 31607), ('re', 31030),
                  (' l', 30628), ('é', 29654), ('g', 29601), ('on', 28357), ('en', 27477), ('qu', 27092), ('ou', 25390),
                  ('c', 25278), ('ai', 24622), ('u', 24453), ('r', 24380), ('i', 24336), ('nt', 24217), ('. ', 24120),
                  (' p', 22597), ('an', 21971), ('d', 21964), ('n', 21008), ('.', 20673), ('-', 20634), ('me', 20438),
                  ('’', 20397), ('l', 20351), ('te', 20345), ('e', 20241), (' c', 19495), ('f', 19463), (' s', 19234),
                  ('m', 19062), (' e', 18751), ('ur', 18413), ('t', 17964), ('b', 17667), ('p', 17340), ('la', 16915),
                  ('et', 16746), ('er', 16489), ('ie', 16360), ('in', 16317), ('s', 16286), ('is', 16140),
                  ('n ', 16049), ('\n', 15809), ('o', 15803), ('v', 15790), (' a', 15742), ('r ', 15714), ('ra', 15441),
                  ('ce', 15264), ('it', 15112), ('il', 15092), ('se', 14388), ('x', 14331), ('co', 14181),
                  ('a ', 14042), ('ar', 13933), ('h', 13849), ('ne', 13819), ('au', 13794), ('tr', 13716),
                  ('us', 13136), ('ns', 13100), (' q', 12783), ('pa', 12654), ('ue', 12270), ('oi', 12170),
                  (' m', 11859), ('ch', 11799), ('un', 11797), ('è', 11735), ('ui', 11659), ('u ', 11495),
                  ('ri', 11361), ('eu', 11100), ('ti', 10976), ('ma', 10419), ('L', 10293), ('po', 10269),
                  ('i ', 10187), ('s,', 9989), ('pr', 9893), ('ve', 9820), ('M', 9416), ('y', 9362), ('C', 9311),
                  ('or', 9285), ('E', 9275), (' t', 9128), (' f', 8863), (' n', 8714), ('ut', 8701), ('el', 8556),
                  ('ll', 8509), ('so', 8436), ('A', 8211), ('ét', 8144), ('à ', 8138), ('ss', 8035), ('ir', 8022),
                  ('ro', 7909), ('e,', 7906), ('pe', 7905), ('em', 7795), ('S', 7670), (' v', 7649), ('si', 7636),
                  ('st', 7593), (' r', 7593), ('nd', 7461), ('I', 7292), ('ê', 7265), ('di', 7213), ('D', 7205),
                  ('to', 6922), ('1', 6843), ("'", 6714), ('l ', 6696), ('mo', 6676), ('P', 6661), ('é ', 6649),
                  ('e\r', 6630), ('bl', 6499), ('ée', 6470), ('sa', 6409), ('pl', 6404), ('at', 6377), ('vo', 6367),
                  ('ta', 6183), ('li', 6137), ('da', 6006), (' à', 5988), ('rs', 5868), ('no', 5847), ('j', 5790),
                  ('rt', 5732), ('lu', 5693), ('s\r', 5535), ('av', 5515), ('as', 5444), ('; ', 5370), ('om', 5338),
                  ('ré', 5186), ('mm', 5135), ('nc', 5110), (' i', 4998), (' b', 4974), ('fa', 4926), (' j', 4914),
                  ('z', 4901), ("'a", 4876), (' u', 4875), ('su', 4740), ('ca', 4652), ('io', 4642), ('té', 4555),
                  (',', 4485), ('T', 4481), ('R', 4468), ('N', 4442), ("'e", 4425), ('O', 4292), ('dé', 4278),
                  ('ni', 4245), ('ho', 4122), ('je', 4071), (' o', 4067), ('t\r', 3644), ('os', 3636), ('B', 3624),
                  ('2', 3521), (':', 3517), ("l'", 3514), ('uv', 3460), ('ec', 3383), ('J', 3088), ('V', 3048),
                  ('nn', 2935), ('0', 2858), ('5', 2725), ('â', 2583), ('H', 2419), ('4', 2402), ('G', 2360),
                  ('id', 2283), ('U', 2260), ('3', 2237), ("'i", 2141), ('!', 2128), ('ç', 2111), ('8', 1990),
                  ('9', 1971), ('6', 1960), ('7', 1956), ('F', 1922), ('î', 1887), ("u'", 1848), ('ô', 1821),
                  ('«', 1561), ('k', 1463), ('ù', 1432), ('?', 1428), ('à', 1409), ('û', 1377), (')', 1332),
                  ('»', 1315), ('(', 1308), (']', 1234), ('[', 1233), ('Q', 1182), ('É', 1096), ('X', 823), ('w', 714),
                  (';', 712), ('K', 696), ('ï', 679), ('*', 524), ('Y', 253), ('Z', 231), ('q', 228), ('W', 220),
                  ('°', 218), ('È', 215), ('º', 185), ('ë', 145), ('\n\r', 140), ('/', 86), ('À', 81), ('Ê', 52),
                  ('—', 34), ('Ç', 24), ('%', 10), ('…', 8), ('Â', 3), ('Î', 3), ('\r', 0), ('”', 0), ('\ufeff', 0),
                  ('$', 0), ('‘', 0), ('•', 0), ('#', 0), ('™', 0), ('“', 0)]


# Code pour générer un corpus de langue française
def generate_corpus():
    # Liste d'URLs pour le Corpus
    url_list = ["https://www.gutenberg.org/ebooks/13846.txt.utf-8",
                "https://www.gutenberg.org/ebooks/4650.txt.utf-8",
                "https://www.gutenberg.org/ebooks/69794.txt.utf-8",
                "https://www.gutenberg.org/ebooks/39331.txt.utf-8",
                "https://www.gutenberg.org/ebooks/67924.txt.utf-8",
                "https://www.gutenberg.org/ebooks/72071.txt.utf-8",
                "https://www.gutenberg.org/ebooks/55639.txt.utf-8",
                "https://www.gutenberg.org/ebooks/66894.txt.utf-8",
                "https://www.gutenberg.org/ebooks/15212.txt.utf-8",
                "https://www.gutenberg.org/ebooks/15212.txt.utf-8",
                "https://www.gutenberg.org/ebooks/11046.txt.utf-8",
                "https://www.gutenberg.org/ebooks/67867.txt.utf-8",
                "https://www.gutenberg.org/ebooks/55637.txt.utf-8",
                "https://www.gutenberg.org/ebooks/55766.txt.utf-8",
                "https://www.gutenberg.org/ebooks/66261.txt.utf-8",
                "https://www.gutenberg.org/ebooks/71208.txt.utf-8"]

    # Ajouter le contenu des URLs dans le Corpus
    corpus = ""

    for (i, url_i) in enumerate(url_list):
        # Retire la partie anglophone au début de chaque texte
        text = load_text_from_web(url_i).strip().split(" ***")[1]
        corpus = corpus + text

    return corpus


# Code utilisé pour obtenir la liste de symbole triée par ordre de fréquence
def find_symbol_frequency():
    french_txt = generate_corpus()[:]

    # Compteur de fréquence
    frequencies = {symbol: 0 for symbol in symbols}

    i = 0

    while i < len(french_txt):
        # Vérifier les paires de caractères
        if i + 1 < len(french_txt):
            pair = french_txt[i] + french_txt[i + 1]
            if pair in frequencies:
                frequencies[pair] += 1
                i += 2  # Sauter les deux caractères utilisés
                continue

        # Vérifier le caractère seul
        if french_txt[i] in frequencies:
            frequencies[french_txt[i]] += 1

        i += 1

    sorted_symbols = sorted(frequencies.items(), key=lambda item: item[1], reverse=True)

    return sorted_symbols


# Code pour déchiffrer le cryptogramme C
def decrypt(C):
    M = ""

    # Étape 1: Séparer C en chunks de 8 bits
    chunks = [C[i:i + 8] for i in range(0, len(C), 8)]

    # Étape 2: Compter la fréquence de chaque chunk
    frequency_count = Counter(chunks)
    sorted_chunks = [chunk for chunk, _ in frequency_count.most_common()]

    # Étape 3: Créer un dictionnaire basé sur la fréquence des chunks et des symboles
    inverted_mapping = dict(zip(sorted_chunks, [symbol for symbol, _ in sorted_symbols]))
    # print(inverted_mapping)

    # Étape 4: Décoder le message
    M = ''.join([inverted_mapping[chunk] for chunk in chunks])

    return M


# TODO: REMOVE! THIS IS FOR TESTING
M = generate_corpus()[50000:150000]
K = gen_key(symbols)
C = chiffrer(M, K, symbols)
D = decrypt(C)

# print("M: ", M)
# print("D: ", D)

# print(K)

# one_char_symbols = [(symbol, count) for symbol, count in sorted_frequencies if len(symbol) == 1]
# two_char_symbols = [(symbol, count) for symbol, count in sorted_frequencies if len(symbol) == 2]
