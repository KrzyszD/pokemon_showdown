import requests
import re
from pokemon import pokemon

url = 'https://www.pikalytics.com/pokedex/ss/{poke_name}'

nature_changes = {'Adamant':['atk','spa'],
#                   'Bashful':['spa','spa'],
                  'Bold':['def','atk'],
                  'Brave':['atk','spe'],
                  'Calm':['spd','atk'],
                  'Careful':['spd','spa'],
#                   'Docile':['def','def'],
                  'Gentle':['spd','def'],
#                   'Hardy':['atk','atk'],
                  'Hasty':['spe','def'],
                  'Impish':['def','spa'],
                  'Jolly':['spe','spa'],
                  'Lax':['def','spd'],
                  'Lonely':['atk','def'],
                  'Mild':['spa','def'],
                  'Modest':['spa','atk'],
                  'Naive':['spe','spd'],
                  'Naughty':['atk','spd'],
                  'Quiet':['spa','spe'],
#                   'Quirky':['spd','spd'],
                  'Rash':['spa','spd'],
                  'Relaxed':['def','spe'],
                  'Sassy':['spd','spe'],
#                   'Serious':['spe','spe'],
                  'Timid':['spe','atk']}



def getPikalytics(pokename, num_moves=4, num_items=1, num_abilities=1, num_natures=1):
    
    type_entry = re.compile('<span class="type (?P<type>[a-zA-Z]+)">[a-zA-Z]+</span>')

    stat_entry = re.compile('</div>\n\s+</span>\n\s+<div style="display:inline-block;vertical-align: middle;margin-left: 20px;">(?P<stat>[0-9]{1,3})</div>')
    
    move_entry = re.compile('<div class="pokedex-move-entry-new">\n\s+<div style="margin-left:10px;display:inline-block;">(?P<move>.+)</div>\n\s+<div style="display:inline-block;color:#333;">')

    item_entry = re.compile('</div>\n\s+</div>\n\s+<div style="display:inline-block;">(?P<item>.+)</div>')

    ability_entry = re.compile('<div class="pokedex-move-entry-new">\n\s+<div style="margin-left:10px;display:inline-block;">(?P<ability>.+)</div>\n\s+<div style="display:inline-block;float:right;">')

    nature_entry = re.compile('<div style="margin-left:10px;display:inline-block;">(?P<nature>.*)</div>')

    ev_entry = re.compile('<div style="display:inline-block;">(?P<ev>[0-9]{1,4})/?</div>')

    
 
    moves_wrapper = re.compile('<div id="moves_wrapper">')
    item_wrapper = re.compile('<div id="items_wrapper">')
    abilities_wrapper = re.compile('<div id="abilities_wrapper">')
    nature_wrapper = re.compile('<div id="dex_spreads_wrapper" style="">')
    
    
    
    text = requests.get(url.format(poke_name=pokename)).text
    
    stat_names = ['hp', 'atk', 'def', 'spa', 'spd', 'spe']
    stats = {}
    typing = []
    moves = []
    items = []
    abilities = []
    nature = []

    for i in range(2):
        match = re.search(type_entry, text) 
        if (match == None):
            break;
        typing.append(match.group(1))
        text = text[match.span()[1]:]
        if (text[:7] == '</span>'):
            break
    
    for i in range(6):
        match = re.search(stat_entry, text) 
        if (match == None):
            break;
        stats[stat_names[i]] = int(match.group(1))
        text = text[match.span()[1]:]
    
    res = re.search(moves_wrapper, text)
    text = text[res.span()[1]:]

    for i in range(num_moves):
        match = re.search(move_entry, text)
        if (match == None):
            break;
        elif (match.group(1) == 'Other'):
            break
        moves.append(match.group(1))
        text = text[match.span()[1]:]

    res = re.search(item_wrapper, text)
    text = text[res.span()[1]:]
    

    for i in range(num_items):
        match = re.search(item_entry, text)
        if (match == None):
            break;
        elif (match.group(1) == 'Other'):
            break
        items.append(match.group(1))
        text = text[match.span()[1]:]

    res = re.search(abilities_wrapper, text)
    text = text[res.span()[1]:]
    

    for i in range(num_abilities):
        match = re.search(ability_entry, text)
        if (match == None):
            break;
        elif (match.group(1) == '{{nature}}'):
            break
        abilities.append(match.group(1))
        text = text[match.span()[1]:]

    res = re.search(nature_wrapper, text)
    text = text[res.span()[1]:]
    

    for i in range(num_natures):
        obj = {}
        match = re.search(nature_entry, text)
        if (match == None):
            break
        elif (match.group(1) == '{{move}}'):
            break
        obj['nature'] = match.group(1)
        text = text[match.span()[1]:]
        
        for j in range(6):
            match = re.search(ev_entry, text)
            if (match == None):
                break;
            obj[stat_names[j]] = int(match.group(1))
            text = text[match.span()[1]:]
        
        nature.append(obj)
    
    return stats, moves, items, abilities, nature, typing

def calcStats(pokemon, pika_stats, lvl=50):
    # atk, def, spa, spd, spe = floor( ( 2 * base + iv + floor(ev / 4) ) * lvl / 100 ) + 5
    # hp                      = floor( ( 2 * base + iv + floor(ev / 4) ) * lvl / 100 ) + 10 + lvl
    
    stat_names = ['atk', 'def', 'spa', 'spd', 'spe']
    
    base_stats = pika_stats[0]
    evs = pika_stats[4]
    
    for stat in stat_names:
        pokemon.stats[stat] = (2 * base_stats[stat] + 31 + evs[0][stat] // 4) * lvl // 100 + 5
        pokemon.evs[stat] = evs[0][stat]
    
    pokemon.stats['hp'] = (2 * base_stats['hp'] + 31 + evs[0]['hp'] // 4) * lvl // 100 + lvl + 10
    pokemon.hp = pokemon.stats['hp']
    pokemon.evs['hp'] = evs[0]['hp']
    
    if evs[0]['nature'] in nature_changes:
        benefial = nature_changes[evs[0]['nature']][0]
        stunted = nature_changes[evs[0]['nature']][1]
        
        pokemon.stats[ benefial ] *= 1.1
        pokemon.stats[ stunted ] *= 0.9
        
        pokemon.stats[ benefial ] = int(pokemon.stats[ benefial ])
        pokemon.stats[ stunted ] = int(pokemon.stats[ stunted ])
        
    pokemon.nature = evs[0]['nature']
        
def updatePred(pokemon, pika_stats):
    
    moves = pika_stats[1]
    items = pika_stats[2]
    abilities = pika_stats[3]
    
    pokemon.pred_moves = []
    for i in range(4 - len(pokemon.moves)):
        pokemon.pred_moves.append(moves[i].replace(' ', ''))
    
    if pokemon.ability == '':
        pokemon.pred_ability = abilities[0].replace(' ', '')
        
    if pokemon.item == '':
        pokemon.pred_item = items[0].replace(' ', '')
        
    pokemon.typing = pika_stats[5]

def createPikalyticsPokemon(pokename):
    poke = pokemon(pokename)
    poke_stats = getPikalytics(pokename)
    
    calcStats(poke, poke_stats)
    updatePred(poke, poke_stats)
    
    return poke
