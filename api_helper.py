import subprocess, shlex
from multiprocessing import Process, Queue
from pokemon import *
import time
import sys
import copy
import re
from sim_parser import outputParser

showdown_cmd = './showdownsimulator/pokemon-showdown/pokemon-showdown simulate-battle'

def prin(*args):
    if True:
        print(*args)

def runSim(state, moves, num_sims=1):
    # state: pokemon on both sides, weather, etc
    # moves: desired move combos
    
    threads = []
    results = Queue()
    
    # start process
    for i in range(num_sims):
        
        t = Process(target=sim_wrapper, args=(results, state, moves, i))
        t.start()
        threads.append(t)

    # Wait for sim to end
    for t in threads:
        t.join()
    
    score = 0
    i = 0
    # Getting the results
    while not results.empty():
        i += 1
        score += results.get()
        
    score /= i
    
    print(score, moves)
        
    
    
def heuristic(prevState, state):
    score = 0
    
    for poke in state.team2.full:
        if poke.faint != 'alive':
            score += 100
        score += (1 - poke.hp / poke.stats['hp']) * 100
    
    for poke in state.team1.full:
        if poke.faint != 'alive':
            score -= 100
        score -= (1 - poke.hp / poke.stats['hp']) * 100
    
    return score



def updateField(proc_input, state):
    
    weather = '>p1 weather ' + state.weather + ' \n'
    proc_input.write(weather)
    
    terrain = '>p1 terrain ' + state.terrain + ' \n'
    proc_input.write(terrain)
    
    for pweather in state.pseudoweather:
        pseudoweather = '>p1 pseudoweather ' + pweather + ' \n'
        proc_input.write(pseudoweather)
        prin(pseudoweather)
        
        
        
def updateSide(proc_input, myTeam):
    
    stat_names = ['hp', 'atk', 'def', 'spa', 'spd', 'spe']
    boosts_names = ['atk', 'def', 'spa', 'spd', 'spe', 'accuracy', 'evasion']
    base = '>' + myTeam.side + ' '
    
    alive_cmd = base
    for poke in myTeam.active:
        alive_cmd += 'fainted ' + poke.faint + ', '
    alive_cmd = alive_cmd[:-2] + ' \n'
    
    proc_input.write(alive_cmd)
    
    
    
    stat_cmd = base
    for poke in myTeam.active:
        stat_cmd += 'stats '
        for stat in stat_names:
            stat_cmd += str(poke.stats[stat]) + ' '
        stat_cmd += ', '
    stat_cmd = stat_cmd[:-2] + ' \n'
    
    proc_input.write(stat_cmd)
    
    
    hp_cmd = base
    for poke in myTeam.active:
        hp_cmd += 'hp ' + str(poke.hp)
        hp_cmd += ', '
    hp_cmd = hp_cmd[:-2] + ' \n'
    
    proc_input.write(hp_cmd)
    
    
    boost_cmd = base
    for poke in myTeam.active:
        boost_cmd += 'boosts '
        for boost in boosts_names:
            boost_cmd += str(poke.boosts[boost]) + ' '
        boost_cmd += ', '
    boost_cmd = boost_cmd[:-2] + ' \n'
    
    proc_input.write(boost_cmd)
    
    
    move_cmd = base
    for poke in myTeam.active:
        move_cmd += 'moves '
        for move in poke.moves:
            move_cmd += move + ' '
        for i in range(4 - len(poke.moves)):
            move_cmd += poke.pred_moves[i] + ' '
        move_cmd += ', '
    move_cmd = move_cmd[:-2] + ' \n'
    
    proc_input.write(move_cmd)
    
    
    ability_cmd = base
    for poke in myTeam.active:
        if (poke.ability == ' ' or poke.ability == ''):
            ability_cmd += 'ability ' + poke.pred_ability
        else:
            ability_cmd += 'ability ' + poke.ability
        ability_cmd += ', '
    ability_cmd = ability_cmd[:-2] + ' \n'
    
    proc_input.write(ability_cmd)
    
    
    item_cmd = base
    for poke in myTeam.active:
        if (poke.item == ' ' or poke.item == ''):
            item_cmd += 'item ' + poke.pred_item
        else:
            item_cmd += 'item ' + poke.item
        item_cmd += ', '
    item_cmd = item_cmd[:-2] + ' \n'
    
    proc_input.write(item_cmd)
    
    
    status_cmd = base
    for poke in myTeam.active:
        status_cmd += 'status ' + pokemon.status
        status_cmd += ', '
    status_cmd = status_cmd[:-2] + ' \n'
    
    proc_input.write(status_cmd)
    
    
    for condition in myTeam.side_conditions:
        condition_cmd = base
        condition_cmd += 'sidecondition ' + condition + ' \n'
        proc_input.write(condition_cmd)



