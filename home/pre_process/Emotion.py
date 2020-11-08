import re

wrong_terms = {
    'ô kêi': ' ok ', 'okie': ' ok ', 'o kê': ' ok ', 'okey': ' ok ', 'ôkê': ' ok ', 'oki': ' ok ', 'oke':  ' ok ',
    'okay': ' ok ', 'okê': ' ok ', 'ote': ' ok ',
    'kg ': u' không ', 'not': u' không ', u' kg ': u' không ', '"k ': u' không ', ' kh ': u' không ',
    'kô': u' không ', 'hok': u' không ', ' kp ': u' không phải ', u' kô ': u' không ', '"ko ': u' không ',
    ' cam ': ' camera ', ' cameera ': ' camera ', 'thuết kế': u'thiết_kế', 'ết_kế ': u' thiết_kế ',
    'gud': u' tốt ', 'god': u' tốt ', 'wel done': ' tốt ', 'good': u' tốt ', 'gút': u' tốt ',
    'sấu': u' xấu ', 'gut': u' tốt ', u' tot ': u' tốt ', u' nice ': u' tốt ', 'perfect': 'rất tốt',
    'bt': u' bình thường ',
    ' m ': u' mình ', u' mik ': u' mình ', 'mìn': u'mình', u' mìnhh ': u' mình ', u' mềnh ': ' mình ',
    ' mk ': u' mình ', ' mik ': ' mình ',
    ' ko ': u' không ', u' k ': u' không ', 'khong': u' không ', u' hok ': u' không ',
    u' wá ': u' quá ', ' wa ': u' quá ', u'qá': u' quá ',
    ' cute ': 'dễ_thương',
    u' tẹc vời ': ' tuyệt_vời ', u'tiệc dời': ' tuyệt_vời ', u'tẹc zời': ' tuyệt_vời ',
    ' dc ': u' được ', u' đc ': u' được ', ' j ': ' gì ',
    ' màn hìn ': ' màn_hình ', u' màng hình ': u' màn_hình ', ' dt ': u' điện_thoại ',
    ' đt ': u' điện_thoại ',
    ' tet ': u' kiểm_tra ', ' test ': u' kiểm_tra ', ' tét ': u' kiểm_tra ',
    u' cẩm ': u' cầm ', u' cấm ': u' cầm ', u' sước ': u' xước ', u' xướt ': u' xước ',
    u'sài ': ' xài ',
    u' mựơt ': u' mượt ',
    u' sức sắc ': u' xuất_sắc ', u' xức sắc ': u' xuất_sắc ',
    ' fai ': u' phải ', u' fải ': u' phải ',
    u' bây_h ': u' bây_giờ ',
    u' mội ': u' mọi ', ' moi ': u' mọi ',
    u'ợc điểm ': u' nhược điểm ',
    u' sámsumg ': ' samsung ', ' sam ': ' samsung ', 'sam_sung ': ' samsung ',
    u' kbiết ': u' không_biết ', u' rất tiết ': u' rất_tiếc ', u' rất_tiết ': u' rất_tiếc ',
    u' rất tiêc ': u' rất_tiếc ',
    u' lát ': ' lag ', u' lác ': ' lag ', ' lat ': ' lag ', ' lac ': ' lag ', u' khựng ': ' lag ', u' giật ': ' lag ',
    u' văng ra ': ' lag ', u' đơ ': ' lag ', u' lắc ': ' lag ',
    u' film ': ' phim ', ' phin ': ' phim ', ' fim ': ' phim ',
    ' nhung ': u' nhưng ', u' ấu hình ': u' cấu_hình ',
    ' sd ': u' sử_dụng ', u' mài ': u' màu ', u' lấm ': u' lắm ',
    u' tôt ': ' tốt ', u' tôn ': u' tốt ', 'aple ': ' apple ', "gja": u" giá ", u"sục": u"sụt",
    u' âm_lượ ': u' âm_lượng ', u' thất_vọ ': u' thất_vọng ', u' dùg ': u' dùng ',
    u' bỗ ': u' bổ ',
    u' sụt ': u' tụt ', u' tuột ': u' tụt ', u' xuống ': u' tụt ',
    u'chíp ': ' chip ',
    ' bin ': ' pin '
}

