from bs4 import BeautifulSoup

def pitcher_stats(playerCard):
    pitcher = {}
    statTables = playerCard.find_all('table', class_='table table-sm text-center border-bottom')

    todayTable = statTables[0]
    if (len(statTables) > 1):
        todayTable = statTables[1]
        seasonTable = statTables[0].find_all('td')
        pitcher["throws"] = seasonTable[0].getText()
        pitcher["era"] = seasonTable[1].getText()
        pitcher["whip"] = seasonTable[2].getText()
    else:
        pitcher["throws"] = ""
        pitcher["era"] = ""
        pitcher["whip"] = ""

    todayTableCols = todayTable.find_all('td')
    pitcher["pitchCount"] = todayTableCols[11].getText() if (len(todayTableCols)) > 11 else "0"

    return pitcher

def batter_stats(playerCard):
    text = playerCard.find('div', class_='card-header card-title').getText()
    batter = {}
    statTables = playerCard.find_all('table', class_='table table-sm text-center border-bottom')
    if (len(statTables) > 1):
        seasonTable = statTables[0].find_all('td')
        batter["bats"] = seasonTable[0].getText()
        batter["avg"]= seasonTable[1].getText()
        batter["obp"] = seasonTable[2].getText()
        batter["slg"] = seasonTable[3].getText()
        batter["ops"] = seasonTable[4].getText()
    else:
        batter["bats"] = ""
        batter["avg"]= ""
        batter["obp"] = ""
        batter["slg"] = ""
        batter["ops"] = ""
    return batter

def parse_name(playerText):
    numName = playerText.split("#")[1].split("[")[0]
    return name_format(numName)

def name_format(name):
    return name.strip('#1234567890 ')
        
def player_stats(playerCard):
    text = playerCard.find('div', class_='card-header card-title').getText()
    isBatter = "At Bat" in text
    stats = batter_stats(playerCard) if isBatter else pitcher_stats(playerCard)
    stats["name"] = parse_name(text)
    return stats

def get_due_up(body):
    table = body.find('table', class_="table table-sm text-left small")
    if table is not None:
        rows = table.find_all('td', class_="text-center")
        players = table.find_all('td', class_="text-left")
        dueUp = []
        for i in range(3):
            order = rows[i * 3].getText()
            name = name_format(players[i].getText())
            today = rows[i * 3 + 2].getText()
            today = today.replace("\t", "").replace("\n", "").strip()
            dueUp.append({"order": order, "name": name, "today": today})
        return dueUp
    return []

def stat_parse(html):
    stats = {}
    body = BeautifulSoup(html, 'html.parser')
    previousTable = body.find('table', class_='table table-sm text-left table-striped small')
    stats["previousData"] = []
    if previousTable is not None:
        previousRows = previousTable.find_all('td')
        for pRow in previousRows:
            stats["previousData"].append(pRow.getText())
    baseIndicator = body.find('div', class_='base-indicator')
    if baseIndicator is not None:
        stats["runnersOn"] = baseIndicator.find('i', class_='sbicon font-size-300 mx-auto').getText()
        numOuts = baseIndicator.find('i', class_='sbicon d-none d-sm-inline noaccess')
        stats["numOuts"] = len(numOuts.getText()) if numOuts is not None else 0
    else:
        stats["runnersOn"] = ""
        stats["numOuts"] = ""

    teamPlayerData = body.find_all('div', class_='sb-col col-lg-6')
    if len(teamPlayerData) > 1:
        visitingTeamPlayerCard = teamPlayerData[0].find('div')
        homeTeamPlayerCard = teamPlayerData[1].find('div')
        stats["visitingTeamPlayer"] = player_stats(visitingTeamPlayerCard) 
        stats["homeTeamPlayer"] = player_stats(homeTeamPlayerCard)
    else:
        stats["visitingTeamPlayer"] = {}
        stats["homeTeamPlayer"] = {}

    scores = body.find_all('span', class_='font-size-400 sb-teamscore text-line-height-75 w-100 sb-teamscore')
    stats["visitorScore"] = scores[0].getText() if len(scores) > 0 else "0"
    stats["homeScore"] = scores[1].getText() if len(scores) > 0 else "0"
    stats["score"] = stats["visitorScore"] + " - " + stats["homeScore"]
    currentInning = body.find('div', class_='text-center mr-5 mx-auto font-size-125 mb-1')
    if currentInning is not None:
        stats["currentInning"] = currentInning.getText()
    else:
        currentInning = body.find('div', class_='h-100 font-size-300 text-line-height-1-25 text-center font-weight-bold')
        if currentInning is not None:
            stats["currentInning"] = currentInning.getText()
        else:
            stats["currentInning"] = ""

    visitorName = body.find('div', class_="w-100 font-size-200 sb-teamname sb-teamnameV")
    if visitorName is None:
        visitorName = body.find('div', class_="w-100 font-weight-bold font-size-200 sb-teamname sb-teamnameV")
    homeName = body.find('div', class_="w-100 font-size-200 sb-teamname sb-teamnameH")
    if homeName is None:
        homeName = body.find('div', class_="w-100 font-weight-bold font-size-200 sb-teamname sb-teamnameH")

    stats["visitor"] = name_format(visitorName.getText()) if visitorName is not None else ""
    stats["home"] = name_format(homeName.getText()) if homeName is not None else ""
    stats["dueUp"] = get_due_up(body)

    return stats
