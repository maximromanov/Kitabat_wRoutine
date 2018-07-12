# Kitābaŧ wRoutine 1.0

A simple markdown-based workflow for sustainable academic writing (with some adaptations for the field of Arabic and Islamic Studies).

## Features

- a nice and simple, yet sufficiently robust interface (<https://atom.io/>)
- atomized drafting; easy inclusion/exclusion of sections into/from the master draft;
- explicit logical markup with *markdown*, a simple text encoding scheme;
- images and illustrations with captions;
- cross-references to sections, images, tables within the text;
- footnotes;
- automatic citation insertion form bibliography files;
- bibliography and citation styles;
- automatic generation of desired formats (e.g., PDF, HTML, DOCX, etc.); PDF requires LaTeX engine to be installed on the machine.

wRoutine is based on *markdown*; you can learn all you need to know about it from the following two tutorials on the basic principles of [*markdown*](https://programminghistorian.org/en/lessons/getting-started-with-markdown) and [*sustainable academic writing*](https://programminghistorian.org/en/lessons/sustainable-authorship-in-plain-text-using-pandoc-and-markdown).

## Requirements

The following software must be installed for the wRoutine to work as intended.

- `Atom` (<https://atom.io/>), a free, hackable text editor. wRoutine is written with this text editor in mind, but it can be used with other editors as well (although some features will not be available). The overall configutation is describe below.
- `Pandoc` (<https://pandoc.org/>) does all the conversion into different formats;
- `LaTeX` is used by `Pandoc` to generate PDF files; `MiKTeX`, <https://miktex.org/>, is the easiest way to install and manage `LaTeX` on any machine.

## Features for the field of Arabic and Islamic studies

These features are implemented in Atom, and require a few simple steps to be activated. They include the following:

- transliteration support, i.e. an easy insertion of tricky characters that are used for transliteration of Arabic.
- conversion of AH years into AH/CE format, which is usually used in publications.

### Transliteration Snippets for Atom

`snippets.csv` contains a table of variables to be converted into transliteration snippets for Atom. You can edit this file and add more relevant snippets.

You can run `generate_snippets.py` to regenerate snippets from `snippets.csv`. Snippets will be saved into `paste_to_snippets.cson.txt`, in the format that Atom requires.

This script (`generate_snippets.py`) also generates *hijri>CE* conversion data (for years only).

### Adding snippets to Atom

1. Open `paste_to_snippets.cson.txt`, select everything and copy into buffer (Ctrl+c).
2. In Atom, open `Atom > Snippets...` (this will open `snippets.scon`)
3. At the end of the file, paste (Ctrl+v) what you copied from `paste_to_snippets.cson.txt`
4. Snippets should start working immediately.

### Current configuration

#### Transliteration

1. Type `code`, then `Tab` key to insert the desired character. *NB:* there is a bit on an issue with the `Tab` key when you are trying to do that in a `list`, where `Tab` adds indentation, rather than does conversion.
2. `Codes` are organized as follows:
	1. All codes start with `,` — a comma
	2. The second character should be:
		1. `*`, `.`, or `8` for characters with `dots` (ḥ, ṭ, ḍ, ġ, etc.)
		2. `_`, or `-` for characters with macrons and breves (ā, ḫ, ḏ, ṯ, etc.)
		3. `^` for characters with `^` (š, ǧ, etc.)
	3. The third character is the desired letter (capitalized, if necessary).
	4. After that, press `Tab` to complete conversion.
3. **NB:** There are some additional characters:
	1. `,<` or `,'` for *hamzaŧ*
	2. `,>` or `,\`` for *ʿayn*
	3. `,=t` for *tāʾ marbūṭaŧ*
	4. `,~a` or `,\`a` for *ã*, *dagger alif*
	5. `,/a` for *alif maḳṣūraŧ*
	6. **EXAMPLE:** `,_a` will change into ā

#### *Hiǧrī* years

1. Works for the range from 1 till 1500;
2. Type `,`;
3. Type the desired year;
4. Add `AH` (no spaces between the year and `AH`);
5. Hit `TAB`;
6. **EXAMPLE:** `,748AH` will convert into `748/1347 CE`.

# Sample project

## Text sections

- draft can be atomized into sections and subsections, all stored as separate files;
- all sections of the main piece must be stored in the `draft` folder;
- if you work on a book project, you can also create subfolders for each chapter;
- the filenames must begin with `0` and end with `.md`; change file names to change their order in folders and subfolders. The initial `0` can be changed into some other character (or, better, prepended with `z`) in order to be excluded from the final draft;
- all files that begin with `0` and end with `.md` will be joined—in alphabetical order—into the master draft in the main folder of the project; subfolders for chapters should also start which allows to easily arrange all folders into a desired order.
- you can ‘play’ with subfolder and file names to achieve desired order of sections in your final document, for example `000 Introduction.md` will be always before `010 Subject of the Study.md`; you can add prefix `z` to exclude a section file from final draft (actually, any other prefix will work; `z.` will also push excluded section to the bottom of the list).
- to start your own project, simply replace the existing files with your files; you must keep `000 YAML Header.md` as it is the necessary element for file conversion; simply change information there into what you need (Title, Subtitle, Author, etc.).

## Illustrations and Images

Store illustrations in the `images` folder. An image can be inserted then with:

``` markdown
![Caption for your image](./images/name_of_the_image_file.jpg)
```

# Old stuff...

## Update from June 16, 2018

	- `Makefile` (i.e., running command `make` from *Terminal* [in the folder of your project]) will run all necessary conversion scripts and will generate multiple output files. More specifically:
	1. `betaCode` and AH dates are converted in all relevant files (`_generateBetaCode.py`)
	2. masterdraft is generated from sections stored in `./draft/` subfolder and saved into `_draft_autogenerated.md` (`_compile_masterDraft.py`)
	3. some final formatting is applied and bibliography file (`biblio.bib`) is updated; `main.md` file is created for conversion into other formats (`_draft_to_main.py`).
	4. [Optional] Optional means the line of code is *commented out*, you need to *uncomment* it for it to work (remove `#` in front of it)
	5. [Optional] conversion of betaCode transliteration into *Der Islam* system (`mod_translit_to_DerIslam.py`)
	6. conversion of `main.md` to PDF
	7. opening of the newly formed PDF
	8. [Optional: Lines 15-17] conversion into `.DOCX` (15), `.HTML` (16), `.TEX` (17).
- `ATOM` (<https://atom.io/>) is a great editor for this *wroutine*; on relevant settings, see *Atom Option* below, and also <http://u.arizona.edu/~selisker/post/workflow/> for more details.


## `Atom` options

- ATOM is a nice option for an editor, particularly since it has a plugin that make auto-lookup into a bibtex file
- For settings in ATOM, see <http://u.arizona.edu/~selisker/post/workflow/>
- Bibliography file can be selected
- Themes: *UITheme*: One Light; *Syntax Theme*: Base16 Tomorrow Light (or their Dark varieties)
- `insert-timestamp` is a nice option for generating foonote numbers: with a timestamp there will not be any collisions. Python timestamp (`crtl+alt+shift+U`) would work fine for this. Example of a timestamp: `1529359692`

# To Generate the Final Text

Simpy run the `wRoutine.py` script (for example, in*Terminal*, from the project's folder run: `python3 wRoutine.py`). A main draft and then a PDF file should be generated.



## Just a note on how to use  `Imagemagick`
	1. Imagemagick
		1. convert img1 img2 -append img12
			1. -append :: vertically
			2. +append :: horizontally

### Issue with typesetting bibliography

Currently the following hack is implemented (*pandoc* does not seem to generate bibliography correctly --- each item looks like a regular paragraph)

From here <https://tex.stackexchange.com/questions/57637/hanging-indents-in-bibliography>

The answer provided by @jon just gives me an error message.

But I found the following workaround to be working nicely. If your bibliography should appear at the end of the document (the default), just add the following lines at the very end of the Markdown document:

\noindent
\vspace{-2em}
\setlength{\parindent}{-0.5in}
\setlength{\leftskip}{0.5in}
\setlength{\parskip}{15pt}

However, if you're manually defining the position of the bibliography (using the tag <div id="refs"></div>), you have to wrap the above lines and the <div> tag in a Latex group to limit the formatting changes to the bibliography only:

\begingroup
\noindent
\vspace{-2em}
\setlength{\parindent}{-0.5in}
\setlength{\leftskip}{0.5in}
\setlength{\parskip}{15pt}

<div id="refs"></div>

\endgroup

Explanation of the commands:

\setlength{\parindent} and \setlength{\leftskip} define the hanging indentation of the bibiography entries.
\setlength{\parskip} defines the spacing between bibliography entries.
\noindent is needed in order to also have the very first bibliography entry correctly hanging indented.
\vspace{-2em} reduces the vertical spacing between the bibliography and the last paragraph before it (because \noindent adds a blank paragraph).
source: https://groups.google.com/d/msg/pandoc-discuss/4SKA5E11rO4/fDGiNSOsIMkJ
		
		
