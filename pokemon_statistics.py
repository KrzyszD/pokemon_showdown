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
    
    stat_entry_term = '</div>\n                    </span>\n                    <div style="display:inline-block;vertical-align: middle;margin-left: 20px;">.*</div>'
    stat_entry = re.compile(stat_entry_term)
    
    move_entry_term = '<div class="pokedex-move-entry-new">\n                  <div style="margin-left:10px;display:inline-block;">.*</div>\n                  <div style="display:inline-block;color:#333;">'
    move_entry = re.compile(move_entry_term)

    item_entry_term = '</div>\n                  </div>\n                  <div style="display:inline-block;">.*</div>'
    item_entry = re.compile(item_entry_term)
   
    ability_entry_term = '<div class="pokedex-move-entry-new">\n                  <div style="margin-left:10px;display:inline-block;">.*</div>\n                    <div style="display:inline-block;float:right;">'
    ability_entry = re.compile(ability_entry_term)
   
    nature_entry_term = '<div style="margin-left:10px;display:inline-block;">.*</div>'
    nature_entry = re.compile(nature_entry_term)
    
    ev_entry_term = '<div style="display:inline-block;">.{1,4}</div>'
    ev_entry = re.compile(ev_entry_term)

    
 
    moves_wrapper_term = '<div id="moves_wrapper">'
    moves_wrapper = re.compile(moves_wrapper_term)

    item_wrapper_term = '<div id="items_wrapper">'
    item_wrapper = re.compile(item_wrapper_term)

    abilities_wrapper_term = '<div id="abilities_wrapper">'
    abilities_wrapper = re.compile(abilities_wrapper_term)

    nature_wrapper_term = '<div id="dex_spreads_wrapper" style="">'
    nature_wrapper = re.compile(nature_wrapper_term)
    
    
    
    text = requests.get(url.format(poke_name=pokename)).text
    
    stat_names = ['hp', 'atk', 'def', 'spa', 'spd', 'spe']
    stats = {}
    moves = []
    items = []
    abilities = []
    nature = []

    i = 0
    while (i < 6):
        res = re.search(stat_entry, text)
        if (res == None):
            break;
        stats[stat_names[i]] = int(text[res.span()[0]:res.span()[1]][131:-6])
        text = text[res.span()[1]:]
        i += 1
    
    res = re.search(moves_wrapper, text)
    text = text[res.span()[1]:]

    i = 0
    while (i < num_moves):
        i += 1
        res = re.search(move_entry, text)
        if (res == None):
            break;
        elif (text[res.span()[0]:res.span()[1]][107:-71] == 'Other'):
            break
        moves.append(text[res.span()[0]:res.span()[1]][107:-71])
        text = text[res.span()[1]:]

    res = re.search(item_wrapper, text)
    text = text[res.span()[1]:]
    

    i = 0
    while (i < num_items):
        i += 1
        res = re.search(item_entry, text)
        if (res == None):
            break;
        elif (text[res.span()[0]:res.span()[1]][85:-6] == 'Other'):
            break
        items.append(text[res.span()[0]:res.span()[1]][85:-6])
        text = text[res.span()[1]:]

    res = re.search(abilities_wrapper, text)
    text = text[res.span()[1]:]
    

    i = 0
    while (i < num_abilities):
        i += 1
        res = re.search(ability_entry, text)
        if (res == None):
            break;
        abilities.append(text[res.span()[0]:res.span()[1]][107:-74])
        text = text[res.span()[1]:]

    res = re.search(nature_wrapper, text)
    text = text[res.span()[1]:]
    

    i = 0
    while (i < num_natures):
        i += 1
        obj = {}
        res = re.search(nature_entry, text)
        if (res == None):
            break
        elif ("{{move}}" in text[res.span()[0]:res.span()[1]][52:-6]):
            break
        obj['nature'] = text[res.span()[0]:res.span()[1]][52:-6]
        text = text[res.span()[1]:]
        
        j = 0
        while (j < 6):
            res = re.search(ev_entry, text)
            if (res == None):
                break;
            obj[stat_names[j]] = int(text[res.span()[0]:res.span()[1]][35:-6].replace("/", ""))
            text = text[res.span()[1]:]
            j += 1
        
        nature.append(obj)
    
    return stats, moves, items, abilities, nature

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

def createPikalyticsPokemon(pokename):
    poke = pokemon(pokename)
    poke_stats = getPikalytics(pokename)
    
    calcStats(poke, poke_stats)
    updatePred(poke, poke_stats)
    
    return poke