emotion_icons = {
    "👹": "negative", "👻": "positive", "💃": "positive",'🤙': ' positive ', '👍': ' positive ',
    "💄": "positive", "💎": "positive", "💩": "positive","😕": "negative", "😱": "negative", "😸": "positive",
    "😾": "negative", "🚫": "negative",  "🤬": "negative","🧚": "positive", "🧡": "positive",'🐶':' positive ',
    '👎': ' negative ', '😣': ' negative ','✨': ' positive ', '❣': ' positive ','☀': ' positive ',
    '♥': ' positive ', '🤩': ' positive ', 'like': ' positive ', '💌': ' positive ',
    '🤣': ' positive ', '🖤': ' positive ', '🤤': ' positive ', ':(': ' negative ', '😢': ' negative ',
    '❤': ' positive ', '😍': ' positive ', '😘': ' positive ', '😪': ' negative ', '😊': ' positive ',
    '?': ' ? ', '😁': ' positive ', '💖': ' positive ', '😟': ' negative ', '😭': ' negative ',
    '💯': ' positive ', '💗': ' positive ', '♡': ' positive ', '💜': ' positive ', '🤗': ' positive ',
    '^^': ' positive ', '😨': ' negative ', '☺': ' positive ', '💋': ' positive ', '👌': ' positive ',
    '😖': ' negative ', '😀': ' positive ', ':((': ' negative ', '😡': ' negative ', '😠': ' negative ',
    '😒': ' negative ', '🙂': ' positive ', '😏': ' negative ', '😝': ' positive ', '😄': ' positive ',
    '😙': ' positive ', '😤': ' negative ', '😎': ' positive ', '😆': ' positive ', '💚': ' positive ',
    '✌': ' positive ', '💕': ' positive ', '😞': ' negative ', '😓': ' negative ', '️🆗️': ' positive ',
    '😉': ' positive ', '😂': ' positive ', ':v': '  positive ', '=))': '  positive ', '😋': ' positive ',
    '💓': ' positive ', '😐': ' negative ', ':3': ' positive ', '😫': ' negative ', '😥': ' negative ',
    '😃': ' positive ', '😬': ' 😬 ', '😌': ' 😌 ', '💛': ' positive ', '🤝': ' positive ', '🎈': ' positive ',
    '😗': ' positive ', '🤔': ' negative ', '😑': ' negative ', '🔥': ' negative ', '🙏': ' negative ',
    '🆗': ' positive ', '😻': ' positive ', '💙': ' positive ', '💟': ' positive ',
    '😚': ' positive ', '❌': ' negative ', '👏': ' positive ', ';)': ' positive ', '<3': ' positive ',
    '🌝': ' positive ',  '🌷': ' positive ', '🌸': ' positive ', '🌺': ' positive ',
    '🌼': ' positive ', '🍓': ' positive ', '🐅': ' positive ', '🐾': ' positive ', '👉': ' positive ',
    '💐': ' positive ', '💞': ' positive ', '💥': ' positive ', '💪': ' positive ',
    '💰': ' positive ',  '😇': ' positive ', '😛': ' positive ', '😜': ' positive ',
    '🙃': ' positive ', '🤑': ' positive ', '🤪': ' positive ', '☹': ' negative ',  '💀': ' negative ',
    '😔': ' negative ', '😧': ' negative ', '😩': ' negative ', '😰': ' negative ', '😳': ' negative ',
    '😵': ' negative ', '😶': ' negative ', '🙁': ' negative ', ':))': ' positive ', ':)': ' positive ',
    'he he': ' positive ', 'hehe': ' positive ', 'hihi': ' positive ', 'haha': ' positive ',
    'hjhj': ' positive ', ' lol ': ' negative ', 'huhu': ' negative ', ' 4sao ': ' positive ', ' 5sao ': ' positive ',
    ' 1sao ': ' negative ', ' 2sao ': ' negative ',
    ': ) )': ' positive ', ' : ) ': ' positive '
}

