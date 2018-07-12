# The Workflow

The process of algorithmic analysis involves a series of steps, which can be summed up as follows: 1) finding the machine-readable text of a book; 2) tagging the logical structure of the book; 3) tagging—manually and semi-automatically—relevant data in the structured text (alternatively, extracting relevant data automatically); 4) extracting and modeling tagged data; 5) visualizing and analyzing results. All these steps occur in this order only procedurally, but not necessarily on the conceptual level where one finds oneself constantly thinking about what kind of data can be extracted from a given source—and how exactly—and what kind of processes it can help to model.

## Step 1 {-}

Finding an electronic text of a medieval Arabic book has become rather easy over the past decades as a number of open-access electronic libraries have appeared in the Middle East.[^fn00004] Most of these libraries are repositories of text files in a variety of formats—usually, HTML, TXT, or MS Word—and offer no analytical tools, except for basic search capabilities. Before proceeding any further, one must collate the found text with a printed edition on which it is based in order to establish its overall adequacy. In most cases, these electronic texts are high-quality reproductions of printed editions (they seem to be produced with double-keying method),[^fn00005] and, for this reason, inherit all of the potential and real issues of critical editions of the printed era. It is also worth stressing here that most of these digital texts are based on printed editions that are widely used in the field of Arabic and Islamic studies.

