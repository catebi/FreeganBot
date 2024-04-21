from pymorphy3 import MorphAnalyzer
from spellchecker import SpellChecker
import string


class Lemmatizer:

    def load_more_words(self, new_words):
        self.spell.word_frequency.load_words(new_words)

    def __init__(self, language='ru'):
        self.morph = MorphAnalyzer()

        # Load russian spellchecker
        self.spell = SpellChecker(language=language)
        self.load_more_words(['когтеточка', 'мальт-паст', 'веревка', 'габапентин', 'паучи'])

    def lemmatize(self, text):
        try:
            # Check if the input text is a valid string
            if not isinstance(text, str):
                raise ValueError(f"Input {text} must be a string.")

            # Remove punctuation
            text_no_punct = text.lower().translate(str.maketrans('', '', string.punctuation))

            # TODO: disable spellchecking until performance issues are resolved
            # Spellcheck and correct the text
            # words = text_no_punct.split()
            # words = [word for word in words if word is not None]

            # Spellcheck
            # corrected_words = []
            # for word in words:
            #     correction = spell.correction(word)
            #     corrected_words.append(correction if correction is not None else word)

            # corrected_text = " ".join(corrected_words)

            # Process the text
            words = text_no_punct.split()
            # Lemmatize the text and return a set of lemmas
            return {self.morph.parse(word)[0].normal_form for word in words}

        except Exception as e:
            print(f"An error occurred: {e}")
            return set()
