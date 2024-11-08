from crypt import load_text_from_web, gen_key, chiffrer
from collections import Counter
import re

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

# Clé pour tester
K = gen_key(symbols)  # TODO: REMOVE WHEN TESTS ARE DONE

# Liste de symboles paf leurs fréquences dans le corpus
sorted_symbols = [('e ', 73170), ('\r\n', 71828), ('s ', 58454), (', ', 48803), ('t ', 43032), (' d', 39881),
                  (' ', 38737), ('es', 36856), ('le', 33815), ('a', 32326), ('de', 31688), ('re', 31037), (' l', 30439),
                  ('é', 29648), ('g', 29601), ('on', 28312), ('en', 27483), ('qu', 27132), ('ou', 25347), ('c', 25304),
                  ('ai', 24612), ('u', 24463), ('r', 24408), ('i', 24359), ('nt', 24221), ('. ', 23502), (' p', 22454),
                  ('an', 21941), ('d', 21842), ('n', 21029), ('-', 20634), ('.', 20462), ('me', 20436), ('’', 20397),
                  ('l', 20391), ('te', 20342), ('e', 20268), ('f', 19486), (' c', 19377), (' s', 19153), ('m', 19071),
                  (' e', 18666), ('ur', 18425), ('t', 17983), ('b', 17696), ('p', 17391), ('la', 16969), ('et', 16792),
                  ('er', 16458), ('ie', 16358), ('in', 16343), ('s', 16340), ('is', 16137), ('n ', 16029), ('o', 15815),
                  ('\n', 15814), ('v', 15807), ('r ', 15715), (' a', 15664), ('ra', 15439), ('ce', 15274),
                  ('it', 15116), ('il', 15102), ('se', 14395), ('x', 14331), ('co', 14233), ('a ', 13987),
                  ('ar', 13916), ('h', 13840), ('ne', 13812), ('au', 13804), ('tr', 13740), ('us', 13146),
                  ('ns', 13141), (' q', 12743), ('pa', 12682), ('ue', 12260), ('oi', 12159), ('ch', 11810),
                  ('un', 11804), (' m', 11781), ('è', 11735), ('ui', 11643), ('u ', 11467), ('ri', 11356),
                  ('eu', 11103), ('ti', 10973), ('ma', 10444), ('po', 10302), ('L', 10293), ('i ', 10198), ('s,', 9988),
                  ('pr', 9905), ('ve', 9835), ('M', 9416), ('y', 9362), ('C', 9311), ('or', 9280), ('E', 9275),
                  (' t', 9065), (' f', 8833), ('ut', 8705), (' n', 8682), ('el', 8565), ('ll', 8499), ('so', 8444),
                  ('A', 8211), ('à ', 8164), ('ét', 8144), ('ss', 8046), ('ir', 8025), ('pe', 7913), ('e,', 7906),
                  ('ro', 7904), ('em', 7802), ('S', 7670), ('si', 7640), (' v', 7594), ('st', 7593), (' r', 7545),
                  ('nd', 7470), ('I', 7292), ('ê', 7265), ('di', 7220), ('D', 7205), ('to', 6937), ('1', 6843),
                  ('mo', 6709), ("'", 6705), ('l ', 6682), ('P', 6661), ('é ', 6639), ('e\r', 6633), ('_', 6570),
                  ('bl', 6504), ('ée', 6470), ('sa', 6418), ('pl', 6415), ('vo', 6379), ('at', 6375), ('ta', 6184),
                  ('li', 6135), ('da', 6037), (' à', 5958), ('rs', 5876), ('no', 5861), ('j', 5802), ('rt', 5747),
                  ('lu', 5696), ('s\r', 5536), ('av', 5524), ('as', 5444), ('; ', 5368), ('om', 5324), ('ré', 5189),
                  ('mm', 5145), ('nc', 5114), (' b', 4940), ('fa', 4933), ('z', 4901), (' j', 4890), ("'a", 4876),
                  (' u', 4866), (' i', 4775), ('su', 4750), (',', 4699), ('ca', 4661), ('io', 4641), ('té', 4558),
                  ('T', 4481), ('R', 4468), ('N', 4442), ("'e", 4419), ('O', 4292), ('dé', 4288), ('ni', 4251),
                  ('ho', 4120), ('je', 4083), (' o', 4019), ('t\r', 3645), ('os', 3631), ('B', 3624), ("l'", 3531),
                  ('2', 3521), (':', 3517), ('uv', 3462), ('ec', 3389), ('J', 3088), ('V', 3048), ('nn', 2933),
                  ('0', 2858), ('5', 2725), ('â', 2583), ('id', 2462), ('H', 2419), ('4', 2402), ('G', 2360),
                  ('U', 2260), ('3', 2237), ("'i", 2144), ('!', 2128), ('ç', 2111), ('8', 1990), ('9', 1971),
                  ('6', 1960), ('7', 1956), ('F', 1922), ('î', 1887), ("u'", 1843), ('ô', 1821), ('«', 1561),
                  ('k', 1463), ('ù', 1432), ('?', 1428), ('à', 1413), ('û', 1377), (')', 1332), ('»', 1315),
                  ('(', 1308), (']', 1234), ('[', 1233), ('Q', 1182), ('É', 1096), ('X', 823), ('w', 714), (';', 714),
                  ('K', 696), ('ï', 679), ('*', 524), ('Y', 253), ('Z', 231), ('q', 228), ('W', 220), ('°', 218),
                  ('È', 215), ('º', 185), ('ë', 145), ('\n\r', 145), ('/', 86), ('À', 81), ('Ê', 52), ('—', 34),
                  ('Ç', 24), ('%', 10), ('…', 8), ('Â', 3), ('Î', 3), ('\r', 0), ('”', 0), ('\ufeff', 0), ('$', 0),
                  ('‘', 0), ('•', 0), ('#', 0), ('™', 0), ('“', 0)]

