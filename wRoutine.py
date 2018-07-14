import os, sys, re

sys.path.append("./scripts/")
import betaCode

# LOADING SETTINGS from SETTINGS.YML
def loadSettings(ymlFile):
    with open(ymlFile, "r", encoding="utf8") as f1:
        data = f1.read()

        data = re.sub("#.*\n", "", data)
        data = re.sub("\n\n", "\n", data)

        data = re.split(r"\n(?=\w)", data)
        
        dic = {}

        for d in data:
            d = d.split(":")
            dic[d[0].strip()] = d[1].strip()

    return(dic)

# FORMS THE YAML HEADER
def formYMLheader(settings):
    template = "---\n%s\n---\n\\newpage\n\n\n"

    vals = []
    listOfVals = ["author", "title", "date", "abstract", "bibliography", "csl",
                  "papersize", "indent", "fontsize", "documentclass", "header-includes", "geometry"]

    for l in listOfVals:
        if l in settings:
            lNew = ("%s: %s" % (l, settings[l]))
            vals.append(lNew)

    vals = "\n".join(vals)
    vals = template % vals

    return(vals)

settings = loadSettings("_settings.yml")
ymlHeader = formYMLheader(settings)

# AH>CE conversion
def AHCE(ah):
    ce = int(ah)-(int(ah)/33)+622
    return(int(ce))

def processAHdates(text):
    # convert AH periods to CE only
    for d in re.finditer(r"@\d+-\d+TOCE", text):
        print(d.group())
        ah = d.group()[1:-4].split("-")
        ce1 = AHCE(ah[0])
        ce2 = AHCE(ah[1])
        ahcePeriod = "%s–%s CE" % (ce1, ce2)
        text = text.replace(d.group(), ahcePeriod)
        
    # convert AH periods into AH/CE format
    for d in re.finditer(r"@\d+-\d+AH", text):
        print(d.group())
        ah = d.group()[1:-2].split("-")
        ce1 = AHCE(ah[0])
        ce2 = AHCE(ah[1])
        ahcePeriod = "%s–%s AH / %s–%s CE" % (ah[0], ah[1], ce1, ce2)
        text = text.replace(d.group(), ahcePeriod)
        
    # convert AH dates into AH/CE format
    for d in re.finditer(r"@\d+AH", text):
        print(d.group())
        ah = d.group()
        ce = AHCE(ah[1:-2])
        ahce = "%s/%s CE" % (ah[1:-2], ce)
        text = text.replace(d.group(), ahce)

    # convert AH dates into CE only
    for d in re.finditer(r"@\d+TOCE", text):
        print(d.group())
        ah = d.group()
        ce = AHCE(ah[1:-2])
        ahce = "%s CE" % (ce)
        text = text.replace(d.group(), ahce)
        
    return(text)

# betaCode
def translitFile(file):
    with open(file, "r", encoding="utf8") as f:
        text = f.read()
        text = processAHdates(text)
        for i in re.finditer(r"@@.*?@@", text):
            print(i.group())
            iNew = betaCode.betacodeToTranslit(i.group())
            text = text.replace(i.group(), iNew[2:-2])

        text = processAHdates(text)
        with open(file, "w", encoding="utf8") as f:
            f.write(text)
        print("\tAH>CE & Translit Conversion: %s " % file)

def processArabicQuotes(file):
    with open(file, "r", encoding="utf8") as f:
        text = f.read()
        for i in re.finditer(r"(<!--@@.*?-->\n)(<p class=\"arabic\">.*?</p>)?", text):
            print(i.group(1)[6:-4])
            iNew = betaCode.betacodeToArabic(i.group(1)[6:-4])
            text = text.replace(i.group(), "%s<p class=\"arabic\">%s</p>" % (i.group(1), iNew))
        with open(file, "w", encoding="utf8") as f:
            f.write(text)
        print("To Arabic: %s has been processed..." % file)

# convert relevant files
def convertRelevant():
    for path, subdirs, files in os.walk("."):
       for file in files:
           if file.endswith(tuple([".md"])):
               #print(file)
               f = os.path.join(path, file)
               translitFile(f)
               #processArabicQuotes(f)

# insert Arabic quotations into the master_draft
def insertQuotations(text):
    bqFolder = "./blockquotes/"
    
    # preprocess tags
    for r in re.findall("ARABIC:.*\n", text):
        r1 = r.replace("ARABIC:", r"\begin{arab}{")
        r1 = r1.replace("\n", "}\end{arab}\n")

        text = text.replace(r, r1)

    # replace filenames with quotes
    loq = os.listdir(bqFolder)
    for l in loq:
        if l.startswith("."):
            pass
        else:
            with open(bqFolder+l, "r", encoding = "utf8") as f1:
                quote = f1.read()
            text = text.replace(l, quote)
    return(text)


