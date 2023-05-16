
import random


class Grammar:
    def __init__(self):
      #define the non-terminal symbols
        self.VN = {'S', 'A', 'B'}
      #define the terminal symbols
        self.VT = {'a', 'b', 'c', 'd'}
      #define the productions
        self.P = {
            'S': ['bA', 'BC'],
            'A': ['a', 'aS', 'bCaCa'],
            'B': ['A', 'bS', 'bCAa'],
            'C': ['AB', 'aS', 'bCaCa', ''],
            'D': ['AB']
        }
        #define the start symbol
        self.start = 'S'

    #method to generate n number of strings according to given the rules
    def generate_strings(self, n=5):
        strings = []
        for i in range(n):
            string = ''
            stack = [self.start]
            while stack:
                symbol = stack.pop()
                if symbol in self.VT:
                    string += symbol
                elif symbol in self.VN:
                    productions = self.P[symbol]
                    production = random.choice(productions)
                    for s in reversed(production):
                        stack.append(s)
            strings.append(string)
        return strings

# Chomsky classification to identify the type of the grammar
    def chomsky_classifier(self):
        type1 = True
        type2 = True
        type3_right = True
        type3_left = True

        for rule in self.P.keys():
            if len(self.P) != 1:
                type2 = False
                break

            if all(len(p) < 1 for p in self.P):
                type1 = False
                break
                
        for i in self.VN:
            for production in self.P[i]:
                if (len(self.P) == 2 and self.P[1] not in self.VN and
                    self.P[0] not in self.VT) or len(self.P) > 2:
                    type3_right = False
                    break

                if (len(self.P) == 1 and self.P[0] not in self.VT) or (len(self.P) == 2 and self.P[0] not in self.VN) or len(self.P) > 2:
                    type3_left = False
                    break

                if any(len(lst) > 2 for lst in self.P) or any(len(lst) == 0 for lst in self.P):
                    type2 = False
                    break

                if len(self.P) == 0:
                    type1 = False
                    break

        if type3_right:
            return 'Type 3: Right linear regular grammar'
        elif type3_left:
            return 'Type 3: Left linear regular grammar'
        elif type2:
            return 'Type 2: Context-free grammar'
        elif type1:
            return 'Type 1: context-sensitive grammar'
        else:
            return 'Type 0: unrestrictive grammar'


    def new_starter(self):
            for i in self.P:
                for j in self.P[i]:
                    for k in j: 
                        if self.start == k:
                            self.P['0'] = self.start
                            self.starter_symbol = '0'
                            return
            

    def remove_nonsolitary(self, nonterminal):
            visited = []  
            queue = []

            queue.append('S')
            visited.append('S')
            
            while queue:
                m = queue.pop(0)
                for neighbour in self.P[m]:
                    for letter in neighbour:
                        if letter in nonterminal:
                            if letter not in visited:
                                visited.append(letter)
                                queue.append(letter)

            for i in list(self.P):
                if i not in visited:
                    del self.P[i]   

    def remove_epsilon(self):
            nullable = []
            for i in self.P:
                for j in self.P[i]:
                    if j == '':
                        nullable.append(i)
                        self.P[i].remove(j)
            
            for i in self.P:
                for j in self.P[i]:
                    for k in j:
                        if k in nullable:
                            self.P[i].append(j[:j.rfind(k)])
                            

    def remove_units(self, nonterminal):
            g = {}
            for i in self.P:
                for j in self.P[i]:
                    g_keys = []
                    guf_keys = []

                    if len(j) == 1 and j in nonterminal:
                        g_keys.append(j)
                        self.P[i].remove(j)
                    else:
                        guf_keys.append(j)

                if g_keys:
                    g[i] = g_keys

            for i in g:
                for j in g[i]:
                    temp = self.P[i] + self.P[j]
                    self.P[i] = temp

    def remove_other(self, terminal, upper_alphabet):
            new_rules = {}
            for i in terminal:
                new_key = random.choice(upper_alphabet)
                upper_alphabet.remove(new_key)
                self.P[new_key] = [i]
                new_rules[i] = new_key
            remove_dict = {}

            for i in self.P:
                remove_list = []
                for j in self.P[i]:
                    if len(j)>1:
                        for k in j:
                            if k in terminal:
                                new_str = j[:j.find(k)] + new_rules[k] +j[j.find(k)+1]
                                self.P[i].append(new_str)
                                remove_dict[i] = []
                                remove_list.append(j)
                remove_dict[i] = remove_list

            for i in remove_dict:
                for j in remove_dict[i]:
                    if j in self.rules[i]:
                        self.rules[i].remove(j)



                    
    def to_cnf(self):
            self.new_starter()
            nonterminal = []
            for i in self.P:
                nonterminal.append(i)

            self.remove_nonsolitary(nonterminal)

            self.remove_epsilon()

            self.remove_units(nonterminal)

            terminal = set()
            for i in self.P:
                for j in self.P[i]:
                    for k in j:
                        if ord(k) <= ord('z') and ord(k) >= ord('a'):
                            terminal.add(k)

            upper_alphabet = []
            for i in range(ord('A'), ord('Z')):
                upper_alphabet.append(chr(i))

            for i in nonterminal[:]:
                if i in upper_alphabet:
                    upper_alphabet.remove(i)

            self.remove_other(terminal, upper_alphabet)
            self.print_steps()