# one_char_symbols = [(symbol, count) for symbol, count in sorted_symbols if len(symbol) == 1]
# two_char_symbols = [(symbol, count) for symbol, count in sorted_symbols if len(symbol) == 2]


# Générer un corpus de langue française
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

    # Retirer les symboles sur-représentés
    corpus = re.sub(r' {2,}', '', corpus)
    corpus = re.sub(r'_{2,}', '', corpus)
    corpus = re.sub(r'\.{4,}', '', corpus)
    corpus = re.sub(r'\*{2,}', '', corpus)

    return corpus


# Obtenir la liste de symbole triée par ordre de fréquence
def find_symbol_frequency():
    french_txt = generate_corpus()[:]

    # Compter les fréquences
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


# Comparer la vraie clé de test K avec la clé prédite (Test seulement)
def compare_K(K, K_pred):
    inverted_K = {value: key for key, value in K.items()}
    sorted_K = {}

    nb_errors = 0

    for code, symbol in K_pred.items():
        sorted_K[code] = inverted_K[code]

        if sorted_K[code] != symbol:
            nb_errors += 1
        else:
            print("Succès! {0} = {1}".format(code, symbol))

    print("K: ", sorted_K)
    print("Prédiction de K: ", K_pred)
    print("Nombre d'erreurs de substitution: {0} ({1}%)".format(nb_errors, nb_errors / len(K) * 100))


# Divise un dictionnaire en blocs
def divide_dict(d, size=8):
    items = list(d.items())
    blocs = [dict(items[i:i + size]) for i in range(0, len(items), size)]

    return blocs

# Divise une liste en blocs
def divide_list(l, size=8):
    return [l[i:i + size] for i in range(0, len(l), size)]

# Code pour déchiffrer le cryptogramme C
def decrypt(C):
    # Étape 1: Séparer C en chunks de 8 bits
    chunks = [C[i:i + 8] for i in range(0, len(C), 8)]

    # Étape 2: Compter la fréquence de chaque chunk
    frequency_count = Counter(chunks)
    sorted_chunks = [chunk for chunk, _ in frequency_count.most_common()]

    # Étape 3: Créer un dictionnaire basé sur la fréquence des chunks et des symboles
    inverted_mapping = dict(zip(sorted_chunks, [symbol for symbol, _ in sorted_symbols]))
    compare_K(K, inverted_mapping)

    # Étape 4: Décoder le message
    M = ''.join([inverted_mapping[chunk] for chunk in chunks])

    return M


# TODO: REMOVE! THIS IS FOR TESTING
M = generate_corpus()[50000:250000]
C = chiffrer(M, K, symbols)
D = decrypt(C)

# print("M: ", M)
# print("D: ", D)

# print(find_symbol_frequency())