[^fn00004]: Altogether, the libraries that I was able to survey include over 30,000 texts. The largest online libraries are: *al-Maktabaŧ al-šāmilaŧ* ([`www.shamela.ws`](http://www.shamela.ws); 6,300 texts); *al-Mishkāŧ* ([`www.almeshkat.net`](http://www.almeshkat.net); 7,300 texts); *Ṣayd al-fawāʾid* ([*www.saaid.net*](http://www.saaid.net); 10,000 texts); *al-Warrāq* ([*www.alwaraq.com*](http://www.alwaraq.com); 860 texts); *al-Maktabaŧ al-šīʿaŧ* ([`www.shiaonlinelibrary.com`](http://www.shiaonlinelibrary.com); 1,970 texts); other libraries come on CDs, DVDs (for example, *al-Muʿjam al-fiqhī*, Qom/Iran, 1,130 texts), and even external HDD (*al-Jāmiʿ al-kabīr*, ʿAmmān/Jordan, 2,400 texts).

[^fn00005]: The double-keying transcription method is confirmed to be the most accurate digitization approach, see [@HaafMeasuring2013].

## Step 2 {-}

The tagged logical structure offers one an ability to work with every logical unit of a book on the machine level. To provide this structural tagging, I am using a lightweight scheme of my own design, whose current version is named `OpenArabic mARkdown` (*more on it in the final section*): built on `regular expressions`[^fn00006] and implemented in `EditPad Pro` ([`https://www.editpadpro.com/`](https://www.editpadpro.com/)), the scheme offers the dynamic highlighting of tagging patterns and the folding of a tagged text into a table of contents. In a nutshell, this tagging task can be described as: 1) collating the electronic text with the relevant printed edition, and 2) ensuring that all words of chapter headers are on the same line and prepended with relevant `mARkdown` tags. For example, chapter headers of the first level receive tag '`### |`', those of the second—'`### ||`', those of the third—'`### |||`', and so on. Logical units of specific types have their own patterns.

[^fn00006]: An integral part of most programming languages, `regular expressions` is a mini-language for describing search patterns. For more details, see [`http://www.regular-expressions.info/`](http://www.regular-expressions.info/).

## Step 3 {-}

After the structure is tagged, one can either design a data extraction routine or manually tag needed information. A combination of automatic tagging (using entity lists) and manual disambiguation offers perhaps the optimal solution. Figure {@fig:md01} shows an example of an automatically tagged biography using entities lists for toponyms and ‘descriptive names’; year statements are rather regular in classical Arabic and can be identified with regular expressions and converted into numbers.[^fn00007] The morphology of tags is as follows: the tag starts with `@`, which is followed by `SOC` or `TOP`, which introduces the category of an entity, and concludes with two numbers—the first one marks the length of a prefix that should be dropped[^fn00008] and the second the length of an entity in words. When the tag is properly entered in front of the necessary word or the word group (up to 3 words), it is dynamically highlighted. Automatically inserted tags are highlighted in black.

> [**NB:** Below is just an example of how Arabic can be added into the text as a blockquote.]

> ARABIC:harawi.txt

![Automatically tagged entities in a biography: '`@SOC01`' for “descriptive names” (*nisbaŧ*s) that behave as social markers; '`@TOP01`'—for place names (toponyms); '`@YY167`'—for dates (year statements). You can see a mild issue of what happens when right-to-left and left-to-right languages appear in the same document: the order of symbols in tags appears different ('`SOC01@`', '`TOP01@`', '`YY167@`'), but the logical order remains correct.](./images/md_ara_01.png){#fig:md01}

[^fn00007]: Date statements can offer a valuable insight into a large Arabic corpus as well as specific books, see my blogpost “Chronological Coverage of an Arabic Corpus: An Experiment with Date Statements” [`https://alraqmiyyat.github.io/2016/03-29.html`](https://alraqmiyyat.github.io/2016/03-29.html).

[^fn00008]: Certain prepositions (*wa-*, *fa-*, 'and') and conjunctions (*li-*, 'for'; *bi-*, 'in, with', etc.) are attached to words in Arabic.

To avoid false positives, automatic tags can be disambiguated in the manner shown on Figure {@fig:md02}: '`@SOC01`' becomes '`@S01`'; '`@TOC01`' becomes '`@T01`'; '`@YY167`' becomes the year of death '`@YD167`'. These are manual variations of automatic tags for the same categories—they are shorter (to make manual tagging easier and faster), and are highlighted with different colors for the ease of visual recognition. To make things more accessible, Figure {@fig:md03} shows the same information in English.

![Manually disambiguated tagged entities in a biography: '`@S01`' for “descriptive names” (*nisbaŧ*s); '`@T01`'—for place names (toponyms); '`@YD167`'—for the date of death (year statements).](./images/md_ara_02.png){#fig:md02}

![Manually disambiguated tagged entities in the translated version of the Arabic biography given above.](./images/md_eng_01.png){#fig:md03}

**NB:** Automatic tagging of toponyms can be enhanced by inserting URIs of respective toponyms from a gazetteer of Islamic places. In our particular case, this will be al-Ṯurayyā Gazetteer ([`https://althurayya.github.io/`](https://althurayya.github.io/)), which was developed with this purpose in mind. The URIs in the gazetteer are designed to be human readable and aid in with disambiguation of complicated cases, such as, for example Ṭarābulus/Aṭrābulus—the toponym that may refer to the city of Tripoli in North Africa (sometimes appearing in the sources as Ṭarābulus al-Ġarb, ‘Tripoli of the West’) and to Tripoli in Levant (sometimes appearing in the sources as Ṭarābulus al-Šarq, ‘Tripoli of the East’); in such an ambiguous case the URIs of both places can be automatically inserted and flagged for disambiguation. A quick glance at the text is usually enough to determine which of two Tripolis is referred to, and the coordinates encoded into the URIs—'`ATRABULUS_131E328N_S`' and '`ATRABULUS_358E344N_S`'—help one to decide which of the URIs must be removed (the first URI is for the city in North Africa; the second—for that in Levant). The use of URIs in the process of tagging allows one to pull out all available information on tagged places from the gazetteer, such as transliteration of the place name, its coordinates, settlement type categorization and regional classification; for example, '`ATRABULUS_358E344N_S`' can be transformed into: *Aṭrābulus*, a *town* in the region of *al-Šām (Greater Syria)* with the coordinates of *34.4 LAT*, *35.8 LON*.

## Step 4 {-}

Now that we have our data tagged automatically and, ideally, disambiguated, one can proceed to extracting, enriching and modeling this data. In terms of **modeling** some explanations are required, particularly to those not familiar with Islamic history.[^fn00009] Traditional Arabic biographies usually include three major markers—chronological, geographical and onomastic/social—which can be used in a variety of distant reading modes of analysis. In the example above—in the bio-bibliographical record of al-Harawī (\textarabic{الهروي})—we have all three of them: 1) dates—in our case, the year of death, 163/780 CE ('`@YD163`'); 2) locations with which this person is associated—the village of Bāšān ('`@T01 Bāšān`') and the city of Herat ('`@S01 Harawī`'), the city of Nishapur ('`@T01 Naysābūr`'), the city of Mecca ('`@T01 Makkaŧ`'); and 3) “descriptive names” (sing. *nisbaŧ*)—a ‘jurist’ ('`@S01 faqīh [jurist]`'), a ‘traditionist’ ('`@S01 muḥaddiṯ [traditionist]`', a specialist in the study and transmission of “the words of the Prophet”), and, again, a Herati ('`@S01 Harawī`'), a person who is strongly associated with the city of Herat (in this particular case, this person got the name of ‘Herati’ because he comes from the village of Bāšān in the district of Herat/Harāŧ). From this profile we get this person’s *terminus ante quem*; we can construct his geographical network (on the level of settlements, and—through the gazetteer—on the level of regions); and we also know what kind of religious specialization he had and to what geographical community he belonged (onomastic data often also provides social, professional, occupational, communal and ethnic markers). Combining thousands of such biographical profiles together and subsetting them with different parameters we can get detailed insights into chronological and geographical patterns of a variety of social, religious and professional groups that can be identified in a specific biographical collection.

[^fn00009]: One should think of *modeling*, to quote Willard McCarty, “a continual process of coming to know by manipulating representations”. See his “Modeling: A Study in Words and Meanings”, in [@NewCompanionDH2016]; and, more extensively, [@McCartyHumanities2014, pp.20–72].

**NB:** It should be noted that the tagging does not have to be limited to these three types of markers and can be extended in a similar manner to any other relevant category, especially around specific linguistic patterns. For example, one can tag specific phrases that describe biographees’ religious training, tag people one studied under, or, as immediately relevant to our example, books that one composed.

In terms of **extraction**, with a relatively simple script (in my case, written in `Python`), one can automatically extract tagged data from all biographies and convert it into a format suitable for further analysis and visualization. The script performs the following: 1) numbers all biographies sequentially (using biographical tags, '`### $ `', as anchors); 2) splits the entire text of the book into individual biographies; 3) extracts all tagged items with regular expressions and reformats everything into a CSV-format file, where the abstraction of our biography will look as follows (assuming we used URIs from the gazetteer to tag and disambiguate toponyms):[^fn00010]

```
======================
id, item, category
======================
000006, 163, year_of_death
000006, BASHAN_623E342N_S, toponym
000006, NAYSABUR_587E361N_S, toponym
000006, MAKKA_398E213N_S, toponym
000006, harawī, descriptive_name
000006, faqīh, descriptive_name
000006, muḥaddiṯ, descriptive_name
======================
```

[^fn00010]: Additional lists of aliases should also be constructed and used in order to unify different forms of the same words or different names of the same entities. For example, such lists allow us to unify different names commonly employed for Baġdād (Madīnaŧ al-salām, Baġḏād, and Baġdād); the same approach, amplified with some scripting, can also be used to unify various morphological forms of the same words. Arabic morphology is particularly challenging because of a plethora of attached prefixes and suffixes, which in different often stackable combinations can multiply words into over 50 variations; existing morphological analyzers do not yet offer a reliable solution, especially for classical Arabic.

Converted into such a format our data can now be enriched, reshaped and subset for a variety of research questions. (Further data manipulations and visualizations are performed in `R`, [`https://www.r-project.org/`](https://www.r-project.org/)) The easiest example of the enrichment of our data can be given on geographical information—now that we have our geographical data in the form of URIs, we can add additional geographical information from the gazetteer, such as coordinates and regions; regions are particularly relevant, since they will allow one to move between local and regional levels of data analysis. In a similar way, a detailed onomastic table can provide broader categories for conducting analysis on a higher level: for example, descriptive names like *faqīh*, ‘jurist’, *qāḍī*, ‘judge’, *muftī*, ‘jurisconsult’ can be thus combined into a broader category of ‘legal professions’ and one can then graph and map both specific legal professions as well as all legal professionals together as a broader category.

The filtering and subsetting of the enriched data then can be performed in the following manner:

1) one first identifies a type (let’s say ‘jurisconsults’) or a broader category (in this case, the corresponding category will be ‘legal professions’) and filters the data set using the selected value;
2) the filtered results will have the IDs of all the biographees associated with the selected type or the broader category, and this list of IDs can be used to re-subset the main data set to get all relevant chronological, geographical and onomastic markers;
3) aggregating chronological markers, we can now build a graph of the temporal distribution of jurisconsults or legal professionals more generally;
4) aggregating geographical markers, we can build a cartogram of their spatial distribution;
5) combining chronological and geographical markers, we can also build cartograms of spatial distribution for different chronological periods and with that trace their spatial dynamic of their distribution over time;
6) combining geographical data further, we can also build cartograms of interregional connections, and also trace how the configuration and density of these connections was changing over time.

Keeping in mind that all biographies now have IDs, one can easily go back and forth between distant and close reading of relevant biographies, thus improving the outcome of both.
