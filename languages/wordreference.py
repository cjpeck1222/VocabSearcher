import requests
from bs4 import BeautifulSoup
from languages import language_terms


def print_entry(w, languagepair):
    """This function takes search results and compiles them into strings.

    w = Entry to be compiled.
    languagepair = Pair of languages, abbreviated as four-letter combination. (e.g. enfr = English-French)
    """
    # Get l1 and l2 by searching keys in LanguageTerms l_terms by values from abbreviations.
    l1 = list(language_terms.l_terms.keys())[list(language_terms.l_terms.values()).index(languagepair[0:2])]
    l2 = list(language_terms.l_terms.keys())[list(language_terms.l_terms.values()).index(languagepair[2:4])]

    # Add l1 and its additional information if it exists.
    entry = l1 + ":\n"
    entry += "  " + w['l1']
    if 'l1_add' in w:
        entry += " " + w['l1_add']
    entry += "\n"

    # Add all l2 entries.
    entry += l2 + ":\n"
    for e in w['l2']:
        entry += "  " + e['word']
        if 'add' in e:
            entry += " " + e['add']
        entry += '\n'

    # Iterate through l1 example sentences if they exist.
    if len(w['l1_ex']) > 0:
        if len(w['l1_ex']) > 1:
            plural_marker = 's'
        else:
            plural_marker = ''
        entry += ("Example sentence" + plural_marker + " in " + l1 + ":\n")
        for x in w['l1_ex']:
            entry += "  " + x + '\n'

    # Iterate through l2 example sentences if they exist.
    if len(w['l2_ex']) > 0:
        if len(w['l2_ex']) > 1:
            plural_marker = 's'
        else:
            plural_marker = ''
        entry += ("Example sentence" + plural_marker + " in " + l2 + ":\n")
    for x in w['l2_ex']:
        entry += "  " + x + '\n'

    entry += "\n"
    return entry


def print_error(term, url):
    """This function returns an error message for when no valid search results exist."""
    return "No results found for " + term + " on WordReference!\nSource: " + url


def order_error(term, url):
    """This function returns an error message for when only disallowed, reverse-language results exist."""
    return "No results found in the right language-pair order for " + term + " on Wordreference!\nSource: " + url


def new_entry():
    """This function creates and returns an empty dictionary for search results with l2, l1_ex and l2_ex initialized."""
    return {'l2': [], 'l1_ex': [], 'l2_ex': []}


