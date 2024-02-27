from better_logic import (
    Sentence,
    Symbol,
    Not,
    And,
    Or,
    Implication,
    check_knowledge,
    model_check,
)


gilderoy = "Gilderoy"
minerva = "Minerva"
pomona = "Pomona"
horace = "Horace"

gryffindor = "Gryffindor"
hufflepuff = "Hufflepuff"
ravenclaw = "Ravenclaw"
slytherin = "Slytherin"

persons = [gilderoy, minerva, pomona, horace]
houses = [gryffindor, hufflepuff, ravenclaw, slytherin]

knowledge = And([])
symbols = []

for person in persons:
    for house in houses:
        symbols.append(Symbol(f"{person}{house}"))


# A PERSON IS IN ONE HOUSE
for person in persons:
    knowledge.add(Or([Symbol(f"{person}{house}") for house in houses]))


# ONE PERSON IN ONE HOUSE
for person in persons:
    for house in houses:
        knowledge.add(
            Implication(
                Symbol(f"{person}{house}"),
                Not(
                    Or(
                        [
                            Symbol(f"{person}{other_house}")
                            for other_house in houses
                            if house != other_house
                        ]
                    )
                ),
            )
        )


# EACH HOUSE MUST ONLY HAVE ONE PERSON
for house in houses:
    for person in persons:
        knowledge.add(
            Implication(
                Symbol(f"{person}{house}"),
                Not(
                    Or(
                        [
                            Symbol(f"{other_person}{house}")
                            for other_person in persons
                            if person != other_person
                        ]
                    )
                ),
            )
        )

knowledge.add(Or([Symbol(f"{gilderoy}{gryffindor}"), Symbol(f"{gilderoy}{ravenclaw}")]))
knowledge.add(Not(Symbol(f"{pomona}{slytherin}")))
knowledge.add(Symbol(f"{minerva}{gryffindor}"))

check_knowledge(knowledge)