# combine master draft
def combineMasterDraft(draftFolder):
    print("=" * 80)
    print("generating master draft from frile in `%s` folder" % draftFolder)
    print("\tNB: only files that start with `0` and end with `.md` will be included!")
    
    master = []
    for path, subdirs, files in os.walk(draftFolder):
        for file in files:
            if file[0] == "0" and file.endswith(tuple([".md"])):
                #print(file)
                i = os.path.join(path, file)
                master.append(i)

    master = sorted(master)
    print("=" * 80)
    print("\t"+"\n\t".join(master))

    masterDraft = [ymlHeader]

    for i in master:
        with open(i, "r", encoding="utf8") as ft:
            masterDraft.append(ft.read())

    # remove comments
    masterDraftFinal = []
    masterDraft = "\n\n\n".join(masterDraft).split("\n")

    # removes lines commented out in LaTeX style (the first character on the line is %)
    for m in masterDraft:
        if len(m) > 0 and m[0] == "%":
            pass
        else:
            masterDraftFinal.append(m)

    # ? add a check if `masterdraft_autogenerated.md` already exists
    #   if yes, ask if you want to overwrite it
    #      yes > generates a new file
    #      no  > stops the script

    masterDraftFinal = "\n".join(masterDraftFinal)
    masterDraftFinal = insertQuotations(masterDraftFinal)
    
    with open("%s.md" % settings['draft_in'], "w", encoding="utf8") as f9:
        f9.write(masterDraftFinal)

    print("=" * 80)
    print("`%s.md` has been produced" % settings['draft_in'])
    print("IMPORTANT: Do not edit this file, as it will be overwritten when you run this script again!")
    print("=" * 80)

# uload master bibliography
def loadMasterBibliography(bibliography):
    newBIBdic  = {}
    with open(bibliography, "r", encoding="utf8") as f1:
        bib = re.split("\n@", f1.read())
        for rec in bib[1:]:
            key = rec.split("\n")[0].split("{")[1].replace(",", "")
            newBIBdic[key] = "@"+rec
    return(newBIBdic)

# update project bibliography
def updateBibliographies(draftFile):
    bibDIC = loadMasterBibliography(settings['bibliography_master'])
    projectFile = "%s.md" % draftFile

    with open(projectFile, "r", encoding="utf8") as f1:
        f1 = f1.read()
        
        bibList = []
        # collect all records from bibDIC using these keys
        # ---must be done *after* transliteration is done
        refList = sorted(list(set(re.findall("@\w+", f1))))
        for k in refList:
            #print(k[1:])
            if k[1:] in bibDIC:
                bibList.append(bibDIC[k[1:]])
                #print(bibDIC[k[1:]])
            elif k[1:] == "fig":
                pass
            else:
                print("\t%s\t: not in master bibliography" % k[1:])
    # save biblio.bib
    bibList = list(set(bibList))
    with open(settings['bibliography'], "w", encoding="utf8") as f9:
        f9.write("\n\n".join(sorted(bibList)))

# MAIN FUNCTION

def main():
    
    convertRelevant()
    combineMasterDraft(settings['draft_folder'])
    updateBibliographies(settings['draft_in'])

    # Running Pandoc
    print("=" * 80)
    print("Running Pandoc... a PDF file will be generated shortly, inshallah")
    print("=" * 80)

    # definiing a template
    if 'latex_template' in settings:
        latex_template = "--template=%s" % settings['latex_template']
    else:
        latex_template = ""

    # definiing whether TOC to be added or not
    if 'toc' in settings:
        toc = settings['toc']
    else:
        toc = ""

    draft_in  = settings['draft_in']
    draft_out = settings['draft_out']

    # you might need to replace `pandoc` with full path (in the next line)
    pandocPath = "pandoc"

    line1 = "%s -N %s --filter pandoc-fignos --filter pandoc-citeproc %s --pdf-engine=xelatex %s.md -o %s.pdf" % (pandocPath, latex_template, toc, draft_in, draft_out)
    line2 = "open %s.pdf" % draft_out

    print(line1)
    os.system(line1)

    print(line2)
    os.system(line2)

    # TO ADD: 1) conversion to DOCX and HTML
        
main()

