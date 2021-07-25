import yaml
import re
from collections import Counter
import json

if __name__ == '__main__':
    '''This file will parse keystrokes and return stats about your most used keys.'''
    
    # load the configuration file
    with open('configuration.yml', 'r') as stream:
        try:
            config = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)
    
    # read in the logged keystrokes
    with open(config['log_file_path'], 'r') as log_file:
        log_data = log_file.read().splitlines()

    # join the items in the list to make a single string
    # also convert characters to the same case
    key_data = ''.join(log_data).upper()

    # remove the keylogger message and timestamp
    key_data_cleaned = re.sub(r'KEYLOGGING HAS BEGUN.[A-Z]{3} [A-Z]{3} [0-9]{2} [0-9]{2}:[0-9]{2}:[0-9]{2} [0-9]{4}', '', key_data)

    print(key_data_cleaned)

    # each character is one item in a list
    # but the modifiers are encapsulated by [] so we will treat them as a single token
    #key_tokens = re.findall('\[.*?\]|\w', key_data_cleaned)
    key_tokens = []
    idx = 0
    while True:
        c = key_data[idx]
        if c != '[':
            idx += 1
            key_tokens.append(c)  # append if not [
        else:
            closing_index = key_data[idx+1:].find(']') # find if ] exist after current [
            if closing_index == -1:
                # append the rest sub-srting and break since no ] after current [
                key_tokens.extend(key_data[idx:])
                break
            else:
                # check if [ in the  middle, append only c if True
                if '[' in key_data[idx+1:idx+closing_index+2]:
                    key_tokens.append(c)
                    idx += 1
                else:
                    # extend from [ to the nearest ]
                    key_tokens.append(key_data[idx:idx+closing_index+2])
                    idx += closing_index+2
        if idx>=len(key_data): break  # break loop if idx exceeds maximum value

    total_tokens = len(key_tokens)

    # count the frequency of each token
    token_freq = Counter(key_tokens)
    
    # normalize the frequencies
    for key in token_freq:
        token_freq[key] /= total_tokens

    sorted_token_freq = sorted(token_freq.items(), key=lambda pair: pair[1])
    for t in sorted_token_freq:
        print(t)

    with open('./results.json', 'w') as results_file:
        json.dump(sorted_token_freq, results_file)

