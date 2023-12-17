from spacy.lang.ru import Russian
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
        doc = nlp(text_no_punct)

        # Lemmatize the text and return a set of lemmas
        return {token.lemma_ for token in doc if token is not None}

    except Exception as e:
        print(f"An error occurred: {e}")
        return set()

# Load Russian language models
nlp = Russian()

# Adding the lemmatizer component to the pipeline
lemmatizer = nlp.add_pipe("lemmatizer")

# Add new words to the vocabulary
nlp_new_words = ['когтеточка', 'мальт-паст', 'веревка', 'габапентин', 'паучи']
for word in nlp_new_words:
    nlp.vocab.strings.add(word)  # Add the word to the vocabulary
    nlp.vocab[word]  # This creates a Lexeme object for the word

# Load russsian spellchecker
spell = SpellChecker(language='ru')

new_words = ['обработать']
spell.word_frequency.load_words(new_words)

# # Example text
# text = "Это пиример текста, кооторый нужно абработать. когтеточка всему голова. всем по когтеточке"

# # Process the example text
# try:
#     lemmas = lemmatize(text)
#     print(lemmas)
# except Exception as e:
#     print(f"Failed to process text: {e}")