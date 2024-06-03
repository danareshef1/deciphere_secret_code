import json


def open_abc(abc_filename):
    # open the abc file
    try:
        with open(abc_filename, 'r') as abc_file:
            abc_file = abc_file.read()
            abc_ch = abc_file.split()
            return abc_ch
    except FileNotFoundError:
        print(f"Error: Lexicon file '{abc_filename}' not found.")
        exit(1)


def open_lexicon(lexicon_filename):
    # open the lexicon file
    try:
        with open(lexicon_filename, 'r') as lexicon_file:
            lexicon_words = lexicon_file.read()
            lexicon_words = lexicon_words.split()
            return lexicon_words
    except FileNotFoundError:
        print(f"Error: Lexicon file '{lexicon_filename}' not found.")
        exit(1)


def decipher_phrase(phrase, lexicon_filename, abc_filename):
    # This function decipher phrase by other functions
    print(f'starting deciphering using {lexicon_filename} and {abc_filename}')
    lexicon = open_lexicon(lexicon_filename)
    abc = open_abc(abc_filename)
    return identify_k(abc, lexicon, phrase)


def find_index_of_char(char, k, abc):
    # This function get char (from the phrase), k (from the range 0 to 25) and shift the 'k' value
    # returns the deciphered character after the shift.
    if char in abc:
        index_of_k = (abc.index(char) - k) % len(abc)
        return abc[index_of_k]
    return char


def find_words(word_split, lexicon):
    # This function checks if the words from the deciphered phrase are in the lexicon file
    for word in word_split:
        if word not in lexicon:
            return False
    return True


def identify_k(abc, lexicon, phrase):
    # Identify the key 'K' for deciphering a given phrase
    # return a dictionary containing the deciphered phrase, status, and key (K).
    if not phrase:     # Check if the phrase is empty
        result_p = {"status": 2, 'deciphered_phrase': '', 'K': -1}
    else:
        for k in range(26):
            word_after = ''.join(find_index_of_char(char, k, abc) for char in phrase)
            word_split = word_after.split()
            if find_words(word_split, lexicon):
                result_p = {"status": 0, "orig_phrase": word_after, "K": k}
                return result_p
        result_p = {"status": 1, "orig_phrase": 'The given phrase cannot be deciphered', "K": -1}
    return result_p


students = {'id1': '314652439', 'id2': '207106931'}

if __name__ == '__main__':
    with open('config-decipher.json', 'r') as json_file:
        config = json.load(json_file)

    result = decipher_phrase(config['secret_phrase'],
                             config['lexicon_filename'],
                             config['abc_filename'])

    assert result["status"] in {0, 1, 2}

    if result["status"] == 0:
        print(f'deciphered phrase: {result["orig_phrase"]}, K: {result["K"]}')
    elif result["status"] == 1:
        print("cannot decipher the phrase!")
    else:  # result["status"] == 2:
        print("empty phrase")

