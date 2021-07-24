import yaml
import re
from collections import Counter

if __name__ == '__main__':
    '''This file will parse keystrokes and return stats about your most used keys.'''
    
    # load the configuration file
    with open('configuration.yml', 'r') as stream:
        try:
            config = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)
    
    # read in the logged keystrokes
    with open (config['log_file_path'], 'r') as log_file:
        log_data = log_file.readlines()

    # get rid of the keylogging message, timestamps, and newline characters
    # also join the items in the list to make a single string
    # also convert characters to the same case
    key_data = ''.join([s for s in log_data if '\n' not in s]).upper()

    # each character is one item in a list
    # but the modifiers are encapsulated by [] so we will treat them as a single token
    key_tokens = re.findall('\[.*?\]|\w', key_data)
    total_tokens = len(key_tokens)

    # count the frequency of each token
    token_freq = Counter(key_tokens)
    
    # normalize the frequencies
    for key in token_freq:
        token_freq[key] /= total_tokens

    sorted_token_freq = sorted(token_freq.items(), key=lambda pair: pair[1])
    for t in sorted_token_freq:
        print(t)