grammar = Grammar()
grammar.to_cnf()

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

fa = FiniteAutomaton()
grammar_to_finite_automaton(g)
string = g.generate_strings()
for x in range(5):
  print(accepts(fa, string[x]))

class Conversion:
    def __init__(self, Q, sigma, delta, q0, F):
        self.Q = Q
        self.sigma = sigma
        self.delta = delta
        self.q0 = q0
        self.F = F

    def is_deterministic(self):
        if not self.Q or not self.sigma:
            return False

        for i in self.Q:
            for j in self.sigma:
                if (i, j) not in self.delta or self.delta[(i, j)] not in self.Q:
                    return False

        if self.q0 not in self.Q:
            return False

        if not set(self.F).issubset(set(self.Q)):
            return False
        return True

    def convert_to_dfa(self):
        if self.is_deterministic():
            return self

        dfa_states = set()
        dfa_accept_states = set()
        dfa_transitions = dict()
        state_queue = [frozenset([self.q0])]
        while state_queue:
            current_states = state_queue.pop(0)
            dfa_states.add(current_states)
            if any(state in self.F for state in current_states):
                dfa_accept_states.add(current_states)
            for symbol in self.sigma:
                next_states = set()
                for state in current_states:
                    next_states |= set(self.delta.get((state, symbol), set()))
                if next_states:
                    next_states = frozenset(next_states)
                    dfa_transitions[(current_states, symbol)] = next_states
                    if next_states not in dfa_states:
                        state_queue.append(next_states)

        dfa = Conversion(dfa_states, self.sigma, dfa_transitions, self.q0, dfa_accept_states)
        return dfa

    def convert_to_grammar(self):
        productions = dict()
        for state in self.Q:
            for symbol in self.sigma:
                next_states = self.delta.get((state, symbol), set())
                for next_state in next_states:
                    if next_state in self.F:
                        if state not in productions:
                            productions[state] = set()
                        productions[state].add(symbol)
                    else:
                        if next_state not in productions:
                            productions[next_state] = set()
                        productions[next_state].add(symbol + ' ' + state)
        start_symbol = self.q0
        if start_symbol in productions:
            productions['S'] = productions[start_symbol]
            del productions[start_symbol]
            for state in self.Q:
                for symbol in self.sigma:
                    next_states = self.delta.get((state, symbol), set())
                    for next_state in next_states:
                        if state in productions and symbol + state in productions[state]:
                            if next_state not in productions:
                                productions[next_state] = set()
                            productions[next_state].add(symbol + ' S')
        else:
            start_symbol = 'S'
            productions[start_symbol] = set()
            for accept_state in self.F:
                productions[start_symbol].add('eps' + accept_state)

        return start_symbol, productions

Q = {'q0', 'q1', 'q2', 'q3'}
sigma = {'a', 'b'}
delta =  {
        ('q0', 'a'): {'q0', 'q1'},
        ('q1', 'a'): {'q2'},
        ('q1', 'b'): {'q1'},
        ('q2', 'a'): {'q3'},
        ('q3', 'a'): {'q1'}
        }
