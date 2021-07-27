class pokemon:
    
    name = ''
    
    ability = ''
    pred_ability = ''
    
    item = ''
    pred_item = ''
    
    moves = []
    pred_moves = []
    max_moves = []
    
    nature = ''
    status = ''
    
    typing = []
    
    faint = 'alive'
    first_turn = True
    protected = False
    
    def __init__(self, pokename):
        self.name = pokename
        self.hp = 100  # Current hp
        
        self.stats = {'hp':100,  # Max HP
                     'atk':101,
                     'def':102,
                     'spa':103,
                     'spd':104,
                     'spe':105}
        
        self.evs = {'hp':0,  
                   'atk':0,
                   'def':0,
                   'spa':0,
                   'spd':0,
                   'spe':0}
        
        self.ivs = {'hp':31,  
                   'atk':31,
                   'def':31,
                   'spa':31,
                   'spd':31,
                   'spe':31}
        
        self.boosts = {'atk':0,
                      'def':0,
                      'spa':0,
                      'spd':0,
                      'spe':0,
                      'accuracy': 0, 
                      'evasion': 0};

class team:
    
    def __init__(self):
        self.side = ''                # p1, p2
        self.full = []                # all six pokemon
        self.active = []              # p1a, p1b  /   p2a, p2b
        self.side_conditions = []     # lightscreen, etc
        
class state:
    
    def __init__(self):
        self.team1 = ''
        self.team2 = ''
        self.weather = 'clear'
        self.pseudoweather = []
        self.terrain = ''
    
        