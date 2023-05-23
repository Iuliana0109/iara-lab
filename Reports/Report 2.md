# The title of the work

### Course: Formal Languages & Finite Automata
### Author: Iuliana Stețenco

----

## Theory
A mathematical model of computation is known as a finite automaton. It is an abstract machine with a finite set of possible states at any given moment. As a result of some inputs, it can transition from one state to another. To define the automaton we use a list of states, its starting state, and the inputs that cause each transition. Deterministic and non-deterministic finite-state machines are the two types of finite-state machines.


## Objectives:

1. Understand what an automaton is and what it can be used for.

Continuing the work in the same repository and the same project, the following need to be added: 
    a. Provide a function in your grammar type/class that could classify the grammar based on Chomsky hierarchy.
b. For this you can use the variant from the previous lab.

2. According to your variant number (by universal convention it is register ID), get the finite automaton definition and do the following tasks:

    a. Implement conversion of a finite automaton to a regular grammar.

    b. Determine whether your FA is deterministic or non-deterministic.

    c. Implement some functionality that would convert an NDFA to a DFA.

    d. Represent the finite automaton graphically (Optional, and can be considered as a bonus point):
       
    - You can use external libraries, tools or APIs to generate the figures/diagrams.

    - Your program needs to gather and send the data about the automaton and the lib/tool/API return the visual representation.


## Implementation description

We wrote a code that check the type pf the grammar a language has, using Chomsky hierarchy. In order to do this, we have several for loops.

The first for loop is iterating over the keys of the dictionary self.P, which contains the productions of the grammar. For each production, it checks if the length of the dictionary is equal to 1. If the lenght is not 1, the grammar cannot be of type 2. If the productions have length smaller than 1, in which case the grammar cannot be of type 1.

The second for loop is iterating over the non-terminal symbols (VN). For each non-terminal, it iterates through its productions and checks if the production meets the conditions for being a type 3 right linear grammar or a type 3 left linear grammar. We compare the length of the production and the types of its symbols (VT or VN). If any production does not meet the conditions for a type 3 grammar, the type3_right or type3_left flags are set to False, respectively. Finally, if any production has length 0, the grammar cannot be of type 1.

```
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
```

The code below is a way to convert the given automaton into a regular grammar.
We iterate through the states and symbols of the automaton in order to determine the transitions that are allowed. If the next transition is a final state, it will add a production to the respective dictionary for the current state and symbol. If it's not a final state, it will add a production for the next state, the symbel and current state.

If there is a start state already, it will add it to the productions by naming it "S". If there is no start state, it will create one and add it to the productions with epsilon transitions to each final state.

```
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
```
In order to check if an automaton is deterministic, we have to have certain things satisfied. The code below check if there are all the conditions for an automaton to be deterministic.


Firstly, we check if the set of states and input alphabet sigma are not empty. If either of them is empty, the automaton is not deterministic. Next, we check if for each state and symbol, there is exactly one transition defined in Q. Any state-input pair must have a unique transition defined in Q to be deterministic. Also, we have to check if q0 (the initial state) is in Q. Lastly, the method checks if all the final/accepting states in the automaton are also present in Q.

If all the above conditions are satisfied, the automaton is deterministic.
```
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
```
In order to convert from NFA to DFA we check if the given automaton is already deterministic.

If it's not, we initialize empty sets for the DFA's states, accepting states and a dictionary for the transitions.

We loop through each state set. and add the set to dfa_states and check if any  states are accepting states, adding the set to dfa_accept_states if so. For each symbol in sigma, we compute the set of next states and add the transition to dfa_transitions. After all of that, we create an object of the Conversion class, creating the DFA.
```
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
```

## Conclusions / Screenshots / Results
In conclusion, this laboratory work made us learn and revise all that we know about the finite automata so far. It helped us better remember the characteristics of each type of the grammar, according to Chomsky classification and the differences between DFA and NFA.