sentiment_stopwords = ["ufeff", "+", "\"", "", ".", ",", "!", "%", "....", "...", ")", "(", "thì", "là", "và", "bị", "với",
                       "thế_nào", "?", "", "một_số", "mot_so", "thi", "la", "va", "bi", "voi", "trong",
                       "the_nao", " j ", "gì", "có", "pin", "giá", "j7pro", "chứ", "máy", "tôi", "của", "để", "ai",
                       "sản_phẩm", "j7", "thấy", "bản", "vì", "nên", "ace", "pubg", "j5", "ip7", "ip7+", "nhé", "nhe",
                       "nhé'", "như", "từ ", "vậy", "2h", "thui", "thôi", "bin`", "fb", "facebook", "youtube", "pr", "phải"
                       "khi", "triệu", "triệu'", "18tr", "fan", "xài", "lại", "chụp", "camera", "plus", "điện_thoại",
                       "tới", "web", "reset", "nguyên_đán", "s9", "j8", "màn_hình", "64gb", "tết", "nhân_viên"]


s1 = u'ÀÁÂÃÈÉÊÌÍÒÓÔÕÙÚÝàáâãèéêìíòóôõùúýĂăĐđĨĩŨũƠơƯưẠạẢảẤấẦầẨẩẪẫẬậẮắẰằẲẳẴẵẶặẸẹẺẻẼẽẾếỀềỂểỄễỆệỈỉỊịỌọỎỏỐốỒồỔổỖỗỘộỚớỜờỞởỠỡỢợỤụỦủỨứỪừỬửỮữỰựỲỳỴỵỶỷỸỹ'
s0 = u'AAAAEEEIIOOOOUUYaaaaeeeiioooouuyAaDdIiUuOoUuAaAaAaAaAaAaAaAaAaAaAaAaEeEeEeEeEeEeEeEeIiIiOoOoOoOoOoOoOoOoOoOoOoOoUuUuUuUuUuUuUuYyYyYyYy'



def preprocess_feature(sentence):
    # replace_wrong_terms
    for key, value in wrong_terms.items():
        if sentence.find(key) >= 0:
            sentence = sentence.replace(key, value)

    # remove_stopwords
    # for w in sentiment_stopwords:
    #     sentence = sentence.replace("%s " % w, " ")
    #     sentence = sentence.replace("%s " % w, " ")

    # replace_emotion_icons
    for key, value in emotion_icons.items():
        if sentence.find(key) >= 0:
            sentence = sentence.replace(key, value)

    # remove_repeated_characters
    sentence = re.sub(r'([A-Z])\1+', lambda m: m.group(1), sentence, flags=re.IGNORECASE)

    # remove_numbers
    # sentence = re.sub("[aj]*(ip)*\s*([0-9./])+(trieu)*(tr)*", " ", sentence, flags=re.IGNORECASE)

    # remove_special_character
    punctuation = """!"#$%&\'()*+,-./:;<=>?@[\\]^`{|}~"""
    translator = str.maketrans(punctuation, ' ' * len(punctuation))
    sentence = sentence.translate(translator)

    # replace_not_terms
    text = re.split("\s*[\s,;]\s*", sentence)
    for idx in range(len(text)):
        if idx < len(text) - 1 and text[idx] in not_list:
            if text[idx + 1] in pos_list:
                text[idx] = "notpositive"
                text[idx + 1] = ""
            if text[idx + 1] in neg_list:
                text[idx] = "notnegative"
                text[idx + 1] = ""
        elif text[idx] not in not_list:
            if text[idx] in neu_list:
                text.append("neutral")
            elif text[idx] in pos_list:
                text.append("positive")
            elif text[idx] in neg_list:
                text.append("negative")

    # indicate_vietnamese_phrases
    length = len(text)
    for idx in range(length):
        if text[idx] in degree_list:
            if idx + 1 < length and (text[idx + 1] in pos_list):
                text[idx] = "%s_%s" % (text[idx], text[idx + 1])
            elif idx - 1 >= 0 and (text[idx - 1] in pos_list):
                text[idx] = "%s_%s" % (text[idx - 1], text[idx])
    sentence = " ".join(text)

    # remove_ vietnamese_accents
    # result = ''
    # for c in sentence:
    #     result += s0[s1.index(c)] if c in s1 else c

    # sentence = result
    return sentence


path = "/Users/duynk/Desktop/AI/"


def load_word(s):
    cat_f = open(path + s, "r", encoding="utf-8")
    l = [w.replace("\n", "").replace(".", "") for w in cat_f.readlines()]
    cat_f.close()
    return l

pos_list = load_word('pos.txt')
neu_list = load_word('neutral.txt')
neg_list = load_word('neg.txt')
not_list = load_word('not.txt')
degree_list = load_word('degree.txt')