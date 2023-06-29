# VocabSearcher

	What is it?
When reading something in a foreign language that you are learning, especially in the beginning, there are going to be many words that you don't recognize. You could spend the time and energy looking up all the words in your dictionary of choice, but if you're dealing with a long list of words, that can become a very slow and tedious process.

In fact, people who discuss foreign language acquisition specifically discourage looking up every single word. It takes too long, and the tediousness is downright draining! The better idea is to look up the few key words that stand out, learn what you can and accept that you're not going to understand everything.

It was with that situation in mind that I started this project. Vocab Searcher is a program that, given a list of terms, will look up each term in a selected dictionary, extract the results and then display them for the user to look through.

Hopefully, by facilitating the searching of larger volumes of terms, this program will enable foreign language students to learn vocabulary more quickly.

	How does it work?
Vocab Searcher, written in Python, uses the requests and BeautifulSoup packages to look up terms in the selected dictionary, parsing the needed information.

It uses PyQt5 to create the GUI, cycling through four widgets in a QStackedLayout:

(1) Info: gives brief instructions on how to use the program.

(2) Options: the user can select the language and dictionary to look the terms up in, as well as type in the terms.

(3) Ticker: tells the user the progress of the searches. There is also a cancel button, should the user decide they want to stop it.

(4) Results: the user can cycle through the results and see what the program found on the dictionary.

	Search Direction and Strict Search
Foreign languages that, like English, use a variant of the Latin alphabet as their writing system present a unique challenge, specifically one of ambiguity.

For example, if you were looking up terms in an English-Arabic dictionary, "house" would be unambiguously English, while its Arabic translation "بيت" would be unambiguously Arabic, simply because of the different writing systems.

But if you were looking up terms in an English-French dictionary, would "chat" refer to the English word for "talk informally," or would it refer to the French word for "cat?"

Search direction removes this ambiguity.

There is also strict search. If you go to WordReference's English-French dictionary, set it up to French to English and then type in an English word that does not resemble any French word, WordReference returns the English-to-French results for that English word. This could be useful if someone types a mixture of English and French words on purpose, but if someone is reading an article or short story in French, and they only want to look up French words, this might not be wanted. For this reason, there is a "strict search" option, which enables the user to disallow any search results outside of the specified direction.

	Features
- Can look up French, Spanish, Italian, Portuguese, Romanian, German, Dutch, Polish, Czech, Swedish, Icelandic, Turkish, Greek, Korean and Arabic on WordReference (wordreference.com). *See note below.
- Can look up Arabic on arabdict (arabdict.com).
- Can look up Hebrew on Morfix (morfix.co.il).
- Can look up Chinese on MDBG (mdbg.net).

Note: WordReference uses very similar formatting for most of its various dictionaries. Once one of these languages was supported, it was extremely easy to add support for the others.

WordReference also has an English-Russian dictionary, but the Russian-to-English dictionary entries use a very different format. I don't know Russian, so I was uncertain how to parse the results from those pages. As such, this program does not support Russian yet.

	Future Plans
- Add support for Japanese through Jisho (jisho.org). Any more languages and/or dictionaries that could be supported are also a possibility.
- Add dark mode to GUI.
- Enable user to set default settings so that settings can be pre-set upon loading.
