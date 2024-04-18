import re
import datetime
from collections import Counter
from enum import Enum
import time

#OS types for import
class OSEnum(Enum):
    IOS = 1,
    ANDROID = 2

#initializing vars
name_1 = ' Smartie' #Get names from chat
name_2 = ' Kim van Embden'
filename = "smartie.txt"
interesting_words_threshold = 3000 #threshold for interesting words, is equal to the amount of times used
wFilename = f"Results\chatresults_{name_1}_and{name_2}.txt"

debug = True   #turn debug console logs on/off
maximumWaitingPeriods = 5 # maximum waiting periods to display
minimumWaitingSpan = datetime.timedelta(days=2) #timedelta for the minimum waiting time (keep high as possible)
minLine = 0 #start line
maxLine = -1 #-1 is all
OS = OSEnum.IOS

# available variables
longest_massages_from_name_1 = [["",0]]
longest_massages_from_name_2 = [["",0]]
line_number = 0
longest_wait = datetime.timedelta(seconds=0)
waiting_periods = []
number_of_messages = 0
messages_name_1 = 0
messages_name_2 = 0
words_by_name_1 = 0
words_by_name_2 = 0
all_words_count = 0
all_words = []
chars_by_name_1 = 0
chars_by_name_2 = 0
all_char_count = 0
emoji_list = []

if(debug):
    start_time = time.time()

days_of_week = {
    "monday" : 0,
    "tuesday" : 0,
    "wednesday" : 0,
    "thursday" : 0,
    "friday" : 0,
    "saturday" : 0,
    "sunday" : 0,
}

time_of_day ={
    "00:00" : 0,
    "01:00" : 0,
    "02:00" : 0,
    "03:00" : 0,
    "04:00" : 0,
    "05:00" : 0,
    "06:00" : 0,
    "07:00" : 0,
    "08:00" : 0,
    "09:00" : 0,
    "10:00" : 0,
    "11:00" : 0,
    "12:00" : 0,
    "13:00" : 0,
    "14:00" : 0,
    "15:00" : 0,
    "16:00" : 0,
    "17:00" : 0,
    "18:00" : 0,
    "19:00" : 0,
    "20:00" : 0,
    "21:00" : 0,
    "22:00" : 0,
    "23:00" : 0,
}


def debugConsole(message):
    if debug:
        print(message)


def dayOfWeekFunc(weekday):
    match weekday:
        case 1:
            days_of_week["monday"] = days_of_week["monday"] + 1
        case 2: 
            days_of_week["tuesday"] = days_of_week["tuesday"] + 1
        case 3: 
            days_of_week["wednesday"] = days_of_week["wednesday"] + 1
        case 4: 
            days_of_week["thursday"] = days_of_week["thursday"] + 1
        case 5: 
            days_of_week["friday"] = days_of_week["friday"] + 1
        case 6: 
            days_of_week["saturday"] = days_of_week["saturday"] + 1
        case 7:
            days_of_week["sunday"] = days_of_week["sunday"] + 1

def timeOfDayFunc(timeOfDay):
    match timeOfDay:
        case 0:
            time_of_day["00:00"] = time_of_day["00:00"] + 1
        case 1:
            time_of_day["01:00"] = time_of_day["01:00"] + 1
        case 2:
            time_of_day["02:00"] = time_of_day["02:00"] + 1
        case 3:
            time_of_day["03:00"] = time_of_day["03:00"] + 1
        case 4:
            time_of_day["04:00"] = time_of_day["04:00"] + 1
        case 5:
            time_of_day["05:00"] = time_of_day["05:00"] + 1
        case 6:
            time_of_day["06:00"] = time_of_day["06:00"] + 1
        case 7:
            time_of_day["07:00"] = time_of_day["07:00"] + 1
        case 8:
            time_of_day["08:00"] = time_of_day["08:00"] + 1
        case 9:
            time_of_day["09:00"] = time_of_day["09:00"] + 1
        case 10:
            time_of_day["10:00"] = time_of_day["10:00"] + 1
        case 11:
            time_of_day["11:00"] = time_of_day["11:00"] + 1
        case 12:
            time_of_day["12:00"] = time_of_day["12:00"] + 1
        case 13:
            time_of_day["13:00"] = time_of_day["13:00"] + 1
        case 14:
            time_of_day["14:00"] = time_of_day["14:00"] + 1
        case 15:
            time_of_day["15:00"] = time_of_day["15:00"] + 1
        case 16:
            time_of_day["16:00"] = time_of_day["16:00"] + 1
        case 17:
            time_of_day["17:00"] = time_of_day["17:00"] + 1
        case 18:
            time_of_day["18:00"] = time_of_day["18:00"] + 1
        case 19:
            time_of_day["19:00"] = time_of_day["19:00"] + 1
        case 20:
            time_of_day["20:00"] = time_of_day["20:00"] + 1
        case 21:
            time_of_day["21:00"] = time_of_day["21:00"] + 1
        case 22:
            time_of_day["22:00"] = time_of_day["22:00"] + 1
        case 23:
            time_of_day["23:00"] = time_of_day["23:00"] + 1
        
