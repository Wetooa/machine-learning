from dataclasses import dataclass, field
from termcolor import cprint


@dataclass(eq=True, frozen=True)
class Sentence:
    def evaluate(self, model) -> bool:
        raise Exception("nothing to evaluate")

    def formula(self) -> str:
        return ""

    def symbols(self) -> set:
        return set()

    @classmethod
    def parenthesize(cls, s) -> str:
        def balanced(s):
            count = 0
            for c in s:
                if c == "(":
                    count += 1
                elif count <= 0:
                    return False
                else:
                    count -= 1
            return count == 0

        if (
            not len(s)
            or s.isalpha()
            or (s[0] == "(" and s[-1] == ")" and balanced(s[1:-1]))
        ):
            return s
        return f"({s})"


@dataclass(eq=True, frozen=True)
class Symbol(Sentence):
    name: str

    def formula(self) -> str:
        return self.name

    def evaluate(self, model) -> bool:
        return bool(model[self.name])

    def symbols(self) -> set:
        return {self.name}


@dataclass(eq=True, frozen=True)
class Not(Sentence):
    operand: Sentence

    def formula(self) -> str:
        return "¬" + Sentence.parenthesize(self.operand.formula())

    def evaluate(self, model) -> bool:
        return not self.operand.evaluate(model)

    def symbols(self) -> set:
        return self.operand.symbols()


@dataclass(eq=True, frozen=True)
class And(Sentence):
    conjuctions: list[Sentence] = field()

    def add(self, conjuction: Sentence) -> None:
        self.conjuctions.append(conjuction)

    def formula(self) -> str:
        return " ^ ".join(
            [
                Sentence.parenthesize(conjuction.formula())
                for conjuction in self.conjuctions
            ]
        )

    def evaluate(self, model) -> bool:
        return all(conjunction.evaluate(model) for conjunction in self.conjuctions)

    def symbols(self) -> set:
        return set.union(*[conjuction.symbols() for conjuction in self.conjuctions])


@dataclass(eq=True, frozen=True)
class Or(Sentence):
    disjunctions: list[Sentence] = field()

    def add(self, disjunction: Sentence):
        self.disjunctions.append(disjunction)

    def formula(self) -> str:
        return " v ".join(
            [
                Sentence.parenthesize(disjunction.formula())
                for disjunction in self.disjunctions
            ]
        )

    def evaluate(self, model) -> bool:
        return any(disjunction.evaluate(model) for disjunction in self.disjunctions)

    def symbols(self) -> set:
        return set.union(*[disjunction.symbols() for disjunction in self.disjunctions])


@dataclass(eq=True, frozen=True)
class Implication(Sentence):
    antecedent: Sentence = field()
    consequent: Sentence = field()

    def formula(self) -> str:
        return f"{Sentence.parenthesize(self.antecedent.formula())} -> {Sentence.parenthesize(self.consequent.formula())}"

    def evaluate(self, model) -> bool:
        return (not self.antecedent.evaluate(model)) or (
            self.consequent.evaluate(model)
        )

    def symbols(self) -> set:
        return set.union(self.antecedent.symbols(), self.consequent.symbols())


@dataclass(eq=True, frozen=True)
class Bidirectional(Sentence):
    left: Sentence = field()
    right: Sentence = field()

    def formula(self):
        return f"{Sentence.parenthesize(self.left.formula())} <=> {Sentence.parenthesize(self.right.formula())}"

    def evaluate(self, model):
        return (self.left.evaluate(model) and self.right.evaluate(model)) or (
            not self.left.evaluate(model) and not self.right.evaluate(model)
        )

    def symbols(self):
        return set.union(self.left.symbols(), self.right.symbols())


def create_model(symbols, model=dict()):
    if not symbols:
        return [model]

    remaining = symbols.copy()
    p = remaining.pop()

    model_true = model.copy()
    model_true[p] = True

    model_false = model.copy()
    model_false[p] = False

    return create_model(remaining, model_true) + create_model(remaining, model_false)


def evaluate_query(knowledge, query, model):
    for world in model:
        if knowledge.evaluate(world) and not query.evaluate(world):
            return False
    return True


def model_check(knowledge: Sentence, query: Sentence):
    symbols = set.union(knowledge.symbols(), query.symbols())
    model = create_model(symbols)

    return evaluate_query(knowledge, query, model)


def check_knowledge(knowledge: Sentence):
    symbols = knowledge.symbols()
    model = create_model(symbols)

    for symbol in symbols:
        symbol = Symbol(symbol)
        if evaluate_query(knowledge, symbol, model):
            cprint(f"{symbol.formula()}: YES", "green")
        elif evaluate_query(knowledge, Not(symbol), model):
            cprint(f"{symbol.formula()}: NO", "red")
        else:
            print(f"{symbol.formula()}: Maybe")
