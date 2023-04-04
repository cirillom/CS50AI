from logic import *

AKnight = Symbol("A is a Knight")
AKnave = Symbol("A is a Knave")
AUnique = And(Or(AKnight, AKnave), Not(And(AKnave, AKnight))) #XOR of AKnight and AKnave

BKnight = Symbol("B is a Knight")
BKnave = Symbol("B is a Knave")
BUnique = And(Or(BKnight, BKnave), Not(And(BKnave, BKnight))) #XOR of AKnight and AKnave

CKnight = Symbol("C is a Knight")
CKnave = Symbol("C is a Knave")
CUnique = And(Or(CKnight, CKnave), Not(And(CKnave, CKnight))) #XOR of AKnight and AKnave

# Puzzle 0
# A says "I am both a knight and a knave."
statement = And(AKnight, AKnave)
knight = Biconditional(statement, AKnight)
knave = Biconditional(Not(statement), AKnave)

knowledge0 = And(
    AUnique,
    knight, 
    knave
)

# Puzzle 1
# A says "We are both knaves."
# B says nothing.
statement = And(AKnave, BKnave)
knight = Biconditional(statement, AKnight)
knave = Biconditional(Not(statement), AKnave)

knowledge1 = And(
    AUnique,
    BUnique,
    knight, 
    knave
)

# Puzzle 2
# A says "We are the same kind."
# B says "We are of different kinds."
Astatement = Or(And(AKnight, BKnight), And(AKnave, BKnave))
knight0 = Biconditional(Astatement, AKnight)
knave0 = Biconditional(Not(Astatement), AKnave)
Bstatement = Or(And(BKnight, AKnave), And(BKnave, AKnight))
knight1 = Biconditional(Bstatement, BKnight)
knave1 = Biconditional(Not(Bstatement), BKnave)


knowledge2 = And(
    AUnique,
    BUnique,
    knight0, 
    knave0,
    knight1, 
    knave1
)

# Puzzle 3
# A says either "I am a knight." or "I am a knave.", but you don't know which.
# B says "A said 'I am a knave'."
# B says "C is a knave."
# C says "A is a knight."
Astatement = Or(AKnight, AKnave)
knight0 = Biconditional(Astatement, AKnight)
knave0 = Biconditional(Not(Astatement), AKnave)


Bstatement = And(AKnight, CKnave)
knight1 = Biconditional(Bstatement, BKnight)
knave1 = Biconditional(Not(Bstatement), BKnave)


Cstatement = AKnight
knight2 = Biconditional(Cstatement, CKnight)
knave2 = Biconditional(Not(Cstatement), CKnave)


knowledge3 = And(
    AUnique,
    BUnique,
    CUnique, 
    knight0, 
    knave0,
    knight1, 
    knave1,
    knight2, 
    knave2
)


def main():
    symbols = [AKnight, AKnave, BKnight, BKnave, CKnight, CKnave]
    puzzles = [
        ("Puzzle 0", knowledge0),
        ("Puzzle 1", knowledge1),
        ("Puzzle 2", knowledge2),
        ("Puzzle 3", knowledge3)
    ]
    for puzzle, knowledge in puzzles:
        print(puzzle)
        if len(knowledge.conjuncts) == 0:
            print("    Not yet implemented.")
        else:
            for symbol in symbols:
                if model_check(knowledge, symbol):
                    print(f"    {symbol}")


if __name__ == "__main__":
    main()
