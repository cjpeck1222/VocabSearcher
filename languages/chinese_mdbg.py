import requests
from bs4 import BeautifulSoup


def print_entry(w):
    """This function converts dictionary entry(w) into a formatted string."""
    entry = "Chinese:\n"
    if 'hanz' in w:
        entry += "  Hanzi: " + w['hanz'] + '\n'
    else:
        entry += "  Simplified: " + w['simp'] + '\n'
        entry += "  Traditional: " + w['trad'] + '\n'
    entry += "  Pinyin: " + w['piny'] + '\n'
    entry += "  Definition: " + w['defs'] + '\n\n'
    return entry


def mdbg(terms, ticker):
    """This function looks up terms on MDBG.net and extracts search results.

    terms = Terms to look up.
    ticker = Window to update progress.

    Returns a list of entries formatted into strings.
    """

    # Declare empty list for results and start ticker.
    term_results = []
    n = 1

    # If user clicks cancel button, cancel_process will be set to True.
    cancel_process = False

    for term in terms:
        if cancel_process:
            break

        # Get BeautifulSoup.
        params = {"wdqb": term}
        url = "https://www.mdbg.net/chinese/dictionary?"
        r = requests.get(url, params=params, timeout=10)
        soup = BeautifulSoup(r.text, "lxml")

        entries = soup.findAll("tr", class_="row")

        # Declare empty string to contain all search results for each term.
        output = ''

        for i in entries:
            # Create empty dictionary for each row.
            result = {}

            # Extract hanzi.
            hanzis = i.find_all("div", class_="hanzi")
            hanzi = []
            for h in hanzis:
                hanzi.append(h.text)

            # If both traditional Chinese and Simplified Chinese are listed, then hanzi will have two results.
            # Otherwise, it only has one.
            if len(hanzi) == 2:
                result["simp"] = hanzi[0]
                result["trad"] = hanzi[1]
            else:
                result["hanz"] = hanzi[0]

            # Extract pinyin pronunciation and definitions.
            # For some reason, definitions on MDBG sometimes start with a space,
            # hence the if statement to remove space if it exists.
            result["piny"] = i.find("div", class_="pinyin").text
            if result["piny"][0] == ' ':
                result["piny"] = result["piny"][1:]
            result["defs"] = i.find("div", class_="defs").text

            # Add this row's data to the result for the term.
            output += print_entry(result)

        # If results were found, entries would have results added to it. Add to term_results.
        # If no results were found, entries would still be ''. Add error message instead.
        if len(output) == 0:
            term_results.append("No results found for " + term + " on MDBG!\nSource: " + r.url)
        else:
            output += "\nSource:\n" + r.url
            term_results.append(output)

        # Update ticker to show progress.
        # ticker returns True if user clicked cancel button.
        cancel_process = ticker.update_ticker(n, len(terms))
        n += 1

    return term_results
