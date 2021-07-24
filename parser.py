import yaml

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
    key_data = ''.join([s for s in log_data if '\n' not in s])

    print(key_data)
