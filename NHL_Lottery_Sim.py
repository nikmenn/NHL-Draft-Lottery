import random
import json
from urllib.request import urlopen

lottery_prob = {1: [.185, .165, .144], 2: [.135, .13, .123], 3: [.115, .113, .111],
                4: [.095, .096, .097], 5: [.085, .087, .089], 6: [.075, .078, .08], 7: [.065, .068, .071],
                8: [.06, .063, .067], 9: [.05, .053, .057], 10: [.035, .038, .041], 11: [.03, .033, .036],
                12: [.025, .027, .03], 13: [.02, .022, .024], 14: [.015, .017, .018], 15: [.01, .011, .012]}


def create_prob_tuples(lottery_prob):
    '''
    Takes in lottery_prob dictionary as the argument, and returns three lists containing the
    probabilties of each rank getting a pick at a said slot (i.e: the first item returns a list containing
    tuples of each rank's probabilities for the first pick, and so on for the subsequent lists)
    '''
    prob_first_pick = []
    prob_second_pick = []
    prob_third_pick = []

    for rank in lottery_prob:
        prob_first_pick.append((rank, lottery_prob[rank][0]))
        prob_second_pick.append((rank, lottery_prob[rank][1]))
        prob_third_pick.append((rank, lottery_prob[rank][2]))

    return prob_first_pick, prob_second_pick, prob_third_pick


def lottery_slot_winner(prob_list):
    '''
    Takes in list of tuples containing the rank and probability weights and returns one number
    '''
    POPULATION = [x[0] for x in prob_list]
    WEIGHTS = [x[1] for x in prob_list]
    winner = random.choices(population=POPULATION, weights=WEIGHTS)[0]
    return winner


def get_standings():
    '''
    Uses the NHL statsapi to return a dictionary of the league's current standings
    '''
    with urlopen('https://statsapi.web.nhl.com/api/v1/standings') as response:
        source = response.read()

    standings_data = json.loads(source)

    standings = {}
    for record in standings_data['records']:
        for team in record['teamRecords']:
            name = team['team']['name']
            #place = int(team['leagueRank'])
            # The above uncommented code is what you would use if every team has played 82 games
            # Due to covid the 2019-2020 standings go by point percentage
            place = int(team['ppLeagueRank'])
            standings[name] = place

    return standings


def reverse_standings(standings):
    '''
    Takes in the standings dictionary and reverses the values of the current standings so standings align
    with the lottery format and returns it in dictionary format
    '''
    for key, value in standings.items():
        value = abs((value - 31) - 1)
        standings[key] = value
    return standings


def lottery_winners(lottery_prob, lottery_order):
    '''
    Takes in two arguments, lottery_prob which is a dictionary that contains lottery probabilities of each place.
    lottery_order which is a dictionary containing the league's standings in ascending order.
    Returns three unique winners in a list and in order of where they are selecting (i.e. the first element of the list corresponds to the first pick)
    '''
    prob_first_pick, prob_second_pick, prob_third_pick = create_prob_tuples(lottery_prob)

    lottery_winning_places = []

    lottery_winning_places.append(lottery_slot_winner(prob_first_pick))

    while len(lottery_winning_places) == 1:
        second_winner = lottery_slot_winner(prob_second_pick)
        if second_winner not in lottery_winning_places:
            lottery_winning_places.append(second_winner)

    while len(lottery_winning_places) == 2:
        third_winner = lottery_slot_winner(prob_third_pick)
        if third_winner not in lottery_winning_places:
            lottery_winning_places.append(third_winner)

    lottery_winners = []
    for winner in lottery_winning_places:
        for team, place in lottery_order.items():
            if place == winner:
                lottery_winners.append(team)

    return lottery_winners


def draft_order(lottery_prob, lottery_order):
    '''
    Takes in two arguments, lottery_prob which is a dictionary that contains lottery probabilities of each place.
    lottery_order which is a dictionary containing the league's standings in ascending order.
    Returns a list of tuples that have the team name and their selection in order of their selection (post-lottery).
    '''

    winners = lottery_winners(lottery_prob, lottery_order)

    for team, place in lottery_order.items():
        temp_val = 0
        if team not in winners:
            for winner in winners:
                if lottery_order[winner] > lottery_order[team]:
                    temp_val += 1
        lottery_order[team] += temp_val

    for winner in winners:
        lottery_order[winner] = winners.index(winner) + 1

    d_order = sorted(lottery_order.items(), key=lambda x: x[1])

    return d_order


#lottery_order = reverse_standings(get_standings())
#print(draft_order(lottery_prob, lottery_order))
