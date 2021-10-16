import json
import re
from collections import Counter

import yaml
from prettytable import PrettyTable


class Keyboard:
    def __init__(self, key_set):
        self.key_set = key_set


if __name__ == "__main__":
    """This file will parse keystrokes and return stats about your most used keys."""

    # load the configuration file
    with open("configuration.yml", "r") as stream:
        try:
            config = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)

    # read in the logged keystrokes
    with open(config["log_file_path"], "r") as log_file:
        log_data = log_file.read().splitlines()

    # join the items in the list to make a single string
    # also convert characters to the same case
    key_data = "".join(log_data).upper()

    # remove the keylogger message and timestamp
    key_data_cleaned = re.sub(
        r"KEYLOGGING HAS BEGUN.[A-Z]{3} [A-Z]{3} [0-9]{2} [0-9]{2}:[0-9]{2}:[0-9]{2} [0-9]{4}",
        "",
        key_data,
    )

    # each character is one item in a list
    # but the modifiers are encapsulated by [] so we will treat them as a single token
    key_tokens = []
    idx = 0
    while True:
        c = key_data[idx]
        if c != "[":
            idx += 1
            key_tokens.append(c)  # append if not [
        else:
            closing_index = key_data[idx + 1 :].find(
                "]"
            )  # find if ] exist after current [
            if closing_index == -1:
                # append the rest sub-srting and break since no ] after current [
                key_tokens.extend(key_data[idx:])
                break
            else:
                # check if [ in the  middle, append only c if True
                if "[" in key_data[idx + 1 : idx + closing_index + 2]:
                    key_tokens.append(c)
                    idx += 1
                else:
                    # extend from [ to the nearest ]
                    key_tokens.append(key_data[idx : idx + closing_index + 2])
                    idx += closing_index + 2
        if idx >= len(key_data):
            break  # break loop if idx exceeds maximum value

    # still this logic isn't perfect because you can type with the [] in real life
    # so we will only use acceptable tokens
    acceptable_tokens = [
        "[DEL]",
        "[RIGHT]",
        " ",
        "E",
        "T",
        "A",
        "[LEFT]",
        "[RETURN]",
        "S",
        "C",
        "I",
        "R",
        "O",
        "L",
        "N",
        "[DOWN]",
        "[LEFT-CMD]",
        "D",
        "P",
        "M",
    ]
    input_keyboard = Keyboard(acceptable_tokens)

    # count the frequency of each token
    token_freq = Counter(key_tokens)
    sorted_token_freq = sorted(
        token_freq.items(), key=lambda pair: pair[1], reverse=True
    )

    # print the frequency
    t = PrettyTable(["Key", "Count"])
    for key, value in sorted_token_freq:
        t.add_row([key, value])
    print(t)

    # normalize the frequencies
    total_tokens = len(key_tokens)
    for key in token_freq:
        token_freq[key] /= total_tokens

    sorted_token_freq = sorted(
        token_freq.items(), key=lambda pair: pair[1], reverse=True
    )
    scale_factor = config["scale_categories"] / max(token_freq.values())

    scaled_token_freq = {}
    for token in sorted_token_freq:
        value = token[1] * scale_factor
        scaled_token_freq[token[0]] = {
            "scaled_frequency": value,
            "proportion": token[1],
        }

    # print the scaled frequency
    t = PrettyTable(["Key", "Scaled Frequency", "Proportion"])
    for key, value in scaled_token_freq.items():
        t.add_row([key, value["scaled_frequency"], value["proportion"]])
    print(t)

    with open("./results.json", "w") as results_file:
        json.dump(scaled_token_freq, results_file)
