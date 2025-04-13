from stat_formatter import stat_format



stats = { 
    "previousData": ["l1", "l2", "l3" ],
    "visitingTeamPlayer": {"name": "v-player", "avg": ".346" },
    "homeTeamPlayer": {"name": "v-player", "pitchCount": 10, "era": "1.23" },
    "currentInning": "Top 3", 
    "runnersOn": "1", 
    "numOuts": 2, 
    "home": "Texas", 
    "visitor": "Not Texas", 
    "homeScore": "5", 
    "visitorScore": "4", 
    "dueUp": [
        {"order": "2", "name": "Mays", "today": "1-2"},
        {"order": "3", "name": "Jackson", "today": "0-1"},
        {"order": "4", "name": "Henderson", "today": "1-1"},
    ]
}
p_stats = { 
    "previousData": ["l1", "l2"],
    "visitingTeamPlayer": {"name": "v-player", "avg": ".346" },
    "homeTeamPlayer": {"name": "v-player", "pitchCount": 10, "era": "1.23" },
    "currentInning": "Bot 3", 
    "runnersOn": "1", 
    "numOuts": 2, 
    "home": "Texas", 
    "visitor": "Not Texas", 
    "homeScore": "5", 
    "visitorScore": "4", 
    "dueUp": [
        {"order": "5", "name": "Jones", "today": "0-1"},
        {"order": "6", "name": "Johnson", "today": "1-1"},
        {"order": "7", "name": "Hays", "today": "0-1"},
    ]
}

post = stat_format(stats, p_stats)

print(post)

print(stats["currentInning"])
