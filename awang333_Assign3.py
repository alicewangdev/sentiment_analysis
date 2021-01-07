# This program prompts the user for a file containing tweets and a file containing keywords, to analyze each individual tweet for a happiness score.
# This program then compiles all happiness scores from individual tweets and sorts according to timezone.
# After sorting by timezone, the overall happiness of the timezones Pacific, Mountain, Central, and Eastern are determined.
# This allows for the comparison of overall happiness of the 4 timezones listed based on tweets.

class Keyword: # Defining the class Keyword to keep track of keywords and their sentiment values
  def __init__(self, word, score): # Constructing a method
    self.word = word
    self.score = score

class Timezone: # Defining the class Timezone to keep track of where each timezone is located and their individual happiness scores
  def __init__(self, name, latStart, latEnd): # Constructing a method
    self.name = name
    self.latStart = latStart
    self.latEnd = latEnd
    self.count = 0
    self.totalScore = 0
    self.totalHappiness = 0
    self.averageScore = 0

keyword_list = []
timezones = []

def main():
    try: # Prompting users to input their own files
        tweets = input("Please enter the name of the file containing the tweets: ")
        keywords = input("Please enter the name of the file containing the keywords: ")
        timezones.append(Timezone("Pacific", -125.242264, -115.236428)) # Appending objects into the timezone list to keep track of timezones and their locations
        timezones.append(Timezone("Mountain", -115.236428, -101.998892))
        timezones.append(Timezone("Central", -101.998892, -87.518395))
        timezones.append(Timezone("Eastern", -87.518395, -67.444574))

        keywordFile = open(keywords, "r", encoding="utf-8")
        for line in keywordFile:
            arr = line.strip("\n").split(",") # Strip a line then split it and store it
            keyword_list.append(Keyword(arr[0], int(arr[1]))) # Appending objects into the keyword list to keep track of keywords and their values

        tweetsFile = open(tweets, "r", encoding="utf-8")
        for line in tweetsFile:
            arr = line.strip("\n").split() # Strip a line then split it and store it as longitudes and latitudes
            long = float(arr[0].strip("[,"))
            lat = float(arr[1].strip("]"))
            if (long >= 24.660845 and long <= 49.189787): # Check to see if the tweet falls within the correct longitutde
                sumScore = 0
                count = 0
                for i in range(len(arr)):
                    if (i >= 5): # Looks at the tweet only, ignoring everything else
                        s = stripSpecialChar(arr[i]) # Removes all special charcaters from one word
                        score = tweet_word_Calculation(s) # Obtains the word and checks to see if it's a keyword with a sentiment value
                        if score > 0:
                            sumScore += score # Adds up all the sentiment values of found keywords in one tweet
                            count += 1

                if count > 0:
                    avgScore = sumScore / count # Determining the happiness value of one tweet
                    addToTimezone(lat, avgScore) # Checks which timezone and adds it to the total timezone score
                    print(count)

        for timezone in timezones: # Determines the happiness score of a timezone
            if timezone.count > 0:
                timezone.averageScore = timezone.totalScore / timezone.count


        for timezone in timezones:
            print(timezone.name + "  \tTotal Happiness:"  + "{:10.6f}".format(timezone.averageScore) + "  \tTotal Count:" + str(timezone.count))

        keywordFile.close()
        tweetsFile.close()

    except IOError:
        print("Error: file not found.")

    except ValueError:
        print("Error: file contents invalid.")

    except RuntimeError as error:
        print("Error:", str(error))

def stripSpecialChar(str): # Function to remove special charcaters in a tweet
    str = str.strip("%!@#$^&*()-+=_<>,./{}[]\"\'")
    return str

def tweet_word_Calculation(word): # Function to check if individual words in a tweet are in the keyword list and returns the score associated with the keyword
    score = 0
    for keyword in keyword_list:
        if word == keyword.word:
            score = keyword.score
    return score

def addToTimezone(lat, score): # Function to check which timezone an individual tweet is in
    for timezone in timezones:
        if lat >= timezone.latStart  and lat <= timezone.latEnd:
            timezone.totalScore += score
            timezone.count += 1



main()
