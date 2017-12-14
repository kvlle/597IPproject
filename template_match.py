#************************************************************************
#*						CARD MATCH BLACKJACK HELPER
#*
#*
#*							Kyle Wright
#*							Anthony Chan
#*							Joseph Cao
#*
#*
#*							University of Massachusetts Amherst
#*							ECE597ip Image Processing 2017
#*
#*
#*			USAGE: $ python template_match.py -c1 card1.png -c2 card2.png -d /PathToDeckFile
#*
#*			
#************************************************************************

#import packages
import numpy as np
import cv2
import argparse
import glob
from matplotlib import pyplot as plt

match1 = None
found1 = None
match2 = None
found2 = None
points = 0



def PointCalculator(bestImg):  #--------------------------------------------------------- Point Calculator Function -------------
	global points

	#format information about this match
	bestImg = bestImg.replace("_", " ")
	bestImg = bestImg.replace("cards/", "")
	bestImg = bestImg.replace(".png","")

	#determine suit
	if "spades" in bestImg:
		print '\n' + "Suit:" + '\n' + "     " + "Spades"
	if "diamonds" in bestImg:
		print '\n' + "Suit:" + '\n' + "     " + "Diamonds"
	if "hearts" in bestImg:
		print '\n' + "Suit:" + '\n' + "     " + "Hearts"
	if "clubs" in bestImg:
		print '\n' + "Suit:" + '\n' + "     " + "Clubs"

	#determine rank, assign points
	if "2" in bestImg:
		print '\n' + "Rank:" + '\n' + "     " + "Two"
		points += 2
	if "3" in bestImg:
		print '\n' + "Rank:" + '\n' + "     " + "Three"
		points += 3
	if "4" in bestImg:
		print '\n' + "Rank:" + '\n' + "     " + "Four"
		points += 4
	if "5" in bestImg:
		print '\n' + "Rank:" + '\n' + "     " + "Five"
		points += 5
	if "6" in bestImg:
		print '\n' + "Rank:" + '\n' + "     " + "Six"
		points += 6
	if "7" in bestImg:
		print '\n' + "Rank:" + '\n' + "     " + "Seven"
		points += 7
	if "8" in bestImg:
		print '\n' + "Rank:" + '\n' + "     " + "Eight"
		points += 8
	if "9" in bestImg:
		print '\n' + "Rank:" + '\n' + "     " + "Nine"
		points += 9
	if "10" in bestImg:
		print '\n' + "Rank:" + '\n' + "     " + "Ten"
		points += 10
	if "jack" in bestImg:
		print '\n' + "Rank:" + '\n' + "     " + "Jack"
		points += 10
	if "queen" in bestImg:
		print '\n' + "Rank:" + '\n' + "     " + "Queen"
		points += 10
	if "king" in bestImg:
		print '\n' + "Rank:" + '\n' + "     " + "King"
		points += 10
	if "ace" in bestImg:
		print '\n' + "Rank:" + '\n' + "     " + "Ace"
		points += 1 #or 11........ need to code that in
	if "joker" in bestImg:
		print '\n' + "Rank:" + '\n' + "     "
		if "red" in bestImg:
			print "Red Joker... Try again!"
		if "black" in bestImg:
			print "Black Joker... Try again!"

	print '\n' + "Points:" + '\n' + "     "
	print points


ap = argparse.ArgumentParser()
ap.add_argument("-c1", "--c1", required=True, help="card 1 in your hand.")
ap.add_argument("-c2", "--c2", required=True, help="card 2 in your hand.")
ap.add_argument("-d", "--deck", required=True, help="Cards in the deck.")
args = vars(ap.parse_args())

c1 = cv2.imread(args["c1"])
c2 = cv2.imread(args["c2"])

for imagePath in glob.glob(args["deck"] + "/*.png"):
	d = cv2.imread(imagePath)

	result = cv2.matchTemplate(d, c1, cv2.TM_CCOEFF)
	(min_val, max_val, min_loc, max_loc) = cv2.minMaxLoc(result)

	if found1 is None or max_val > found1[0]:
		found1 = (max_val, max_loc)
		match1 = imagePath

	result = cv2.matchTemplate(d, c2, cv2.TM_CCOEFF)
	(min_val, max_val, min_loc, max_loc) = cv2.minMaxLoc(result)

	if found2 is None or max_val > found2[0]:
		found2 = (max_val, max_loc)
		match2 = imagePath

PointCalculator(match1)
PointCalculator(match2)




#match = cv2.imread(match)
#plt.imshow(match),plt.show()