from spacy.lang.ru import Russian
from spellchecker import SpellChecker
import string


# Load Russian language models
nlp = Russian()
spell = SpellChecker(language='ru')

# List of custom words to add
new_words = ['обработать']

# Add words to spellchecker
spell.word_frequency.load_words(new_words)

# Adding the lemmatizer component to the pipeline
lemmatizer = nlp.add_pipe("lemmatizer")

def lemmatize(text):
    # Remove punctuation
    text_no_punct = text.lower().translate(str.maketrans('', '', string.punctuation))

    # Spellcheck and correct the text
    words = text_no_punct.split()
    words = [word for word in words if word is not None]

    # spellcheck
    corrected_words = []
    for word in words:
        correction = spell.correction(word)
        corrected_words.append(correction if correction is not None else word)

    corrected_text = " ".join(corrected_words)

    # Process the text
    doc = nlp(corrected_text)

    return {token.lemma_ for token in doc if token is not None}

# Example text
text = "Это пиример текста, кооторый нужно абработать. когтеточка всему голова. всем по когтеточке"
# Process the example text
lemmas = lemmatize(text)
print(lemmas)