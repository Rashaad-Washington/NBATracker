from nba_api.stats.endpoints import playercareerstats
from nba_api.live.nba.endpoints import scoreboard
from nba_api.stats.endpoints import playergamelog
from nba_api.stats.endpoints import boxscoretraditionalv2
import pandas as pd 
from nba_api.stats.library.parameters import SeasonAll
from nba_api.stats.static import players
import json

def findPlayerId(name):
    playerRetrieval = players.find_players_by_full_name(name)
    playerID = playerRetrieval[0]
    return playerID["id"]







print("\nWelcome to Rashaad's Stat Tracking App!")
default = True
while default == True:
    thisPlayer = {
  "playerName": "",
  "playerID": 0,
  "season_min_avg": 0,
  "season_pts_avg": 0,
  "year": 0,
  "pm3_assists": 0,
  "pm3_oreb": 0,
  "pm3_dreb": 0,
  "pm3_totreb": 0,
  "pm3_steals": 0,
  "pm3_blocks": 0,
  "pm3_points": 0,
  "pm3_3pm": 0,
  "10pm3_assists": 0,
  "10pm3_oreb": 0,
  "10pm3_dreb": 0,
  "10pm3_totreb": 0,
  "10pm3_steals": 0,
  "10pm3_blocks": 0,
  "10pm3_points": 0,
  "10pm3_3pm": 0
}
    option = input("\n1. Search the stats for an NBA player\n2. Exit\n")
    if option == "1":
        playerName = input("Please enter the first and last name of the player you choose to view stats. ")
        try:
            thisPlayer["playerID"] = findPlayerId(playerName)
        except BaseException: 
            print("Sorry, player can not be found.")
            continue

        thisPlayer["playerName"] = playerName
        thisPlayer["year"] = input("Please enter the season year: ")
        print("Here is a 10-game snapshot for " + playerName + " during the " + str(thisPlayer["year"]) + "-" + str(int(thisPlayer["year"]) + 1) + " season!\n")
        preSnapshot = playergamelog.PlayerGameLog(player_id='' + str(findPlayerId(playerName)), season = str(thisPlayer["year"]),).get_json()
        postSnapshot = json.loads(preSnapshot)
        average = 0
        index = 0
        for i in postSnapshot["resultSets"][0]["rowSet"]:
            if index < 10: 
                print("\n" + str(index + 1) + " game(s) ago")
                print("--------------")
                print("Minutes: " + str(i[6]))
                print("3PM: " + str(i[10]))
                print("offReb: " + str(i[16]))
                print("defReb: " + str(i[17]))
                print("totReb: " + str(i[18]))
                print("Assists: " + str(i[19]))
                print("Steals: " + str(i[20]))
                print("Blocks: " + str(i[21]))
                print("Points: " + str(i[24]))
            thisPlayer["season_min_avg"] += i[6]
            thisPlayer["season_pts_avg"] += i[24]
            index+= 1
        thisPlayer["season_min_avg"] = thisPlayer["season_min_avg"] / index
        thisPlayer["season_pts_avg"] = thisPlayer["season_pts_avg"] / index

        index = 0
        for i in postSnapshot["resultSets"][0]["rowSet"]:
            if i[6] >= (int(thisPlayer["season_min_avg"]) - 3) and i[6] <= (int(thisPlayer["season_min_avg"]) + 3):
                thisPlayer["pm3_3pm"] += (i[10])
                thisPlayer["pm3_points"] += (i[24])
                thisPlayer["pm3_blocks"] += (i[21])
                thisPlayer["pm3_steals"] += (i[20])
                thisPlayer["pm3_totreb"] += (i[18])
                thisPlayer["pm3_dreb"] += (i[17])
                thisPlayer["pm3_oreb"] += (i[16])
                thisPlayer["pm3_assists"] += (i[19])
                index += 1
                
        thisPlayer["pm3_3pm"] = thisPlayer["pm3_3pm"] / index
        thisPlayer["pm3_oreb"] = thisPlayer["pm3_oreb"] / index
        thisPlayer["pm3_dreb"] = thisPlayer["pm3_dreb"] / index
        thisPlayer["pm3_totreb"] = thisPlayer["pm3_totreb"] / index
        thisPlayer["pm3_assists"] = thisPlayer["pm3_assists"] / index
        thisPlayer["pm3_steals"] = thisPlayer["pm3_steals"] / index
        thisPlayer["pm3_blocks"] = thisPlayer["pm3_blocks"] / index
        thisPlayer["pm3_points"] = thisPlayer["pm3_points"] / index
        

        print("\n" + thisPlayer["playerName"] + " averages " + str(round(thisPlayer["season_pts_avg"], 1)) + " PPG this season")
        print("In games where " + thisPlayer["playerName"] + " played +/- 3 minutes of their seasons average minutes of " + str(round(thisPlayer["season_min_avg"], 1)) + ", " + thisPlayer["playerName"] + " averaged the following this season...\n")
        print("3PM: " + str(round(thisPlayer["pm3_3pm"], 1)))
        print("Points: " + str(round(thisPlayer["pm3_points"], 1)))
        print("Blocks: " + str(round(thisPlayer["pm3_blocks"], 1)))
        print("Steals: " + str(round(thisPlayer["pm3_steals"], 1)))
        print("totReb: " + str(round(thisPlayer["pm3_totreb"], 1)))
        print("defReb: " + str(round(thisPlayer["pm3_dreb"], 1)))
        print("offReb: " + str(round(thisPlayer["pm3_oreb"], 1)))
        print("Assists: " + str(round(thisPlayer["pm3_assists"], 1)))

        index = 0
        subindex = 0
        for i in postSnapshot["resultSets"][0]["rowSet"]:
            if index < 10: 
                if i[6] >= (thisPlayer["season_min_avg"] - 5) and i[6] <= (thisPlayer["season_min_avg"] + 5):
                    thisPlayer["10pm3_3pm"] += (i[10])
                    thisPlayer["10pm3_points"] += (i[24])
                    thisPlayer["10pm3_blocks"] += (i[21])
                    thisPlayer["10pm3_steals"] += (i[20])
                    thisPlayer["10pm3_totreb"] += (i[18])
                    thisPlayer["10pm3_dreb"] += (i[17])
                    thisPlayer["10pm3_oreb"] += (i[16])
                    thisPlayer["10pm3_assists"] += (i[19])
                    subindex +=1
            index+=1
            
        
        thisPlayer["10pm3_3pm"] = thisPlayer["10pm3_3pm"] / subindex
        thisPlayer["10pm3_oreb"] = thisPlayer["10pm3_oreb"] / subindex
        thisPlayer["10pm3_dreb"] = thisPlayer["10pm3_dreb"] / subindex
        thisPlayer["10pm3_totreb"] = thisPlayer["10pm3_totreb"] / subindex
        thisPlayer["10pm3_assists"] = thisPlayer["10pm3_assists"] / subindex
        thisPlayer["10pm3_steals"] = thisPlayer["10pm3_steals"] / subindex
        thisPlayer["10pm3_blocks"] = thisPlayer["10pm3_blocks"] / subindex
        thisPlayer["10pm3_points"] = thisPlayer["10pm3_points"] / subindex
        print("\nDue to coaching adjustments, hot/cold streaks, and injury performances, it is always great to monitor the last 10 game averages when playing +/- 5 of " + thisPlayer["playerName"] + "'s season average minutes...\n")
        print("3PM: " + str(round(thisPlayer["10pm3_3pm"], 1)))
        print("Points: " + str(round(thisPlayer["10pm3_points"], 1)))
        print("Blocks: " + str(round(thisPlayer["10pm3_blocks"], 1)))
        print("Steals: " + str(round(thisPlayer["10pm3_steals"], 1)))
        print("totReb: " + str(round(thisPlayer["10pm3_totreb"], 1)))
        print("defReb: " + str(round(thisPlayer["10pm3_dreb"], 1)))
        print("offReb: " + str(round(thisPlayer["10pm3_oreb"], 1)))
        print("Assists: " + str(round(thisPlayer["10pm3_assists"], 1)))



        continue

    elif option != "1" and option != "2":
         print("I am sorry, that is not an option. Please pick an option from the menu.")
         continue
    break

print("Thank you for using my stat tracker\n")

