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
sorted_symbols = [('e ', 65584), ('\r\n', 62873), ('s ', 51220), (', ', 45178), ('t ', 38458), (' d', 34708),
                  (' ', 32875), ('es', 31826), ('le', 29938), ('re', 27784), ('de', 27705), (' l', 27020), ('a', 26914),
                  ('g', 25945), ('é', 25637), ('on', 25053), ('en', 24195), ('qu', 24055), ('ou', 23164), ('c', 22213),
                  ('ai', 22170), ('r', 21993), ('nt', 21467), ('u', 21399), ('i', 21317), ('. ', 20252), (' p', 20080),
                  ('an', 19338), ('d', 18948), ('n', 18786), ('-', 18684), ('me', 18666), ('e', 18080), ('te', 17991),
                  ('.', 17711), (' c', 17445), (' s', 17358), ('f', 17239), ('l', 16946), (' e', 16671), ('m', 16509),
                  ('ur', 16106), ('t', 15969), ('’', 15857), ('b', 15428), ('et', 15337), ('p', 15102), ('ie', 14874),
                  ('er', 14821), ('in', 14679), ('la', 14664), ('is', 14579), ('s', 14321), ('n ', 14232), ('v', 14219),
                  (' a', 14131), ('o', 14011), ('\n', 14006), ('r ', 14005), ('il', 13890), ('ce', 13711),
                  ('ra', 13667), ('it', 13583), ('se', 13018), ('x', 12861), ('co', 12600), ('au', 12299),
                  ('a ', 12295), ('ne', 12150), ('tr', 12019), (' q', 11936), ('ns', 11782), ('ar', 11766),
                  ('us', 11753), ('h', 11674), ('oi', 11534), ('ue', 11468), ('pa', 11200), (' m', 10776),
                  ('un', 10496), ('ui', 10415), ('ch', 10389), ('u ', 10206), ('eu', 10119), ('è', 9986), ('ri', 9825),
                  ('ma', 9430), ('i ', 9356), ('s,', 9185), ('ti', 9043), ('ve', 9013), ('pr', 8954), ('po', 8825),
                  ('L', 8659), (' n', 8247), (' t', 8190), ('M', 8036), ('y', 7990), (' f', 7950), ('C', 7926),
                  ('ut', 7915), ('E', 7897), ('el', 7872), ('or', 7719), ('so', 7701), ('ll', 7617), ('ss', 7406),
                  ('e,', 7374), ('ir', 7321), ('ét', 7244), (' v', 7073), ('ro', 7066), ('à ', 7047), ('em', 6948),
                  ('pe', 6924), ('si', 6849), ('ê', 6757), (' r', 6708), ("'", 6698), ('nd', 6649), ('st', 6576),
                  ('A', 6568), ('di', 6465), ('D', 6264), ('l ', 6240), ('to', 6144), ('vo', 6132), ('mo', 6082),
                  ('e\r', 5996), ('bl', 5974), ('S', 5965), ('sa', 5806), ('é ', 5773), ('1', 5670), ('at', 5620),
                  ('I', 5514), ('pl', 5499), (' à', 5424), ('da', 5401), ('P', 5399), ('_', 5370), ('no', 5341),
                  ('rs', 5319), ('lu', 5241), ('li', 5139), ('j', 5136), ('; ', 5130), ('ta', 5045), ('av', 5041),
                  ('ée', 5030), ('rt', 4891), ("'a", 4876), ('as', 4849), ('mm', 4848), ('s\r', 4788), ('om', 4744),
                  ('nc', 4723), (' j', 4707), ('ré', 4622), ('fa', 4585), (' b', 4468), (' i', 4452), ("'e", 4419),
                  (' u', 4413), (',', 4375), ('z', 4183), ('ca', 4162), ('su', 4106), ('io', 4087), ('je', 3953),
                  ('té', 3904), ('ho', 3849), ('dé', 3825), ('N', 3818), ('R', 3813), ('ni', 3661), ("l'", 3531),
                  ('T', 3526), (' o', 3515), ('O', 3465), (':', 3228), ('t\r', 3222), ('os', 3011), ('uv', 3008),
                  ('ec', 3002), ('2', 2935), ('J', 2847), ('B', 2774), ('nn', 2697), ('V', 2665), ('â', 2379),
                  ('0', 2359), ('5', 2247), ("'i", 2147), ('!', 2122), ('id', 2118), ('G', 1980), ('ç', 1953),
                  ('4', 1901), ("u'", 1843), ('H', 1813), ('U', 1812), ('3', 1795), ('F', 1791), ('î', 1755),
                  ('9', 1609), ('6', 1555), ('ô', 1541), ('7', 1510), ('?', 1422), ('8', 1416), ('«', 1343),
                  ('à', 1290), ('û', 1262), ('ù', 1262), ('»', 1105), ('Q', 1032), ('k', 973), ('[', 963), (']', 963),
                  ('É', 778), ('w', 701), ('X', 685), (';', 649), (')', 599), ('(', 575), ('ï', 366), ('K', 241),
                  ('°', 217), ('q', 212), ('W', 211), ('È', 186), ('Z', 146), ('\n\r', 145), ('ë', 133), ('Y', 101),
                  ('/', 86), ('À', 79), ('*', 52), ('Ê', 51), ('—', 34), ('Ç', 23), ('%', 10), ('º', 10), ('…', 8),
                  ('Â', 3), ('Î', 3), ('\r', 0), ('”', 0), ('\ufeff', 0), ('$', 0), ('‘', 0), ('•', 0), ('#', 0),
                  ('™', 0), ('“', 0)]


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

    # Retirer les symboles non-présents dans la liste (principalement pour les tests)
    corpus = re.sub(r'[Œœ\xa0ÔË&üανάγκη}>æ=§|<+Ûòβοῦςπόρ′]', '', corpus)

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
    print("Nombre d'erreurs de substitution: {0}/{1} ({2}%)".format(nb_errors, len(K_pred),
                                                                    nb_errors / len(K_pred) * 100))


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
M = generate_corpus()[:]
C = chiffrer(M, K, symbols)
D = decrypt(C)

# print("M: ", M)
# print("D: ", D)

# print(find_symbol_frequency())
