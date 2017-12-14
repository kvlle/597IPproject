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
#*			USAGE: $ python flann_kp_match.py -c1 card1.png -c2 card2.png -d deck
#*
#*			
#************************************************************************

#import packages
import numpy as np
import cv2
import argparse
import glob
from matplotlib import pyplot as plt


#global initializations
best = 0
bestImg = ""
bestkp1 = 0
bestkp2 = 0
points = 0
bestMatchesMask = 0;


#-----------------------------------Function Declarations-----------------------------------------------


def TraverseDatabase(img):	#--------------------------------------------------Traverse Database Function -------------
	for imagePath in glob.glob(args["deck"] + "/*.png"):
		matchCounter = 0
		global best
		global bestImg
		global bestkp1
		global bestkp2
		global bestMatchesMask

		img3 = cv2.imread(imagePath)

		kp1, des1 = sift.detectAndCompute(img,None)
		kp2, des2 = sift.detectAndCompute(img3,None)

		# FLANN parameters
		FLANN_INDEX_KDTREE = 1
		index_params = dict(algorithm = FLANN_INDEX_KDTREE, trees = 5)
		search_params = dict(checks=50)   # or pass empty dictionary
		flann = cv2.FlannBasedMatcher(index_params,search_params)
		matches = flann.knnMatch(des1,des2,k=2)
		# Need to draw only good matches, so create a mask
		matchesMask = [[0,0] for i in xrange(len(matches))]
		# ratio test as per Lowe's paper
		for i,(m,n) in enumerate(matches):
		    if m.distance < 0.7*n.distance:
		    	matchCounter += 1
		        matchesMask[i]=[1,0]

		if matchCounter > best:
			best = matches
			bestImg = imagePath
			bestkp1 = kp1
			bestkp2 = kp2
			bestMatchesMask = matchesMask	


def PointCalculator():  #--------------------------------------------------------- Point Calculator Function -------------
	global bestImg
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

#-----------------------------------End Function Declarations----------------------------------
#-----------------------------------            -----------------------------------------------

ap = argparse.ArgumentParser()
ap.add_argument("-c1", "--c1", required=True, help="card 1 in your hand.")
ap.add_argument("-c2", "--c2", required=True, help="card 1 in your hand.")
ap.add_argument("-d", "--deck", required=True, help="Cards in the deck.")
args = vars(ap.parse_args())

img1 = cv2.imread(args["c1"])
img2 = cv2.imread(args["c2"])

sift = cv2.xfeatures2d.SIFT_create()

#-----------------------------------First Card-----------------------------------------------
TraverseDatabase(img1)

bestImage = cv2.imread(bestImg)

draw_params = dict(matchColor = (0,255,0),
                   singlePointColor = (255,0,0),
                   matchesMask = bestMatchesMask,
                   flags = 0)

img4 = cv2.drawMatchesKnn(img1,bestkp1,bestImage,bestkp2,best,None,**draw_params)


PointCalculator()

#-----------------------------------Second Card-----------------------------------------------
best = 0
bestImg = ""
bestkp1 = 0
bestkp2 = 0
points = 0
bestMatchesMask = 0;

TraverseDatabase(img2)

bestImage = cv2.imread(bestImg)

draw_params = dict(matchColor = (0,255,0),
                   singlePointColor = (255,0,0),
                   matchesMask = bestMatchesMask,
                   flags = 0)

img5 = cv2.drawMatchesKnn(img2,bestkp1,bestImage,bestkp2,best,None,**draw_params)

PointCalculator()

#-----------------------------------Show The Matches--------------------------------------------
plt.imshow(img4),plt.show()
plt.imshow(img5),plt.show()
