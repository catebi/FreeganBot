from pymorphy3 import MorphAnalyzer
from spellchecker import SpellChecker
import string

def lemmatize(text):
    try:
        # Check if the input text is a valid string
        if not isinstance(text, str):
            raise ValueError("Input must be a string.")

        # Remove punctuation
        text_no_punct = text.lower().translate(str.maketrans('', '', string.punctuation))

        #TODO: disable spellchecking until performance issues are resolved
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
        return {morph.parse(word)[0].normal_form for word in words}

    except Exception as e:
        print(f"An error occurred: {e}")
        return set()

# Load Russian language models
morph = MorphAnalyzer()

# Load russsian spellchecker
spell = SpellChecker(language='ru')

# Add new words to the vocabulary
new_words = ['когтеточка', 'мальт-паст', 'веревка', 'габапентин', 'паучи']
spell.word_frequency.load_words(new_words)

# # Example text
# text = "Это пиример текста, кооторый нужно абработать. когтеточка всему голова. всем по когтеточке"

# # Process the example text
# try:
#     lemmas = lemmatize(text)
#     print(lemmas)
# except Exception as e:
#     print(f"Failed to process text: {e}")