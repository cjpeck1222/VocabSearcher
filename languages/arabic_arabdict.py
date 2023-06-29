import requests
from bs4 import BeautifulSoup


def print_entry(w):
    """This function compiles entry(w) into a string."""
    entry = "English:\n"
    entry += "  " + w['l1']
    if 'l1_add' in w:
        entry += " " + w['l1_add']
    entry += "\nArabic:\n"
    entry += w['l2']
    if 'l2_add' in w:
        entry += " " + w['l2_add']
    entry += '\n\n'
    return entry


def strip(w):
    """This function strips extra spaces from the beginning and end of additional information tags.

    Sometimes, additional information tags are just a space. This function also removes this space.

    Returns w after being processed.
    """
    if len(w) > 1:
        if w[0] == ' ':
            w = w[1:]

        if w[-1] == ' ':
            w = w[:-1]
    else:
        if w == ' ':
            w = ''
    return w


def get_entries(entry, lang):
    """This function extracts word and additional information (if it exists) from a row.

    entry = Entry to have words extracted from.
    lang = 'latin' for English, 'arabic' for Arabic

    The process is the same for English and Arabic, with the only difference being that ArabDict.com uses
    'latin' for English and 'arabic' for Arabic.

    Returns a tuple: the word and the clarifying information.
    """
    term = lang + '-term'
    entry.find(class_=lang)
    word = "".join(entry.find(class_=lang).find(class_=term).contents[0])
    clarify = strip("".join(entry.find(class_=lang).find(class_='term-info').contents))

    # Sometimes, this terms are surrounded in HTML <mark> tags. These must be removed.
    word.replace('<mark>', '')
    word.replace('</mark>', '')
    return word, clarify


def check_search_success(entry):
    """This function checks an entry and returns a boolean for whether there are valid search results."""
    e = entry.findAll("div", class_="rec-body description text-center p-10")
    if len(e) > 0:
        for d in e:
            for c in d.findAll('span'):
                if "No exact translation found for" in c.text:
                    return False
    return True


# This function looks up terms on ArabDict.com and extracts the results.
def arabdict(terms, ticker):
    """This function looks up terms on ArabDict.com and extracts the results.

    terms = Terms to look up.
    ticker = Window with ticker page to update progress.

    Returns a list of results compiled into strings.
    """
    # Create an empty list for the results.
    total_results = []

    # Start ticker variable.
    n = 1

    # If user clicks cancel button, cancel_process will be set to True.
    cancel_process = False

    for t in terms:
        if cancel_process:
            break

        # Get BeautifulSoup.
        url = "https://www.arabdict.com/en/english-arabic/" + t
        r = requests.get(url, timeout=10)
        soup = BeautifulSoup(r.text, "lxml")

        entries = soup.findAll("div", class_="rec-body description")

        # Check if search failed and add error message if it did.
        if not check_search_success(soup):
            total_results.append("No results found for " + t + " on ArabDict!\nSource: " + r.url)
        else:
            # Declare empty string for word.
            results = ''

            for e in entries:
                # Declare empty dictionary for entry.
                entry = {}

                # Entry's l1 and l2 keys refer to English and Arabic words respectively.
                entry["l1"], english_clarify = get_entries(e, 'latin')
                entry["l2"], arabic_clarify = get_entries(e, 'arabic')

                # Define l1_add and l2_add keys only if there is something to add.
                if english_clarify != '':
                    entry["l1_add"] = english_clarify
                if arabic_clarify != '':
                    entry["l2_add"] = arabic_clarify

                # Add entry to word search results.
                results += print_entry(entry)

            # Add word search results to total results.
            results += "\nSource:\n" + r.url
            total_results.append(results)

        # Update ticker to show progress.
        # Ticker returns True if user clicked cancel button.
        cancel_process = ticker.update_ticker(n, len(terms))
        n += 1

    return total_results
