import re

actualhp = re.compile(r"\|-damage\|p(?P<side>1|2)(?P<position>a|b):\ (?P<pokemon>.+)\|(?P<hp>[0-9]+)/(?P<maxhp>[0-9]+)", re.VERBOSE)
percenthp = re.compile(r"\|-damage\|p(?P<side>1|2)(?P<position>a|b):\ (?P<pokemon>.+)\|p(?P<hp>[0-9]+)/100", re.VERBOSE)
fnt = re.compile(r"\|-damage\|p(?P<side>1|2)(?P<position>a|b):\ (?P<pokemon>.+)\|0\ fnt", re.VERBOSE)
faint = re.compile(r"\|faint\|p(?P<side>1|2)(?P<position>a|b):\ (?P<pokemon>.+)", re.VERBOSE)
anim = re.compile(r"\|-anim\|p(?P<side>1|2)(?P<position>a|b):\ (?P<pokemon>[a-zA-Z\.\ \-\0-9’]+)\|(?P<move>[a-zA-Z0-9\ ]+)\|p(?P<targetside>1|2)(?P<targetpos>a|b):\ (?P<target>[a-zA-Z\.\ \-\0-9’]+)", re.VERBOSE)
move = re.compile(r"\|move\|p(?P<side>1|2)(?P<position>a|b):\ (?P<pokemon>.+)\|(?P<move>.+)\|p(?P<targetside>1|2)(?P<targetposition>a|b)?:\ (?P<target>.+)(\|\[notarget\])?", re.VERBOSE)
persistmove = re.compile(r"\|move\|p(?P<side>1|2)(?P<position>a|b):\ (?P<pokemon>.+)\|(?P<move>.+)\|\|\[still\]", re.VERBOSE)
supereffective = re.compile(r"\|-supereffective\|p(?P<side>1|2)(?P<position>a|b):\ (?P<pokemon>.+)", re.VERBOSE)
resist = re.compile(r"\|-resisted\|p(?P<side>1|2)(?P<position>a|b):\ (?P<pokemon>.+)", re.VERBOSE)
crit = re.compile(r"\|-crit\|p(?P<side>1|2)(?P<position>a|b):\ (?P<pokemon>.+)", re.VERBOSE)
miss = re.compile(r"\|-miss\|p(?P<side>1|2)(?P<position>a|b):\ (?P<pokemon>.+)\|p(?P<targetside>1|2)(?P<targetpos>a|b):\ (?P<targetpoke>.+)", re.VERBOSE)
immune = re.compile(r"\|-immune\|p(?P<side>1|2)(?P<position>a|b):\ (?P<pokemon>[a-zA-Z\.\ \-\0-9’]+)(\|.+)?", re.VERBOSE)
status = re.compile(r"\|-status\|p(?P<side>1|2)(?P<position>a|b):\ (?P<pokemon>[a-zA-Z\.\ \-\0-9’]+)\|(?P<status>[a-zA-Z0-9\ ]+)(.+)?", re.VERBOSE)
prepare = re.compile(r"\|-prepare\|p(?P<side>1|2)(?P<position>a|b):\ (?P<pokemon>.+)\|(?P<move>.+)", re.VERBOSE)
hitcount = re.compile(r"\|-hitcount\|p(?P<side>1|2)(?P<position>a|b)?:\ (?P<pokemon>.+)\|(?P<count>[0-9])", re.VERBOSE)

time = re.compile(r"\|t:\|(?P<time>[0-9]+)", re.VERBOSE)
turn = re.compile(r"\|turn\|(?P<turn>[0-9]+)", re.VERBOSE)
upkeep = re.compile(r"\|upkeep", re.VERBOSE)
starttext = re.compile(r"\|start", re.VERBOSE)
clearpoke = re.compile(r"\|clearpoke", re.VERBOSE)
gametype = re.compile(r"\|gametype\|(?P<mode>.+)", re.VERBOSE)
player = re.compile(r"\|player\|p(?P<side>1|2)\|(?P<name>.+)\|\|", re.VERBOSE)
teamsize = re.compile(r"\|teamsize\|p(?P<side>1|2)\|(?P<size>[1-6])", re.VERBOSE)
teampreview = re.compile(r"\|teampreview\|(?P<size>[1-6])", re.VERBOSE)

