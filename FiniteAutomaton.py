class FiniteAutomaton:
    def __init__(self):
        self.states = set()
        self.alphabet = set()
        self.transitions = {}
        self.start_state = None
        self.final_states = set()

def grammar_to_finite_automaton(grammar):
    fa = FiniteAutomaton()
    fa.states.add('q0')
    fa.start_state = 'q0'
    for symbol in grammar.VT:
        fa.alphabet.add(symbol)
    for variable in grammar.VN:
        for production in grammar.P[variable]:
            source_state = 'q' + str(hash(production))
            fa.states.add(source_state)
            if variable == grammar.start:
                fa.transitions[(fa.start_state, '')] = source_state
            for i in range(len(production)):
                if production[i] in grammar.VT:
                    fa.transitions[(source_state, production[i])] = 'q' + str(hash(production[:i] + '.' + production[i+1:]))
            if production[-1] in grammar.VN:
                fa.final_states.add(source_state)
    return fa

def accepts(fa, input_string):
    current_state = fa.start_state
    for symbol in input_string:
        if (current_state, symbol) in fa.transitions:
            current_state = fa.transitions[(current_state, symbol)]
        else:
            return False
    return current_state in fa.final_states