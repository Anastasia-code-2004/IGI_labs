def count_punctuation(text):
    """Count the number of punctuation marks in the text."""
    punctuation = '!"(),-.:;?—«»–-'
    count = sum(1 for char in text if char in punctuation)  # count punctuation marks
    return count


def input_text_output_punctuation():
    """Input text and count the number of punctuation marks in it."""
    text = input('Enter text: ')
    count = count_punctuation(text)
    print('Amount of punctuation marks: ', count)
