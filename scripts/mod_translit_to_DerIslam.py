# conventional US/LOC transliteration
translitDerIslam = {
# Alphabet letters
    'Ṯ' : 'Th', # thā’
    'ṯ' : 'th', # thā’
    'Ǧ' : 'J',  # jīm
    'ǧ' : 'j',  # jīm
    'Ḫ' : 'Kh', # khā’
    'ḫ' : 'kh', # khā’
    'Ḏ' : 'Dh', # dhāl
    'ḏ' : 'dh', # dhāl
    'Š' : 'Sh', # shīn
    'š' : 'sh', # shīn
    'Ġ' : 'Gh', # ghayn
    'ġ' : 'gh', # ghayn
    'Ḳ' : 'Q',  # qāf
    'ḳ' : 'q',  # qāf
    'á' : 'ā',  # alif maqṣūraŧ
    'ã' : 'ā',  # dagger alif
    'ŧ' : 't'   # tā’ marbūṭaŧ
    }


def forDerIslam(file):
    with open(file, "r", encoding="utf8") as f1:
        f1 = f1.read()
        f1 = f1.replace("ŧ+", "t")
        f1 = f1.replace("ŧ", "")
        f1 = f1.replace("\includegraphics{","\includegraphics[width=\\textwidth]{")
        for k,v in translitDerIslam.items():
            f1 = f1.replace(k, v)
        with open(file, "w", encoding="utf8") as f9:
            f9.write(f1)

    print("%s has been processed" % file)
    
forDerIslam("main.md")

