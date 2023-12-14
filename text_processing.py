from spacy.lang.ru import Russian
from spellchecker import SpellChecker
import string


# Load Russian language models
nlp = Russian()
spell = SpellChecker(language='ru')

# Adding the lemmatizer component to the pipeline
lemmatizer = nlp.add_pipe("lemmatizer")



def process_text(text):
    # Remove punctuation
    text_no_punct = text.lower().translate(str.maketrans('', '', string.punctuation))
    print(text_no_punct)
    # Spellcheck and correct the text
    words = text_no_punct.split()
    print(words)
    corrected_words = [spell.correction(word) for word in words if word is not None]
    print(corrected_words)
    corrected_text = " ".join(corrected_words)
    print(corrected_text)
    # Process the text
    doc = nlp(corrected_text)
    print(doc)
    # Lemmatize the text
    lemmatized_text = ' '.join([token.lemma_ for token in doc if token is not None])

    return lemmatized_text


# Example text
# text = "Это пиример текста, кооторый нужно абработать."
# Process the example text
# lemmatized_text = process_text(text)
# print(lemmatized_text)