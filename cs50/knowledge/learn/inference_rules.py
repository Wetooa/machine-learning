"""
- MODUS PONENS                  a -> b ^ a           :=         b
- AND ELIMINATION               a ^ b                :=         b
- DOUBLE NEGATION               !(!a)                :=         a
- IMPLICATION ELIMINATION       a -> b               :=         !a ^ b
- BICONDITIONAL ELIMINATION     a <-> b              :=         (a -> b) ^ (b -> a)
- DE MORGAN'S                   !(a ^ b)             :=         !a v !b
- DISTRIBUTIVE PROPERTY         a ^ (b v c)          :=         (a ^ b) v (a ^ c)
- RESOLUTION ???                (a v b) ^ !a         :=         b
                                (a v b) ^ (!a v c)   :=         b v c
"""
