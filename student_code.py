from crypt import load_text_from_web, gen_key, chiffrer
from collections import Counter

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

# Liste de symboles fixés
symboles = ['b', 'j', '\r', 'J', '”', ')', 'Â', 'É', 'ê', '5', 't', '9', 'Y', '%', 'N', 'B', 'V', '\ufeff', 'Ê', '?',
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

# Code utilisé pour obtenir la liste de symbole triée par ordre de fréquence
"""
french_txt = corpus[:]

# Compteur de fréquence
frequencies = {symbol: french_txt.count(symbol) for symbol in symboles}
sorted_frequencies = sorted(frequencies.items(), key=lambda item: item[1], reverse=True)

one_char_symbols = [(symbol, count) for symbol, count in sorted_frequencies if len(symbol) == 1]
two_char_symbols = [(symbol, count) for symbol, count in sorted_frequencies if len(symbol) == 2]

# Arrangement de la liste en ordre descendant
sorted_symbols = sorted(frequencies, key=frequencies.get, reverse=True)

# Output the sorted list
print(sorted_symbols)
"""

# Liste de symboles paf leurs fréquences dans le corpus
# sorted_symbols = [' ', 'e', 's', 'a', 'i', 'n', 't', 'r', 'u', 'l', 'o', 'e ', 'd', 's ', 'c', 'm', '\r', '\n', '\r\n',
#                    'p', ' d', 't ', 'es', ',', ', ', 'é', ' l', 'le', 'de', 'en', 're', 'nt', 'v', 'on', '.', 'ou',
#                    ' p', '_', 'ai', 'an', ' s', ' e', ' c', 'q', 'qu', 'n ', 'ur', 'it', 'f', 'er', 'te', ' a', 'is',
#                    'r ', 'g', 'h', 'b', 'et', 'la', 'me', 'a ', 'se', 'ie', 'in', 'ne', 'ue', '. ', 'ar', ' m', 'eu',
#                    'ns', ' q', 'ra', '’', 'ce', '-', 'co', 'il', 'us', 'tr', "'", 'au', 'oi', 'ui', 'e,', 'ri', ' t',
#                    'pa', 'i ', 's,', 'ti', 'll', ' r', ' f', 'un', ' n', 'u ', '\n\r', ' v', 'ut', 'à', 'ta', 'st',
#                    'or', 'el', 'ch', 've', 'ma', 'so', 'ir', 'ss', 'nd', 'em', 'x', 'po', 'à ', 'ro', 'e\r', 'j', 'pr',
#                    'sa', ' à', 'si', 'om', 'to', 'l ', 'è', 'rs', 'rt', 'at', 'L', 'li', 'as', ' b', 'lu', 'nc', 'av',
#                    'pe', 'vo', ' i', 'di', 'io', 'mo', ' u', 'da', 'no', 's\r', 'M', 'C', ' j', 'y', 'pl', 'E', 'é ',
#                    'ét', 'A', 'ré', ' o', 'té', 'su', 'mm', 'S', 'nn', 'ée', 'ni', 'I', '1', 'fa', 'D', 'P', 'uv', 'bl',
#                    'os', 'ê', 'dé', 't\r', 'ec', 'ca', ';', "l'", "'a", '; ', 'je', 'z', 'ho', 'R', 'N', 'T', "'e", 'O',
#                    'B', '2', "u'", 'id', ':', 'J', 'V', '0', '5', 'â', '4', "'i", 'H', 'G', '3', '!', 'U', '8', '9',
#                    '7', '6', 'F', 'ç', 'î', 'ô', '«', 'k', 'ù', 'û', '?', ')', '(', '»', ']', '[', 'Q', 'É', 'X', 'w',
#                    'K', 'ï', '*', 'Y', 'Z', 'W', '°', 'º', 'È', 'ë', '/', 'À', 'Ê', '—', 'Ç', '%', '…', 'Â', '”',
#                    '\ufeff', '$', 'Î', '‘', '•', '#', '™', '“']

sorted_symbols = [(' ', 680106), ('e', 450591), ('s', 245857), ('a', 226470), ('i', 211640), ('n', 209688),
                      ('t', 209206), ('r', 204770), ('u', 190642), ('l', 164662), ('o', 163383), ('e ', 142159),
                      ('d', 112439), ('s ', 94263), ('c', 89177), ('m', 83847), ('\r', 81885), ('\n', 81885),
                      ('\r\n', 81885), ('p', 79065), (' d', 74198), ('t ', 72060), ('es', 71084), (',', 66793),
                      (', ', 61091), ('é', 60213), (' l', 59323), ('le', 55053), ('de', 54005), ('en', 52900),
                      ('re', 48495), ('nt', 46531), ('v', 45425), ('on', 43803), ('.', 43675), ('ou', 43066),
                      (' p', 42978), ('_', 39582), ('ai', 39305), ('an', 37274), (' s', 37123), (' e', 36945),
                      (' c', 36296), ('q', 33669), ('qu', 33446), ('n ', 32569), ('ur', 32162), ('it', 31499),
                      ('f', 30634), ('er', 30395), ('te', 29004), (' a', 28918), ('is', 28835), ('r ', 28283),
                      ('g', 28282), ('h', 28181), ('b', 27622), ('et', 27336), ('la', 27112), ('me', 26810),
                      ('a ', 25491), ('se', 24726), ('ie', 24590), ('in', 23897), ('ne', 23664), ('ue', 23574),
                      ('. ', 23525), ('ar', 23259), (' m', 23226), ('eu', 23139), ('ns', 22994), (' q', 21694),
                      ('ra', 20559), ('’', 20397), ('ce', 20324), ('-', 19803), ('co', 19667), ('il', 19414),
                      ('us', 19301), ('tr', 19037), ("'", 18760), ('au', 18659), ('oi', 18632), ('ui', 18263),
                      ('e,', 18087), ('ri', 17591), (' t', 17537), ('pa', 17241), ('i ', 16966), ('s,', 16922),
                      ('ti', 16906), ('ll', 16685), (' r', 16189), (' f', 16012), ('un', 15483), (' n', 15311),
                      ('u ', 15308), ('\n\r', 15054), (' v', 14648), ('ut', 14629), ('à', 14523), ('ta', 14381),
                      ('st', 14226), ('or', 14158), ('el', 14042), ('ch', 13984), ('ve', 13955), ('ma', 13842),
                      ('so', 13760), ('ir', 13680), ('ss', 13602), ('nd', 13592), ('em', 13498), ('x', 13350),
                      ('po', 13286), ('à ', 12975), ('ro', 12608), ('e\r', 12567), ('j', 12420), ('pr', 12221),
                      ('sa', 12143), (' à', 11991), ('si', 11850), ('om', 11629), ('to', 11511), ('l ', 11191),
                      ('è', 11106), ('rs', 10934), ('rt', 10350), ('at', 10183), ('L', 10118), ('li', 9995),
                      ('as', 9945), (' b', 9776), ('lu', 9745), ('nc', 9661), ('av', 9644), ('pe', 9638), ('vo', 9577),
                      (' i', 9531), ('di', 9500), ('io', 9336), ('mo', 9305), (' u', 9262), ('da', 9228), ('no', 9113),
                      ('s\r', 9077), ('M', 9042), ('C', 8994), (' j', 8850), ('y', 8749), ('pl', 8546), ('E', 8461),
                      ('é ', 8442), ('ét', 8201), ('A', 8006), ('ré', 7889), (' o', 7859), ('té', 7811), ('su', 7724),
                      ('mm', 7474), ('S', 7329), ('nn', 7202), ('ée', 7016), ('ni', 6922), ('I', 6832), ('1', 6790),
                      ('fa', 6772), ('D', 6533), ('P', 6501), ('uv', 6364), ('bl', 6196), ('os', 6169), ('ê', 6162),
                      ('dé', 6153), ('t\r', 6031), ('ec', 5955), ('ca', 5770), (';', 5442), ("l'", 5114), ("'a", 4907),
                      ('; ', 4782), ('je', 4751), ('z', 4651), ('ho', 4582), ('R', 4248), ('N', 4122), ('T', 4122),
                      ("'e", 4042), ('O', 3872), ('B', 3547), ('2', 3517), ("u'", 3361), ('id', 3344), (':', 3193),
                      ('J', 2983), ('V', 2956), ('0', 2852), ('5', 2711), ('â', 2512), ('4', 2386), ("'i", 2377),
                      ('H', 2372), ('G', 2315), ('3', 2229), ('!', 2125), ('U', 2113), ('8', 1986), ('9', 1963),
                      ('7', 1951), ('6', 1940), ('F', 1888), ('ç', 1804), ('î', 1745), ('ô', 1728), ('«', 1499),
                      ('k', 1463), ('ù', 1365), ('û', 1314), ('?', 1308), (')', 1304), ('(', 1280), ('»', 1258),
                      (']', 1162), ('[', 1161), ('Q', 1121), ('É', 989), ('X', 787), ('w', 714), ('K', 680), ('ï', 675),
                      ('*', 414), ('Y', 247), ('Z', 230), ('W', 220), ('°', 218), ('º', 185), ('È', 177), ('ë', 144),
                      ('/', 85), ('À', 78), ('Ê', 35), ('—', 34), ('Ç', 23), ('%', 10), ('…', 8), ('Â', 3), ('”', 0),
                      ('\ufeff', 0), ('$', 0), ('Î', 0), ('‘', 0), ('•', 0), ('#', 0), ('™', 0), ('“', 0)]


def decrypt(C):
    M = ""

    one_char_symbols = [(symbol, count) for symbol, count in sorted_symbols if len(symbol) == 1]
    two_char_symbols = [(symbol, count) for symbol, count in sorted_symbols if len(symbol) == 2]

    # Step 1: Separate C into 8-bit chunks
    chunks = [C[i:i + 8] for i in range(0, len(C), 8)]

    # Step 2: Count frequency of each chunk
    frequency_count = Counter(chunks)
    sorted_chunks = list(frequency_count)

    # Step 3: Create a dictionary based on the frequency of each chunk, but give priority to pairs
    mapping = {sym: "" for sym, _ in sorted_symbols}

    position = 0

    for char, _ in one_char_symbols:
        for two_char, _ in two_char_symbols:
            if position >= len(sorted_chunks):
                break

            if char in two_char and mapping[two_char] == "":
                mapping[two_char] = sorted_chunks[position]
                position = position + 1

        if position >= len(sorted_chunks):
            break

        mapping[char] = sorted_chunks[position]
        position = position + 1

    # Step 4: Invert the resulting dictionary
    inverted_mapping = {value: key for key, value in mapping.items()}

    # Step 5: Decode message
    M = ''.join(inverted_mapping.get(code, '') for code in chunks)

    return M

M = corpus[10000:12000]
K = gen_key(symboles)
C = chiffrer(M, K, symboles)
D = decrypt(C)

print("M: ", M)
print("D: ", D)

