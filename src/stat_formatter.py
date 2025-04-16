def format_runners(stats):
    runnersOn = stats["runnersOn"]
    fb = '■' if (runnersOn == "1" or runnersOn == "4" or runnersOn == "6" or runnersOn == "7") else '□'
    sb = '■' if (runnersOn == "2" or runnersOn == "4" or runnersOn == "5" or runnersOn == "7") else '□'
    tb = '■' if (runnersOn == "3" or runnersOn == "5" or runnersOn == "6" or runnersOn == "7") else '□'
    return f'    {sb}\n  /   \\ \n{tb}     {fb}'

def format_outs(stats):
    return f'Outs: {stats["numOuts"]}'

def format_score(stats):
    visitor = stats["visitor"]
    home = stats["home"]
    visitor = "@TexasBaseball" if visitor == "Texas" else visitor
    home = "@TexasBaseball" if home == "Texas" else home
    return f'{stats["currentInning"]}\n{visitor}: {stats["visitorScore"]}\n{home}: {stats["homeScore"]}'

def pitcher_info(pitcher):
    return f'Pitching: {pitcher["name"]} (ERA: {pitcher["era"]})'

def batter_info(batter):
    return f'At Bat: {batter["name"]} (AVG: {batter["avg"]})'

def format_pitcher_batter(pitcher, batter):
    return f'{batter_info(batter)}\n{pitcher_info(pitcher)}'

def format_due_up(stats):
    players = stats["dueUp"]
    if (len(players) > 2):
        dueUp = []
        for p in players:
            dueUp.append(f'{p["order"]} {p["name"]} ({p["today"]})')
        return f'\n\nDue Up:\n' + "\n".join(dueUp)
    return ""

def format_pitcher_count(pitcher):
    return f'\n\nPitcher: {pitcher["name"]}, PC: {pitcher["pitchCount"]}'

def format_inning(stats, batter, pitcher):
    atBat = format_pitcher_batter(pitcher, batter)
    score = format_score(stats)
    runners = format_runners(stats)
    outs = format_outs(stats)
    return f'{atBat}\n\n{runners}\n{outs}\n\n{score}'

def format_top_inning(stats):
    batter = stats["visitingTeamPlayer"]
    pitcher = stats["homeTeamPlayer"]

    return format_inning(stats, batter, pitcher)

def format_bot_inning(stats):
    batter = stats["homeTeamPlayer"]
    pitcher = stats["visitingTeamPlayer"]

    return format_inning(stats, batter, pitcher)

def format_mid_inning(stats, previousStats):
    score = format_score(stats)
    dueUp = format_due_up(previousStats)
    pitcher = stats["visitingTeamPlayer"]
    pitcherCount = format_pitcher_count(pitcher)
    return score + dueUp + pitcherCount

def format_end_inning(stats, previousStats):
    score = format_score(stats)
    dueUp = format_due_up(previousStats)
    pitcher = stats["homeTeamPlayer"]
    pitcherCount = format_pitcher_count(pitcher)
    return score + dueUp + pitcherCount

def format_final(stats):
    score = format_score(stats)
    return score + "\n\nHook 'em"

def format_pbp(stats, previousStats):
    cur = stats["previousData"]
    prev = previousStats["previousData"]
    toPost = list(set(cur) - set(prev))
    return "\n".join(toPost)

def stat_format(stats, previousStats):
    # print(stats)
    new_pbp = format_pbp(stats, previousStats)
    curInning = stats["currentInning"]
    prevInning = previousStats["currentInning"]
    if (curInning != prevInning and prevInning != "" and prevInning[:3] != "Mid" and prevInning[:3] != "End"): 
        curInning = curInning.replace("Top", "End").replace("Bot", "Mid")
    if (curInning == "End 9" and stats["visitorScore"] != stats["homeScore"]):
        curInning = "Final"
    if (curInning == "Mid 9" and int(stats["homeScore"]) > int(stats["visitorScore"])):
        curInning = "Final"
    stats["currentInning"] = curInning
    if (len(new_pbp) == 0 and curInning != "Final"):
        return ""
    new_pbp = new_pbp + '\n\n'

    match curInning[:3]:
        case "Top":
            return new_pbp + format_top_inning(stats)
        case "Bot":
            return new_pbp + format_bot_inning(stats)
        case "Fin":
            return new_pbp + format_final(stats)
        case "Mid":
            return new_pbp + format_mid_inning(stats, previousStats)
        case "End":
            return new_pbp + format_end_inning(stats, previousStats)
        case "Not":
            return ""
        case _:
            print("no inn found")