generation = re.compile(r"\|gen\|(?P<gen>[0-9])", re.VERBOSE)
gamemode = re.compile(r"\|tier\|\[Gen\ (?P<gen>[1-9])\](?P<mode>.+)", re.VERBOSE)
rule = re.compile(r"\|rule\|(?P<rule>.+):(?P<desc>.+)", re.VERBOSE)

activate = re.compile(r"\|-activate\|p(?P<side>1|2)(?P<position>a|b):\ (?P<pokemon>.+)\|(move:\ (?P<move>.+)(\|.+)?)?(ability:\ (?P<ability>.+)(\|.+)?)?", re.VERBOSE)
ability = re.compile(r"\|-ability\|p(?P<side>1|2)(?P<position>a|b):\ (?P<pokemon>[a-zA-Z\.\ \-\0-9’]*)\|(?P<ability>[a-zA-Z\.\ \-\’]+)(?P<boost>\|.*)?", re.VERBOSE)
switch = re.compile(r"\|switch\|p(?P<side>1|2)(?P<position>a|b):\ (?P<pokeout>.+)\|(?P<pokein>[a-zA-Z\.\ \-\’0-9\%]+)(,\ L(?P<level>[0-9]+))?(,\ (?P<gender>,*.*))?\|(?P<hp>[0-9]+)/(?P<maxhp>[0-9]+)", re.VERBOSE)
drag = re.compile(r"\|drag\|p(?P<side>1|2)(?P<position>a|b):\ (?P<pokeout>.+)\|(?P<pokein>[a-zA-Z\.\ \-’0-9\%]+)(,\ L(?P<level>[0-9]+))?(?P<gender>,*.*)?\|(?P<hp>[0-9]+)/(?P<maxhp>[0-9]+)", re.VERBOSE)
heal = re.compile(r"\|-heal\|p(?P<side>1|2)(?P<position>a|b):\ (?P<pokemon>.+)\|(?P<hp>[0-9]+)/(?P<maxhp>[0-9]+)(?P<burn>\ brn)?(?P<par>\ par)?(\|\[silent\])?(\|\[from\]\ item:\ (?P<item>.+))?", re.VERBOSE)
cure = re.compile(r"\|-curestatus\|p(?P<side>1|2)(?P<position>a|b):\ (?P<pokemon>[a-zA-Z\.\ \-\0-9’]+)\|(?P<status>[a-zA-Z0-9\ ]+)(\|.+)?", re.VERBOSE)
sethp = re.compile(r"\|-sethp\|p(?P<side>1|2)(?P<position>a|b):\ (?P<pokemon>.+)\|(?P<hp>[0-9]+)/(?P<maxhp>[0-9]+)(\|.+)?", re.VERBOSE)
swap = re.compile(r"\|swap\|p(?P<side>1|2)(?P<position>a|b):\ (?P<pokemon>.+)\|(?P<target>0|1)\|\[from\]\ move:\ Ally\ Switch", re.VERBOSE)
boost = re.compile(r"\|-boost\|p(?P<side>1|2)(?P<position>a|b):\ (?P<pokemon>.+)\|(?P<stat>.+)\|(?P<amount>[0-9])", re.VERBOSE)
unboost = re.compile(r"\|-unboost\|p(?P<side>1|2)(?P<position>a|b):\ (?P<pokemon>.+)\|(?P<stat>.+)\|(?P<amount>[0-9])", re.VERBOSE)
single = re.compile(r"\|-single(turn|move)\|p(?P<side>1|2)(?P<position>a|b):\ (?P<pokemon>[a-zA-Z\.\ \-\0-9’]+)\|(?P<protect>Protect|Max\ Guard)?(?P<destiny>Destiny\ Bond)?(?P<followme>move:\ Follow\ Me)?(Helping\ Hand\|\[of\]\ p2a:\ (?P<Helpinghand>[a-zA-Z\.\ \-\0-9’]+))?(move:\ (?P<move>[a-zA-Z0-9\ ]+))?", re.VERBOSE)
fail = re.compile(r"\|-fail\|p(?P<side>1|2)(?P<position>a|b):\ (?P<pokemon>[a-zA-Z\.\ \-\0-9’]+)(\|(?P<reason>.+))?", re.VERBOSE)
cant = re.compile(r"\|cant\|p(?P<side>1|2)(?P<position>a|b):\ (?P<pokemon>[a-zA-Z\.\ \-\0-9’]+)\|(?P<par>par)?(?P<slp>slp)?(?P<frz>frz)?(?P<flinch>flinch)?(?P<Tsareena>ability:\ Queenly\ Majesty.+)?(move:\ Taunt\|(?P<taunt>.+))?", re.VERBOSE)
hint = re.compile(r"\|-hint\|(?P<hint>.+)", re.VERBOSE)
win = re.compile(r"\|win\|(?P<name>.+)", re.VERBOSE)

