# MEMBRES DE L'ÉQUIPE (Nom - Matricule):
# Alexandre Stang - 20211138
# Nathan Bussière - 20218547
# Gabriel Hazan - 20198680

from crypt import load_text_from_web, gen_key, chiffrer
from collections import Counter
import re
import random as rnd
import math

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


#### ----- MÉTHODES DE TRAITEMENT DE TEXTE (PRÉ-UTILISÉS) ----- ####

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


# Diviser un texte en groupe de triplets de caractères
def cut_string_into_parts(text, size_parts):
    triplets = []

    for i in range(0, len(text) - 1, size_parts):
        triplets.append(text[i:i + size_parts])

    if len(text) % size_parts != 0:
        triplets.append(text[-1] + '_')

    return triplets


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

    frequencies = {symbol: count / (len(french_txt) // len(symbol)) for symbol, count in frequencies.items()}
    sorted_symbols = sorted(frequencies.items(), key=lambda x: x[1], reverse=True)

    return sorted_symbols


# Obtenir un dictionnaire des bi-caractères les plus communs (non inclus parmi les symboles)
def find_bigram_frequency(nb_bigrams):
    french_txt = generate_corpus()[:]

    bigrams = Counter(cut_string_into_parts(french_txt, 2)).most_common(nb_bigrams)
    bigrams = [(word, count / (len(french_txt) // 2)) for word, count in bigrams if word not in symbols]
    return dict(bigrams)


# Obtenir un dictionnaire des tri-caractères les plus communs triée par ordre de fréquence
def find_trigram_frequency(nb_trigrams):
    french_txt = generate_corpus()[:]

    trigrams = Counter(cut_string_into_parts(french_txt, 3)).most_common(nb_trigrams)
    trigrams = [(word, count / (len(french_txt) // 3)) for word, count in trigrams]
    return dict(trigrams)


# Obtenir un dictionnaire des mots les plus communs triée par ordre de fréquence (non utilisé au final)
def find_word_frequency(nb_words):
    french_txt = generate_corpus()[:]

    words = [word for word in french_txt.split() if len(word) > 2]
    words = Counter(words).most_common(nb_words)
    words = [(word, count / (len(french_txt) // 3)) for word, count in words]
    return dict(words)


# Obtenir un dictionnaire des voisins impossibles
def find_impossible_neighbors():
    one_char_symbols = [symbol for symbol, _ in sorted_symbols if len(symbol) == 1]
    two_char_symbols = [symbol for symbol, _ in sorted_symbols if len(symbol) == 2]

    impossible_neighbors = {}

    for symbol in one_char_symbols:
        neighbors = [word[1] for word in two_char_symbols if word.startswith(symbol)]
        neighbors.extend([word for word in two_char_symbols if (symbol + word[0]) in two_char_symbols])

        if len(neighbors) > 0:
            impossible_neighbors[symbol] = neighbors

    return impossible_neighbors


#### ----- VARIABLES GLOBALES (PRÉ-GÉNÉRÉES) ----- ####

# Clé pour tester
K = gen_key(symbols)  # TODO: REMOVE WHEN TESTS ARE DONE

# Liste de symboles ordonnés selon leurs fréquences dans le corpus
sorted_symbols = [('e ', 0.033419467206536324), ('\r\n', 0.032038030032882386), ('s ', 0.026100041325914713),
                  (', ', 0.023021235201526255), ('t ', 0.01959694239187872), (' d', 0.01768606470792362),
                  ('es', 0.01621749151188133), ('le', 0.015255428293932734), ('re', 0.014157820152268925),
                  ('de', 0.014117564329060271), (' l', 0.013768510672124474), ('on', 0.012766191630967224),
                  ('en', 0.012328982816878298), ('qu', 0.012257643383343975), ('ou', 0.011803618845636243),
                  ('ai', 0.011297108867542545), ('nt', 0.010938882997723762), ('. ', 0.010319758628122311),
                  (' p', 0.01023211303835157), ('an', 0.009854014040619655), ('me', 0.0095115847596549),
                  ('te', 0.009167626776542983), (' c', 0.00888940298575912), (' s', 0.008845070623491363),
                  (' e', 0.008494997831790788), (' ', 0.008376013848003183), ('ur', 0.008207092260741553),
                  ('et', 0.00781523494368516), ('ie', 0.007579305245639504), ('er', 0.0075522981743729395),
                  ('in', 0.007479939606073839), ('la', 0.007472296095338019), ('is', 0.007428982867835037),
                  ('n ', 0.0072521629861463915), (' a', 0.007200696680525201), ('r ', 0.00713649119034431),
                  ('il', 0.007077890941369687), ('ce', 0.00698667837992223), ('ra', 0.006964257415097157),
                  ('it', 0.006921453754976562), ('a', 0.006857248264795671), ('se', 0.006633548183927328),
                  ('g', 0.006610362868028672), ('é', 0.006531889491140916), ('co', 0.006420549018089133),
                  ('au', 0.006267169235990336), ('a ', 0.0062651309664607845), ('ne', 0.00619124369601452),
                  ('tr', 0.006124490368921689), (' q', 0.006082196276183483), ('ns', 0.006003722899295727),
                  ('ar', 0.005995569821177518), ('us', 0.005988945445206474), ('oi', 0.0058773501884634965),
                  ('ue', 0.005843718741225887), ('pa', 0.005707154682745895), ('c', 0.005659510132492615),
                  ('r', 0.005603457720429932), (' m', 0.005491098112613372), ('u', 0.005452116207860689),
                  ('i', 0.005431223945182779), ('un', 0.005348419245544725), ('ui', 0.005307144287571295),
                  ('ch', 0.005293895535629206), ('u ', 0.005200644704652198), ('eu', 0.005156312342384439),
                  ('ri', 0.005006499531962359), ('d', 0.004827641380744162), ('ma', 0.004805220415919089),
                  ('n', 0.004786366422770732), ('i ', 0.004767512429622375), ('-', 0.004760378486268943),
                  ('s,', 0.0046803764072340225), ('ti', 0.004608017838934922), ('e', 0.004606489136787758),
                  ('ve', 0.004592730817463282), ('pr', 0.004562666341902388), ('.', 0.004512473954737167),
                  ('po', 0.004496932149574333), ('f', 0.004392216052493594), ('l', 0.0043175644309737474),
                  ('m', 0.004206223957921964), (' n', 0.0042024022025540534), (' t', 0.004173356861757936),
                  ('t', 0.004068640764677197), (' f', 0.00405106068998481), ('’', 0.004040104991263467),
                  ('ut', 0.0040332258316012285), ('el', 0.0040113144341585435), ('or', 0.003933350624653176),
                  ('b', 0.003930802787741236), ('so', 0.003924178411770191), ('ll', 0.003881374751649597),
                  ('p', 0.003847743304411987), ('ss', 0.0037738560339657234), ('e,', 0.0037575498777293066),
                  ('ir', 0.003730542806462741), ('ét', 0.003691306118018863), ('s', 0.003648757241589463),
                  ('v', 0.0036227693050876735), (' v', 0.0036041700956305107), ('ro', 0.0036006031239537947),
                  ('à ', 0.003590921343688422), ('o', 0.003569774297319319), ('\n', 0.0035685003788633487),
                  ('em', 0.0035404741728320074), ('pe', 0.003528244555654695), ('si', 0.0034900270019755926),
                  (' r', 0.003418178001058881), ('nd', 0.0033881135254979875), ('st', 0.0033509151065836615),
                  ('di', 0.0032943531271385908), ('x', 0.003276773052446204), ('l ', 0.003179700466101285),
                  ('to', 0.003130781997392034), ('vo', 0.0031246671888033777), ('mo', 0.0030991888196839766),
                  ('e\r', 0.003055366024798606), ('bl', 0.00304415554238607), ('h', 0.0029743448109989102),
                  ('sa', 0.002958548222144881), ('é ', 0.002941732498526076), ('at', 0.002863768689020708),
                  ('pl', 0.002802111035751757), (' à', 0.002763893482072655), ('da', 0.0027521734322777307),
                  ('no', 0.002721599389334449), ('rs', 0.0027103889069219123), ('lu', 0.002670642651095646),
                  ('li', 0.0026186667780920677), ('; ', 0.0026140806716505754), ('ta', 0.002570767444147593),
                  ('av', 0.002568729174618041), ('ée', 0.002563123933411773), ('è', 0.0025442699402634158),
                  ('rt', 0.002492294067259837), ("'a", 0.0024846505565240167), ('as', 0.00247089223719954),
                  ('mm', 0.002470382669817152), ('s\r', 0.0024398086268738704), ('om', 0.0024173876620487973),
                  ('nc', 0.0024066867470186487), (' j', 0.0023985336689004402), ('ré', 0.002355220441397458),
                  ('fa', 0.002336366448249101), (' b', 0.002276747064509702), (' i', 0.0022685939863914934),
                  ("'e", 0.0022517782627726884), (' u', 0.0022487208584783605), ('L', 0.00220617198204896),
                  ('ca', 0.0021208194454989658), ('su', 0.0020922836720852363), ('io', 0.002082601891819864),
                  ('M', 0.00204744174243509), ('y', 0.0020357216926401656), ('C', 0.0020194155364037488),
                  ('je', 0.0020143198625798683), ('E', 0.0020120268093591223), ('té', 0.001989351060842855),
                  ('ho', 0.0019613248548115136), ('dé', 0.001949095237634201), ('ni', 0.0018655261869225646),
                  ("l'", 0.0017992824272121213), (' o', 0.0017911293490939127), ('ê', 0.0017215734013979471),
                  ("'", 0.0017065411636175004), ('A', 0.0016734192837622786), ('t\r', 0.001641826106054221),
                  ('D', 0.0015959650416392988), ('os', 0.0015343073883703475), ('uv', 0.0015327786862231834),
                  ('ec', 0.0015297212819288552), ('S', 0.0015197847179722888), ('1', 0.0014446235290700548),
                  ('I', 0.0014048772732437888), ('P', 0.0013755771487564772), ('nn', 0.001374303230300507),
                  ('_', 0.0013681884217118508), ('j', 0.0013085690379724517), (',', 0.0011146786489738077),
                  ("'i", 0.0010940411699870926), ('id', 0.00107926371589784), ('z', 0.0010657601802645572),
                  ('N', 0.0009727641329787424), ('R', 0.0009714902145227724), ("u'", 0.0009391326857411327),
                  ('T', 0.0008983672951500905), ('O', 0.0008828254899872557), (':', 0.0008224417551742746),
                  ('2', 0.0007477901336544287), ('J', 0.0007253691688293556), ('B', 0.0007067699593721926),
                  ('V', 0.0006789985370320451), ('â', 0.0006061304013505574), ('0', 0.0006010347275266771),
                  ('5', 0.0005724989541129477), ('!', 0.000540650992713696), ('G', 0.0005044717085641461),
                  ('ç', 0.0004975925489019078), ('4', 0.0004843437969598191), ('H', 0.0004619228321347459),
                  ('U', 0.0004616680484435519), ('3', 0.00045733672569325367), ('F', 0.0004563175909284776),
                  ('î', 0.00044714537804549316), ('9', 0.00040994695913116724), ('6', 0.0003961886398066905),
                  ('ô', 0.0003926216681299743), ('7', 0.0003847233737029599), ('?', 0.00036230240887788674),
                  ('8', 0.00036077370673072266), ('«', 0.0003421744972735597), ('à', 0.00032867096164027705),
                  ('û', 0.00032153701828684464), ('ù', 0.00032153701828684464), ('»', 0.00028153597876938457),
                  ('Q', 0.00026293676931222164), ('k', 0.00024790453153177483), ('[', 0.0002453566946198347),
                  (']', 0.0002453566946198347), ('É', 0.00019822171174894225), ('w', 0.00017860336752700324),
                  ('X', 0.00017452682846789904), (';', 0.00016535461558491458), (')', 0.0001526154310252139),
                  ('(', 0.00014650062243655757), ('ï', 9.325083097700883e-05), ('\n\r', 7.388727044626383e-05),
                  ('K', 6.140286957775718e-05), ('°', 5.5288060989100865e-05), ('q', 5.40141425331308e-05),
                  ('W', 5.375935884193678e-05), ('È', 4.7389766562086454e-05), ('Z', 3.719841891432593e-05),
                  ('ë', 3.3886230928803756e-05), ('Y', 2.5733152810595333e-05), ('/', 2.1911397442685134e-05),
                  ('À', 2.012791160432704e-05), ('*', 1.3248751942088686e-05), ('Ê', 1.2993968250894673e-05),
                  ('—', 8.662645500596449e-06), ('Ç', 5.860024897462304e-06), ('%', 2.5478369119401318e-06),
                  ('º', 2.5478369119401318e-06), ('…', 2.0382695295521057e-06), ('Â', 7.643510735820395e-07),
                  ('Î', 7.643510735820395e-07), ('\r', 0.0), ('”', 0.0), ('\ufeff', 0.0), ('$', 0.0), ('‘', 0.0),
                  ('•', 0.0), ('#', 0.0), ('™', 0.0), ('“', 0.0)]

# Dictionnaire de 256 tri-caractères ordonnés selon leurs fréquences dans le corpus
sorted_trigrams = {' de': 0.010197210270740862, 'es ': 0.009518466344467128, 'de ': 0.0075961229046265415,
                   ' qu': 0.006120924956756827, 'ent': 0.006016973184264454, 'nt ': 0.005965761649286592,
                   ' le': 0.005822827962109579, 'le ': 0.004878089794458301, 'que': 0.004701524651474931,
                   'e d': 0.004661778385521964, 'et ': 0.004511965536930014, ' et': 0.004325463827458402,
                   'e, ': 0.004162657007304905, ' la': 0.004100744554570476, 're ': 0.004010551104907976,
                   'it ': 0.003959339569930115, 'les': 0.00387220352534092, 'e l': 0.0038622669588526783,
                   's, ': 0.0038576808512427205, 'la ': 0.003817934585289754, 'ue ': 0.003768251752848546,
                   '\n\r\n': 0.003627611119476511, '\r\n\r': 0.003544296831228947, 'lle': 0.0033937196313686704,
                   'ne ': 0.0033830187136121024, 's d': 0.0033577951217573353, ' pa': 0.0032431424315083938,
                   ' co': 0.0032423780802400674, 'e\r\n': 0.003169764709749071, 'ns ': 0.003065048585988371,
                   'ait': 0.00302835972510871, 'our': 0.0029832630002774594, 'on ': 0.00296262551603265,
                   'e s': 0.002772302050219407, 'ant': 0.002766951591341123, 'e c': 0.0027608367811945127,
                   'ur ': 0.0027562506735845553, 't d': 0.0027432567020230086, '.\r\n': 0.002702746084801716,
                   'e p': 0.002700453030996737, ' à ': 0.0026721720340686646, 'us ': 0.0025965012585043635,
                   ' en': 0.002587329043284448, 'is ': 0.0025827429356744904, 'tre': 0.002562869802698007,
                   ' ce': 0.0025483471285998077, 'ais': 0.002518537429135083, 'en ': 0.0024184074129843408,
                   ' se': 0.0024061777926911204, 'men': 0.0023878333622512895, 'par': 0.002350380150103302,
                   'me ': 0.002327449612053514, 'eur': 0.002316748694296946, ' so': 0.0022594223491724753,
                   'ui ': 0.0022410779187326444, 'ans': 0.0022357274598543606, ' un': 0.0022204404344878348,
                   's l': 0.0021998029502430256, 'er ': 0.0021936881400964154, 's\r\n': 0.0021906307350231104,
                   'des': 0.002171521953314953, 'ion': 0.0021592923330217327, 'te ': 0.0021440053076552073,
                   't l': 0.0021302469848253343, ' au': 0.0021279539310203556, 'ien': 0.002124132174678724,
                   'ous': 0.002121074769605419, 'est': 0.0020690988833592322, ' po': 0.002068334532090906,
                   'ell': 0.0020515188041877277, 'qui': 0.0020476970478460962, ', e': 0.002024766509796308,
                   'il ': 0.0020178873483813714, ' ma': 0.0020064220793564774, 'tou': 0.00193610176267046,
                   's p': 0.0019276938987188709, 'res': 0.001920050386035608, 'ce ': 0.0018772467150093366,
                   'ont': 0.0018550805282278745, 'se ': 0.0018405578541296752, 'con': 0.0018023402907133613,
                   'son': 0.001793168075493446, 'e q': 0.001751893107003827, ' to': 0.0017511287557355009,
                   'ons': 0.0017320199740273438, 'eme': 0.0017297269202223651, 'ire': 0.001718261651197471,
                   'e e': 0.0017174972999291446, ' pr': 0.0017067963821725768, 't p': 0.0016922737080743776,
                   's c': 0.0016724005750978943, 'une': 0.0016647570624146316, 'pou': 0.0016517630908530847,
                   ' mo': 0.0016402978218281905, 'e m': 0.0016349473629499068, 'un ': 0.001618895986315055,
                   ' sa': 0.001605137663485182, 'es,': 0.0016020802584118768, 's e': 0.0015982585020702454,
                   'out': 0.0015936723944602878, 'mme': 0.0015929080431919614, ' re': 0.0015791497203620885,
                   's s': 0.0015485756696290375, 'tio': 0.0015485756696290375, 'dan': 0.0015455182645557322,
                   't, ': 0.001530995590457533, 'r l': 0.0015027145935294609, ' no': 0.001498128485919503,
                   't\r\n': 0.0014965997833828505, 'omm': 0.0014805484067479987, 'sse': 0.0014736692453330622,
                   'ill': 0.001470611840259757, ' vo': 0.0014690831377231046, ' pe': 0.0014683187864547784,
                   's a': 0.0014606752737715155, 'st ': 0.0014469169509416426, ' ch': 0.001395705415963782,
                   'ux ': 0.001392648010890477, " l'": 0.001381947093133909, ',\r\n': 0.001381947093133909,
                   'com': 0.001368188770304036, 'e n': 0.001357487852547468, 'rai': 0.0013498443398642054,
                   'onn': 0.0013360860170343323, 'nce': 0.0013330286119610272, '\r\nd': 0.0013299712068877221,
                   ' pl': 0.0013230920454727856, 'ut ': 0.0013139198302528703, 'tai': 0.0013085693713745863,
                   ' da': 0.0013032189124963023, ' du': 0.0013024545612279762, 'rs ': 0.0012795240231781879,
                   ' av': 0.0012787596719098615, 'e t': 0.00126882310542162, 'ure': 0.0012642369978116623,
                   'and': 0.0012565934851283996, ' ne': 0.001252007377518442, ' il': 0.0012504786749817894,
                   ' fa': 0.001249714323713463, 'pas': 0.0012428351622985265, ' je': 0.0012397777572252214,
                   'nte': 0.0012336629470786112, ' su': 0.001216082867907107, 'ran': 0.0012153185166387805,
                   'e f': 0.0012069106526871915, 'e a': 0.0011962097349306237, 'du ': 0.0011878018709790346,
                   ' di': 0.0011870375197107082, 's q': 0.0011839801146374031, 'che': 0.001180922709564098,
                   "qu'": 0.0011732791968808354, 'n d': 0.001169457440539204, 'tes': 0.0011618139278559412,
                   'urs': 0.0011618139278559412, 'ain': 0.0011480556050260681, 't a': 0.0011442338486844369,
                   't s': 0.0011442338486844369, 'mai': 0.0011404120923428054, 'ère': 0.0011320042283912164,
                   'cha': 0.001128182472049585, ', l': 0.0011243607157079537, 'end': 0.0011228320131713011,
                   'e v': 0.001119774608097996, 't e': 0.0011151885004880382, '\r\nc': 0.0011136597979513857,
                   ', d': 0.0011128954466830595, 'e. ': 0.0011067806365364493, 'ouv': 0.001103723231463144,
                   'lus': 0.0010945510162432288, 'eux': 0.0010914936111699237, 't c': 0.0010899649086332712,
                   'je ': 0.0010777352883400506, '\r\nl': 0.0010723848294617669, 'ati': 0.001067798721851809,
                   ' tr': 0.0010670343705834829, 'ieu': 0.0010662700193151565, 'ar ': 0.0010570978040952412,
                   " d'": 0.0010570978040952412, 'ois': 0.0010548047502902623, 'aut': 0.0010517473452169572,
                   ' l’': 0.001050982993948631, '\r\np': 0.0010494542914119785, ' do': 0.001047925588875326,
                   'ble': 0.0010441038325336945, 'plu': 0.0010364603198504318, 'voi': 0.0010249950508255377,
                   'ine': 0.0010242306995572113, ' es': 0.0010227019970205588, 'ren': 0.0010211732944839062,
                   'air': 0.0010173515381422748, 'e r': 0.0010135297818006435, 'tte': 0.0010081793229223595,
                   't q': 0.0009967140538974654, 'es\r': 0.0009967140538974654, ' dé': 0.0009905992437508552,
                   'r, ': 0.0009905992437508552, 'r d': 0.0009760765696526559, 'au ': 0.0009676687057010668,
                   'oit': 0.0009669043544327405, ' ét': 0.0009646113006277617, 're,': 0.0009615538955544566,
                   'leu': 0.0009592608417494777, ' me': 0.0009562034366761726, ', p': 0.0009554390854078464,
                   ', c': 0.0009470312214562573, 'int': 0.000937859006236342, ', s': 0.0009363303036996894,
                   ' vi': 0.0009317441960897318, 'ens': 0.0009302154935530792, 'ett': 0.0009302154935530792,
                   'as ': 0.0009286867910164267, 'éta': 0.0009271580884797742, 'rie': 0.0009195145757965113,
                   'ute': 0.0009195145757965113, 'ses': 0.0009187502245281851, 'ess': 0.0009172215219915325,
                   's m': 0.0009164571707232063, 'oir': 0.0009111067118449223, 'enc': 0.000910342360576596,
                   'ers': 0.0009080493067716172, 'ir ': 0.0009080493067716172, 'té ': 0.0009019344966250069,
                   'ave': 0.0009011701453566807, 'san': 0.0008996414428200281, 'uve': 0.0008988770915517018,
                   'nou': 0.0008866474712584814, 'fai': 0.0008858831199901551, 'a p': 0.0008805326611118713,
                   'ten': 0.0008805326611118713, 'nne': 0.0008774752560385661, 'anc': 0.0008759465535019135,
                   'lui': 0.0008759465535019135, 'ass': 0.0008736534996969347, 'ier': 0.0008736534996969347,
                   'ort': 0.0008698317433553034, 'n, ': 0.0008637169332086931, 'ter': 0.0008614238794037143,
                   'iss': 0.0008560734205254304, 'cou': 0.0008522516641837989, 'vai': 0.0008491942591104939,
                   'ser': 0.0008476655565738413, 's. ': 0.0008407863951589048, 'sur': 0.0008392576926222522,
                   'ins': 0.0008377289900855997, 'nde': 0.0008323785312073158, ', q': 0.0008308498286706632,
                   'ver': 0.0008300854774023369, 'uis': 0.0008293211261340106, ' si': 0.000824735018524053,
                   ', r': 0.0008232063159874005, 'uel': 0.0008186202083774427, '\r\ns': 0.0008178558571091165,
                   ' lu': 0.0008132697494991588, 'pri': 0.0008132697494991588, 'vou': 0.0008071549393525486,
                   'mes': 0.0008010401292059384}

# Dictionnaire des combinaisons de un caractère impossibles à réaliser
impossible_neighbors = {
    ' ': ['d', 'l', 'p', 'c', 's', 'e', 'a', 'q', 'm', 'n', 't', 'f', 'v', 'r', 'à', 'j', 'b', 'i', 'u', 'o', 'e ',
          's ', 't ', 'es', 'le', 're', 'de', 'on', 'en', 'qu', 'ou', 'ai', 'nt', 'an', 'me', 'te', 'ur', 'et', 'ie',
          'er', 'in', 'la', 'is', 'n ', 'r ', 'il', 'ce', 'ra', 'it', 'se', 'co', 'au', 'a ', 'ne', 'tr', 'ns', 'ar',
          'us', 'oi', 'ue', 'pa', 'un', 'ui', 'ch', 'u ', 'eu', 'ri', 'ma', 'i ', 's,', 'ti', 've', 'pr', 'po', 'ut',
          'el', 'or', 'so', 'll', 'ss', 'e,', 'ir', 'ro', 'à ', 'em', 'pe', 'si', 'nd', 'st', 'di', 'l ', 'to', 'vo',
          'mo', 'e\r', 'bl', 'sa', 'at', 'pl', 'da', 'no', 'rs', 'lu', 'li', 'ta', 'av', 'rt', 'as', 'mm', 's\r', 'om',
          'nc', 'ré', 'fa', 'ca', 'su', 'io', 'je', 'té', 'dé', 'ni', "l'", 't\r', 'os', 'uv', 'ec', 'nn', 'id', "u'"],
    'a': ['i', 'n', 'u', ' ', 'r', 't', 'v', 's', 's ', 't ', ' d', 're', ' l', 'nt', ' p', 'te', ' c', ' s', ' e',
          'ur', 'ie', 'in', 'is', 'n ', ' a', 'r ', 'il', 'ra', 'it', 'se', 'ne', 'tr', ' q', 'ns', 'us', 'ue', ' m',
          'un', 'ui', 'u ', 'ri', 'i ', 's,', 'ti', 've', ' n', ' t', ' f', 'ut', 'so', 'ss', 'ir', ' v', 'ro', 'si',
          ' r', 'nd', 'st', 'to', 'vo', 'sa', ' à', 'no', 'rs', 'ta', 'rt', 's\r', 'nc', ' j', 'ré', ' b', ' i', ' u',
          'su', 'io', 'té', 'ni', ' o', 't\r', 'uv', 'nn', 'id', "u'"],
    'é': ['t', ' ', 'e', 'e ', 't ', ' d', 'es', ' l', 'en', ' p', 'te', ' c', ' s', ' e', 'et', 'er', ' a', 'tr', ' q',
          ' m', 'eu', 'ti', ' n', ' t', ' f', 'el', 'e,', ' v', 'em', ' r', 'to', 'e\r', ' à', 'ta', ' j', ' b', ' i',
          ' u', 'té', ' o', 't\r', 'ec'],
    'c': ['e', 'o', 'h', 'a', 'e ', 'es', 'on', 'en', 'ou', 'ai', 'an', 'et', 'er', 'au', 'a ', 'ar', 'oi', 'eu', 'el',
          'or', 'e,', 'em', 'e\r', 'at', 'av', 'as', 'om', 'ho', 'os', 'ec'],
    'r': ['e', ' ', 'a', 'i', 'o', 's', 't', 'é', 'e ', 's ', 't ', ' d', 'es', ' l', 'on', 'en', 'ou', 'ai', ' p',
          'an', 'te', ' c', ' s', ' e', 'et', 'ie', 'er', 'in', 'is', ' a', 'il', 'it', 'se', 'au', 'a ', 'tr', ' q',
          'ar', 'oi', ' m', 'eu', 'i ', 's,', 'ti', ' n', ' t', ' f', 'el', 'or', 'so', 'ss', 'e,', 'ir', 'ét', ' v',
          'em', 'si', ' r', 'st', 'to', 'e\r', 'sa', 'é ', 'at', ' à', 'ta', 'av', 'ée', 'as', 's\r', 'om', ' j', ' b',
          ' i', ' u', 'su', 'io', 'té', ' o', 't\r', 'os', 'ec', 'id'],
    'u': ['r', 's', 'e', 'n', 'i', ' ', 't', 'v', "'", 'e ', 's ', 't ', ' d', 'es', 're', ' l', 'en', 'nt', ' p', 'te',
          ' c', ' s', ' e', 'et', 'ie', 'er', 'in', 'is', 'n ', ' a', 'r ', 'il', 'ra', 'it', 'se', 'ne', 'tr', ' q',
          'ns', ' m', 'eu', 'ri', 'i ', 's,', 'ti', 've', ' n', ' t', ' f', 'el', 'so', 'ss', 'e,', 'ir', ' v', 'ro',
          'em', 'si', ' r', 'nd', 'st', 'to', 'vo', 'e\r', 'sa', ' à', 'no', 'rs', 'ta', 'rt', "'a", 's\r', 'nc', ' j',
          'ré', ' b', ' i', "'e", ' u', 'su', 'io', 'té', 'ni', ' o', 't\r', 'ec', 'nn', "'i", 'id'],
    'i': ['e', 'n', 's', 'l', 't', ' ', 'r', 'o', 'd', 'e ', 's ', 't ', ' d', 'es', 'le', 're', 'de', ' l', 'on', 'en',
          'ou', 'nt', ' p', 'te', ' c', ' s', ' e', 'et', 'er', 'la', 'n ', ' a', 'r ', 'ra', 'se', 'ne', 'tr', ' q',
          'ns', 'oi', ' m', 'eu', 'ri', 's,', 'ti', ' n', ' t', ' f', 'el', 'or', 'so', 'll', 'ss', 'e,', ' v', 'ro',
          'em', 'si', ' r', 'nd', 'st', 'di', 'l ', 'to', 'e\r', 'sa', ' à', 'da', 'no', 'rs', 'lu', 'li', 'ta', 'rt',
          's\r', 'om', 'nc', ' j', 'ré', ' b', ' i', ' u', 'su', 'té', 'dé', 'ni', "l'", ' o', 't\r', 'os', 'ec', 'nn'],
    'd': ['e', 'i', 'a', 'é', 'e ', 'es', 'en', 'ai', 'an', 'et', 'ie', 'er', 'in', 'is', 'il', 'it', 'au', 'a ', 'ar',
          'eu', 'i ', 'el', 'e,', 'ir', 'ét', 'em', 'e\r', 'é ', 'at', 'av', 'ée', 'as', 'io', 'ec', 'id'],
    'n': ['t', ' ', 'e', 's', 'd', 'o', 'c', 'i', 'n', 'e ', 's ', 't ', ' d', 'es', 'de', ' l', 'on', 'en', 'ou', 'nt',
          ' p', 'te', ' c', ' s', ' e', 'et', 'ie', 'er', 'in', 'is', 'n ', ' a', 'il', 'ce', 'it', 'se', 'co', 'ne',
          'tr', ' q', 'ns', 'oi', ' m', 'ch', 'eu', 'i ', 's,', 'ti', ' n', ' t', ' f', 'el', 'or', 'so', 'ss', 'e,',
          'ir', ' v', 'em', 'si', ' r', 'nd', 'st', 'di', 'to', 'e\r', 'sa', ' à', 'da', 'no', 'ta', 's\r', 'om', 'nc',
          ' j', ' b', ' i', ' u', 'ca', 'su', 'io', 'té', 'dé', 'ni', ' o', 't\r', 'os', 'ec', 'nn', 'id'],
    'e': [' ', 's', 'n', 't', 'r', 'u', 'l', ',', 'm', '\r', 'c', '\r\n', 's ', ', ', 't ', ' d', 'le', 're', ' l',
          'nt', ' p', 'me', 'te', ' c', ' s', ' e', 'ur', 'la', 'n ', ' a', 'r ', 'ce', 'ra', 'se', 'co', 'ne', 'tr',
          ' q', 'ns', 'us', 'ue', ' m', 'un', 'ui', 'ch', 'u ', 'ri', 'ma', 's,', 'ti', ' n', ' t', ' f', 'ut', 'so',
          'll', 'ss', ' v', 'ro', 'si', ' r', 'nd', 'st', 'l ', 'to', 'mo', 'sa', ' à', 'no', 'rs', 'lu', 'li', 'ta',
          'rt', 'mm', 's\r', 'nc', ' j', 'ré', ' b', ' i', ' u', 'ca', 'su', 'té', 'ni', "l'", ' o', 't\r', 'uv', 'nn',
          "u'"],
    '.': [' ', ' d', ' l', ' p', ' c', ' s', ' e', ' a', ' q', ' m', ' n', ' t', ' f', ' v', ' r', ' à', ' j', ' b',
          ' i', ' u', ' o'], 'f': ['a', 'ai', 'an', 'au', 'a ', 'ar', 'at', 'av', 'as'],
    'l': ['e', 'a', 'l', ' ', 'u', 'i', "'", 'e ', ' d', 'es', 'le', ' l', 'en', 'ai', ' p', 'an', ' c', ' s', ' e',
          'ur', 'et', 'ie', 'er', 'in', 'la', 'is', ' a', 'il', 'it', 'au', 'a ', ' q', 'ar', 'us', 'ue', ' m', 'un',
          'ui', 'u ', 'eu', 'i ', ' n', ' t', ' f', 'ut', 'el', 'll', 'e,', 'ir', ' v', 'em', ' r', 'l ', 'e\r', 'at',
          ' à', 'lu', 'li', 'av', "'a", 'as', ' j', ' b', ' i', "'e", ' u', 'io', "l'", ' o', 'uv', 'ec', "'i", 'id',
          "u'"],
    'm': ['e', 'a', 'o', 'm', 'e ', 'es', 'on', 'en', 'ou', 'ai', 'an', 'me', 'et', 'er', 'au', 'a ', 'ar', 'oi', 'eu',
          'ma', 'el', 'or', 'e,', 'em', 'mo', 'e\r', 'at', 'av', 'as', 'mm', 'om', 'os', 'ec'],
    't': [' ', 'e', 'r', 'i', 'o', 'a', 'é', '\r', 'e ', '\r\n', ' d', 'es', 're', ' l', 'on', 'en', 'ou', 'ai', ' p',
          'an', ' c', ' s', ' e', 'et', 'ie', 'er', 'in', 'is', ' a', 'r ', 'il', 'ra', 'it', 'au', 'a ', ' q', 'ar',
          'oi', ' m', 'eu', 'ri', 'i ', ' n', ' t', ' f', 'el', 'or', 'e,', 'ir', 'ét', ' v', 'ro', 'em', ' r', 'e\r',
          'é ', 'at', ' à', 'rs', 'av', 'ée', 'rt', 'as', 'om', ' j', 'ré', ' b', ' i', ' u', 'io', ' o', 'os', 'ec',
          'id'], 'b': ['l', 'le', 'la', 'll', 'l ', 'lu', 'li', "l'"],
    'p': ['a', 'r', 'o', 'e', 'l', 'e ', 'es', 'le', 're', 'on', 'en', 'ou', 'ai', 'an', 'et', 'er', 'la', 'r ', 'ra',
          'au', 'a ', 'ar', 'oi', 'eu', 'ri', 'el', 'or', 'll', 'e,', 'ro', 'em', 'l ', 'e\r', 'at', 'rs', 'lu', 'li',
          'av', 'rt', 'as', 'om', 'ré', "l'", 'os', 'ec'],
    's': [' ', 'e', ',', 'o', 's', 'i', 't', 'a', '\r', 'u', 'e ', '\r\n', 's ', ', ', 't ', ' d', 'es', ' l', 'on',
          'en', 'ou', 'ai', ' p', 'an', 'te', ' c', ' s', ' e', 'ur', 'et', 'ie', 'er', 'in', 'is', ' a', 'il', 'it',
          'se', 'au', 'a ', 'tr', ' q', 'ar', 'us', 'oi', 'ue', ' m', 'un', 'ui', 'u ', 'eu', 'i ', 's,', 'ti', ' n',
          ' t', ' f', 'ut', 'el', 'or', 'so', 'ss', 'e,', 'ir', ' v', 'em', 'si', ' r', 'st', 'to', 'e\r', 'sa', 'at',
          ' à', 'ta', 'av', 'as', 's\r', 'om', ' j', ' b', ' i', ' u', 'su', 'io', 'té', ' o', 't\r', 'os', 'uv', 'ec',
          'id', "u'"],
    'v': ['e', 'o', 'e ', 'es', 'on', 'en', 'ou', 'et', 'er', 'oi', 'eu', 'el', 'or', 'e,', 'em', 'e\r', 'om', 'os',
          'ec'],
    'o': ['n', 'u', 'i', 'r', 'm', 's', 's ', 're', 'nt', 'me', 'ur', 'ie', 'in', 'is', 'n ', 'r ', 'il', 'ra', 'it',
          'se', 'ne', 'ns', 'us', 'ue', 'un', 'ui', 'u ', 'ri', 'ma', 'i ', 's,', 'ut', 'so', 'ss', 'ir', 'ro', 'si',
          'nd', 'st', 'mo', 'sa', 'no', 'rs', 'rt', 'mm', 's\r', 'nc', 'ré', 'su', 'io', 'ni', 'uv', 'nn', 'id', "u'"],
    '\n': ['\r', '\r\n'], 'h': ['o', 'on', 'ou', 'oi', 'or', 'om', 'os'],
    "'": ['a', 'e', 'i', 'e ', 'es', 'en', 'ai', 'an', 'et', 'ie', 'er', 'in', 'is', 'il', 'it', 'au', 'a ', 'ar', 'eu',
          'i ', 'el', 'e,', 'ir', 'em', 'e\r', 'at', 'av', 'as', 'io', 'ec', 'id'],
    'j': ['e', 'e ', 'es', 'en', 'et', 'er', 'eu', 'el', 'e,', 'em', 'e\r', 'ec'],
    ',': [' ', ' d', ' l', ' p', ' c', ' s', ' e', ' a', ' q', ' m', ' n', ' t', ' f', ' v', ' r', ' à', ' j', ' b',
          ' i', ' u', ' o'],
    'à': [' ', ' d', ' l', ' p', ' c', ' s', ' e', ' a', ' q', ' m', ' n', ' t', ' f', ' v', ' r', ' à', ' j', ' b',
          ' i', ' u', ' o'],
    ';': [' ', ' d', ' l', ' p', ' c', ' s', ' e', ' a', ' q', ' m', ' n', ' t', ' f', ' v', ' r', ' à', ' j', ' b',
          ' i', ' u', ' o'], 'q': ['u', 'ur', 'us', 'ue', 'un', 'ui', 'u ', 'ut', 'uv', "u'"], '\r': ['\n', '\n\r']}


#### ----- MÉTHODES DE DÉCHIFFREMENT ----- ####

# Comparer la vraie clé de test K avec la clé prédite (Debug)


def compare_K(K, K_pred):
    inverted_K = {value: key for key, value in K.items()}
    sorted_K = {}

    nb_errors = 0

    for code, symbol in K_pred.items():
        sorted_K[code] = inverted_K[code]

        if sorted_K[code] != symbol:
            nb_errors += 1
        else:
            print(f"Succès! {code} = {symbol}")

    print("K: ", sorted_K)
    print("Prédiction de K: ", K_pred)
    print(f"Nombre d'erreurs de substitution: {nb_errors}/{len(K_pred)} ({nb_errors / len(K_pred) * 100}%)")


# Calculer un score au message M
def score_message(M, errors):
    score = 0.0

    for trigram, freq in sorted_trigrams.items():
        score += M.count(trigram) * freq

    return score - len(errors)


# Échanger deux symboles dans la clé
def swap_symbols(K_pred, errors, distance=32, use_errors=True):
    keys = list(K_pred.keys())
    i, j = 0, 0

    if use_errors and len(errors) > 1:
        i = keys.index(rnd.choice(list(errors)))

        eligible_errors = [e for e in errors if
                           max(i - distance, 0) <= keys.index(e) <= min(i + distance, len(keys) - 1)]

        if eligible_errors:
            j = keys.index(rnd.choice(eligible_errors))
        else:
            j = keys.index(rnd.choice(list(errors)))
    else:
        i = rnd.randint(0, len(keys) - 1)

    j = rnd.randint(max(i - distance, 0), min(i + distance, len(keys) - 1))
    K_pred[keys[i]], K_pred[keys[j]] = K_pred[keys[j]], K_pred[keys[i]]
    return K_pred


# Déchiffrer un texte avec la clé prédite
def decrypt_with_mapping(chunks, K_pred):
    decrypted_chunks = [K_pred[chunk] for chunk in chunks]
    errors = set()

    # Trouver toutes les combinaisons impossibles présentement dans le texte
    for i in range(len(decrypted_chunks) - 1):
        if decrypted_chunks[i] in impossible_neighbors:
            if decrypted_chunks[i + 1] in impossible_neighbors[decrypted_chunks[i]]:
                errors.add(chunks[i])
                errors.add(chunks[i + 1])

    return ''.join(decrypted_chunks), errors


# Technique de MCMC (Markov Chain Monte Carlo)
def mcmc(chunks, K_pred, max_iterations=10000, initial_temp=1.0, cooling_rate=0.99):
    # Initialiser les variables de base
    current_K = K_pred.copy()
    decrypted_message, errors = decrypt_with_mapping(chunks, K_pred)
    lowest_conflicts = len(errors)  # TODO: REMOVE! DEBUG
    best_score = score_message(decrypted_message, errors)
    best_K = current_K.copy()
    temp = initial_temp

    for iteration in range(max_iterations):
        # Mettre à jour la température
        temp = max(temp * (cooling_rate if iteration % 100 != 0 else 0.95), 0.01)

        # Échanger aléatoirement certains symboles
        new_mapping = swap_symbols(current_K.copy(), errors, 32, False)

        # Évaluer le nouveau message obtenu
        decrypted_message, errors = decrypt_with_mapping(chunks, new_mapping)
        score = score_message(decrypted_message, errors)

        print(
            f"Iteration {iteration}, Temp: {temp}, Best Score: {best_score}, Conflicts: {lowest_conflicts}")
        # TODO: REMOVE! DEBUG

        # Continuer à itérer avec le meilleur score obtenu
        if score >= best_score:
            best_score = score
            best_K = new_mapping.copy()
            current_K = new_mapping.copy()
            lowest_conflicts = len(errors)  # TODO: REMOVE! DEBUG
        elif math.exp((score - best_score) / temp) > rnd.random():
            current_K = new_mapping.copy()

    return decrypt_with_mapping(chunks, best_K), best_K


# Déchiffrer le cryptogramme C
def decrypt(C):
    # Séparer C en chunks de 8 bits
    chunks = [C[i:i + 8] for i in range(0, len(C), 8)]

    # Compter la fréquence de chaque chunk
    frequency_count = Counter(chunks)
    sorted_chunks = [chunk for chunk, _ in frequency_count.most_common()]

    # Créer un dictionnaire basé sur la fréquence des chunks et des symboles
    mapping = dict(zip(sorted_chunks, [symbol for symbol, _ in sorted_symbols]))
    print(mapping)

    # Décoder le message avec la technique MCMC
    M, best_mapping = mcmc(chunks, mapping, 10000)
    compare_K(K, best_mapping)  # TODO: REMOVE! DEBUG FUNCTION

    return M


# TODO: REMOVE! DEBUG FUNCTIONS
M = generate_corpus()[:120000]
C = chiffrer(M, K, symbols)
D = decrypt(C)

print("M: ", M)
print("D: ", D)

