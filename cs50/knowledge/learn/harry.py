from better_logic import Implication, Symbol, And, Or, Not, model_check

rain = Symbol("It is raining")
hagrid = Symbol("Harry visited hagrid")
dumbledore = Symbol("Harry visited dumbledore")

knowledge = And(
    [
        Implication(Not(rain), hagrid),
        Or([hagrid, dumbledore]),
        Not(And([hagrid, dumbledore])),
        dumbledore,
    ]
)
query = rain


print(knowledge.formula())
print(model_check(knowledge, query))