def createDayStatsString(days):
    result = "\nDay stats:\n"
    max_day = 0
    favorite_day = ""

    for day, amount in days.items():
        result = result + f"{day}: {amount} messages\n"
        if amount > max_day:
            max_day = amount
            favorite_day = day
    result = result + f"favorite day: {favorite_day} with {max_day} messages\n"
    return result


def createTimeStatsString(timezones):
    result = "\nTime stats: \n"
    max_time = 0
    favorite_time = ""

    for time, amount in timezones.items():
        result = result + f"{time}: {amount} messages\n"
        if amount > max_time:
            max_time = amount
            favorite_time = time
    result = result + f"favorite time: {favorite_time} with {max_time} messages\n"
    return result

def extract_emojis(text):
    return re.findall(r'[^\w\s,.:;\>\<\+\'\\[\]\|\–\%\#\{\}\~´\&\€•\*=\^…@‘’?!\(\)\\\/\”\“\-(‎)\"]', text)


# data object waiting periods is : [duration, firstDate, nextDate]
def create_list_of_waiting_periods(duration, firstDate, nextDate):
    if(duration > minimumWaitingSpan):
        buffer = [[duration, firstDate, nextDate]]
        count = len(waiting_periods)
        reorder = False

        # just add, list is not full yet
        if count == 0 or count < maximumWaitingPeriods:
            waiting_periods.append(buffer.pop())
            if(count >= 2):
                reorder = True

        #list is full but new timedelta is till bigger than the smallest one
        elif buffer[0][0] > waiting_periods[-1][0]:
            waiting_periods[-1] = buffer.pop()
            reorder = True

        #reorder list 
        if reorder:
            while waiting_periods[count-1][0] > waiting_periods[count-2][0] and count >= 2:
                buffer.append(waiting_periods[count-2])
                waiting_periods[count-2]=waiting_periods[count-1]
                waiting_periods[count-1]=buffer.pop(0)
                count = count - 1
            reorder = False


with open(f"Input/{filename}", "r", encoding="utf8") as file:
    # read the files, split the dates into messages
    content = file.read()

    if OS == OSEnum.IOS:
        lines = re.split(r'(\[\d{2}\-\d{2}\-\d{4}\, \d{2}\:\d{2}:\d{2}\])', content, flags=re.MULTILINE)
    else:
        lines = re.split(r'(\d{2}\-\d{2}\-\d{4} \d{2}\:\d{2} \-)', content, flags=re.MULTILINE)

    # Get the start date time
    if OS == OSEnum.IOS:
        current_date_time = datetime.datetime.strptime(lines[1], '[%d-%m-%Y, %H:%M:%S]')
    else:
        current_date_time = datetime.datetime.strptime(lines[1], '%d-%m-%Y %H:%M -')
        
    start_date = current_date_time

    for line in lines[minLine:maxLine]:
        # go through the lines
        line_number = line_number + 1

        # these are the date lines
        if line_number % 2 == 0 or line_number == 2:
            if OS == OSEnum.IOS:
                new_date_time = datetime.datetime.strptime(line, '[%d-%m-%Y, %H:%M:%S]')
            else:
                new_date_time = datetime.datetime.strptime(line, '%d-%m-%Y %H:%M -')

            create_list_of_waiting_periods((new_date_time - current_date_time), current_date_time, new_date_time)
            dayOfWeekFunc(new_date_time.isoweekday())
            timeOfDayFunc(new_date_time.hour)

            current_date_time = new_date_time

        # these are the messages
        else:
            number_of_messages =  number_of_messages + 1

            # remove whatsapp edits and removal char and message, only keep text that is send by user
            if OS == OSEnum.IOS:
                if "‎" in line:
                    line = line.split("‎", 1)[0]
            elif OS == OSEnum.ANDROID:
                if "<Dit bericht is bewerkt>" or "<Media weggelaten>" in line:
                    line.replace("<Dit bericht is bewerkt>","")
                    line.replace("<Media weggelaten>", "")

            chars_in_message = 0
            if line.startswith(name_1):
                messages_name_1 = messages_name_1 + 1
                emoji_list = emoji_list + extract_emojis(line[len(name_1) + 2:])
                newCollection = (line[len(name_1) + 2:]).split()
                words_by_name_1 = words_by_name_1 + len(newCollection)
                for word in newCollection:
                    chars_by_name_1 = chars_by_name_1 + len(word)
                    chars_in_message = chars_in_message + len(word)
                if chars_in_message > longest_massages_from_name_1[0][1]:
                    longest_massages_from_name_1.insert(0, [line, chars_in_message])
                all_words = all_words + newCollection
            else: 
                messages_name_2 = messages_name_2 + 1
                emoji_list = emoji_list + extract_emojis(line[len(name_1) + 2:])
                newCollection = (line[len(name_2) + 2:]).split()
                words_by_name_2 = words_by_name_2 + len(newCollection)
                for word in newCollection:
                    chars_by_name_2 = chars_by_name_2 + len(word)
                    chars_in_message = chars_in_message + len(word)
                if chars_in_message > longest_massages_from_name_2[0][1]:
                    longest_massages_from_name_2.insert(0, [line, chars_in_message])
                all_words = all_words + newCollection

    all_words_count = len(all_words)
    most_occuring = Counter({k: c for k, c in Counter(all_words).most_common(10) if c <= interesting_words_threshold}).most_common(10)
    most_occuring_emojis = Counter(emoji_list).most_common(10)
    end_date = current_date_time
    all_char_count = chars_by_name_1 + chars_by_name_2
    

