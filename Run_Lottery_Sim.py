import NHL_Lottery_Sim as lottery

lottery_prob = {1: [.185, .165, .144], 2: [.135, .13, .123], 3: [.115, .113, .111],
                4: [.095, .096, .097], 5: [.085, .087, .089], 6: [.075, .078, .08], 7: [.065, .068, .071],
                8: [.06, .063, .067], 9: [.05, .053, .057], 10: [.035, .038, .041], 11: [.03, .033, .036],
                12: [.025, .027, .03], 13: [.02, .022, .024], 14: [.015, .017, .018], 15: [.01, .011, .012]}

#lottery_prob = lottery.lottery_prob

lottery_order = lottery.reverse_standings(lottery.get_standings())
print(lottery.draft_order(lottery_prob, lottery_order))
