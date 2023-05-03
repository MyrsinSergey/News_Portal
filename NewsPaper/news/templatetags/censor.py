from django import template
from news.censored_words import *

register = template.Library()


@register.filter()
def censor(text):
    if not isinstance(text, str):
        raise ValueError("Фильтр цензурирования применяется только к строковым значениям")

    words = text.split()

    for i in range(len(words)):
        word = words[i].strip(".,!?:;-")

        suffix = words[i][len(word):]

        word_parts = word.split('-')

        for j in range(len(word_parts)):
            word_part_lower = word_parts[j].lower()

            if word_part_lower in censored_words:
                censored_word_part = word_part_lower[0] + '*' * len(word_parts[j])

                if word_parts[j].istitle():
                    censored_word_part = censored_word_part.title()
                elif word_parts[j].isupper():
                    censored_word_part = censored_word_part.upper()

                word_parts[j] = censored_word_part

        censored_word = '-'.join(word_parts)

        words[i] = censored_word + suffix

    censored_text = ' '.join(words)

    return censored_text