q0 = 'q2'
F = {'q3'}
convesion = Conversion(Q, sigma, delta, q0, F)
print("Is this Automaton deterministic? ", convesion.is_deterministic())
dfa = convesion.convert_to_dfa()
print("States: ", dfa.Q)
print("Transition function: ", dfa.delta)
print("Initial state: ", dfa.q0)
print("Final states: ", dfa.F)

grammar = convesion.convert_to_grammar()
print("Regular grammar productions: ", grammar)

import copy
import random

class Grammar:

    
    def __init__(self, rules):
        self.rules = rules
        self.is_cnf = False
        self.starter_symbol = 'S'

    def check_string(self, string):
        for i in range (len(string)):
            if string[i] in self.rules.keys():
                return "false"
        return "true"
    
    def generate_string(self):
        new_str = self.starter_symbol

        j = len(new_str) - 1
        while (self.check_string(new_str) == "false"):
            if new_str[j] in self.rules.keys():
                new_str = new_str[0:j] + random.choice(self.rules[new_str[j]])
                j = len(new_str) - 1
        return new_str
    
    def new_start(self):
        for i in self.P:
            for j in self.P[i]:
                for k in j: 
                    if self.start_symbol == k:
                        self.P['0'] = self.start_symbol
                        self.start_symbol = '0'
                        return
        

    def remove_nonsolitary(self, nonterminal):
        visited = []  
        queue = []

        queue.append('S')
        visited.append('S')
        
        while queue:
            m = queue.pop(0)
            for neighbour in self.P[m]:
                for letter in neighbour:
                    if letter in nonterminal:
                        if letter not in visited:
                            visited.append(letter)
                            queue.append(letter)

        for i in list(self.P):
            if i not in visited:
                del self.P[i]    

    def remove_epsilon(self):
        nullable = []
        for i in self.P:
            for j in self.P[i]:
                if j == '':
                    nullable.append(i)
                    self.P[i].remove(j)
        
        for i in self.P:
            for j in self.P[i]:
                for k in j:
                    if k in nullable:
                        self.P[i].append(j[:j.rfind(k)])
                        

    def remove_units(self, nonterminal):
        g = {}
        for i in self.rules:
            for j in self.rules[i]:
                g_keys = []
                guf_keys = []

                if len(j) == 1 and j in nonterminal:
                    g_keys.append(j)
                    self.rules[i].remove(j)
                else:
                    guf_keys.append(j)

            if g_keys:
                g[i] = g_keys

        for i in g:
            for j in g[i]:
                temp = self.rules[i] + self.rules[j]
                self.rules[i] = temp

    def remove_other(self, terminal, upper_alphabet):
        new_rules = {}
        for i in terminal:
            new_key = random.choice(upper_alphabet)
            upper_alphabet.remove(new_key)
            self.P[new_key] = [i]
            new_rules[i] = new_key
        remove_dict = {}

        for i in self.P:
            remove_list = []
            for j in self.P[i]:
                if len(j)>1:
                    for k in j:
                        if k in terminal:
                            new_str = j[:j.find(k)] + new_rules[k] +j[j.find(k)+1]
                            self.P[i].append(new_str)
                            remove_dict[i] = []
                            remove_list.append(j)
            remove_dict[i] = remove_list

        for i in remove_dict:
            for j in remove_dict[i]:
                if j in self.P[i]:
                    self.P[i].remove(j)


    def print_steps(self):
        for i in self.rules:
            for j in self.rules[i]:
                print(i, " -> ", j)
                
    def to_cnf(self):
        self.new_start()
        print("Add a new starting nonterminal")
        self.print_steps()
        nonterminal = []
        for i in self.rules:
            nonterminal.append(i)

        self.remove_nonsolitary(nonterminal)
        print("Removed the unreachable nonterminals")
        self.print_steps()
        self.remove_epsilon()
        print("Removed the epsilon producitons")
        self.print_steps()
        # remove unit productions
        self.remove_units(nonterminal)
        print("Removed the unit productions")
        self.print_steps()
        # step3
        terminal = set()
        for i in self.rules:
            for j in self.rules[i]:
                for k in j:
                    if ord(k) <= ord('z') and ord(k) >= ord('a'):
                        terminal.add(k)

        upper_alphabet = []
        for i in range(ord('A'), ord('Z')):
            upper_alphabet.append(chr(i))

        for i in nonterminal[:]:
            if i in upper_alphabet:
                upper_alphabet.remove(i)

        self.remove_other(terminal, upper_alphabet)