def search(terms, language_pair, strict_search, ticker):
    """This function looks up terms on WordReference, extracts search results and compiles list of results.

    terms = Terms to be looked up.
    language_pair = List of to and from languages to be looked up.
    strict_search = If reverse-order results should be disallowed if correct-order results don't exist.
    ticker = The window that has a ticker page to update user on progress.

    Returns a list of search results and/or error messages compiled into strings.
    """
    # Determine ending of URL address.
    # Spanish uses a different format.
    # All other languages use a pair of two-letter abbreviations. See l_terms in language_terms.py for more info.
    foreign_language = "Spanish"
    if language_pair == ['English', 'Spanish']:
        l_term = "es/translation.asp?tranword="
    elif language_pair == ['Spanish', 'English']:
        l_term = "es/en/translation.asp?spen="
    else:
        l_term = ''
        for language in language_pair:
            l_term += language_terms.l_terms[language]
            if language != "English":
                foreign_language = language
        l_term += '/'

    # Define empty list for search results and start ticker variable.
    # If user clicks the cancel button, cancel_process will be set to True.
    return_terms = []
    num = 1
    cancel_process = False

    for term in terms:
        if cancel_process:
            break

        url = "https://www.wordreference.com/" + l_term + term
        r = requests.get(url, timeout=10)
        soup = BeautifulSoup(r.text, "lxml")

        # Determine whether page has valid search results.
        if len(soup.find_all(id='noTransFound')) > 0:
            return_terms.append(print_error(term, r.url))
        else:
            # Extract search results from page.
            entries = soup.findAll('tr', class_=['odd', 'even'])

            # Declare empty string for definitions.
            defs = ''

            # Declare empty dictionary for entry.
            entry = new_entry()

            # after_frwrd is used because on WordReference, additional info added to clarify the meaning
            # of the source word is added in an unclassed element immediately after the word.
            # after_frwrd is set to True after FrWrd, to False after anything else.
            after_frwrd = False

            # first_entry is used to prevent an empty entry at first FrWrd.
            first_entry = True

            # A string to hold the language pair for this specific search result's website.
            # This will be changed as the function checks the language pair in the header.
            pair = ''

            # If the header finds the langauges in the wrong order (i.e. opposite of language_pair passed to this
            # function, then this will be set to True.
            wrong_order = False

            # Determine the language pair order by iterating through elements of the header on the website.
            header = soup.find('tr', class_='langHeader')
            if header is not None:
                for c in header:
                    if foreign_language == "Spanish":
                        if c.text in language_terms.spanish_terms["English"]:
                            pair += language_terms.l_terms["English"]
                        elif c.text in language_terms.spanish_terms["Spanish"]:
                            pair += language_terms.l_terms["Spanish"]
                    else:
                        if c.text == language_terms.autoglottonyms[foreign_language]:
                            pair += language_terms.l_terms[foreign_language]
                        elif c.text == language_terms.english_names[foreign_language]:
                            pair += language_terms.l_terms["English"]
                    if len(pair) == 4:
                        continue
                # If search results have language pair in wrong order and strict_search is set to True.
                if pair != l_term[:-1] and strict_search:
                    wrong_order = True
                else:
                    # Iterate through search results for each term.
                    for i in entries:
                        to2 = ''
                        for n in i.children:
                            if n.name is not None:
                                # Find out what we're looking at.
                                cl = n.attrs.get('class')

                                # FrWrd is class used for words in left column (the source language).
                                # If first entry, set first_entry to false.
                                # Otherwise, add previous entry to definitions and start new entry.
                                # after_frwrd is set to True as this element may be followed by additional info.
                                if cl == ['FrWrd']:
                                    if first_entry:
                                        first_entry = False
                                    else:
                                        defs += print_entry(entry, pair)
                                        entry = new_entry()

                                    entry['l1'] = n.text
                                    after_frwrd = True

                                # If both class is None and after_frwrd is True, this means it's
                                # clarifying information after source language word.
                                elif cl is None and after_frwrd:
                                    fr2 = n.text

                                    # On WordReference, if both source language and target language have
                                    # clarifying info, these are bundled into one element.
                                    # This element must therefore be iterated through to be split up.
                                    for c in n.children:
                                        if c.name is not None:

                                            # Target language clarifier in this case is class dsense.
                                            # If this exists, then this must be removed from the overarching element.
                                            # Set it to to2 so it can be paired with the ToWrd which follows it.
                                            cl2 = c.attrs.get('class')
                                            if cl2 == ['dsense']:
                                                to2 = c.text
                                                fr2 = fr2.replace(to2, "")
                                                to2 = " " + to2
                                    entry['l1_add'] = fr2
                                    after_frwrd = False

                                # On WordReference, To2 is class used for target language clarifiers that
                                # do not have corresponding clarifier for source language.
                                # Set it to to2 so it can be paired with the ToWrd which follows it.
                                elif cl == ['To2']:
                                    to2 = n.text
                                    after_frwrd = False

                                # On WordReference, ToWrd is class for target language word.
                                # If to2 is set to anything,
                                # then this means there is additional info to pair with target word.
                                # See two preceding if statements on same indentation level.
                                # (i.e. (cl is None and after_frwrd) and (cl == ['To2']))
                                elif cl == ['ToWrd']:
                                    entry['l2'].append({'word': n.text, 'add': to2})
                                    to2 = ''
                                    after_frwrd = False

                                # On WordReference, FrEx is class for example sentences in source language.
                                elif cl == ['FrEx']:
                                    entry['l1_ex'].append(n.text)
                                    after_frwrd = False

                                # On WordReference, ToEx is class for example sentences in target language.
                                elif cl == ['ToEx']:
                                    entry['l2_ex'].append(n.text)
                                    after_frwrd = False

            # As unlikely as it is, if user types gibberish words made of punctuation marks,
            # WordReference leads to home page rather than "no translation found" page.
            # This if-else statement catches this.
            # Add compiled results or error message accordingly.
            if 'l1' in entry:
                defs += print_entry(entry, pair)
                defs += "\nSource:\n" + r.url
            elif wrong_order:
                defs += order_error(term, r.url)
            else:
                defs += print_error(term, r.url)
            return_terms.append(defs)

        # Have ticker window update progress.
        cancel_process = ticker.update_ticker(num, len(terms))
        num += 1
    return return_terms
