import sys
from languages import hebrew_morfix, arabic_arabdict, chinese_mdbg, wordreference
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtWidgets import QWidget, QApplication, QVBoxLayout, QComboBox, QLabel
from PyQt5.QtWidgets import QLineEdit, QPushButton, QHBoxLayout, QCheckBox, QFrame
from PyQt5.QtWidgets import QPlainTextEdit, QStackedLayout, QProgressBar


class VocabWindow(QWidget):
    def __init__(self):
        self.app = QApplication(sys.argv)
        super().__init__()

        self.setWindowTitle("Vocab Searcher")

        # Declare instance variables that need to accessed by various functions.

        # langs_latin is a set of all the languages that use the Latin script.
        self.langs_latin = {'French',
                            'Spanish',
                            'Portuguese',
                            'Italian',
                            'Romanian',
                            'German',
                            'Dutch',
                            'Polish',
                            'Czech',
                            'Swedish',
                            'Icelandic',
                            'Turkish'
                            }

        # en_to_l2(i.e. English to L2) indicates whether English is the source or target language.
        self.en_to_l2 = True

        # input_box is where user inputs terms.
        self.input_box = QPlainTextEdit()
        font = QFont()
        font.setPointSize(16)
        self.input_box.setFont(font)

        # cancel_process is used to determine whether user clicked the cancel button on ticker_page.
        self.cancel_process = False

        # results is what the search functions return.
        # terms is what was looked up.
        self.results = []
        self.terms = []

        # results_label and results_view is where results are displayed.
        # results_index is which result is being shown. results_index_label is where the index is shown.
        self.results_label = QLineEdit()
        self.results_label.setReadOnly(True)
        self.results_label.setFont(font)

        self.results_view = QPlainTextEdit()
        self.results_view.setReadOnly(True)
        self.results_view.setFont(font)

        self.results_index = 0

        self.results_index_label = QLabel()
        self.results_index_label.setAlignment(Qt.AlignCenter)

        # ticker is the label and ticker_bar is the progress bar which indicate progress of searching.
        self.ticker = QLabel()
        self.ticker.setFont(QFont('Times font', 16))
        self.ticker.setAlignment(Qt.AlignCenter)

        self.ticker_bar = QProgressBar()
        self.ticker_bar.setAlignment(Qt.AlignCenter)

        # Setting up individual pages for StackedLayout pages.
        self.info_page = QWidget()
        self.options_page = QWidget()
        self.ticker_page = QWidget()
        self.results_page = QWidget()
        self.pages = QStackedLayout()

        self.setLayout(self.pages)

        self.create_info_page()
        self.create_input_page()
        self.create_ticker_page()
        self.create_results_page()

        # Enter the mainloop.
        self.show()

        sys.exit(self.app.exec_())

    def create_info_page(self):
        """"This function creates the info page that first shows at loading."""
        info_label = QLabel("This program enables you to look up a list of terms on\n" +
                            "foreign-language dictionaries instead of looking them up\n" +
                            "one by one.\n\n" +
                            "Simply type each word or phrase you want to look up\n" +
                            "in its own line in the input box, select your options and then search!")
        info_label.setFont(QFont('Times font', 16))
        info_label.setAlignment(Qt.AlignCenter)
        info_button = QPushButton("OK")

        info_layout = QVBoxLayout()

        info_layout.addWidget(info_label)
        info_layout.addWidget(info_button)

        self.info_page.setLayout(info_layout)
        self.pages.addWidget(self.info_page)

        info_button.clicked.connect(lambda: self.pages.setCurrentWidget(self.options_page))

    def create_input_page(self):
        """Create the input/options page."""
        # The first row is for language selection.
        language_select_label = QLabel("Select language:")
        language_select = QComboBox()
        langs = ['French',
                 'Spanish',
                 'Italian',
                 'Portuguese',
                 'Romanian',
                 'German',
                 'Dutch',
                 'Polish',
                 'Czech',
                 'Swedish',
                 'Icelandic',
                 'Turkish',
                 'Greek',
                 'Chinese',
                 'Korean',
                 'Arabic',
                 'Hebrew'
                 ]
        language_select.addItems(langs)

        language_row = QHBoxLayout()
        language_row.addWidget(language_select_label)
        language_row.addWidget(language_select)

        # The second row is for dictionary selection.
        search_select_label = QLabel("Search on:")
        search_select = QComboBox()
        lang_search_options = {'French': ["WordReference"],
                               'Spanish': ["WordReference"],
                               'Italian': ["WordReference"],
                               'Portuguese': ["WordReference"],
                               'Romanian': ["WordReference"],
                               'German': ["WordReference"],
                               'Dutch': ["WordReference"],
                               'Polish': ["WordReference"],
                               'Czech': ["WordReference"],
                               'Swedish': ["WordReference"],
                               'Icelandic': ["WordReference"],
                               'Turkish': ["WordReference"],
                               'Greek': ["WordReference"],
                               'Chinese': ["MDBG"],
                               'Korean': ["WordReference"],
                               'Arabic': ["ArabDict", "WordReference"],
                               'Hebrew': ["Morfix"]
                               }
        search_select.addItems(lang_search_options['French'])

        search_row = QHBoxLayout()
        search_row.addWidget(search_select_label)
        search_row.addWidget(search_select)

        # The third row is for direction selection.
        direction_label = QLabel("Set Direction:")
        direction = QLineEdit()
        direction.setText("English to French")
        direction.setReadOnly(True)
        direction_switch = QPushButton()
        direction_switch.setIcon(QIcon("view/switch.png"))

        direction_row = QHBoxLayout()
        direction_row.addWidget(direction_label)
        direction_row.addWidget(direction)
        direction_row.addWidget(direction_switch)

        # The fourth row is for an option to include or exclude reverse-language search results.
        # I.e. If direction is set to English-to-French, but a word searched on WordReference returns
        # French-to-English results but no English-to-French, should this be included?
        reverse_checkbox = QCheckBox("Allow search results with reversed language pair")

        # Encase the last two rows in a frame which can be hidden based on whether
        # the language selected uses the Latin alphabet. See switch_direction() above for reasoning for this.
        latin_layout = QVBoxLayout()
        latin_layout.addLayout(direction_row)
        latin_layout.addWidget(reverse_checkbox)

        latin_visible = QFrame()
        latin_visible.setLayout(latin_layout)

        # Button to start search.
        search_button = QPushButton("Search")

        # Putting together the options page and adding it to the StackedLayout pages.
        options = QVBoxLayout()
        options.addLayout(language_row)
        options.addLayout(search_row)
        options.addWidget(latin_visible)
        options.addWidget(self.input_box)
        options.addWidget(search_button)

        self.options_page.setLayout(options)

        self.pages.addWidget(self.options_page)

        # If language_select is changed, search_select must be updated.
        language_select.currentIndexChanged.connect(lambda:
                                                    self.update_search_options(search_select, lang_search_options,
                                                                               language_select.currentText(),
                                                                               latin_visible, direction)
                                                    )

        # If direction_switch is clicked, change direction of search.
        direction_switch.clicked.connect(lambda: self.switch_direction(direction, language_select.currentText()))

        # Make search_button start search.
        search_button.clicked.connect(lambda: self.run_searches(self.input_box.toPlainText(),
                                                                language_select.currentText(),
                                                                search_select.currentText(),
                                                                not reverse_checkbox.isChecked())
                                      )

    def update_search_options(self, search, options, lang, latin_visible, direction):
        """This function updates the dictionary seasrch options when a different language is selected.

        search = QComboBox that lists dictionary options.
        options = Dictionary that contains dictionary options.
        lang = Language that search must be set to.
        latin_visible = Frame that should be visible with languages with Latin alphabet.
        direction = QLineEdit that states language order, must be updated with new langauge.
        """
        # Repopulate search QComboBox with appropriate search options.
        search.clear()
        search.addItems(options[lang])

        # If language uses Latin alphabet, latin_visible should be visible, hidden otherwise.
        # Also update direction with new language if it needs to be visible.
        if lang in self.langs_latin:
            latin_visible.setHidden(False)
            if self.en_to_l2:
                direction.setText("English to " + lang)
            else:
                direction.setText(lang + " to English")
        else:
            latin_visible.setHidden(True)

    def switch_direction(self, direction_bar, lang):
        """This function toggles the direction of the language search.

        direction_bar = the QLineEdit that states the direction to the user.
        lang = the foreign language currently selected.

        This is relevant to languages that use the Latin alphabet and have words that resemble English words.
        E.g. does "chat" refer to the English verb "to chat", or is it the French word for "cat"?
        Is "case" an English word, or is it the Italian word for "houses"?

        The search direction determines how the search function used will approach such ambiguous cases.

        For languages that do not use the Latin alphabet (e.g. Chinese or Arabic), there is no such ambiguity.
        """
        if self.en_to_l2:
            self.en_to_l2 = False
        else:
            self.en_to_l2 = True

        if self.en_to_l2:
            direction_bar.setText("English to " + lang)
        else:
            direction_bar.setText(lang + " to English")

    def run_searches(self, user_input, foreign_lang, dictionary, strict_search):
        """This function starts the search process, preparing the parameters.

        user_input = What has been typed into the input box.
        foreign_lang = The foreign language selected.
        dictionary = The dictionary selected.
        strict_search = Whether reverse-language results should be excluded.
        """
        # If input has nothing in it, ignore. Split into list otherwise.
        if len(user_input) > 0 and not self.cancel_process:
            self.terms = user_input.split('\n')

            # Define dictionary search function to be called.
            dictionaries = {"WordReference": [wordreference.search, 3],
                            "MDBG": [chinese_mdbg.mdbg, 1],
                            "ArabDict": [arabic_arabdict.arabdict, 1],
                            "Morfix": [hebrew_morfix.morfix, 1]
                            }
            f = dictionaries[dictionary][0]

            # Define language_pair.
            language_pair = []
            if self.en_to_l2:
                language_pair.append("English")
                language_pair.append(foreign_lang)
            else:
                language_pair.append(foreign_lang)
                language_pair.append("English")

            # If foreign language does not use Latin alphabet, then strict_search does not matter.
            if foreign_lang not in self.langs_latin:
                strict_search = False

            # Change page to ticker page and then run search.
            self.pages.setCurrentWidget(self.ticker_page)
            self.app.processEvents()

            # Call function with correct number of parameters.
            # WordReference requires language_pair and strict_search; other functions don't.
            if dictionaries[dictionary][1] == 3:
                self.results = f(self.terms, language_pair, strict_search, self)
            else:
                self.results = f(self.terms, self)

            # Reset ticker label and progress bar for next search if there is one.
            self.ticker.setText('')
            self.ticker_bar.setValue(0)

            # If the process was canceled, it should go back to the options page without displaying results.
            # Make cancel_process False so that search can be started if the user tries to start it.
            # Empty out terms and results as these are only needed for searching and results.
            if self.cancel_process:
                self.cancel_process = False
                self.results = []
                self.terms = []
                self.pages.setCurrentWidget(self.options_page)
            # If the process finished without being canceled, it should go to the results page.
            # show_results is called with inc of 0 to show first result.
            else:
                self.show_results(0)
                self.pages.setCurrentWidget(self.results_page)

    def create_ticker_page(self):
        """This function creates the ticker page which reports progress to the user and has a cancel button."""
        ticker_frame = QFrame()
        ticker_frame_layout = QVBoxLayout()
        ticker_frame_layout.addWidget(self.ticker)
        ticker_frame_layout.addWidget(self.ticker_bar)
        ticker_frame.setLayout(ticker_frame_layout)

        cancel_button = QPushButton("Cancel")
        cancel_button.clicked.connect(self.cancel)

        ticker_display = QVBoxLayout()
        ticker_display.addWidget(ticker_frame)
        ticker_display.addWidget(cancel_button)

        self.ticker_page.setLayout(ticker_display)

        self.pages.addWidget(self.ticker_page)

    def cancel(self):
        """If the cancel button is clicked on the ticker page, then set cancel_process to True."""
        self.cancel_process = True

    def update_ticker(self, x, y):
        """This function is called by the search functions in the language folder to update ticker.

        Returns cancel_process so that if user clicks the cancel button, the search process will end.
        """
        self.ticker.setText("Searching in progress.\nPlease wait.\n" + str(x) + " out of " + str(y))
        self.ticker_bar.setValue(round(x/y*100))
        self.app.processEvents()
        return self.cancel_process

    def create_results_page(self):
        """This function creates the results page where search results are displayed to the user."""
        # First row is for "previous" and "next" buttons,
        # as well as an indicator of which result is displayed and how many results there are.
        prev_btn = QPushButton("Previous")
        next_btn = QPushButton("Next")
        nav_row = QHBoxLayout()
        nav_row.addWidget(prev_btn)
        nav_row.addWidget(self.results_index_label)
        nav_row.addWidget(next_btn)

        # Bottom row is for "new search" and "exit" buttons.
        again = QPushButton("New Search")
        close = QPushButton("Exit")
        end_row = QHBoxLayout()
        end_row.addWidget(again)
        end_row.addWidget(close)

        # Put results page together and add it to the QStackedLayout pages.
        results_layout = QVBoxLayout()
        results_layout.addLayout(nav_row)
        results_layout.addWidget(self.results_label)
        results_layout.addWidget(self.results_view)
        results_layout.addLayout(end_row)

        self.results_page.setLayout(results_layout)
        self.pages.addWidget(self.results_page)

        # Add functionality to the buttons.
        prev_btn.clicked.connect(lambda: self.show_results(-1))
        next_btn.clicked.connect(lambda: self.show_results(1))
        again.clicked.connect(self.start_new_search)
        close.clicked.connect(self.close)

    def show_results(self, inc):
        """This function updates the results page. inc is used to change the entry being shown."""
        self.results_index += inc

        # If results_index is out of bounds, make it loop.
        if self.results_index < 0:
            self.results_index = len(self.results) - 1
        elif self.results_index >= len(self.results):
            self.results_index = 0

        # Change text of results' label, view and index label to reflect change.
        self.results_label.setText(self.terms[self.results_index])
        self.results_view.setPlainText(self.results[self.results_index])
        self.results_index_label.setText(str(self.results_index + 1) + "/" + str(len(self.results)))

    def start_new_search(self):
        """This function goes back to the options page for a new search."""
        self.input_box.setPlainText('')
        self.results_index = 0
        self.pages.setCurrentWidget(self.options_page)
