# Constraint-Solver
On giving Latex code of a generic solution and specific solution , it will generate constraints on variables by indexwise mapping of variables to its values.

## Let's take a example
### Suppose this is latex code for  generic solution for a question   "[string(Given,), string(latex(P~=~)₹latex(expr(a*100) )),string(latex(r~ =~ val(b) \\%) per annum),string(latex(t ~ = ~ 1) year),string(We know that for latex(1^{st}) year, latex(C.I.) & latex(S.I.) are equal.),string(Hence, latex(C.I. ~- ~S.I. ~ = ~0)),string(Hence, required answer is latex(0).)]"   and this is its specific solution latex code   "[string(Given,), string(latex(P~=~)latex(₹)latex(42500 )),string(latex(r~ =~ 34 \\\\%) per annum),string(latex(t ~ = ~ 1) year),string(We know that for latex(1^{st}) year, latex(C.I.) & latex(S.I.) are equal.),string(Hence, latex(C.I. ~- ~S.I. ~ = ~0)),string(Hence, required answer is latex(0).),string(Hence, the fourth option is correct.)]"   then the code will return the constarints on the variables and expressions to create real world problems based on these constarints.

### Here is what code returns  

{'Constraints': '10000  < (a*100) < 50000', 'Variable_ranges': {'b': {'Range': [20, 50], 'isFloat': False, 'Var_mapped': 34}}}
