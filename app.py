__author__ = "Hannah Provenza, Sooyoung Jeong"
import sys
import difflib
from difflib import SequenceMatcher
import mistake_reporting

text = sys.argv[1]
print(text)

#TODO: run kaldi script to get the phonetic transcription
# currently cheating with manual transcription
with open(text, 'r') as f:
    transcript = f.readlines()

#TODO: align the transcription and master transcription
with open('/home/anna/say-it-right/transcriptions/MASTER.txt', 'r') as f:
    correct = f.readlines()
d = difflib.Differ()
diff = d.compare(correct, transcript)


#TODO: error dictionaries should map incorrect to correct phonemes
devoice = {'b': 'p',
           'd':'t',
           'g': 'k',
           'v': 'f',
           'D':'T',
           'z':'s',
           'Z':'S' }
devoice = {v: k for k, v in devoice.items()}

th_changes = {'s': 'T',
              'f': 'T'}

dh_changes = {'z': 'D',
              'v': 'D'}

#This hasn't been finished yet
vowel_shifts = {'@': 'a',
           'I': 'i',
           '3`': '3',
           'oU':'o'}
vowel_shifts = {v: k for k, v in vowel_shifts.items()}

def track_word(i, code):
    beginning = []
    end = []
    for char in reversed(correct[i][:code[3]]):
        if char != ' ':
            beginning.append(char)
        else:
            break
    for char in correct[i][code[3]:]:
        if char != ' ':
            end.append(char)
        else:
            break
    word = ''.join(beginning[::-1])+''.join(end)

    return word

#TODO: identify the differences
print('\n'.join(diff))
print()
i = 0
for i in range(len(correct)):
    #where i loops through the sentences
    #compares the same sentence
    s = SequenceMatcher(None, transcript[i], correct[i])
    #since opcodes returns a list you need to loop through inside
    for o in s.get_grouped_opcodes():
        for code in o:
            if code[0] == 'replace':
                if transcript[i][code[1]] in th_changes:
                    if (th_changes[transcript[i][code[1]:code[2]]] == correct[i][code[3]:code[4]]):
                        word = (track_word(i, code))
                        print("unvoiced th articulation error! in word {}".format(word))
                        mistake_reporting.th_articulation()
                        print()
                if transcript[i][code[1]] in dh_changes:
                    if (dh_changes[transcript[i][code[1]:code[2]]] == correct[i][code[3]:code[4]]):
                        word = (track_word(i, code))
                        print("voiced th articulation error! in word {}".format(word))
                        mistake_reporting.dh_articulation()
                        print()
                if transcript[i][code[1]] in devoice:
                    if (devoice[transcript[i][code[1]:code[2]]] == correct[i][code[3]:code[4]]):
                        word = (track_word(i, code))
                        print("devoicing error! in word {}".format(word))
                        mistake_reporting.final_devoicing()
                        print()
                if transcript[i][code[1]] in vowel_shifts:
                    if (vowel_shifts[transcript[i][code[1]:code[2]]] == correct[i][code[3]:code[4]]):
                        word = (track_word(i, code))
                        print("vowel shift error! in word {}".format(word))
                        mistake_reporting.vowel_shift()
                        print()
            if code[0] == 'delete':
                if correct[i][code[3]] == 'h':
                    word = (track_word(i, code))
                    print("h deletion! in word {}".format(word))
                    mistake_reporting.h_deletion()
                    print()
