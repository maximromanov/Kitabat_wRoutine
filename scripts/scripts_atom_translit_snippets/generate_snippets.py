import re

template = """
  "%s":
    "prefix": "%s"
    "body": "%s"
"""

# AH>CE conversion
def AHCE(ah):
    ce = int(ah)-(int(ah)/33)+622
    return(int(ce))

def generateSnippets(csvFile):

    # conversing transliteration snippets
    snippets = []
    with open("snippets.csv", "r", encoding="utf8") as f1:
        data = f1.read().split("\n")

        c = 0
        for d in data[1:]:
            c += 1
            d = d.split("\t")

            if re.search("^\w$", d[1]):
                pass
            else:
                s = template[1:] % (d[2] + " - %s (%d)" % (d[3], c), d[0]+d[1], d[2])
                snippets.append(s)

        snippets = '".text.md":\n' + "\n".join(snippets)

        # add AH > CE year conversion snippets
        ahce = ["\n\n# AH to CE year conversion\n\n"]
        for ah in range(1, 1500, 1):
            ce = AHCE(ah)
            val = "%d/%d CE" % (ah, ce)
            fin = template[1:] % ("%d AH" % ah, ",%dAH" % ah, val)
            ahce.append(fin)

        ahce = "\n".join(ahce)
        

    with open("paste_to_snippets.cson.txt", "w", encoding="utf8") as f1:
        f1.write(snippets+ahce)


generateSnippets("snippets.csv")
        
