import requests
from bs4 import BeautifulSoup


def print_entry(w, pair):
    """ This function compiles individual search results into a string.

    w = Entry result to be compiled.
    pair = Language pair, this will be "enTohe" or "heToen" as on Morfix.

    Returns compiled string.
    """
    # Check language pair and put language names in right order.
    # Indentation helps with left-to-right language (English), but not with right-to-left language (Hebrew).
    if pair == "enTohe":
        langs = ["English", "Hebrew"]
        l1_indent = "  "
        l2_indent = ""
    else:
        langs = ["Hebrew", "English"]
        l1_indent = ""
        l2_indent = "  "

    # Compile elements of entry into formatted text.
    txt = ''
    txt += langs[0] + ":\n"
    txt += l1_indent + w['l1']
    if w['l1_add'] != '':
        txt += " (" + w['l1_add'] + ")"
    txt += "\n" + langs[1] + ":\n"
    txt += l2_indent + w['l2'] + "\n\n"
    return txt


def check_search_success(entry):
    """This function checks whether there is a 'No Translations Found' message on the website."""
    error_msg = entry.findAll("div", class_="Transletion_noresult_content")
    return len(error_msg) == 0


def morfix(terms, ticker):
    """This function iterates through a list of terms and looks them up on morfix.co.il.

    terms = The list of terms to look up.
    ticker = The window to update with progress in order to communicate this progress to the user.
    """
    # Assign empty list for search results.
    total_results = []

    # Initialize n for progress ticker.
    n = 1

    # If the user clicks the cancel button, cancel_process will turn True, and the for loop will stop.
    cancel_process = False

    for t in terms:
        if cancel_process:
            break

        # Get BeautifulSoup.
        r = requests.get("https://www.morfix.co.il/" + t, timeout=10)
        soup = BeautifulSoup(r.text, "lxml")

        # Check validity of search results.
        if not check_search_success(soup):
            total_results.append("No results found for " + t + " on Morfix!\nSource: " + r.url)

        else:
            # Create empty string for word.
            word_entry = ''

            # If search results contain Translation_content_enTohe, it is English to Hebrew.
            # Otherwise, it's Hebrew to English.
            entries = soup.findAll("div", class_="Translation_content_enTohe")
            if len(entries) > 0:
                language_pair = "enTohe"
            else:
                entries = soup.findAll("div", class_="Translation_content_heToen")
                language_pair = "heToen"

            # Extract each individual entry.
            for e in entries:
                # l1 refers to source language word.
                entry = dict()
                entry['l1'] = e.find("span", class_="Translation_spTop_"+language_pair).text[:-1]

                # l1_add refers to clarifier for source language word, if it exists.
                entry['l1_add'] = e.find("span", class_="Translation_sp2Top_"+language_pair).text

                # l2 refers to translation results.
                l2 = e.find("div", class_="normal_translation_div")

                # For some reason, search results on Morfix end in many spaces and begin with two letters that create
                # a newline. These two lines strip search results of this.
                l2 = l2.text.replace('            ', '')
                l2 = l2[2:]
                entry['l2'] = l2

                # Once finished, add formatted entry to word_entry.
                word_entry += print_entry(entry, language_pair)

            # Finally, add URL source to word results, and then word results to list of results.
            word_entry += "\nSource:\n" + r.url
            total_results.append(word_entry)

        # Have ticker window update progress to communicate with user and update n.
        # Window.update_ticker returns True if user clicked the cancel button.
        cancel_process = ticker.update_ticker(n, len(terms))
        n += 1

    return total_results
