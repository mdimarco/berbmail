
#removes past messages!
def remove_history(message):
	message_lines = str(message).split('\r\n')
	return " ".join( [line for line in message_lines if not line or line[0] != '>'] )


def print_top(word_freq_table, number):
	for x in range(number):
		most_used = max(word_freq_table, key=lambda word: word_freq_table[word])   
		print( most_used + " " + str(word_freq_table[most_used]))
		word_freq_table[most_used] = 0


def word_freq( word_list ):
	most_common_1000words = common1000_words()
	freq_table = {}

	for word in word_list:
		if len(word) < 4 or word in most_common_1000words or odd_stuff_in_word(word):
			continue
		if not word in freq_table:
			freq_table[word] = 1
		else:
			freq_table[word] += 1
	return freq_table


def exciting_words( freq_table ):
	exciting_table = {}
	for word in freq_table.keys():
		if "!" not in word:
			continue
		if word not in exciting_table:
			exciting_table[word] = 1
		else:
			exciting_table[word] += 1
	return exciting_table



def common1000_words():
	with open('most_common_words','r') as comm_file:
		return { word.strip('\n') for word in comm_file.readlines() }

def odd_stuff_in_word(word):
	odd_stuff = ["&","ccc",">","<","=",";"]
	for odd in odd_stuff:
		if word.find(odd) != -1:
			return True
	return False


import mailbox
import re


berb_box = mailbox.mbox('Berb.mbox')


msg_list_plaintext = [ message.get_payload()[0] for message in berb_box ]
message_plaintext_no_history = map(remove_history, msg_list_plaintext)
print("Emails Parsed: "+str(len(message_plaintext_no_history)))



refined_messages_string = reduce(lambda rest,x:rest+x, message_plaintext_no_history)
word_freq_table = word_freq( refined_messages_string.split(' ') )


print_top(word_freq_table, 25)







'''msg_list_html = [ message.get_payload()[1] for message in berb_box ]
#message_html_no_history = map(remove_history, msg_list_html)

ital_list_list = map(only_italics, msg_list_html)
ital_list = reduce(lambda total,rest: total+rest, ital_list_list)
ital_list_nohtml = map(remove_html, ital_list)
print(ital_list_nohtml)'''



'''def only_italics(messages_string):
	if type(messages_string) != type("LOL"):
		messages_string = str(messages_string)
	italics_phrases = []
	stop_ind = 0#used for index movement
	start_ind = messages_string.find("<i>")
	while start_ind > -1:
		stop_ind = messages_string.find("</i>", start_ind+1)

		ital_line = messages_string[start_ind+3:stop_ind]
		if (stop_ind - start_ind) < 50 and (stop_ind - start_ind) > 3:
			italics_phrases.append(ital_line)
		#get next italics
		start_ind = messages_string.find("<i>", stop_ind)

	return italics_phrases

def remove_html(htmled_string):
	return re.sub('\r\n','',re.sub('<[^<]+?>', '', htmled_string))'''