start = re.compile(r"\|-start\|p(?P<side>1|2)(?P<position>a|b):\ (?P<pokemon>[a-zA-Z\.\ \-\0-9’]+)\|(?P<dynamax>Dynamax)?(Disable\|(?P<move_disable>[a-zA-Z0-9\ ]+)\|.+)?(typechange\|(?P<type>[a-zA-Z]+)\|.+)?(?P<conf>confusion)?(move:\ (?P<move>[a-zA-Z0-9\ ]+)(\|.+))?(ability:\ (?P<ability>.+))?((?P<ability_status>[a-zA-Z0-9\ ]+)(\|.+)?)?", re.VERBOSE)
end = re.compile(r"\|-end\|p(?P<side>1|2)(?P<position>a|b):\ (?P<pokemon>[a-zA-Z\.\ \-\0-9’]+)\|(?P<dynamax>Dynamax)?(Disable\|(?P<move_disable>[a-zA-Z0-9\ ]+)\|.+)?(typechange\|(?P<type>[a-zA-Z]+)\|.+)?(?P<conf>confusion)?(move:\ (?P<move>[a-zA-Z0-9\ ]+)(\|.+)?)?(ability:\ (?P<ability>[a-zA-Z0-9\ ]+)(\|.+)?)?((?P<ability_status>[a-zA-Z0-9\ ]+)(\|.+)?)?", re.VERBOSE)
fieldstart = re.compile(r"\|-fieldstart\|move:\ (?P<field>[a-zA-Z0-9\ ]+)(?P<extra>\|.+)?", re.VERBOSE)
fieldend = re.compile(r"\|-fieldend\|((move:\ )?(?P<field>[a-zA-Z0-9\ ]+))", re.VERBOSE)
sidestart = re.compile(r"\|-sidestart\|p(?P<side>1|2):\ (?P<player>.+)\|(move:\ )?(?P<move>.+)", re.VERBOSE)
sideend = re.compile(r"\|-sideend\|p(?P<side>1|2):\ (?P<player>[a-zA-Z\.\ \-\0-9’]+)\|(move:\ )?(?P<move>[a-zA-Z0-9\ \-]+)", re.VERBOSE)
weather = re.compile(r"\|-weather\|(?P<weather>[a-zA-Z0-9\ ]+)(\|.+)?", re.VERBOSE)