def teamToPack(myTeam):
    '''
        pokemon||item|ability|move1,move2,move3,move4|nature|evs||ivs||lvl|] 
        
        Reminder: remove aquare bracket if last
    '''
    stat_names = ['hp', 'atk', 'def', 'spa', 'spd', 'spe']
    
    packedFormat = ''
    
    for pokemon in myTeam.active:
        packedFormat += pokemonToPack(pokemon)
    
    for pokemon in myTeam.full:
        if not pokemon in myTeam.active:
            packedFormat += pokemonToPack(pokemon)
       
    packedFormat = packedFormat[:-1]
    
    return packedFormat



def pokemonToPack(pokemon):
    '''
        pokemon||item|ability|move1,move2,move3,move4|nature|evs||ivs||lvl|]
    '''
    
    stat_names = ['hp', 'atk', 'def', 'spa', 'spd', 'spe']
    
    packedFormat = pokemon.name + '||'
    
    if pokemon.item == '' or pokemon.item == ' ':
        packedFormat += pokemon.pred_item + '|'
    else:
        packedFormat += pokemon.item + '|'

    if pokemon.ability == '' or pokemon.ability == ' ':
        packedFormat += pokemon.pred_ability + '|'
    else:
        packedFormat += pokemon.ability + '|'

    for move in pokemon.moves:
        packedFormat += move + ','
    for i in range(4 - len(pokemon.moves)):
        packedFormat += pokemon.pred_moves[i] + ','
    packedFormat = packedFormat[:-1] + '|'

    packedFormat += pokemon.nature + '|'

    for stat in stat_names:
        packedFormat += str(pokemon.evs[stat]) + ','
    packedFormat = packedFormat[:-1] + '||'

    for stat in stat_names:
        packedFormat += str(pokemon.ivs[stat]) + ','
    packedFormat = packedFormat[:-1] + '||50|]'
    
    return packedFormat

def sim_wrapper(q, state, moves, i):
    q.put(sim(state, moves, i))

def sim(state, moves, i):

    proc = subprocess.Popen(shlex.split(showdown_cmd), 
                        stdout=subprocess.PIPE, 
                        stderr=subprocess.PIPE, 
                        stdin=subprocess.PIPE, 
                        bufsize=1, 
                        universal_newlines=True)

    proc.stdin.write('>start {"formatid":"vgc"}\n')

    team_one = '>player p1 {"name":"Alice","team":"'+ teamToPack(state.team1) + '"}\n'
    team_two = '>player p2 {"name":"Bobby","team":"'+ teamToPack(state.team2) + '"}\n'

    proc.stdin.write(team_one)
    proc.stdin.write(team_two)      

    # Select the first two since they are active
    
    proc.stdin.write('>p1 team 1234\n')
    proc.stdin.write('>p2 team 1234\n')

    # update to current state

    updateSide(proc.stdin, state.team1)
    updateSide(proc.stdin, state.team2)

    updateField(proc.stdin, state)

    # Run move

    for move in moves:
        proc.stdin.write(move[0])
        proc.stdin.write(move[1])
    
    newState = copy.deepcopy(state)
    exit_phase = '|turn|' + str(len(moves) + 1)
    
    # Temporary, save output to file
    
    f = open("outputs/thread" + str(i) + ".txt", "w")

    while True:

        for line in iter(proc.stdout.readline, ''):
            f.write(line)
#                 f.flush()

            # Parser here with update to state
            outputParser(line, newState)

            if (exit_phase in line):
                # Run heuristic here

                f.close()
                proc.kill()
                return (heuristic(state, newState))

            if ('|error|' in line):
                f.close()
                proc.kill()
                return ("Error", i)
                    

