# NOTE:
#   Import necessary libraries
#   Import CSV file to get the list of word
#   Use Free dictionary API to get each word info
#   Format those info
#   Add those info to respective CSV fields
#   Download audio file respectively and put them in a directory
import pandas
import pandas as pd
import requests as rq
import json

API = 'https://api.dictionaryapi.dev/api/v2/entries/en/'
FP = 'Gregmat-Vocab-Grouped.csv'
DOWNLOAD = './audio_files'
TESTNUM = 5


# NOTE function for importing CSV and get word list
#   Parameter:  csv file
#   Return:     List of word
def getWordList(file_path):
    path = file_path
    alpha = lambda x: str(x)
    word_csv = pd.read_csv(path, index_col=0, converters={'Word': alpha})
    word_series = word_csv.loc[:, "Word"]
    # print(f"Debug: the current word_series is: \b {word_series}")
    # print(f"Debug: the word_series contains {word_series.dtypes} type data.")
    return word_series


# NOTE: function for API request
#   Parameter:  word
#   Return:     JSON data of that word
def getJSON(given_word):
    query = given_word
    r = rq.get(API + query, timeout=3)
    result = r.json()
    return result


# NOTE: function to parse json into respective fields
#   Parameter:  json file
#   Return:     a container that contains word, phonetics, part of speech, audio file path, definition 1 to 3 (if exists), examples 1 to 3,
def parseInfo(returned_json, word):
    info = returned_json
    # print(info)
    # print(f"Returned JSON looks like this: {info}")
    word_dict = {
        "word_base": str(word),
        "word_phonetic": "",
        "word_audio_url": "",

        "word_pos1": "",
        "word_def1": "",
        "word_syn1": "",
        "word_ant1": "",

        "word_pos2": "",
        "word_def2": "",
        "word_syn2": "",
        "word_ant2": "",

        "word_pos3": "",
        "word_def3": "",
        "word_syn3": "",
        "word_ant3": "",

        "word_source_url": ""
    }
    try:
        word_dict["word_base"] = info[0]["word"]  # Word itself
    except:
        pass
    try:
        word_dict["word_phonetic"] = info[0]["phonetic"]  # Word itself
    except:
        pass
    try:
        word_dict["word_audio_url"] = info[0]["phonetics"][0]["audio"]  # Word itself
    except:
        pass
    try:
        word_dict["word_source_url"] = info[0]["sourceUrls"][0]
    except:
        pass

    pos_group_counter = 1
    prefix = "word_"
    for word_group in info:
        # Below gets all the pos populated
        try:
            for pos in word_group["meanings"]:
                try:
                    # Part of speech
                    word_dict[prefix + "pos" + str(pos_group_counter)] = pos["partOfSpeech"]

                    # Definition
                    single_pos_definition_container = ""
                    for definition in pos["definitions"]:
                        single_pos_definition_container += definition["definition"]
                        single_pos_definition_container += ";;;"
                    word_dict[prefix + "def" + str(pos_group_counter)] = single_pos_definition_container

                    # Synonym
                    single_pos_synonyms_container = ""
                    for syno in pos["synonyms"]:
                        single_pos_synonyms_container += syno + ","
                    word_dict[prefix + "syn" + str(pos_group_counter)] = single_pos_synonyms_container

                    # Antonym
                    single_pos_antonyms_container = ""
                    for ant in pos["synonyms"]:
                        single_pos_antonyms_container += ant + ","
                    word_dict[prefix + "ant" + str(pos_group_counter)] = single_pos_antonyms_container

                    pos_group_counter = pos_group_counter + 1
                except:
                    pass
        except:
            pass

        # Below gets all definitions combined and populated

    return word_dict


# NOTE: function to download audio file and save into pre-defined directory
#   Parameter:  audio file url
#   Return:     Nothing, maybe a result for debugging
def audioDownload(audio_file_url):
    # TODO
    return


# NOTE: Main, initiates other functions and get result.
def main():
    word_series = getWordList(FP)  # Get the series of word
    newDictionary = []
    for wd in word_series:
        print("\b")
        print(f"Now processing word: {wd}")
        current_word_dict = parseInfo(getJSON(wd), wd)
        # print(f"Currently the dictionary entry for {wd} looks like this: {current_word_dict}")
        newDictionary.append(current_word_dict)
    print(f"\b The number of things in newDictionary: {len(newDictionary)}")
    output = pd.DataFrame.from_records(newDictionary)
    # print(output.shape)
    output.to_csv('output.csv', sep=',', encoding='utf-8', columns=[1:])


# get word data
main()
