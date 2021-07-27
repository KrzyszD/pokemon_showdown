from pokemon import *

def heuristic(prevState, state, side=1):
    score = 0
    
    for poke in state.team2.full:
        if poke.faint != 'dead':
            score += 100
        score += (1 - poke.hp / poke.stats['hp']) * 100
#         score += statusScore(poke.status)
#         score -= sumBoosts(poke.boosts)
    
    for poke in state.team1.full:
        if poke.faint != 'dead':
            score -= 100
        score -= (1 - poke.hp / poke.stats['hp']) * 100
#         score -= statusScore(poke.status)
#         score += sumBoosts(poke.boosts)
    
    if side == 2:
        return -score
    return score

def statusScore(status):
    if status == '':
        return 0
    elif status == 'brn':
        return 25
    elif status == 'psn':
        return 10
    elif status == 'tox':
        return 25
    elif status == 'slp':
        return 15
    elif status == 'frz':
        return 25
    elif status == 'par':
        return 20
    
def sumBoosts(boosts):
    values = boosts.values()
    return sum(values) * 10
