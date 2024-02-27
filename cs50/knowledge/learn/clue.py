from better_logic import Symbol, And, Not, Or, Implication, check_knowledge


knife = Symbol("knife")
revolver = Symbol("revolver")
wrench = Symbol("wrench ")
weapons = [knife, revolver, wrench]

scarlet = Symbol("Ms. Scarlet")
mustard = Symbol("Col. Mustard")
plum = Symbol("Professor plum")
characters = [scarlet, mustard, plum]

ballroom = Symbol("ballroom")
kitchen = Symbol("kitchen")
library = Symbol("library ")
places = [ballroom, kitchen, library]

knowledge = And(
    [
        Or(list(weapons)),
        Or(list(characters)),
        Or(list(places)),
    ]
)
symbols = characters + places + weapons

knowledge.add(Not(mustard))
knowledge.add(Not(revolver))
knowledge.add(Not(kitchen))
#
knowledge.add(Or([Not(scarlet), Not(library), Not(wrench)]))
knowledge.add(Not(plum))
knowledge.add(Not(ballroom))
#
check_knowledge(knowledge)
