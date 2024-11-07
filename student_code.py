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
sorted_symbols = [(' ', 128345), ('\r\n', 67477), ('e ', 64833), ('s ', 53863), (', ', 45957), ('_', 39582),
                  ('t ', 39556), (' d', 37276), ('es', 34060), ('le', 31753), ('a', 31035), ('de', 29506),
                  ('re', 28817), (' l', 28544), ('g', 28282), ('é', 27891), ('on', 25743), ('en', 24733), ('ou', 23631),
                  ('ai', 23618), ('. ', 23525), ('c', 23231), ('r', 23116), ('qu', 23044), ('u', 22796), ('i', 22555),
                  ('nt', 21619), ('d', 20663), ('an', 20491), ('’', 20397), ('.', 20150), (' p', 20091), ('-', 19803),
                  ('n', 19464), ('l', 19462), ('e', 18963), ('te', 18375), ('me', 18348), ('f', 17879), ('m', 17662),
                  (' s', 17491), ('ur', 17323), (' c', 17037), ('t', 16955), ('b', 16902), (' e', 16820), ('p', 16209),
                  ('la', 15746), ('er', 15481), ('et', 15302), ('s', 15133), ('v', 15100), ('o', 15060), ('ie', 14856),
                  ('in', 14723), ('ra', 14668), ('is', 14616), ('n ', 14602), ('r ', 14424), (' a', 14305),
                  ('\n', 14263), ('il', 14194), ('it', 14027), ('h', 13601), ('ce', 13432), ('x', 13350), ('a ', 13179),
                  ('ar', 13115), ('au', 12876), ('se', 12785), ('co', 12667), ('ne', 12648), ('tr', 12236),
                  ('us', 11985), ('ns', 11901), ('pa', 11472), ('è', 11106), ('ch', 10936), ('ri', 10809),
                  (' m', 10771), ('un', 10723), ('u ', 10583), ('ue', 10545), ('ui', 10459), ('oi', 10452),
                  (' q', 10402), ('eu', 10389), ('L', 10118), ('ti', 9981), ('ma', 9595), ('po', 9385), ('s,', 9358),
                  ('ve', 9112), ('M', 9042), ('C', 8994), ('pr', 8954), ('y', 8749), ('i ', 8694), ('or', 8569),
                  ('E', 8461), (' t', 8440), (' f', 8352), ('A', 8006), ('ll', 7808), ('ut', 7720), ('ét', 7710),
                  ('à ', 7645), ('so', 7610), ('el', 7491), ('ro', 7353), ('S', 7329), ('ss', 7278), ('e,', 7243),
                  (' n', 7211), ('ir', 7189), (' v', 7157), (' r', 7053), ('pe', 7016), ('nd', 6959), ('em', 6864),
                  ('I', 6832), ('si', 6814), ('1', 6790), ('D', 6533), ('di', 6527), ('st', 6519), ('P', 6501),
                  ('to', 6475), ('ê', 6162), ('é ', 6129), ('sa', 6084), ('mo', 6053), ('l ', 5998), ('pl', 5938),
                  ('li', 5900), ('bl', 5898), ('e\r', 5880), ('at', 5871), ('ée', 5860), ('ta', 5823), ("'", 5809),
                  ('da', 5784), (' à', 5660), ('vo', 5640), ('rs', 5588), ('rt', 5278), ('av', 5257), ('j', 5216),
                  ('lu', 5214), ('no', 5141), ('s\r', 5108), ('om', 4986), ('as', 4980), (' b', 4822), ('ré', 4797),
                  ('mm', 4784), ('; ', 4782), ('z', 4651), ('nc', 4472), (' u', 4447), ('fa', 4403), ('su', 4396),
                  (' i', 4389), ('io', 4339), ('ca', 4300), ('R', 4248), (',', 4235), ('N', 4122), ('T', 4122),
                  (' j', 4098), ('té', 4044), ('ni', 4004), ('O', 3872), ("'a", 3868), ('dé', 3782), ('ho', 3644),
                  (' o', 3625), ('B', 3547), ('2', 3517), ('t\r', 3275), ("'e", 3271), (':', 3193), ('uv', 3159),
                  ('je', 3106), ('ec', 3102), ('os', 3010), ('J', 2983), ('V', 2956), ("l'", 2908), ('0', 2852),
                  ('5', 2711), ('nn', 2627), ('â', 2512), ('4', 2386), ('H', 2372), ('G', 2315), ('3', 2229),
                  ('!', 2125), ('U', 2113), ('8', 1986), ('9', 1963), ('7', 1951), ('id', 1942), ('6', 1940),
                  ('F', 1888), ('ç', 1804), ('î', 1745), ('ô', 1728), ("'i", 1552), ('«', 1499), ('k', 1463),
                  ('ù', 1365), ("u'", 1352), ('û', 1314), ('?', 1308), (')', 1304), ('(', 1280), ('»', 1258),
                  ('à', 1218), (']', 1162), ('[', 1161), ('Q', 1121), ('É', 989), ('X', 787), ('w', 714), ('K', 680),
                  ('ï', 675), (';', 660), ('*', 414), ('Y', 247), ('Z', 230), ('q', 223), ('W', 220), ('°', 218),
                  ('º', 185), ('È', 177), ('\n\r', 145), ('ë', 144), ('/', 85), ('À', 78), ('Ê', 35), ('—', 34),
                  ('Ç', 23), ('%', 10), ('…', 8), ('Â', 3), ('\r', 0), ('”', 0), ('\ufeff', 0), ('$', 0), ('Î', 0),
                  ('‘', 0), ('•', 0), ('#', 0), ('™', 0), ('“', 0)]


# Code pour générer un corpus de langue française
def generate_corpus():
    # List of URLs for the Corpus
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

    # Add URLs to the Corpus
    corpus = ""

    for (i, url_i) in enumerate(url_list):
        text = load_text_from_web(url_i).strip().split("***")[2]  # Retire la partie anglophone au début de chaque texte
        corpus = corpus + text

    return corpus


# Code utilisé pour obtenir la liste de symbole triée par ordre de fréquence
def find_symbol_frequency():
    french_txt = generate_corpus[:]

    # Compteur de fréquence
    frequencies = {symbol: 0 for symbol in symbols}

    i = 0

    while i < len(french_txt):
        # Vérifie les paires de caractères
        if i + 1 < len(french_txt):
            pair = french_txt[i] + french_txt[i + 1]
            if pair in frequencies:
                frequencies[pair] += 1
                i += 2  # Sauter les deux caractères utilisés
                continue

        # Vérifie le caractère seul
        if french_txt[i] in frequencies:
            frequencies[french_txt[i]] += 1

        i += 1

    sorted_symbols = sorted(frequencies.items(), key=lambda item: item[1], reverse=True)

    # Output the sorted list
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

    # Étape 4: Décoder le message
    M = ''.join([inverted_mapping[chunk] for chunk in chunks])

    return M


# TODO: REMOVE! THIS IS FOR TESTING
M = generate_corpus()[0:10000]
K = gen_key(symbols)
C = chiffrer(M, K, symbols)
D = decrypt(C)

print("M: ", M)
print("D: ", D)

# one_char_symbols = [(symbol, count) for symbol, count in sorted_frequencies if len(symbol) == 1]
# two_char_symbols = [(symbol, count) for symbol, count in sorted_frequencies if len(symbol) == 2]
