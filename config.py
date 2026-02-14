# Категории уравнений для тестов

VERY_QUICK = [
    'quadfor2', 'sparse5', 'hunecke', 'solotarev', 'chandra4', 'quadgrid', 'lorentz',
    'liu', 'hemmecke', 'boon', 'chandra5', 'caprasse', 'issac97', 'hcyclic5',
    'redcyc5', 'cyclic5', 'extcyc4', 'chemequ', 'uteshev_bikker', 'chandra6', 'geneig'
]

QUICK = [
    'chemequs', 'vermeer', 'camera1s', 'reimer4', 'redeco7', 'tangents', 'cassou',
    'butcher', 'eco7', 'cohn2', 'dessin1', 'des18_3', 'hcyclic6', 'noon5',
    'katsura6', 'cyclic6', 'butcher8', 'redcyc6', 'cpdm5', 'extcyc5'
]

MEDIUM = ['noon6', 'reimer5', 'kotsireas', 'assur44']

TOO_LONG = [
    'reimer8', 'reimer7', 'redeco12', 'redcyc8', 'redcyc7', 'noon9', 'noon8', 'mckay',
    'mckay.gls50mod', 'katsura10', 'ilias13', 'ilias12', 'ilias_k_2', 'ilias_k_3',
    'hf855', 'hcyclic8', 'hcyclic7', 'hawes4', 'hairer4'
]

# Соответствие порядков для разных библиотек
ORDER_MAPPING = {
    'ginv': {
        'deglex': 'TOPdeglex',     # grlex
        'lex': 'TOPlex'
    },
    'sympy': {
        'deglex': 'grlex',
        'lex': 'lex'
    }
}

# Директории по умолчанию
JSON_DIR = 'json-benchmarks'
RESULTS_DIR = 'results'