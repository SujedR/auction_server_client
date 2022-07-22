#!/usr/bin/python3

import json
from flask import Flask, request
from threading import Thread
import time
import urllib.request

#Set auction server URL
AUCTION_SERV_URL = "http://localhost:8800"

app = Flask(__name__)

#Select the strategy for each player
strat = ["int", "comp1", "comp1", ""]

#Global variables 
agent_ids = []
competitionID = []
startMessage = {}
valuations = []
bid = 0
nbItem = 0
nbBundle = 0
nbDesirableBundles = 0
nbAgents = 0
goodBundle = []
desirableBundles = []

 
def send_bid(agent_id):
    with open(str(agent_id) + '.json', 'r') as bid_file:
        auction_bid = bid_file.read()

        req = urllib.request.Request(f'{AUCTION_SERV_URL}/' + competitionID[0],
                                    headers={'Content-type': 'application/json'},
                                    data=auction_bid.encode('utf-8'))
        res = urllib.request.urlopen(req)
        htmldoc = res.read().decode('utf-8')
        print(htmldoc)

def numberItemsBundles():
    global valuations, nbItem, nbBundle
    #Couting item number
    for j in valuations[0]:
        if j["node"] == "leaf":
            nbItem = nbItem+1

    #Couting number of bundles with triangular numbers
    nbBundle = int((nbItem*(nbItem +1)/2))

def combin(n, k):
    #Nombre de combinaisons de n objets pris k a k
    if k > n//2:
        k = n-k
    x = 1
    y = 1
    i = n-k+1
    while i <= n:
        x = (x*i)//y
        y += 1
        i += 1
    return x