enditem = re.compile(r"\|-enditem\|p(?P<side>1|2)(?P<position>a|b):\ (?P<pokemon>[a-zA-Z\.\ \-\0-9’]+)\|(?P<item>[a-zA-Z0-9\ ]+)(\|.+)?", re.VERBOSE)
formechange = re.compile(r"\|-formechange\|p(?P<side>1|2)(?P<position>a|b):\ (?P<pokemon>[a-zA-Z\.\ \-\0-9’]+)\|(?P<newform>[a-zA-Z\.\ \-\0-9’]+)(\|.+)?", re.VERBOSE)
detailschange = re.compile(r"\|detailschange\|p(?P<side>1|2)(?P<position>a|b):\ (?P<pokemon>.+)\|(?P<newdetails>[a-zA-Z\.\ \-0-9]+)(.+)?", re.VERBOSE)
replace = re.compile(r"\|replace\|p(?P<side>1|2)(?P<position>a|b):\ (?P<pokemon>[a-zA-Z0-9\ ]+)\|(?P<poke>[a-zA-Z0-9\ ]+),(\|.+)?", re.VERBOSE)
transform = re.compile(r"\|-transform\|p(?P<side>1|2)(?P<position>a|b):\ (?P<pokemon>.+)\|p(?P<targetside>1|2)(?P<targetpos>a|b):\ (?P<target>[a-zA-Z\.\ \-\0-9’]+)(\|.+)?", re.VERBOSE)
clearallboost = re.compile(r"\|-clearallboost", re.VERBOSE)
clearnegativeboost = re.compile(r"\|-clearnegativeboost\|p(?P<side>1|2)(?P<position>a|b)?:\ (?P<pokemon>.+)\|\[silent\]", re.VERBOSE)
clearboost = re.compile(r"\|-clearboost\|p(?P<side>1|2)(?P<position>a|b)?:\ (?P<pokemon>.+)", re.VERBOSE)
setboost = re.compile(r"\|-setboost\|p(?P<side>1|2)(?P<position>a|b)?:\ (?P<pokemon>.+)\|(?P<stat>.+)\|(?P<amount>[0-9])(\|.+)", re.VERBOSE)
zbroken = re.compile(r"\|-zbroken\|p(?P<side>1|2)(?P<position>a|b)?:\ (?P<pokemon>.+)", re.VERBOSE)
block = re.compile(r"\|-block\|p(?P<side>1|2)(?P<position>a|b)?:\ (?P<pokemon>.+)\|ability:\ (?P<ability>.+)\|\[of\]\ p(?P<targetside>1|2)(?P<targetpos>a|b):\ (?P<target>.+)", re.VERBOSE)

poke = re.compile(r"\|poke\|p(?P<side>1|2)\|(?P<pokemon>[a-zA-Z\.\ -]+)(,\ L(?P<level>[0-9]+))?(,\ (?P<gender>F|M))?", re.VERBOSE)
item = re.compile(r"\|-item\|p(?P<side>1|2)(?P<position>a|b):\ (?P<pokemon>[a-zA-Z\.\ \-\0-9’]+)\|(?P<item>[a-zA-Z0-9\ ]+)(\|.+)?", re.VERBOSE)


def prin(arg):
    if False:
        print(arg)

