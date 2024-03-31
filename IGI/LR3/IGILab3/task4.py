text = ('So she was considering in her own mind, as well as she could, for the hot day made her feel very sleepy and '
        'stupid, whether the pleasure of making a daisy-chain would be worth the trouble of getting up and picking '
        'the daisies, when suddenly a White Rabbit with pink eyes ran close by her.')
list_of_words = text.lower().replace(',', '').split()


def count_words_ending_with_consonant(words):
    vowels = 'aeiou'
    count = sum(1 for word in words if word[-1] not in vowels)
    return count


def print_average_length_words(func):
    """Decorator that prints the words with the average length."""
    def wrapper(words):
        ave_length, ave_length_words = func(words)
        if ave_length_words:  # if there are words with the average length
            print(f'Words with length {ave_length}: {', '.join(ave_length_words)}')
        else:
            print(f'No words with length {ave_length}')

    return wrapper


@print_average_length_words
def average_length_words(words):
    """Calculate the average length of the words and return the words with the average length."""
    ave_length = round(sum(len(word) for word in words) / len(words))
    ave_length_words = [word for word in words if len(word) == ave_length]
    return ave_length, ave_length_words


def every_seventh_word(words):
    """Return every seventh word from the list."""
    get_seventh_words = words[::7]
    return get_seventh_words


def output_ending_with_consonant():
    """Output the number of words ending with a consonant."""
    count = count_words_ending_with_consonant(list_of_words)
    print(f'Number of words ending with a consonant: {count}')


def average_length():
    """Output the average length of the words and the words with the average length."""
    average_length_words(list_of_words)


def print_every_seventh_word():
    """Output every seventh word from the list."""
    a = every_seventh_word(list_of_words)
    print('Every seventh word:', ' '.join(a))
