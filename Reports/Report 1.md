# The title of the work

### Course: Formal Languages & Finite Automata
### Author: Iuliana Stețenco

----

## Theory
 A language typically consists of three essential components: an alphabet, a vocabulary, and a grammar that defines the language's rules and constraints. These components can be arranged in many different ways, meaning that when constructing a language, they should be carefully selected to suit the intended purpose.


## Objectives:

1. Understand what a language is and what it needs to have in order to be considered a formal one.

2. Provide the initial setup for the evolving project that you will work on during this semester. I said project because usually at lab works, I encourage/impose students to treat all the labs like stages of development of a whole project. Basically you need to do the following:

    a. Create a local && remote repository of a VCS hosting service (let us all use Github to avoid unnecessary headaches);

    b. Choose a programming language, and my suggestion would be to choose one that supports all the main paradigms;

    c. Create a separate folder where you will be keeping the report. This semester I wish I won't see reports alongside source code files, fingers crossed;

3. According to your variant number (by universal convention it is register ID), get the grammar definition and do the following tasks:

    a. Implement a type/class for your grammar;

    b. Add one function that would generate 5 valid strings from the language expressed by your given grammar;

    c. Implement some functionality that would convert and object of type Grammar to one of type Finite Automaton;
    
    d. For the Finite Automaton, please add a method that checks if an input string can be obtained via the state transition from it;


## Implementation description

We defined a class named Grammar, The constructor method, __init__(), initializes the grammar by defining the non-terminal symbols, terminal symbols, productions, and the start symbol.

The non-terminal and terminal symbols are defined as sets of strings.

The productions are defined as a dictionary, where each key is a non-terminal symbol, and the corresponding value is a list of strings representing the possible productions for that non-terminal symbol.

The start symbol of the grammar is defined as the string 'S'.

```
class Grammar:
    def __init__(self):
      #define the non-terminal symbols
        self.VN = {'S', 'A', 'B'}
      #define the terminal symbols
        self.VT = {'a', 'b', 'c', 'd'}
      #define the productions
        self.P = {
            'S': ['bS', 'dA'],
            'A': ['aA', 'dB', 'b'],
            'B': ['cB', 'a']
        }
        #define the start symbol
        self.start = 'S'
```

The function generate_strings takes in a grammar and an optional argument n that defaults to 5. The function generates a list of n valid strings from the given grammar and returns it.

It initialize an empty list called strings to store the generated strings. It then runs a loop n times, where in each iteration it generates a new valid string from the grammar.

To generate a new string, the function uses a stack-based approach. It starts with a stack that contains the start symbol of the grammar, and an empty string to store the string being generated. The function then repeatedly pops a symbol from the stack until the stack is empty.

If the symbol is a terminal symbol (VT), the function appends it to the string being generated. If the symbol is a non-terminal symbol (VN), the function randomly selects one of the productions for the symbol, and pushes the symbols of the production onto the stack in reverse order. (The reason for reversing the order of the production is that the stack is a last-in-first-out data structure, which means that the last symbol pushed onto the stack will be the first one to be processed.) This process continues until the stack is empty.

Finally, the function appends the generated string to the list of strings and returns the list of n elements.

```
#method to generate n number of strings according to given the rules
    def generate_strings(grammar, n=5):
        strings = []
        for i in range(n):
            string = ''
            stack = [grammar.start]
            while stack:
                symbol = stack.pop()
                if symbol in grammar.VT:
                    string += symbol
                elif symbol in grammar.VN:
                    productions = grammar.P[symbol]
                    production = random.choice(productions)
                    for s in reversed(production):
                        stack.append(s)
            strings.append(string)
        return strings
```

After all of this, we declare the class FiniteAutomaton
```
class FiniteAutomaton:
    def __init__(self):
        self.states = set()
        self.alphabet = set()
        self.transitions = {}
        self.start_state = None
        self.final_states = set()
```
The grammar_to_finite_automaton function takes a Grammar object as input and returns a FiniteAutomaton object. The function creates a new FiniteAutomaton object, adds a single start state 'q0' to the automaton, and adds all the terminal symbols from the grammar to the automaton's alphabet. For each production in the grammar, the function creates a new state with a unique name based on the production's hash code, and adds this state to the automaton's set of states. If the production is valid, the function adds a transition from the start state to the new state with an empty string symbol. If the final symbol in the production is a non-terminal symbol, the function adds the new state to the set of final states.
```
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
```

The function takes a FiniteAutomaton object and input string, and returns True if the automaton accepts the input string, False otherwise. It starts in the initial state and moves to the next state based on the input symbol. If the transition is not defined, it returns False.

```
def accepts(fa, input_string):
    current_state = fa.start_state
    for symbol in input_string:
        if (current_state, symbol) in fa.transitions:
            current_state = fa.transitions[(current_state, symbol)]
        else:
            return False
    return current_state in fa.final_states
```
## Conclusions / Screenshots / Results
In conclusion, I must say that I had the opportunity to implement a program that generates strings for a context-free grammar and also converts the grammar into a finite automaton. It was fun and made me open the class notes for sure.
<br> <br>
Let me finish with:
<blockquote> <i>
"I am not bound to please thee with my answers." </i>
- William Shakespeare, The Merchant of Venice
</blockquote> <br>
This quote reminds us that sometimes, the answers we give may not always please others, but as long as we stay true to ourselves and provide our best effort, we can be proud of what we have accomplished.