def outputParser(text, newState):

    match = actualhp.match(text)
    if match != None:
        # This is actual HP amount
        # side, position, pokemon, hp, maxhp
        prin("actualhp")

        team = newState.team1
        if match.group('side') == '2':
            team = newState.team2

        pokemon = team.active[0]
        if match.group('position') == 'b':
            pokemon = team.active[1]

        pokemon.hp = int(match.group('hp'))

        return

    match = fnt.match(text)
    if match != None:
        # If the pokemon faints during a move
        # side, position, pokemon
        prin("fnt")

        team = newState.team1
        if match.group('side') == '2':
            team = newState.team2

        pokemon = team.active[0]
        if match.group('position') == 'b':
            pokemon = team.active[1]

        pokemon.hp = 0
        pokemon.faint = 'dead'

        return

    match = switch.match(text)
    if match != None:
        # The switching another pokemon in
        # side, position, pokeout, pokein, level, gender?, hp, maxhp
        prin("switch")

        team = newState.team1
        if match.group('side') == '2':
            team = newState.team2

        idx = -1
        for i in range(6):
            if team.full[i].name == match.group('pokein'):
                idx = i
                break

        if match.group('position') == 'a':
            team.active[0] = team.full[idx]
        else:
            team.active[1] = team.full[idx]

        return

    match = drag.match(text)
    if match != None:
        # The switching another pokemon in
        # side, position, pokeout, pokein, level, gender?, hp, maxhp
        prin("switch")

        team = newState.team1
        if match.group('side') == '2':
            team = newState.team2

        idx = -1
        for i in range(6):
            if team.full[i].name == match.group('pokein'):
                idx = i
                break

        if match.group('position') == 'a':
            team.active[0] = team.full[idx]
        else:
            team.active[1] = team.full[idx]

        return

    match = heal.match(text)
    if match != None:
        # Heals
        # side, position, pokemon, hp, maxhp, burn?, par?, item?
        prin("heal")

        team = newState.team1
        if match.group('side') == '2':
            team = newState.team2

        pokemon = team.active[0]
        if match.group('position') == 'b':
            pokemon = team.active[1]

        pokemon.hp = int(match.group('hp'))

        return

    match = boost.match(text)
    if match != None:
        # A boost to a pokemon
        # side, position, pokemon, stat, amount
        prin("boost")

        team = newState.team1
        if match.group('side') == '2':
            team = newState.team2

        pokemon = team.active[0]
        if match.group('position') == 'b':
            pokemon = team.active[1]

        stat = match.group('stat')
        amt = match.group('amount')

        pokemon.boosts[stat] += int(amt)

        return

    match = unboost.match(text)
    if match != None:
        # An unboost to a pokemon
        # side, position, pokemon, stat, amount
        prin("unboost")

        team = newState.team1
        if match.group('side') == '2':
            team = newState.team2

        pokemon = team.active[0]
        if match.group('position') == 'b':
            pokemon = team.active[1]

        stat = match.group('stat')
        amt = match.group('amount')

        pokemon.boosts[stat] -= int(amt)

        return

    match = swap.match(text)
    if match != None:
        # Pokemon swapping positions
        # side, position, pokemon, target
        prin("swap")

        team = newState.team1
        if match.group('side') == '2':
            team = newState.team2

        pokemon = team.active[0]
        team.active[0] = team.active[1]
        team.active[1] = pokemon

        return

    match = status.match(text)
    if match != None:
        # A status effect
        # side, position, pokemon, status
        prin("status")

        team = newState.team1
        if match.group('side') == '2':
            team = newState.team2

        pokemon = team.active[0]
        if match.group('position') == 'b':
            pokemon = team.active[1]

        condition = match.group('status')

        pokemon.status += condition

        return

    match = weather.match(text)
    if match != None:
        # A weather condition
        # weather
        prin("weather")

        condition = match.group('weather')

        newState.weather = condition

        return

    match = fieldstart.match(text)
    if match != None:
        # The start of a field condition
        # field, extra
        prin("fieldstart")

        field = match.group('field')
        newState.pseudoweather.append(field)

        return

    match = fieldend.match(text)
    if match != None:
        # The end of a field condition
        # field
        prin("fieldend")

        field = match.group('field')
        if field in newState.pseudoweather:
            newState.pseudoweather.remove(field)

        return

    match = sidestart.match(text)
    if match != None:
        # The start of a side condition
        # side, player, move
        prin("sidestart")

        team = newState.team1
        if match.group('side') == '2':
            team = newState.team2

        condition = match.group('move')
        team.side_conditions.append(condition)

        return

    match = sideend.match(text)
    if match != None:
        # The end of a side condition
        # side, player, move
        prin("sideend")

        team = newState.team1
        if match.group('side') == '2':
            team = newState.team2

        condition = match.group('move')
        if condition in team.side_conditions:
            team.side_conditions.remove(condition)

        return

    match = enditem.match(text)
    if match != None:
        # The end of an item
        # side, position, pokemon, item
        prin("enditem")

        team = newState.team1
        if match.group('side') == '2':
            team = newState.team2

        pokemon = team.active[0]
        if match.group('position') == 'b':
            pokemon = team.active[1]

        data = match.group('item')

        if pokemon.item == '':
            pokemon.pred_item = ''
        else:
            pokemon.item = ''

        return

    match = item.match(text)
    if match != None:
        # The start of an item
        # side, position, pokemon, item
        prin("item")

        team = newState.team1
        if match.group('side') == '2':
            team = newState.team2

        pokemon = team.active[0]
        if match.group('position') == 'b':
            pokemon = team.active[1]

        data = match.group('item')

        if pokemon.item == '':
            pokemon.pred_item = data
        else:
            pokemon.item = data


        return

    match = clearnegativeboost.match(text)
    if match != None:
        # Clearing all negative boost
        # side, position, pokemon
        prin("clearnegativeboost")


        team = newState.team1
        if match.group('side') == '2':
            team = newState.team2

        pokemon = team.active[0]
        if match.group('position') == 'b':
            pokemon = team.active[1]

        for stat, value in pokemon.boosts.items():
            if value < 0:
                pokemon.boosts[stat] = 0

        return

    match = clearboost.match(text)
    if match != None:
        # Clearing the boosts
        # side, position, pokemon
        prin("clearboost")


        team = newState.team1
        if match.group('side') == '2':
            team = newState.team2

        pokemon = team.active[0]
        if match.group('position') == 'b':
            pokemon = team.active[1]

        pokemon.boosts = {'atk':0,
                          'def':0,
                          'spa':0,
                          'spd':0,
                          'spe':0,
                          'accuracy': 0,
                          'evasion': 0};

        return

    match = setboost.match(text)
    if match != None:
        # Setting a boost
        # side, position, pokemon, stat, amount
        prin("setboost")

        team = newState.team1
        if match.group('side') == '2':
            team = newState.team2

        pokemon = team.active[0]
        if match.group('position') == 'b':
            pokemon = team.active[1]

        stat = match.group('stat')
        amt = match.group('amount')

        pokemon.boosts[stat] = amt

        return

    match = clearallboost.match(text)
    if match != None:
        # Clearing all boosts
        #
        prin("clearallboost")

        for poke in newState.team1.active:
            poke.boosts = {'atk':0,
                          'def':0,
                          'spa':0,
                          'spd':0,
                          'spe':0,
                          'accuracy': 0,
                          'evasion': 0};

        for poke in newState.team2.active:
            poke.boosts = {'atk':0,
                          'def':0,
                          'spa':0,
                          'spd':0,
                          'spe':0,
                          'accuracy': 0,
                          'evasion': 0};

        return

    match = cure.match(text)
    if match != None:
        # Curing a condition
        # side, position, pokemon, status
        prin("cure")

        team = newState.team1
        if match.group('side') == '2':
            team = newState.team2

        pokemon = team.active[0]
        if match.group('position') == 'b':
            pokemon = team.active[1]

        pokemon.status = ''

        return

    match = sethp.match(text)
    if match != None:
        # Set hp moves (ex. Pain split)
        # side, position, pokemon, hp, maxhp
        prin("sethp")

        team = newState.team1
        if match.group('side') == '2':
            team = newState.team2

        pokemon = team.active[0]
        if match.group('position') == 'b':
            pokemon = team.active[1]

        hp = match.group('hp')

        pokemon.hp = hp

        return

    return

    if percenthp.match(text) != None:
        # This is percent HP
        # side, position, pokemon, hp
        prin("percenthp")

        # No work needed

        return

    if time.match(text) != None:
        # The current time
        # time
        prin("time")

        # No work needed

        return

    if turn.match(text) != None:
        # The current turn
        # turn
        prin("turn")

        # No work needed

        return ''

    if upkeep.match(text) != None:
        # The upkeep text
        #
        prin("upkeep")

        # No work needed

        return

    if clearpoke.match(text) != None:
        # The clearpoke text
        #
        prin("clearpoke")

        # No work needed

        return

    if starttext.match(text) != None:
        # The start of match text
        #
        prin("clearpoke")

        # No work needed

        return

    if gametype.match(text) != None:
        # The type of game (singles/doubles)
        # mode
        prin("gametype")

        # No work needed

        return

    if player.match(text) != None:
        # Player side and nickname
        # side, name
        prin("player")

        # No work needed

        return

    if teampreview.match(text) != None:
        # The size of the team battling
        # side, size
        prin("teampreview")

        # No work needed

        return

    if poke.match(text) != None:
        # Pokemon with levels and gender
        # side, pokemon, level, gender
        prin("poke")

        # No work needed

        return

    if teamsize.match(text) != None:
        # The size of the team brought
        # side, size
        prin("teamsize")

        # No work needed

        return

    if generation.match(text) != None:
        # The generation of the battle
        # gen
        prin("generation")

        # No work needed

        return

    if gamemode.match(text) != None:
        # Generation and specific gamemode
        # gen, mode
        prin("gamemode")

        # No work needed

        return

    if rule.match(text) != None:
        # The rules
        # rule, desc
        prin("rule")

        # No work needed

        return

    if faint.match(text) != None:
        # If the pokemon faints after a move
        prin("faint")
        # side, position, pokemon

        # Handled in fnt

        return

    if ability.match(text) != None:
        # The revealing an ability (with a boost)
        # side, position, pokemon, ability, boost
        prin("ability")

        # No work needed

        return

    if move.match(text) != None:
        # The used move
        # side, position, pokemon, move, targetside, targetposition, target
        prin("move")

        # No work needed

        return

    if persistmove.match(text) != None:
        # A move with a lasting effect
        # side, position, pokemon, move
        prin("persistmove")

        # No work needed

        return

    if resist.match(text) != None:
        # If the pokemon resists a move
        # side, position, pokemon
        prin("resist")

        # No work needed

        return

    if supereffective.match(text) != None:
        # If the pokemon resists a move
        # side, position, pokemon
        prin("supereffective")

        # No work needed

        return

    if start.match(text) != None:
        # A start to an effect
        # side, position, pokemon, dynamax, move_disable, type, conf, ability, ability_status
        prin("start")

        # Todo: Will implement later

        return

    if end.match(text) != None:
        # An end to an effect
        # side, position, pokemon, dynamax, move_disable, type, conf, ability, ability_status
        prin("end")

        # Todo: Will implement later

        return

    if miss.match(text) != None:
        # A miss
        # side, position, pokemon, targetside, targetpos, targetpoke
        prin("miss")

        # No work needed

        return

    if cant.match(text) != None:
        # A failed move
        # side, position, pokemon, par, slp, frz, flinch, Tsareena, taunt
        prin("cant")

        # No work needed

        return

    if win.match(text) != None:
        # The win text
        # name
        prin("win")

        # Todo: Will implement later

        return

    if crit.match(text) != None:
        # A critical hit
        # side, position, pokemon
        prin("crit")

        # No work needed

        return

    if immune.match(text) != None:
        # Immunity from a move
        # side, position, pokemon
        prin("immune")

        # No work needed

        return

    if hint.match(text) != None:
        # A hint
        # side, position, pokemon
        prin("hint")

        # No work needed

        return

    if single.match(text) != None:
        # A single turn move or effect
        # side, position, pokemon, protect, destiny, followme, helpinghand, move
        prin("single")

        # No work needed

        return

    if fail.match(text) != None:
        # A failed move
        # side, position, pokemon, reason
        prin("fail")

        # No work needed

        return

    if activate.match(text) != None:
        # Activating an effect
        # side, position, pokemon
        prin("activate")

        # No work needed

        return

    if hitcount.match(text) != None:
        # The number of hits of multi-hit move
        # side, position, pokemon, count
        prin("hitcount")

        # No work needed

        return

    if formechange.match(text) != None:
        # Changing forms
        # side, position, pokemon, newform
        prin("formechange")

        # No work needed

        return

    if prepare.match(text) != None:
        # Preparing a two turn move
        # side, position, pokemon, move
        prin("prepare")

        # No work needed

        return

    if anim.match(text) != None:
        # Casting a two turn move
        # side, position, pokemon, move, targetside, targetpos, target
        prin("anim")

        # No work needed

        return

    if replace.match(text) != None:
        # Revealing Zoroak?
        # side, position, pokemon, poke
        prin("replace")

        # No work needed

        return

    if transform.match(text) != None:
        # Transforming into another pokemon
        # side, position, pokemon, targetside, targetpos, target
        prin("transform")

        # Todo: Implement later

        return

    if detailschange.match(text) != None:
        # Changing forms
        # side, position, pokemon, newdetails
        prin("detailschange")

        # No work needed

        return

    if zbroken.match(text) != None:
        # Z move through protect
        # side, position, pokemon
        prin("zbroken")

        # No work needed

        return

    if block.match(text) != None:
        # Blocking a move
        # side, position, pokemon, ability, targetside, targetpos, target
        prin("block")

        # No work needed

        return

    if text == '|\n':
        return
