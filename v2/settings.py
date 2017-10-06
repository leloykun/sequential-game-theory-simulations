NEARBY = [(0, -1), (1, 0), (0, 1), (-1, 0), (0, 0)]
NEIGHBOUR_SYNONYMS = ('neighbours', 'neighbors', 'neighbour', 'neighbor')
COLOR_CODE = ['#332532', '#644D52', '#F77A52', '#FF974F', '#A49A87']

ID = 0
RESOURCE_COUNT = 5
MAX_RES_AMOUNT = 100
DEF_GROWTH_RATE = [0.02 for _ in range(RESOURCE_COUNT)]  # 0.05
TO_UPDATE_CELLS = True
TO_COLOR_CELLS = True

AGENT_COUNT_INIT = 5
AGENT_COUNT_LIM = 100
AGENTS_CAN_TRADE = True
AGENTS_CAN_DIE = True
AGENTS_CAN_REPRODUCE = True

ENDOWMENT = 100
DEF_RES_INTAKE = 15
AGENTS_CAN_REPRODUCE = 15
MATING_THRESHOLD = 10 * ENDOWMENT

DEF_SKILLS = 1.00  # 0.75
TO_RANDOMIZE_SKILLS = False
IMPROVE_RATE = 1.00

DEF_TEMP = 5

TO_SIMULATE_SEASONS = True
TO_DISPLAY_WORLD = True
TO_DISPLAY_AVE_POS = True
LEN_TRAINING_AGE = 10000

OUTPUT_LOCATION = "tests/test/"
MAP = '../worlds/smallbox3.txt'
FILENAMES = [
    'std_out', 'resEnt', 'ineqGini', 'resOfAgents', 'specsOfAgents',
    'numberOfAgents', 'trading', 'avePos', 'netRes'
]
OUTPUT_TYPE = 1
