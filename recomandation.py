import random

#if a question is positivly matched with a movie 10 times with no negetive maches
#there corilation is maxed out
X = .05

class question:
    #T is a string containg the actual question part of the question
    #M is the number of movies
    def __init__(self, T, M):
        self.text = T
        self.weights = [0.5]*M
        
    #returns the question
    def getQ(self):
        return self.text
    
    #retuns the weights
    def getWeights(self):
        return self.weights
        
    #"movie" is the intiger index associated with the movie in question
    
    #this increses the wight the question has with the given movie up to a maximum of 1
    def goodQ(self, movie):
        self.weights[movie] = min(self.weights[movie] + X, 1.0)
    
    #this decreses the wight the question has with the given movie down to a minimum of 0    
    def badQ(self, movie):
        self.weights[movie] = max(self.weights[movie] - X, 0.0)
    
    #adds weights for M more movies    
    def addM(self, M):
        temp = [0.5]*M
        self.weights.append(temp)
        
        

class recomodation:
    #M is the number of movies
    def __init__(self, M):
        self.qList = []
        self.qCount = 0
        self.mList = [None]*M
        self.mSums = [0.0]*M
        self.mCount = M
        
    #adds the weights of the given question to the running avrage of weights for this recomodation
    def yes(self, question):
        self.qCount += 1
        weights = question.getWeights()
        temp = (question, True)
        self.qList.append(temp)
        for i in range(self.mCount):
            self.mSums[i] += weights[i]
            self.mList[i] = self.mSums[i]/self.qCount
    
    #subracts the weights of the given question to the running avrage of weights for this recomodation        
    def no(self, question):
        self.qCount += 1
        weights = -1*question.getWeights()
        temp = (question, False)
        self.qList.append(temp)
        for i in self.mCount:
            self.mSums[i] += weights[i]
            self.mList[i] = self.mSums[i]/self.qCount
            
    #randomly picks a threshold betwene 0 and 1 and then runs thrue the movies in a random order
    #if the avrage weight of the current movie is grater than or equal to the threshold it is 
    #   picked as the recomodation
    #if no movies pases then a new threshold is picked betwene 0 and the preveus threshold
    #if the theshold gets too low a random movie is selected
    def pick(self):
        roof = 1
        while roof > .01:
            roll = random.uniform(0,roof)
            deck = range(self.mCount)
            random.shuffle(deck)
            for i in range(self.mCount):
                opt = deck[i]
                if self.mList[opt] >= roll:
                    self.mList[opt] = 0.0
                    return opt
            roof = roll
        return random.randint(0,self.mCount)
            
    def good(self, movie):
        for i in range(self.qCount):
            if self.qList[i][1]:
                self.qList[i][0].goodQ(movie)
            else:
                self.qList[i].badQ(movie)
                
    def bad(self, movie):
        for i in range(self.qCount):
            if self.qList[i][1]:
                self.qList[i][0].badQ(movie)
            else:
                self.qList[i].goodQ(movie)
                


#this is just a test and an example of basic funtinality                
movies = ["M1","M2","M3","M4","M5","M6","M7","M8","M9","M10","M11","M12","M13","M14","M15","M16","M17","M18","M19","M20"]
questions = [question("q1", 20), question("q2", 20), question("q3", 20), question("q4", 20),question("q5", 20), question("q6", 20), question("q7", 20), question("q8", 20)]

rec = recomodation(20)
rec.yes(questions[1])
x = rec.pick()
print movies[x]
rec.good(x)
print questions[1].weights
