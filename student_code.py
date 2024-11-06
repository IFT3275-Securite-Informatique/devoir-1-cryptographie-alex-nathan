from crypt import load_text_from_web, gen_key, chiffrer
from collections import Counter

url = "https://www.gutenberg.org/ebooks/13846.txt.utf-8"  # Example URL (replace with your desired URL)
corpus = load_text_from_web(url).strip()
url = "https://www.gutenberg.org/ebooks/4650.txt.utf-8"  # Example URL (replace with your desired URL)
corpus = corpus + load_text_from_web(url).strip()
url = "https://www.gutenberg.org/ebooks/69794.txt.utf-8"
corpus = corpus + load_text_from_web(url).strip()
url = "https://www.gutenberg.org/ebooks/39331.txt.utf-8"
corpus = corpus + load_text_from_web(url).strip()
url = "https://www.gutenberg.org/ebooks/67924.txt.utf-8"
corpus = corpus + load_text_from_web(url).strip()
url = "https://www.gutenberg.org/ebooks/72071.txt.utf-8"
corpus = corpus + load_text_from_web(url).strip()
url = "https://www.gutenberg.org/ebooks/55639.txt.utf-8"
corpus = corpus + load_text_from_web(url).strip()
url = "https://www.gutenberg.org/ebooks/66894.txt.utf-8"
corpus = corpus + load_text_from_web(url).strip()
url = "https://www.gutenberg.org/ebooks/15212.txt.utf-8"
corpus = corpus + load_text_from_web(url).strip()
url = "https://www.gutenberg.org/ebooks/11046.txt.utf-8"
corpus = corpus + load_text_from_web(url).strip()
url = "https://www.gutenberg.org/ebooks/67867.txt.utf-8"
corpus = corpus + load_text_from_web(url).strip()
url = "https://www.gutenberg.org/ebooks/55637.txt.utf-8"
corpus = corpus + load_text_from_web(url).strip()
url = "https://www.gutenberg.org/ebooks/55766.txt.utf-8"
corpus = corpus + load_text_from_web(url).strip()
url = "https://www.gutenberg.org/ebooks/66261.txt.utf-8"
corpus = corpus + load_text_from_web(url).strip()
url = "https://www.gutenberg.org/ebooks/71208.txt.utf-8"
corpus = corpus + load_text_from_web(url).strip()

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

# code utilisé pour obtenir la liste par ordre de fréquence
"""
french_txt = corpus[:]

# Compteur de fréquence
frequencies = {symbol: french_txt.count(symbol) for symbol in symboles}

# Arrangement de la liste en ordre descendant
sorted_symbols = sorted(frequencies, key=frequencies.get, reverse=True)

# Output the sorted list
print(sorted_symbols)
"""

# Liste de symboles paf leurs fréquences dans le corpus
sorted_symbols = [' ', 'e', 's', 'a', 't', 'i', 'n', 'r', 'u', 'o', 'l', 'e ', 'd', 'c', 's ', 'm', 'p', '\r', '\n',
                  '\r\n', 't ', ' d', 'es', ',', ' l', 'é', 'en', ', ', 'le', 'de', 're', 'nt', 'on', ' p', 'v', 'ou',
                  '.', ' c', 'ai', ' e', ' s', 'q', 'qu', 'an', 'n ', 'f', 'h', 'it', 'te', ' a', 'er', 'is', 'g', 'ur',
                  'r ', 'b', 'me', 'la', 'et', 'in', 'se', 'a ', ' q', 'ue', ' m', 'ne', 'ie', 'ar', 'ns', 'eu', 'ce',
                  ' t', '. ', 'co', '_', "'", 'tr', 'ra', 'oi', 'us', '’', 'il', 'ui', 'ti', 'i ', 'pa', 'au', 'or',
                  ' n', 'ri', 'ut', 'e,', ' f', 'un', 'll', 'st', 'u ', '-', ' r', 'el', 's,', 'j', 'ro', 'em', 'nd',
                  'ta', 'ma', 'ch', ' v', 'so', '\n\r', 've', 'ss', 'ir', 'à', 'e\r', 'po', 'y', 'pr', 'x', 'l ', 'si',
                  'to', 'om', 'à ', ' i', 'sa', 'at', ' o', ' à', 'di', 'pe', 'rt', 'è', 'io', 'nc', 'rs', 'as', 'lu',
                  ' u', 'vo', 'no', ' j', 'mo', 'li', ' b', 'E', 'av', 'da', 's\r', 'pl', 'L', 'é ', 'ec', 'C', 'ét',
                  'M', 'su', 'I', 'té', 'A', 'ni', 'ré', 'mm', 'je', 'ée', 'S', 'P', 'os', 'nn', 'fa', 't\r', 'ê', 'D',
                  'bl', 'dé', 'uv', 'ca', ';', 'ho', "l'", '1', "'a", 'T', "'e", '; ', 'w', 'R', 'N', 'O', 'z', "u'",
                  'id', ':', 'G', 'k', 'B', "'i", 'J', 'U', 'V', 'â', '2', 'F', 'H', '!', '0', '5', 'ç', 'î', '4', '3',
                  'ô', '8', '«', '6', '7', '9', ')', '?', 'ù', '(', 'û', '»', ']', '[', 'Q', 'É', '™', 'X', 'K', '*',
                  'Y', 'ï', 'W', 'È', 'º', 'Z', '”', '“', '/', 'ë', '°', 'À', '—', '•', 'Ê', '$', 'Ç', '%', '\ufeff',
                  '‘', '#', '…', 'Î', 'Â']


def decrypt(C):
    M = ""
    # entrez votre code ici.
    # Vous pouvez créer des fonctions auxiliaires et adapter le code à votre façon mais decrypt dois renvoyer le message décrypté
    # Step 1: Separate C into 8-bit chunks
    chunks = [C[i:i + 8] for i in range(0, len(C), 8)]

    # Step 2: Count frequency of each chunk
    frequency_count = Counter(chunks)

    # Step 3: Sort chunks by frequency in descending order
    sorted_chunks = [chunk for chunk, _ in frequency_count.most_common()]

    # Step 4: Map sorted symbols to sorted chunks
    mapping = {symbol: chunk for symbol, chunk in zip(sorted_symbols, sorted_chunks)}

    # Invert mapping for deciphering (chunk -> symbol)
    inverted_mapping = {v: k for k, v in mapping.items()}

    # Step 5: Decipher C using the mapping
    M = ''.join(inverted_mapping.get(chunk, '') for chunk in chunks)
    return M

M = corpus[10000:10100]

print(M)
K = gen_key(symboles)
C = chiffrer(M, K, symboles)
D = decrypt(C)
print(D)