def get_valuations():
    global startMessage, valuations, bid, goodBundle, desirableBundles, player, nbItem, nbDesirableBundles, nbBundle, nbAgents
    x = 0
    h = 0
    y = 0
    p = 0
    j = 0
    bid = 0

    with open('auction.json', 'r') as json_file:
	    json_load = json.load(json_file)

    #Getting valuations
    for i in json_load['agents']:
        valuations.append((i['valuation']['child_nodes']))
        x += 1
    nbAgents = x
    numberItemsBundles()

    #Saving each bundle valuation adding synergy values
    for j in range(nbAgents-1):
        h = 0
        bundle = []
        while h <= combin(2, nbItem)+nbItem:
            if valuations[j][h]["node"] == "leaf": 
                bundle.append(valuations[j][h]["value"])
            else:
                bundle.append((valuations[j][h]["child_nodes"][0]["value"] + valuations[j][h]["child_nodes"][1]["value"] + valuations[j][h]["value"])//2)
            h += 1
        goodBundle.append(bundle)
    
    #Calculating AC Values and adding bundle of 3,4,5
    #A automatiser
    for player in range(nbAgents-1):
        if nbItem == 3:
            goodBundle[player].append(int((valuations[player][0]["value"] + valuations[player][1]["value"] + valuations[player][2]["value"] + 2/(3-1)*(valuations[player][3]["value"] + valuations[player][4]["value"] + valuations[player][5]["value"]))//3))
        elif nbItem == 4:
            goodBundle[player][10] = (valuations[player][0]["value"] + valuations[player][1]["value"] + valuations[player][2]["value"] + 2/(3-1)*(valuations[player][4]["value"] + valuations[player][5]["value"] + valuations[player][7]["value"]))//3
            goodBundle[player][11] = (valuations[player][0]["value"] + valuations[player][1]["value"] + valuations[player][3]["value"] + 2/(3-1)*(valuations[player][4]["value"] + valuations[player][6]["value"] + valuations[player][8]["value"]))//3
            goodBundle[player][12] = (valuations[player][0]["value"] + valuations[player][2]["value"] + valuations[player][3]["value"] + 2/(3-1)*(valuations[player][5]["value"] + valuations[player][6]["value"] + valuations[player][9]["value"]))//3
            goodBundle[player][13] = (valuations[player][1]["value"] + valuations[player][2]["value"] + valuations[player][3]["value"] + 2/(3-1)*(valuations[player][7]["value"] + valuations[player][8]["value"] + valuations[player][9]["value"]))//3
            goodBundle[player][14] = (valuations[player][0]["value"] + valuations[player][1]["value"] + valuations[player][2]["value"] + valuations[player][3]["value"] + 2/(4-1)*(valuations[player][4]["value"] + valuations[player][5]["value"] + valuations[player][6]["value"] + valuations[player][7]["value"] + valuations[player][8]["value"] + valuations[player][9]["value"]))//4
        elif nbItem == 5:   
            goodBundle[player][15] = (valuations[player][0]["value"] + valuations[player][1]["value"] + valuations[player][2]["value"] + 2/(nbItem-1)*(valuations[player][5]["value"] + valuations[player][6]["value"] + valuations[player][9]["value"]))//3
            goodBundle[player][16] = (valuations[player][0]["value"] + valuations[player][1]["value"] + valuations[player][3]["value"] + 2/(nbItem-1)*(valuations[player][5]["value"] + valuations[player][7]["value"] + valuations[player][10]["value"]))//3
            goodBundle[player][17] = (valuations[player][0]["value"] + valuations[player][1]["value"] + valuations[player][4]["value"] + 2/(nbItem-1)*(valuations[player][5]["value"] + valuations[player][8]["value"] + valuations[player][11]["value"]))//3
            goodBundle[player][18] = (valuations[player][0]["value"] + valuations[player][2]["value"] + valuations[player][3]["value"] + 2/(nbItem-1)*(valuations[player][6]["value"] + valuations[player][7]["value"] + valuations[player][12]["value"]))//3
            goodBundle[player][19] = (valuations[player][0]["value"] + valuations[player][2]["value"] + valuations[player][4]["value"] + 2/(nbItem-1)*(valuations[player][6]["value"] + valuations[player][8]["value"] + valuations[player][13]["value"]))//3
            goodBundle[player][20] = (valuations[player][0]["value"] + valuations[player][3]["value"] + valuations[player][4]["value"] + 2/(nbItem-1)*(valuations[player][7]["value"] + valuations[player][8]["value"] + valuations[player][14]["value"]))//3
            goodBundle[player][21] = (valuations[player][1]["value"] + valuations[player][2]["value"] + valuations[player][3]["value"] + 2/(nbItem-1)*(valuations[player][9]["value"] + valuations[player][10]["value"] + valuations[player][12]["value"]))//3
            goodBundle[player][22] = (valuations[player][1]["value"] + valuations[player][2]["value"] + valuations[player][4]["value"] + 2/(nbItem-1)*(valuations[player][9]["value"] + valuations[player][11]["value"] + valuations[player][13]["value"]))//3
            goodBundle[player][23] = (valuations[player][1]["value"] + valuations[player][3]["value"] + valuations[player][4]["value"] + 2/(nbItem-1)*(valuations[player][10]["value"] + valuations[player][11]["value"] + valuations[player][14]["value"]))//3
            goodBundle[player][24] = (valuations[player][2]["value"] + valuations[player][3]["value"] + valuations[player][4]["value"] + 2/(nbItem-1)*(valuations[player][12]["value"] + valuations[player][13]["value"] + valuations[player][14]["value"]))//3
            goodBundle[player][25] = (valuations[player][0]["value"] + valuations[player][1]["value"] + valuations[player][2]["value"] + valuations[player][3]["value"] + 2/(4-1)*(valuations[player][5]["value"] + valuations[player][6]["value"] + valuations[player][7]["value"] + valuations[player][9]["value"] + valuations[player][10]["value"] + valuations[player][12]["value"]))//4
            goodBundle[player][26] = (valuations[player][0]["value"] + valuations[player][1]["value"] + valuations[player][2]["value"] + valuations[player][4]["value"] + 2/(4-1)*(valuations[player][5]["value"] + valuations[player][6]["value"] + valuations[player][8]["value"] + valuations[player][9]["value"] + valuations[player][11]["value"] + valuations[player][13]["value"]))//4            
            goodBundle[player][27] = (valuations[player][0]["value"] + valuations[player][1]["value"] + valuations[player][3]["value"] + valuations[player][4]["value"] + 2/(4-1)*(valuations[player][5]["value"] + valuations[player][7]["value"] + valuations[player][8]["value"] + valuations[player][10]["value"] + valuations[player][11]["value"] + valuations[player][14]["value"]))//4
            goodBundle[player][28] = (valuations[player][0]["value"] + valuations[player][2]["value"] + valuations[player][3]["value"] + valuations[player][4]["value"] + 2/(4-1)*(valuations[player][6]["value"] + valuations[player][7]["value"] + valuations[player][8]["value"] + valuations[player][12]["value"] + valuations[player][13]["value"] + valuations[player][14]["value"]))//4
            goodBundle[player][29] = (valuations[player][1]["value"] + valuations[player][2]["value"] + valuations[player][3]["value"] + valuations[player][4]["value"] + 2/(4-1)*(valuations[player][9]["value"] + valuations[player][10]["value"] + valuations[player][11]["value"] + valuations[player][12]["value"] + valuations[player][13]["value"] + valuations[player][14]["value"]))//4
            goodBundle[player][30] = (valuations[player][0]["value"] + valuations[player][1]["value"] + valuations[player][2]["value"] + valuations[player][3]["value"] + valuations[player][4]["value"] + 2/(5-1)*(valuations[player][5]["value"] + valuations[player][6]["value"] + valuations[player][7]["value"] + valuations[player][8]["value"] + valuations[player][9]["value"] + valuations[player][10]["value"] + valuations[player][11]["value"] + valuations[player][12]["value"] + valuations[player][13]["value"] + valuations[player][14]["value"]))//5

    print("------------- AC VALUES FOR EACH BUNDLE BY AGENT -----------")
    for j in range(nbAgents-1):
        print("------ Agent",j+1,"------------")
        for n in range(nbBundle):
            print(goodBundle[j][n])

#A finir
def intStrat(bidder_number):
    global nbItem, nbDesirableBundles, nbBundle, desirableBundles, goodBundle
    #Saving desirable bundles according to INT strategy
    p = 0 
    desirableBundles = []
    desirableBundles.append(goodBundle[bidder_number][0])
    for i in range(1,len(goodBundle[bidder_number])-1):
        if goodBundle[bidder_number][i] >= desirableBundles[p]:
            p = p+1
            desirableBundles.append(goodBundle[bidder_number][i])
            nbDesirableBundles = nbDesirableBundles + 1

    x=0 
    
    with open("agent"+str(bidder_number+1)+".json", "r") as jsonFile:
        data = json.load(jsonFile)

    for x in range(len(goodBundle[bidder_number])):
            for y in range(len(desirableBundles)):
                if goodBundle[bidder_number][x] == desirableBundles[y]:
                    if x <= nbItem:
                        data["bid"]["child_nodes"][x]["value"] = desirableBundles[y]
                    else:
                        data["bid"]["child_nodes"][x]["child_nodes"][0]["value"] = desirableBundles[y]//2
                        data["bid"]["child_nodes"][x]["child_nodes"][1]["value"] = desirableBundles[y]//2
                else:
                    if x <= nbItem:
                        data["bid"]["child_nodes"][x]["value"] = 0
                    else:
                        data["bid"]["child_nodes"][x]["child_nodes"][0]["value"] = 0
                        data["bid"]["child_nodes"][x]["child_nodes"][1]["value"] = 0

    with open("agent"+str(bidder_number+1)+".json", "w") as jsonFile:
        json.dump(data, jsonFile)

def compStrat(bidder_number):
    global nbItem, nbDesirableBundles, nbBundle, desirableBundles, goodBundle
    x = 0
    y = 0

    #Saving desirable bundles according to COMP strategy
    for i in range(nbBundle):
        if goodBundle[bidder_number][i] >= ((goodBundle[0][i] + goodBundle[1][i] + goodBundle[2][i] - goodBundle[bidder_number][i]))/nbAgents-2:
            desirableBundles.append(goodBundle[bidder_number][i])
            nbDesirableBundles += 1

    with open("agent"+str(bidder_number+1)+".json", "r") as jsonFile:
        data = json.load(jsonFile)

    for x in range(int(nbBundle)):
            for y in range(int(nbDesirableBundles)):
                if goodBundle[bidder_number][x] == desirableBundles[y]:
                    if x <= nbItem:
                        data["bid"]["child_nodes"][x]["value"] = desirableBundles[y]
                    else:
                        data["bid"]["child_nodes"][x]["child_nodes"][0]["value"] = desirableBundles[y]//2
                        data["bid"]["child_nodes"][x]["child_nodes"][1]["value"] = desirableBundles[y]//2
                else:
                    if x <= nbItem:
                        data["bid"]["child_nodes"][x]["value"] = 0
                    else:
                        data["bid"]["child_nodes"][x]["child_nodes"][0]["value"] = 0
                        data["bid"]["child_nodes"][x]["child_nodes"][1]["value"] = 0

    with open("agent"+str(bidder_number+1)+".json", "w") as jsonFile:
        json.dump(data, jsonFile)

def noStrat(bidder_number):
    global nbItem, nbDesirableBundles, nbBundle, desirableBundles, goodBundle

    with open("agent"+str(bidder_number+1)+".json", "r") as jsonFile:
        data = json.load(jsonFile)

    for x in range(int(nbBundle)):
            for y in range(int(nbBundle)):
                    if x <= nbItem:
                        data["bid"]["child_nodes"][x]["value"] = valuations[bidder_number][y]["value"]
                    else:
                        data["bid"]["child_nodes"][x]["child_nodes"][0]["value"] = valuations[bidder_number][y]["value"]//2
                        data["bid"]["child_nodes"][x]["child_nodes"][1]["value"] = valuations[bidder_number][y]["value"]//2

    with open("agent"+str(bidder_number+1)+".json", "w") as jsonFile:
        json.dump(data, jsonFile)

def default_bidder(bidder_number):
    def log(msg):
        print(f'Bidder {bidder_number+1} > {msg}')
    global startMessage, bid, valuations, strat
    message = json.loads(request.data.decode("utf-8"))
    if message['message_type'] == 'start':
        log('start message received')
        agent_ids.append(message['agent_id'])
        if bidder_number == 0:
            startMessage = message
            get_valuations()
        if strat[bidder_number] == "comp1":
            compStrat(bidder_number)
        elif strat[bidder_number] == "int":
            intStrat(bidder_number)
        else:
            noStrat(bidder_number)
        competitionID.append(message['competition_id'])
        return 'ready'
    if message['message_type'] == 'bid_request':
        log('bid request message received')
        t = Thread(target=send_bid, args=(agent_ids[bidder_number],))
        t.start()
        return 'received'
    if message['message_type'] == 'stop':
        log('stop message received')
        return ''
    else:
        log('description received')
        return ''
    return 'Unimplemented request'


@app.route("/bidder1", methods=["GET", "POST"])
def bidder1():
    return default_bidder(0)

@app.route("/bidder2", methods=["GET", "POST"])
def bidder2():
    return default_bidder(1)

@app.route("/bidder3", methods=["GET", "POST"])
def bidder3():
    return default_bidder(2)

@app.route("/bidder4", methods=["GET", "POST"])
def bidder4():
    return default_bidder(3)