with open(wFilename, "w" ,encoding="utf-8") as writeFile:
    writeFile.write(f"Messages from {start_date.strftime('%d-%m-%Y, %H:%M:%S')} till {end_date.strftime('%d-%m-%Y, %H:%M:%S')}\n")
    #writeFile.write(f"Longest wait: {longest_wait} from {dates_longest_wait}\n")
    
    writeFile.write(f"Number of messages: {number_of_messages}\n")
    writeFile.write(f"Number of words: {all_words_count}\n")

    writeFile.write(f"\nstats for {name_1}:\n")
    writeFile.write(f"Messages: {messages_name_1} ({(messages_name_1 / number_of_messages) * 100}%)\n")
    writeFile.write(f"Words: {words_by_name_1} ({(words_by_name_1 / all_words_count) * 100}%)\n")
    writeFile.write(f"Characters: {chars_by_name_1} ({(chars_by_name_1 / all_char_count) * 100}%)\n")

    writeFile.write(f"\nstats for {name_2}:\n")
    writeFile.write(f"Messages: {messages_name_2} ({(messages_name_2 / number_of_messages) * 100}%)\n")
    writeFile.write(f"Words: {words_by_name_2} ({(words_by_name_2 / all_words_count) * 100}%)\n")
    writeFile.write(f"Characters: {chars_by_name_2} ({(chars_by_name_2 / all_char_count) * 100}%)\n")
    writeFile.write(createTimeStatsString(time_of_day))
    writeFile.write(createDayStatsString(days_of_week))

    writeFile.write("\nMost occuring words:\n")
    for word, occurance in most_occuring:
        writeFile.write(f"{word}: {occurance}x\n")

    writeFile.write("\nMost occuring emoji:\n")
    for emoji, amount in most_occuring_emojis:
        writeFile.write(f"{emoji}: {amount}x\n")

    writeFile.write("\nLongest periods of silence:\n")
    i = 1
    for waitingPeriods in waiting_periods:
        writeFile.write(f"{i}: duration: {waitingPeriods[0]} from {waitingPeriods[1].strftime('%d-%m-%Y, %H:%M:%S')} till {waitingPeriods[2].strftime('%d-%m-%Y, %H:%M:%S')}\n")
        i = i + 1
    
    writeFile.write(f"\nlongest message from {name_1}:\n")
    writeFile.write(f"{longest_massages_from_name_1[0][0]}\n")
    writeFile.write(f"{longest_massages_from_name_1[0][1]} characters\n")

    writeFile.write(f"\nlongest message from {name_2}:\n")
    writeFile.write(f"{longest_massages_from_name_2[0][0]}\n")
    writeFile.write(f"{longest_massages_from_name_2[0][1]} characters\n")

if debug:
    print("--- %s seconds ---" % (time.time() - start_time))