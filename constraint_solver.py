import re
from math import *

# x is specific solution string and y is generic solution string
def constraintSolver(x,y):        
    input_string = x
    numbers = re.findall(r'\d+\.\d+|\d+', input_string)
    numbers_array = [float(num) if '.' in num else int(num) for num in numbers]
    # print(len(numbers_array),numbers_array)

    input_string1 = y
    dfracSet = set([])
    def find(ind):
      cnt = 1
      exp = ""
      for j in range(ind+1,len(input_string1)):
        if input_string1[j] in "({[":
          cnt+=1
        if input_string1[j] in ")}]":
          cnt-=1
        if cnt==0:
          break
        exp+=input_string1[j]
      return exp

    def is_number(s):
        try:
            float(s)
            return True
        except ValueError:
            return False

    l = len(input_string1)
    expressions_array = []
    first = []
    i = 0
    while i<len(input_string1)-4:
      if input_string1[i:i+3]=="val" and input_string1[i+3]=="(":
        expressions_array.append(find(i+3))
        i+=(3+len(find(i+3)))
      elif input_string1[i:i+4]=="expr" and input_string1[i+4]=="(":
        expressions_array.append(find(i+4))
        # print(input_string1[i:i+4+len(find(i+3))], "END",find(i+3))
        i+=(5+len(find(i+4)))
      elif i<len(input_string1)-8 and input_string1[i:i+10]=="expr_dfrac":
        # print(input_string1[i:i+27],find(i+10))
        dfracSet.add(len(expressions_array))
        expressions_array.append(find(i+10))
        # print(find(i+10))
        i+=(10+len(find(i+10)))
      elif 48<=ord(input_string1[i])<=57:
        num = ""
        while is_number(num+input_string1[i]):
          num+=input_string1[i]
          i+=1
        expressions_array.append(num)
        # print(input_string[i-10:i])
      else:
        i+=1
    
    variables_dic = {}
    def isExpression(exp):
      for i in exp:
        if (i.isupper() or i.islower()):
          return True
      return False
    def idSingleSlash(exp):
      for i in range(len(exp)):
        if ord(exp[i])==47 and ord(exp[i-1])!=47 and ord(exp[i+1])!=47:
          return i
      return -1
    def checkRange(num):
      arr = [-10000000,-1000000,-100000,-50000,-10000,-5000,-2000,-1000,-500,-200,-100,-50,-20,-10,-1,-0.5,-0.1,0,0.1,0.5,1,10,20,50,100,200,500,1000,2000,5000,10000,50000,100000,1000000,10000000]
      for i in range(1,len(arr)):
        if arr[i-1]<=num<=arr[i]:
          return arr[i-1:i+1]
    def get_all_index(element,total):
      arr,bol = [0],True
      while bol:
        if element in total[arr[-1]:len(total)]:
          arr.append(arr[-1]+1+total[arr[-1]:len(total)].index(element))
        else:
          bol = False
      return arr[1:]
    
    def find_expression_front(ind,all):
      cnt = 1
      res = ""
      for i in range(ind,len(all)):
        if all[i]=="(":
          cnt+=1
        if all[i]==")":
          cnt-=1
        res+=all[i]
        if cnt==0:
          break
      return res

    def find_expression_back(ind,all):
      cnt = 1
      res = ""
      for i in range(len(all)-1,-1,-1):
        if all[i]==")":
          cnt+=1
        if all[i]=="(":
          cnt-=1
        res=all[i]+res
        if cnt==0:
          break
      return res

    i = 0
    constraints_array = []
    only_variables = []
    only_variablesMapped = []
    all_constraints = []


    while i<min(len(numbers_array),len(expressions_array)):
        if len(expressions_array[i])==1 and expressions_array[i] not in only_variables and (expressions_array[i].isupper() or expressions_array[i].islower()):
          only_variables.append(expressions_array[i])
          only_variablesMapped.append(numbers_array[i])
        if i not in dfracSet:
            if len(expressions_array[i])<8 and len(expressions_array[i])>1 and isExpression(expressions_array[i]):
              ranges = checkRange(numbers_array[i])
              constraints_array.append(str(ranges[0])+"  < ("+ expressions_array[i] + ") < "+str(ranges[1]))
            if "//" in expressions_array[i]:
              ind = get_all_index("//",expressions_array[i])
              for j in ind:
                constraints_array.append(find_expression_back(0,expressions_array[i][:j-1])+" % "+find_expression_front(0,expressions_array[i][j+1:])+" == 0")
           
            if idSingleSlash(expressions_array[i])>=0:
              ind = idSingleSlash(expressions_array[i])
              if len(find_expression_back(0,expressions_array[i][:ind])+find_expression_front(0,expressions_array[i][ind+1:]))>len(expressions_array[i])-2 and numbers_array[i]%1==0:
                ind = idSingleSlash(expressions_array[i])
                constraints_array.append(find_expression_back(0,expressions_array[i][:ind])+" % "+find_expression_front(0,expressions_array[i][ind+1:])+" == 0")
              if len(find_expression_back(0,expressions_array[i][:ind])+find_expression_front(0,expressions_array[i][ind+1:]))>len(expressions_array[i])-2 and numbers_array[i]%1!=0:
                ind = idSingleSlash(expressions_array[i])
                ranges = checkRange(numbers_array[i])
                constraints_array.append(str(ranges[0])+" < "+find_expression_back(0,expressions_array[i][:ind])+" / "+find_expression_front(0,expressions_array[i][ind+1:])+" < "+str(ranges[1]))
            if "gcd" in expressions_array[i]:
                if numbers_array[i]==1:
                    constraints_array.append(expressions_array[i]+" == 1")
                else:
                    ranges = checkRange(numbers_array[i])
                    constraints_array.append(str(ranges[0])+" <= "+expressions_array[i]+" <= "+str(ranges[1]))

            if "-" in expressions_array[i]:
              minus_ind = []
              for j in range(len(expressions_array[i])):
                if expressions_array[i][j]=='-':
                  minus_ind.append(j)
              for ind in minus_ind:
                constraints_array.append(find_expression_back(ind-1,expressions_array[i][:ind])+" > "+find_expression_front(0,expressions_array[i][ind+1:]))
        i+=1
    


    variable_ranges = {}
    for i in range(len(only_variables)):
      variables_dic[only_variables[i]] = only_variablesMapped[i]
      ranges = checkRange(only_variablesMapped[i])
      eachRange = {"Range":ranges,"isFloat":only_variablesMapped[i]%1!=0,"Var_mapped":only_variablesMapped[i]}
      variable_ranges[only_variables[i]] = eachRange
    #   all_constraints.append(str(ranges[0])+" < "+only_variables[i]+" < "+ str(ranges[1]))
    arr = []
    def hashed_fun(exp):
      hash_value = 3213
      exp = exp.replace(' ','')
      arr.append(exp)
      for i in exp:
        if i not in "({[]})":
          hash_value = ((hash_value << 5) + hash_value) + ord(i)
      return hash_value

    hashed_map = set([])
    for i in variables_dic:
      for j in variables_dic:
        try:
          if j!=i and gcd(variables_dic[i],variables_dic[j])==1:
            if ord(i)>ord(j):
              i,j = j,i
            if hashed_fun(f"gcd({i},{j}) == 1") not in hashed_map:
              hashed_map.add(hashed_fun(f"gcd({i},{j}) == 1"))
              all_constraints.append(f"gcd({i},{j}) == 1")
        except TypeError:
          wd = 0


    for i in list(set(constraints_array)):
      if hashed_fun(i) not in hashed_map:
        all_constraints.append(i)
        hashed_map.add(hashed_fun(i))
    constrStr = " and ".join(all_constraints)
    return {"Constraints":constrStr,"Variable_ranges":variable_ranges}


x = "[string(求める数は latex(12) の倍数よりも latex(6) 大きい数なので,),string(latex(12 \\\\times \\\\square + 6) と表すことができます。),string(latex((199-6)\\\\div 12 = 16 ) あまり latex(1 ) より,),string(latex(12\\\\times 16+6= \\\\underline{198}) です。latex(\\\\quad \\\\blacktriangleleft 199-1=198) でも可)]"
y = "string(求める数は latex(val(a)) の倍数よりも latex(val(b)) 大きい数なので,),string(latex(val(a) \\\\times \\\\square + val(b)) と表すことができます。),string(latex((val(c)-val(b))\\\\div val(a) = expr((c-b)/a) ) あまり latex(1 ) より,),string(latex(val(a)\\\\times expr((c-b)/a)+val(b)= \\\\underline{expr(a*((c-b)/a)+b)}) です。latex(\\\\quad \\\\blacktriangleleft val(c)-1=expr(c-1)) でも可)]"
x = "[string(Để bất đẳng thức đã cho luôn đúng thì),string(ĐKlatex(\\\\colon ( x -1999)^{4}(1- x )^{4}>0) ),string(latex((x-1999)(1-x)>0) ),string(latex(1< x <1999) ),string(latex(x \\\\in N \\\\implies 2 \\\\leq x \\\\leq 1998).),string(Coi như,),string(latex(4\\\\left(4^{5 y}+5 y\\\\right)+2003 \\\\leq-x^{2}+2000 x+\\\\log _{4}\\\\left[(x-1999)^{4}(1-x)^{4}\\\\right]) ),string(latex(4\\\\cdot 4^{5 y}+20 y+2003 \\\\leq-x^{2}+2000 x+4 \\\\log _{4}(x-1999)(1-x)) ),string(latex(4^{5 y+1}+4(5 y+1) \\\\leq-x^{2}+2000 x-1999+4 \\\\log _{4}\\\\left(-x^{2}+2000 x-1999\\\\right) \\\\qquad \\\\ldots\\\\ldots (i) ) ),string(Đặt latex(u =\\\\log _{4}\\\\left(- x ^{2}+2000 x -1999\\\\right) \\\\Leftrightarrow 4^{u}=\\\\left(- x ^{2}+2000 x -1999\\\\right)) ),string(latex((i)) Trở thành latex(4^{5 y+1}+4(5 y+1) \\\\leq 4^{u}+4 u \\\\qquad \\\\qquad \\\\ldots\\\\ldots (ii) )),string(Xét hàm số),string(latex(f(t)=4^{t}+4 t)),string(latex( f^{\\\\prime}(t)=4^{t} \\\\cdot \\\\ln 4+4>0~ \\\\forall t \\\\Rightarrow f(t)) là hàm số đồng biến trên latex(R)),string(latex(f(5 y+1) \\\\leq f(u))),string(latex(5 y+1 \\\\leq u \\\\qquad \\\\ldots \\\\ldots (iii))),string(latex(5 y+1 \\\\leq \\\\log _{4}\\\\left(-x^{2}+2000 x-1999\\\\right))),string(Xét hàm số latex(g(x)=-x ^{2}+2000x -1999),  với latex(2 \\\\leq x \\\\leq 1998).),string(latex(g^{\\\\prime}(x)=-2 x+2000)),string(latex( g^{\\\\prime}=0 \\\\Leftrightarrow x=1000)),string(latex(g(2)=g(1998)=1997 )),string(latex( g(1000)= 998001 \\\\Rightarrow g(x) \\\\leq 998001 )),string(Do đó latex(5 y+1 \\\\leq \\\\log _{4}(998001) )),string(latex(5y+1\\\\leq 9.96 )),string(latex(5y\\\\leq 9.96-1 )),string(latex(y\\\\leq \\\\dfrac{8.96}{5} )),string(latex(y\\\\leq 1.79 )),string(latex(y\\\\in N \\\\implies y\\\\in \\\\{0;1\\\\} )),string(Thay latex(y=0) vào latex((iii))),string(latex(u\\\\geq  1)),string(latex(4^{u}\\\\geq 4 )),string(latex(-x^2+2000x-1999\\\\geq 4)),string(latex(-x^2+2000x-2003\\\\geq 0)),string(latex( 1.002 \\\\leq x \\\\leq 1998.99799)),string(latex(x\\\\in \\\\{2, 3,\\\\ldots \\\\ldots, 1998 \\\\}) có latex(1997 ) số tự nhiên),string(Với latex(y = 1) ),string(latex(u\\\\geq 6)),string(latex(4^{u}\\\\geq 4^{6})),string(latex(-x^2+2000x-1999\\\\geq 4096 )),string(latex(-x^2+2000x-6095\\\\geq 0 )),string(latex(3.05215 \\\\leq x\\\\leq 1996.94784 )),string(latex(x\\\\in \\\\{ 4, 5,\\\\ldots \\\\ldots, 1996 \\\\}) có latex(1993 ) số tự nhiên.),string(Kết luận có latex(3990 ) cặp số tự nhiên latex((x; y)) thỏa đề bài.),string(Hence, the fourth option is correct.)]"
y = "[string(Để bất đẳng thức đã cho luôn đúng thì),string(ĐKlatex(\\\\colon ( x -val(e))^{4}(1- x )^{4}>0) ),string(latex((x-val(e))(1-x)>0) ),string(latex(1< x <val(e)) ),string(latex(x \\\\in N \\\\implies 2 \\\\leq x \\\\leq val(f)).),string(Coi như,),string(latex(4\\\\left(4^{val(a) y}+val(b) y\\\\right)+val(c) \\\\leq-x^{2}+val(d) x+\\\\log _{4}\\\\left[(x-val(e))^{4}(1-x)^{4}\\\\right]) ),string(latex(4\\\\cdot 4^{val(a) y}+val(g) y+val(c) \\\\leq-x^{2}+val(d) x+4 \\\\log _{4}(x-val(e))(1-x)) ),string(latex(4^{val(a) y+1}+4(val(a) y+1) \\\\leq-x^{2}+val(d) x-val(e)+4 \\\\log _{4}\\\\left(-x^{2}+val(d) x-val(e)\\\\right) \\\\qquad \\\\ldots\\\\ldots (i) ) ),string(Đặt latex(u =\\\\log _{4}\\\\left(- x ^{2}+val(d) x -val(e)\\\\right) \\\\Leftrightarrow 4^{u}=\\\\left(- x ^{2}+val(d) x -val(e)\\\\right)) ),string(latex((i)) Trở thành latex(4^{val(a) y+1}+4(val(a) y+1) \\\\leq 4^{u}+4 u \\\\qquad \\\\qquad \\\\ldots\\\\ldots (ii) )),string(Xét hàm số),string(latex(f(t)=4^{t}+4 t)),string(latex( f^{\\\\prime}(t)=4^{t} \\\\cdot \\\\ln 4+4>0~ \\\\forall t \\\\Rightarrow f(t)) là hàm số đồng biến trên latex(R)),string(latex(f(val(a) y+1) \\\\leq f(u))),string(latex(val(a) y+1 \\\\leq u \\\\qquad \\\\ldots \\\\ldots (iii))),string(latex(val(a) y+1 \\\\leq \\\\log _{4}\\\\left(-x^{2}+val(d) x-val(e)\\\\right))),string(Xét hàm số latex(g(x)=-x ^{2}+val(d)x -val(e)),  với latex(2 \\\\leq x \\\\leq val(f)).),string(latex(g^{\\\\prime}(x)=-2 x+val(d))),string(latex( g^{\\\\prime}=0 \\\\Leftrightarrow x=val(h))),string(latex(g(2)=g(val(f))=val(i) )),string(latex( g(val(h))= val(j) \\\\Rightarrow g(x) \\\\leq val(j) )),string(Do đó latex(val(a) y+1 \\\\leq \\\\log _{4}(val(j)) )),string(latex(val(a)y+1\\\\leq val(k) )),string(latex(val(a)y\\\\leq val(k)-1 )),string(latex(y\\\\leq \\\\dfrac{val(l)}{val(a)} )),string(latex(y\\\\leq val(m) )),string(latex(y\\\\in N \\\\implies y\\\\in \\\\{0;1\\\\} )),string(Thay latex(y=0) vào latex((iii))),string(latex(u\\\\geq  1)),string(latex(4^{u}\\\\geq 4 )),string(latex(-x^2+val(d)x-val(n)\\\\geq 4)),string(latex(-x^2+val(d)x-val(o)\\\\geq 0)),string(latex( val(p) \\\\leq x \\\\leq val(q) )),string(latex(x\\\\in \\\\{2, 3,\\\\ldots \\\\ldots, val(f) \\\\}) có latex(val(r) ) số tự nhiên),string(Với latex(y = 1) ),string(latex(u\\\\geq val(s))),string(latex(4^{u}\\\\geq 4^{val(s)})),string(latex(-x^2+val(d)x-val(e)\\\\geq 4^{val(s)} )),string(latex(-x^2+val(d)x-val(t)\\\\geq 0 )),string(latex(val(u) \\\\leq x\\\\leq val(v) )),string(latex(x\\\\in \\\\{ 4, 5,\\\\ldots \\\\ldots, val(w) \\\\}) có latex(val(x) ) số tự nhiên.),string(Kết luận có latex(val(y) ) cặp số tự nhiên latex((x; y)) thỏa đề bài.),string(Hence, the fourth option is correct.)]"
generic_string_arr = [
     "[string(Given, John borrowedlatex(~₹~  val(x)~)and rate of interestlatex(~ =val(r) \\% ~)per annum),string(After the first year, the interest accrued on the principal will belatex(~ ₹ ~ \\dfrac{val(x) \\times val(r) }{100} =  ₹ ~expr(x*r/100))),string(So, after one year, the total amount owed by John to the bank islatex(~ = val(x) +expr(x*r/100) = ₹ ~  expr(x + (x*r/100)))),string(Now, John repays the loan in two equal installments. Let's assume the value of each installment islatex(~ ₹ ~ y).),string(The first installment consist of the interest accruedlatex(~ ₹ ~ expr(x*r/100) ~)and some part of the principal.),string(latex(\\therefore ~)The remaining amount in the first installment islatex(~=₹~\\left( y - expr(x*r/100)\\right))),string(After, the first installment, remaining principal amountlatex(~ = ₹~\\left(expr(x + (x*r/100)) - y\\right))),string(Now, the interest accrued on the remaining principal amountlatex(~ = ₹~ \\bigg(  expr(x + (x*r/100)) - y \\bigg) \\times \\dfrac{val(r)}{100})),string(The second installment consists of the due amount and the interest accrued on the due amount),string(latex(\\therefore~)The second installment will belatex(~ =  (expr(x + (x*r/100)) - y) + \\bigg((expr(x + (x*r/100)) - y ) \\times \\dfrac{val(r)}{100}\\bigg) = ₹~\\left(expr_dfrac{100 + r}{100} \\times (expr(x+(x*r/100))-y)\\right))),string(As, we know both installments are equal, so),string(latex(y =  expr_dfrac{100 + r}{100} \\times (expr(x+(x*r/100))-y) )),string(latex(expr(gcd((100+r),100))y = \\bigg( expr_dfrac{(100 + r)*gcd((100+r),100)}{100}  \\times expr(x+(x*r/100)) \\bigg) -expr_dfrac{(100 + r)*gcd((100+r),100)}{100}y  )),string(latex(y =  expr( (((100+r)/100)*(x + (x*r/100)))/(1 + ((100+r)/100)) ) ).),string(Therefore, each installment is latex( ₹~expr( (((100+r)/100)*(x + (x*r/100)))/(1 + ((100+r)/100)))).)]",
      "[string(Suppose, in commerce program, the number of male students be latex(val(p)c) and female students be latex(val(q)c)),string(In a similar way we assume that, in humanities program, the number of male students be latex(h) and female students be latex(h).),string(),string(Therefore, latex((val(p)c+h)\\ratio (val(q)c+h)=val(m)\\ratio val(n))),string(latex(\\Rightarrow expr(p*n)c+val(n)h=expr(m*q)c+val(m)h)),string(latex(\\Rightarrow expr((m*q)-(p*n))c=expr(n-m)h)),string(latex(\\Rightarrow h=expr(((m*q)-(p*n))//(n-m))c)),string(),string(It is given that latex(val(p)c=val(x)\\Rightarrow c=expr(x//p)) and latex(h=expr((((m*q)-(p*n))//(n-m))*(x//p)))),string(Thus, total number of students enrolled in these two programs in the college latex(=expr(p+q)c+2h=expr(((p+q)*(x//p))+(2*((((m*q)-(p*n))//(n-m))*(x//p)))))),string(Therefore, the required answer is latex(expr(((p+q)*(x//p))+(2*((((m*q)-(p*n))//(n-m))*(x//p))))).)]",
     "[string(Given,), string(latex(P~=~)₹latex(expr(a*100) )),string(latex(r~ =~ val(b) \\%) per annum),string(latex(t ~ = ~ 1) year),string(We know that for latex(1^{st}) year, latex(C.I.) & latex(S.I.) are equal.),string(Hence, latex(C.I. ~- ~S.I. ~ = ~0)),string(Hence, required answer is latex(0).)]",
     "[string(Let the invested amount or Principal be ₹latex(P),),string(Given,),string(Rate of interestlatex((r) ~ = ~ val(r) \\%) per annum),string(Timelatex((t)~ = val(t)) years),string(Now, as we know,),string(Compound Interest for latex(val(t)) years can be represented as),string(latex(C.I ~ = ~ A-P ~ = ~ \\bigg \\{ P + \\left( \\dfrac{val(t)P \\times val(r)}{100} \\right)  + P\\left( \\dfrac{val(r)}{100} \\right)^{val(t)} \\bigg \\} - P)),string(latex(C.I ~ = ~ \\left( \\dfrac{val(t)P \\times val(r)}{100} \\right) + P  \\left( \\dfrac{val(r)}{100} \\right)^{val(t)} )),string(Simple interest latex(S.I ~ = ~ \\dfrac{P \\times r \\times t}{100})),string(latex(S.I) for latex(val(t)) years latex(= ~ \\dfrac{val(t)P \\times val(r)}{100} )),string(Now, latex(C.I - S.I ~ = ~  \\left( \\dfrac{val(t)P \\times val(r)}{100} \\right) + P  \\left( \\dfrac{val(r)}{100} \\right)^{val(t)} - \\dfrac{val(t)P \\times val(r)}{100} )),string(According to the question,),string(latex(C.I - S.I ~ = ~  val(x) )),string(So, latex(P \\times \\left( \\dfrac{r}{100} \\right)^{val(t)} ~ = ~ val(x) )),string(latex(r ~ = ~ val(r) \\%)),string(latex( P \\left( \\dfrac{expr(r**t)}{expr(100**t)} \\right) ~ = ~ val(x) )),string(latex(P ~ = ~)₹latex(expr((x*(100**t))/(r**t))))]",
     "[string(Let the initial population of Alpha and Beta bacteria colonies be latex(A) million and latex(B) million respectively.),string(),string(Therefore, after latex(val(h)) hours the population of bacteria in the colony of ),string(latex(\\qquad) Alpha bacteria is latex(= A\\times expr((100-x)/100)^{val(h)}) million),string(latex(\\qquad) Beta bacteria is latex(= B\\times expr((100-y)/100)^{val(h)}) million),string(),string(According to the question, latex(\\qquad A\\times expr((100-x)/100)^{val(h)} = B\\times expr((100-y)/100)^{val(h)})),string(latex(\\Rightarrow A\\ratio B = expr(((100-y)/100)*10)^{val(h)}\\ratio expr(((100-x)/100)*10)^{val(h)})),string(latex(\\Rightarrow A\\ratio B = (expr((((100-y)/100)*10)**h)\\times val(z))\\ratio (expr((((100-x)/100)*10)**h)\\times val(z)) )),string(latex(\\Rightarrow A\\ratio B = expr(((((100-y)/100)*10)**h)*z)\\ratio expr(((((100-x)/100)*10)**h)*z) )),string()]",
     "[string(In the given expression latex((n+1)+(2n+3)+(3 n+5)+.....+(val(N)n+p)), the value of latex(‘p’) is latex(val(N)^{\\text{th}}) odd natural number i.e., latex(expr(1+((N-1)*2))).),string(latex(\\therefore~(n+1)+(2 n+3)+(3n+5)+.....+(val(N)n+expr(1+((N-1)*2)))=val(V))),string(latex(\\Rightarrow~n(1+2+3+.....+val(N))+(1+3+5+.....+expr(1+((N-1)*2)))=val(V))),string(latex(\\Rightarrow~expr((N*(N+1))/2)n+expr(N**2)=val(V))),string(latex(\\Rightarrow~expr((N*(N+1))/2)n=expr(V-(N**2)))),string(latex(\\Rightarrow~n=expr((V-(N**2))/((N*(N+1))/2)))),string(latex(\\therefore~\\left(n^{2}+2 n^{2}+3 n^{2}+.....+p n^{2}\\right)=expr((V-(N**2))/((N*(N+1))/2))^{2}\\times(1+2+3+.....+expr(1+((N-1)*2)))=expr(((V-(N**2))/((N*(N+1))/2))**2)\\times expr(((1+((N-1)*2))*(2+((N-1)*2)))/2)=expr((((V-(N**2))/((N*(N+1))/2))**2)*(((1+((N-1)*2))*(2+((N-1)*2)))/2))))]",
     "[string(It is given that, latex(A B=B C)), string(latex(\\sqrt{(val(A)-(-val(C)))^{2}+(val(B)-val(D))^{2}}=\\sqrt{(-val(C)-(-val(E)))^{2}+(val(D)-c)^{2}} )),  string(latex(\\sqrt{(expr(C+A))^{2}+(expr(B-D))^{2}} = \\sqrt{(expr(E-C))^{2}+(val(D)-c)^{2}})),string(Squaring on both sides,), string(latex((expr(C+A))^{2}+(expr(-D+B))^{2} = (expr(E-C))^{2}+(val(D)-c)^{2})),string(latex(expr((-C-A)**2)+expr((D-B)**2) = expr((-E+C)**2)+expr(D*D)-expr(2*D)c+c^{2} )), string(latex(c^{2}-expr(2*D)c +expr(((-E+C)**2)+(D*D)) =expr(((-C-A)**2)+((D-B)**2)) )), string(latex(c^{2}-expr(2*D)c+expr(((-E+C)**2)+D*D-((-C-A)**2)-((D-B)**2)) =0)),string(latex(c^{2}-val(P)c-val(Q)c+expr(((-E+C)**2)+D*D-((-C-A)**2)-((D-B)**2))=0)),string(latex((c-val(P))(c-val(Q))=0)), string(latex(c=val(P)~~) or latex(~~c=val(Q))),string(If latex(c=val(P)) then,), custom_evaluation_expression(lhs([string(latex(B C))]), rhs([string(latex(\\sqrt{(-val(C)-(-val(E)))^{2}+(val(D)-val(P))^{2}})),  string(latex(\\sqrt{(expr(-C+E))^{2}+(expr(D-P))^{2}})),  string(latex(\\sqrt{expr((C-E)**2)+expr((P-D)**2)})),  string(latex(py_fun(prime_factors(expr(((C-E)**2)+((P-D)**2))))) units)]),equating(latex(=))), custom_evaluation_expression(lhs([string(latex(AC))]), rhs([string(latex(\\sqrt{(val(A)-(-val(E)))^{2}+(val(B)-val(P))^{2}})), string(latex(\\sqrt{(expr(A+E))^{2}+(expr(-P+B))^{2}})),  string(latex(\\sqrt{expr((A+E)**2)+expr((P-B)**2)})),  string(latex(py_fun(prime_factors(expr(((A+E)**2)+((P-B)**2)) )) ) units)]),equating(latex(=))),string(Also, latex(A B=py_fun(prime_factors(expr(((C-E)**2)+((P-D)**2))))) units latex(\\qquad (A B=B C))), custom_evaluation_expression(lhs([string(latex(A B+B C))]), rhs([string(latex(py_fun(prime_factors(expr(((C-E)**2)+((P-D)**2))))+py_fun(prime_factors(expr(((C-E)**2)+((P-D)**2)))))), string(latex(2 py_fun(prime_factors(expr(((C-E)**2)+((P-D)**2)))))), string(latex(AC))]),equating(latex(=))),string(So, for latex(c=val(P)), points latex(A), latex(B) and latex(C) lie on a straight line.), string(Thus, latex(c=val(Q)) is the only possible value because other value of latex(c) can not satisfy the condition that points latex(A), latex(B) and latex(C) are vertices of a quadrilateral.)]",
     "[string(Using the distance formula,), string(If latex((x_{1},y_{1})) and latex((x_{2},y_{2})) are two points then the distance between them is given by latex(\\sqrt{(x_{1}-x_{2})^{2}+(y_{1}-y_{2})^{2}}).), string(Here, the given points are latex(A(-val(A),-val(B))) and latex(C(-val(C),val(D))).), custom_evaluation_expression(lhs([string(The exact length of latex(A C))]), rhs([string(latex(\\sqrt{(-val(A)-(-val(C)))^{2}+(-val(B)-val(D))^{2}} )),string(latex(\\sqrt{(expr(C-A))^{2}+(expr(-D-B))^{2}} )),string(latex(\\sqrt{expr((A-C)**2)+expr((D+B)**2)} )),string(latex(\\sqrt{expr(((A-C)**2)+((D+B)**2))} ))]),equating(latex(=))),string(Thus, the exact length of latex(A C) is latex(\\sqrt{expr(((A-C)**2)+((D+B)**2))}) units.)]",
     "[string(Let the speed of the faster val(T) be latex(F) m/s and its length be latex(val(L)) meters.),string(Let the speed of the slower val(T) be latex(S) m/s and its length be latex(val(M)) meters.),custom_evaluation_expression(lhs([string(latex(\\therefore \\dfrac{val(L)+val(M)}{F+S})),string(And, latex(\\dfrac{val(L)}{F+S})),string(latex(\\therefore 1+\\dfrac{val(M)}{val(L)})),string(latex(\\Rightarrow M)),string(latex(\\Rightarrow M))]),rhs([string(latex(val(A)\\qquad \\dotsc (i))),string(latex(expr(B/100)\\qquad \\dotsc (ii))),string(latex(\\dfrac{val(A)}{expr(B/100)})),string(latex(\\dfrac{expr(A-(B/100))}{expr(B/100)} \\times val(X))),string(latex(expr(((A-(B/100))*X)//(B/100))))]),equating(latex(=)))]",
     "[string(latex(\\def\\arraystretch{1.3} \\begin{array}{c}  ~~expr((A//1000)%10)~~expr((A//100)%10)~~expr((A//10)%10)~~expr(A%10)  \\\\\\  \\underline{-~expr((B//1000)%10)~~expr((B//100)%10)~~expr((B//10)%10)~~expr(B%10)~~} \\\\\\  ~~\\boxed{expr(((A-B)//1000)%10)~~expr(((A-B)//100)%10)~~expr(((A-B)//10)%10)~~expr((A-B)%10)}   \\end{array}))]",
     "[string( Given,  latex(T_{val(A)}+T_{expr(A+1)}=0 )), string(latex(\\Rightarrow val(p){ }^{n} C_{expr(A-1)} a^{n-expr(A-1)} b^{expr(A-1)} val(q){ }^{n} C_{val(A)}a^{n-val(A)} b^{val(A)}=0)),string(latex(\\Rightarrow { }^{n} C_{expr(A-1)} a^{n-expr(A-1)} b^{expr(A-1)}= { }^{n} C_{val(A)} a^{n-val(A)} b^{val(A)})), string(latex(\\Rightarrow \\dfrac{a}{b}=\\dfrac{{ }^{n} C_{val(A)}}{{ }^{n} C_{expr(A-1)}}= \\dfrac{n-expr(A-1)}{val(A)}))]",
     "[string(Clearly, latex(\\bigg(\\dfrac{1 - t^{val(q)}}{1 - t}\\bigg)^{3} = (1 - t^{val(q)})^{3}(1 - t)^{- 3})),string(latex(\\therefore) coefficient of latex(t^{val(p)} ) in latex( (1 - t^{val(q)})^{3}(1 - t)^{- 3})),string(latex(\\Rightarrow) coefficient of latex(t^{val(p)}) in latex(\\lparen 1 - t^{expr(3*q)} - 3{t^{val(q)}} + 3t^{expr(2*q)} \\rparen (1 - t)^{- 3})),string(latex(\\Rightarrow) coefficient of latex(t^{val(p)}) in latex((1 - t)^{- 3})),string(latex(\\Rightarrow) latex(^{3 + val(p) - 1}C_{val(p)} = ^{expr(3+p-1)}C_{val(p)} = expr(binomial((3+p-1),p)) \\quad \\lparen \\because) coefficient of latex(x^{r}) in latex(\\lparen 1-x \\rparen^{-n} ~=~ ^{n+r-1}C_{r} \\rparen))]",
     '''[string(Since, the general term in the expansion of binomial latex(\\left( \\sqrt{x} - \\dfrac{k}{{x^{val(q)}}^{}} \\right)^{val(N)}) is ),string(latex(T_{r + 1} = { }^{val(N)}C_{r} x^{\\left( \\dfrac{val(N)-r}{val(p)} \\right)} ( - k)^{r } x^{- val(q)r} = { }^{val(N)}C_{r}( - k)^{r}x ^{\\left( \\dfrac{val(N) - expr(1+(p*q))r}{val(p)} \\right)})), string(latex(\\because) Term is constant, so latex(r = expr(N/(1+(p*q))))), string(latex(\\therefore~{ }^{val(N)}C_{expr(N/(1+(p*q)))} {\\left( - k \\right)^{expr((N)/(1+(p*q)))}} = val(A) \\implies\\dfrac{py_fun(first_n_digits("\\times".join(list(map(str, range(val(N),expr(N-((N)/(1+(p*q)))),-1)))) , 1000 ))}{py_fun(first_n_digits("\\times".join(list(map(str, range(2,expr(1+((N)/(1+(p*q)))),1)))) , 1000 ))}k^{expr((N)/(1+(p*q)))} = val(A))),string(latex(expr((binomial(N,(N/(1+(p*q))))))k^{expr(N/(1+(p*q)))} = val(A))), string(latex(k^{expr(N/(1+(p*q)))} = expr(A/((binomial(N,(N/(1+(p*q))))))) )),string(latex(\\left| k \\right|= expr((A/((binomial(N,(N/(1+(p*q)))))))**(1/((N/(1+(p*q))))))))]''',
     "[string(The general term in the binomial expansion of latex((a+b)^{n}) is latex(T_{r+1}={ }^{n} C_{r} a^{n-r} b^{r}).), string(So, the general term in the binomial expansion of latex(\\left(val(A)^{\\frac{1}{val(p)}}-val(B)^{\\frac{1}{expr(k*p)}} \\right)^{expr(m*k*p)}) is), custom_evaluation_expression(lhs([string(latex(T_{(r+1)}))]), rhs([string(latex({ }^{expr(m*k*p)} C_{r}\\left(val(A)^{\\frac{1}{val(p)}}\\right)^{expr(m*k*p)-r}\\left(-val(B)^{\\frac{1}{expr(k*p)}}\\right)^{r})), string(latex({ }^{expr(m*k*p)} C_{r} ~ val(A)^{\\frac{expr(m*k*p)-r}{val(p)}}(-1)^{r} ~ val(B)^{\\frac{r}{expr(k*p)}})), string(latex((-1)^{r} ~ { }^{expr(m*k*p)} C_{r} ~ val(A)^{expr(m*k)-\\frac{r}{val(p)}} ~ val(B)^{\\frac{r}{expr(k*p)}}))]),equating(latex(=))),string(The possible non-negative integral values of 'latex(r)' for which latex(\\dfrac{r}{val(p)}) and latex(\\dfrac{r}{expr(p*k)}) are integer, where latex(r \\leq expr(m*k*p)), are latex(r=0), latex(expr(k*p)), latex(expr(2*k*p)), latex(expr(3*k*p)), latex(......), latex(expr(m*k*p)).),string(latex(\\therefore) There are latex(expr(m+1)) rational terms in the binomial expansion and remaining latex(expr(m*k*p +1)- expr(m+1)=expr(m*k*p +1- m-1)) terms are irrational terms.)]",
     '''[string(We have,),string(latex(\\lparen x+ val(p) \\rparen^{val(A)} +\\lparen x- val(p) \\rparen^{val(A)} = a_{0}+a_{1} x+a_{2} x^{2} +..... . .+ a_{val(A)} x^{val(A)} )),string(latex(\\therefore a_{0}+a_{1} x+a_{2} x^{2} +..... . .+ a_{val(A)} x^{val(A)} )),string(latex(= \\lbrack \\lparen ^{val(A)}C_{0} x^{val(A)} + ^{val(A)}C_{1} x^{expr(A-1)} val(p) + ^{val(A)}C_{2} x^{expr(A-2)} val(p)^{2} + \\dots + ^{val(A)}C_{val(A)} val(p)^{val(A)} \\rparen + \\lparen ^{val(A)}C_{0} x^{val(A)} - ^{val(A)}C_{1} x^{expr(A-1)} val(p) + ^{val(A)}C_{2} x^{expr(A-2)} val(p)^{2} - \\dots + ^{val(A)}C_{val(A)} val(p)^{val(A)} \\rparen \\rbrack)),string(latex(= 2 \\lbrack ^{val(A)}C_{0} x^{val(A)} + ^{val(A)}C_{2} x^{expr(A-2)} \\cdot val(p)^{2} + ^{val(A)}C_{4} x^{expr(A-4)} \\cdot val(p)^{4} + \\dots + ^{val(A)}C_{val(A)} \\cdot  val(p)^{val(A)} \\rbrack )),string(By comparing coefficients, we get),string(latex( a_{expr(k+2)} = 2 ^{val(A)}C_{expr(A-k-2)} \\lparen val(p) \\rparen ^{expr(A-k-2)};~ a_{val(k)} = 2 ^{val(A)}C_{expr(A-k)} \\lparen val(p) \\rparen^{expr(A-k)} ) ),evaluation_expression(lhs([string(latex(\\dfrac{a_{expr(k+2)}}{a_{val(k)}}))]),rhs([string(latex( \\dfrac{2 \\lparen ^{val(A)}C_{expr(k+2)} \\rparen \\lparen val(p) \\rparen^{expr(A-k-2)}}{2 \\lparen ^{val(A)}C_{val(k)} \\rparen \\lparen val(p) \\rparen ^{expr(A-k)}} = \\dfrac{2 \\cdot py_fun(first_n_digits("\\cdot".join(list(map(str, range(val(A),expr(A-k-2),-1)))) , 1000 )) \\cdot \\lparen val(p) \\rparen^{expr(A-k-2)} \\cdot py_fun(first_n_digits("\\cdot".join(list(map(str, range(1,expr(k+1),1)))) , 1000 )) }{py_fun(first_n_digits("\\cdot".join(list(map(str, range(1,expr(k+2+1),1)))) , 1000 )) \\cdot 2 \\cdot  py_fun(first_n_digits("\\cdot".join(list(map(str, range(val(A),expr(A-k),-1)))) , 1000 )) \\cdot \\lparen val(p) \\rparen ^{expr(A-k)} } \\quad \\lbrack \\because~ ^{val(A)}C_{expr(A-k-2)} ~=~  ^{val(A)}C_{expr(k+2)}) and latex(^{val(A)}C_{expr(A-k)} ~=~ ^{val(A)}C_{val(k)} \\rbrack)),string(latex(\\dfrac{py_fun(first_n_digits("\\times".join(list(map(str, range(val(A),expr(A-k-2),-1)))) , 1000 )) \\times \\lparen val(p) \\rparen^{expr(A-k-2)} \\times py_fun(first_n_digits("\\times".join(list(map(str, range(1,expr(k+1),1)))) , 1000 )) }{py_fun(first_n_digits("\\times".join(list(map(str, range(1,expr(k+2+1),1)))) , 1000 )) \\times py_fun(first_n_digits("\\times".join(list(map(str, range(val(A),expr(A-k),-1)))) , 1000 )) \\times \\lparen val(p) \\rparen ^{expr(A-k)} } = \\dfrac{expr(binomial(A,(k+2))) }{expr(binomial(A,k)) \\times val(p)^{2} }  = expr(((binomial(A,(k+2)))* ((p)**((A-k-2))))/((binomial(A,k))*((p)**(A-k))))))]))]''',
     "[string(The amount of markup can be found with the following equation.),string(Markup rate latex(\\times) wholesale price latex(=) amount of markup),string(Since markup rate is a percentage, we have to convert it into a decimal first.),string(So, latex(val(b) \\%=\\dfrac{val(b)}{100}=expr(b/100))),string(Now, using the formula and substituting the values, we get latex(expr(b/100) \\times \\$ val(a)=\\$ expr((b/100)*a))),string(Therefore, the amount of markup on the headphones is latex(\\$ expr((b/100)*a))).)]",
     "[string(The amount of markdown can be found with the following equation.),string(Markdown rate latex(\\times) original price latex(=) amount of markdown),string(Since the markdown rate is a percentage, we have to convert it into a decimal first.),string(So, latex(val(a) \\%=\\dfrac{val(a)}{100}=expr(a/100))),string(Now, using the formula and substituting the values, we get latex(expr(a/100) \\times \\$ val(b)=\\$ expr(a*b/100))),string(Therefore, the amount of markdown for the book is latex(\\$ expr(a*b/100))).)]",
     "[string(To find the amount of commission made, use the following formula Commission rate latex(\\times) retail price latex(=) amount of commission made Since the commission rate is a percentage, we have to convert it into a decimal first. So, latex(val(a) \\%=\\dfrac{val(a)}{100}=expr(a/100))),string(Now, using the formula and substituting the values, we get latex(expr(a/100) \\times \\$ val(b)=\\$ expr((a/100)*b))),string(Therefore, the amount of commission Sophia makes by selling a computer is latex(\\$ expr((a/100)*b))).)]",
     "[string(We have to convert the percentage of tax into a decimal first.),string(latex(val(c) \\%=\\dfrac{val(c)}{100}=expr(c/100))),string(latex(val(b) \\%=\\dfrac{val(b)}{100}=expr(b/100))),string(Since both sales tax rates apply to latex(\\$ val(d)), we can add the two rates.),string(latex(expr(c/100)+expr(b/100)=expr((c+b)/100))),string(latex(expr((c+b)/100) \\times \\$ val(d)=\\$ expr((c+b)*d/10000))),string(Emma pays latex(\\$ expr((c+b)*d/10000)) in sales tax for her smartwatch purchase.)]",

     ]

specific_string_arr = [
     "[string(Given, John borrowedlatex(~₹~  476150~)and rate of interestlatex(~ =14 \\\\% ~)per annum),string(After the first year, the interest accrued on the principal will belatex(~ ₹ ~ \\\\dfrac{476150 \\\\times 14 }{100} =  ₹ ~66661)),string(So, after one year, the total amount owed by John to the bank islatex(~ = 476150 +66661 = ₹ ~  542811)),string(Now, John repays the loan in two equal installments. Let's assume the value of each installment islatex(~ ₹ ~ y).),string(The first installment consist of the interest accruedlatex(~ ₹ ~ 66661 ~)and some part of the principal.),string(latex(\\\\therefore ~)The remaining amount in the first installment islatex(~=₹~\\\\left( y - 66661\\\\right))),string(After, the first installment, remaining principal amountlatex(~ = ₹~\\\\left(542811 - y\\\\right))),string(Now, the interest accrued on the remaining principal amountlatex(~ = ₹~ \\\\bigg(  542811 - y \\\\bigg) \\\\times \\\\dfrac{14}{100})),string(The second installment consists of the due amount and the interest accrued on the due amount),string(latex(\\\\therefore~)The second installment will belatex(~ =  (542811 - y) + \\\\bigg((542811 - y ) \\\\times \\\\dfrac{14}{100}\\\\bigg) = ₹~\\\\left(\\\\dfrac{57}{50} \\\\times (542811-y)\\\\right))),string(As, we know both installments are equal, so),string(latex(y =  \\\\dfrac{57}{50} \\\\times (542811-y) )),string(latex(2y = \\\\bigg( \\\\dfrac{57}{25}  \\\\times 542811 \\\\bigg) -\\\\dfrac{57}{25}y  )),string(latex(y =  289161 ).),string(Therefore, each installment is latex( ₹~289161).),string(Hence, the third option is correct.)]",
     " [string(Suppose, in commerce program, the number of male students be latex(8c) and female students be latex(13c)),string(In a similar way we assume that, in humanities program, the number of male students be latex(h) and female students be latex(h).),string(),string(Therefore, latex((8c+h)\\\\ratio (13c+h)=18\\\\ratio 23)),string(latex(\\\\Rightarrow 184c+23h=234c+18h)),string(latex(\\\\Rightarrow 50c=5h)),string(latex(\\\\Rightarrow h=10c)),string(),string(It is given that latex(8c=72\\\\Rightarrow c=9) and latex(h=90)),string(Thus, total number of students enrolled in these two programs in the college latex(=21c+2h=369)),string(Therefore, the required answer is latex(369).)]",
     "[string(Given,), string(latex(P~=~)latex(₹)latex(42500 )),string(latex(r~ =~ 34 \\\\%) per annum),string(latex(t ~ = ~ 1) year),string(We know that for latex(1^{st}) year, latex(C.I.) & latex(S.I.) are equal.),string(Hence, latex(C.I. ~- ~S.I. ~ = ~0)),string(Hence, required answer is latex(0).),string(Hence, the fourth option is correct.)]",
     "[string(Let the invested amount or Principal be latex(₹)latex(P), ),string(Given,),string(Rate of interestlatex((r) ~ = ~ 5 \\\\%) per annum),string(Timelatex((t)~ = 2) years),string(Now, as we know,),string(Compound Interest for latex(2) years can be represented as),string(latex(C.I ~ = ~ A-P ~ = ~ \\\\bigg \\\\{ P + \\\\left( \\\\dfrac{2P \\\\times 5}{100} \\\\right)  + P\\\\left( \\\\dfrac{5}{100} \\\\right)^{2} \\\\bigg \\\\} - P)),string(latex(C.I ~ = ~ \\\\left( \\\\dfrac{2P \\\\times 5}{100} \\\\right) + P  \\\\left( \\\\dfrac{5}{100} \\\\right)^{2} )),string(Simple interest latex(S.I ~ = ~ \\\\dfrac{P \\\\times r \\\\times t}{100})),string(latex(S.I) for latex(2) years latex(= ~ \\\\dfrac{2P \\\\times 5}{100} )),string(Now, latex(C.I - S.I ~ = ~  \\\\left( \\\\dfrac{2P \\\\times 5}{100} \\\\right) + P  \\\\left( \\\\dfrac{5}{100} \\\\right)^{2} - \\\\dfrac{2P \\\\times 5}{100} )),string(According to the question,),string(latex(C.I - S.I ~ = ~  171 )),string(So, latex(P \\\\times \\\\left( \\\\dfrac{r}{100} \\\\right)^{2} ~ = ~ 171 )),string(latex(r ~ = ~ 5 \\\\%)),string(latex( P \\\\left( \\\\dfrac{25}{10000} \\\\right) ~ = ~ 171 )),string(latex(P ~ = ~)latex(₹)latex(68400)),string(Hence, the first option is correct.)]",
     "[string(Let the initial population of Alpha and Beta bacteria colonies be latex(A) million and latex(B) million respectively.),string(),string(Therefore, after latex(4) hours the population of bacteria in the colony of latex(-)),string(latex(\\qquad) Alpha bacteria is latex(= A\\times 0.8^{4}) million),string(latex(\\qquad) Beta bacteria is latex(= B\\times 0.9^{4}) million),string(),string(According to the question, latex(\\qquad A\\times 0.8^{4} = B\\times 0.9^{4})),string(latex(\\Rightarrow A\\ratio B = 9^{4}\\ratio 8^{4})),string(latex(\\Rightarrow A\\ratio B = (6561\\times 3)\\ratio (4096\\times 3) )),string(latex(\\Rightarrow A\\ratio B = 19683\\ratio 12288 )),string()]",
     "[string(In the given expression latex((n+1)+(2n+3)+(3 n+5)+.....+(26n+p)),  the value of latex(‘p’) is latex(26^{\\\\text{th}}) odd natural number i.e., latex(51).),string(latex(\\\\therefore~(n+1)+(2 n+3)+(3n+5)+.....+(26n+51)=1378)),string(latex(\\\\Rightarrow~n(1+2+3+.....+26)+(1+3+5+.....+51)=1378)),string(latex(\\\\Rightarrow~351n+676=1378)),string(latex(\\\\Rightarrow~351n=702)),string(latex(\\\\Rightarrow~n=2)),string(latex(\\\\therefore~\\\\left(n^{2}+2 n^{2}+3 n^{2}+.....+p n^{2}\\\\right)=2^{2}\\\\times(1+2+3+.....+51)=4\\\\times 1326=5304)),string(Hence, the third option is correct.)]",
     "[string(It is given that, latex(A B=B C)), string(latex(\\\\sqrt{(2-(-3))^{2}+(5-6)^{2}}=\\\\sqrt{(-3-(-8))^{2}+(6-c)^{2}} )),  string(latex(\\\\sqrt{(5)^{2}+(-1)^{2}} = \\\\sqrt{(5)^{2}+(6-c)^{2}})),string(Squaring on both sides,), string(latex((5)^{2}+(-1)^{2} = (5)^{2}+(6-c)^{2})),string(latex(25+1 = 25+36-12c+c^{2} )), string(latex(c^{2}-12c +61 =26 )), string(latex(c^{2}-12c+35 =0)),string(latex(c^{2}-7c-5c+35=0)),string(latex((c-7)(c-5)=0)), string(latex(c=7~~) or latex(~~c=5)),string(If latex(c=7) then,), custom_evaluation_expression(lhs([string(latex(B C))]), rhs([string(latex(\\\\sqrt{(-3-(-8))^{2}+(6-7)^{2}})),  string(latex(\\\\sqrt{(5)^{2}+(-1)^{2}})),  string(latex(\\\\sqrt{25+1})),  string(latex(\\\\sqrt{26}) units)]),equating(latex(=))), custom_evaluation_expression(lhs([string(latex(AC))]), rhs([string(latex(\\\\sqrt{(2-(-8))^{2}+(5-7)^{2}})), string(latex(\\\\sqrt{(10)^{2}+(-2)^{2}})),  string(latex(\\\\sqrt{100+4})),  string(latex(2\\\\sqrt{26} ) units)]),equating(latex(=))),string(Also, latex(A B=\\\\sqrt{26}) units latex(\\\\qquad (A B=B C))), custom_evaluation_expression(lhs([string(latex(A B+B C))]), rhs([string(latex(\\\\sqrt{26}+\\\\sqrt{26})), string(latex(2 \\\\sqrt{26})), string(latex(AC))]),equating(latex(=))),string(So, for latex(c=7),  points latex(A),  latex(B) and latex(C) lie on a straight line.), string(Thus, latex(c=5) is the only possible value because other value of latex(c) can not satisfy the condition that points latex(A),  latex(B) and latex(C) are vertices of a quadrilateral.),string(Hence, the second option is correct.)]",
     "[string(Using the distance formula,), string(If latex((x_{1},y_{1})) and latex((x_{2},y_{2})) are two points then the distance between them is given by latex(\\\\sqrt{(x_{1}-x_{2})^{2}+(y_{1}-y_{2})^{2}}).), string(Here, the given points are latex(A(-6,-3)) and latex(C(-8,13)).), custom_evaluation_expression(lhs([string(The exact length of latex(A C))]), rhs([string(latex(\\\\sqrt{(-6-(-8))^{2}+(-3-13)^{2}} )),string(latex(\\\\sqrt{(2)^{2}+(-16)^{2}} )),string(latex(\\\\sqrt{4+256} )),string(latex(\\\\sqrt{260} ))]),equating(latex(=))),string(Thus, the exact length of latex(A C) is latex(\\\\sqrt{260}) units.)]",
     "[string(Let the speed of the faster train be latex(F) m/s and its length be latex(L) meters.),string(Let the speed of the slower train be latex(S) m/s and its length be latex(M) meters.),custom_evaluation_expression(lhs([string(latex(\\\\therefore \\\\dfrac{L+M}{F+S})),string(And, latex(\\\\dfrac{L}{F+S})),string(latex(\\\\therefore 1+\\\\dfrac{M}{L})),string(latex(\\\\Rightarrow M)),string(latex(\\\\Rightarrow M))]),rhs([string(latex(15\\\\qquad \\\\dotsc (i))),string(latex(7.75\\\\qquad \\\\dotsc (ii))),string(latex(\\\\dfrac{15}{7.75})),string(latex(\\\\dfrac{7.25}{7.75} \\\\times 248)),string(latex(232))]),equating(latex(=))),string(Hence, the second option is correct.)]",
     " [string(latex(\\\\def\\\\arraystretch{1.3} \\\\begin{array}{c}  ~~9~~9~~7~~1  \\\\\\\\  \\\\underline{-~4~~4~~9~~3~~} \\\\\\\\  ~~\\\\boxed{5~~4~~7~~8}   \\\\end{array}))]",
     "[string( Given, latex(T_{5}+T_{6}=0 )), string(latex(\\\\Rightarrow ~{ }^{n} C_{4} a^{n-4} b^{4} -{ }^{n} C_{5}a^{n-5} b^{5}=0)),string(latex(\\\\Rightarrow { }^{n} C_{4} a^{n-4} b^{4}= { }^{n} C_{5} a^{n-5} b^{5})), string(latex(\\\\Rightarrow \\\\dfrac{a}{b}=\\\\dfrac{{ }^{n} C_{5}}{{ }^{n} C_{4}}= \\\\dfrac{n-4}{5})),string(Hence, the first option is correct.)]",
     "[string(Clearly, latex(\\\\bigg(\\\\dfrac{1 - t^{10}}{1 - t}\\\\bigg)^{3} = (1 - t^{10})^{3}(1 - t)^{- 3})),string(latex(\\\\therefore) coefficient of latex(t^{7} ) in latex( (1 - t^{10})^{3}(1 - t)^{- 3})),string(latex(\\\\Rightarrow) coefficient of latex(t^{7}) in latex(\\\\lparen 1 - t^{30} - 3{t^{10}} + 3t^{20} \\\\rparen (1 - t)^{- 3})),string(latex(\\\\Rightarrow) coefficient of latex(t^{7}) in latex((1 - t)^{- 3})),string(latex(\\\\Rightarrow) latex(^{3 + 7 - 1}C_{7} = ^{9}C_{7} = 36 \\\\quad \\\\lparen \\\\because) coefficient of latex(x^{r}) in latex(\\\\lparen 1-x \\\\rparen^{-n} ~=~ ^{n+r-1}C_{r} \\\\rparen)),string(Hence, the fourth option is correct.)]",
     '''[string(Since, the general term in the expansion of binomial latex(\\\\left( \\\\sqrt{x} - \\\\dfrac{k}{{x^{3}}^{}} \\\\right)^{14}) is ),string(latex(T_{r + 1} = { }^{14}C_{r} x^{\\\\left( \\\\dfrac{14-r}{2} \\\\right)} ( - k)^{r } x^{- 3r} = { }^{14}C_{r}( - k)^{r}x ^{\\\\left( \\\\dfrac{14 - 7r}{2} \\\\right)})), string(latex(\\\\because) Term is constant, so latex(r = 2)), string(latex(\\\\therefore~{ }^{14}C_{2} {\\\\left( - k \\\\right)^{2}} = 364 \\\\implies\\\\dfrac{14\\\\times13}{2}k^{2} = 364)),string(latex(91k^{2} = 364)), string(latex(k^{2} = 4 )),string(latex(\\\\left| k \\\\right|= 2)),string(Hence, the first option is correct.)]''',
     "[string(The general term in the binomial expansion of latex((a+b)^{n}) is latex(T_{r+1}={ }^{n} C_{r} a^{n-r} b^{r}).), string(So, the general term in the binomial expansion of latex(\\\\left(17^{\\\\frac{1}{3}}-15^{\\\\frac{1}{12}} \\\\right)^{84}) is), custom_evaluation_expression(lhs([string(latex(T_{(r+1)}))]), rhs([string(latex({ }^{84} C_{r}\\\\left(17^{\\\\frac{1}{3}}\\\\right)^{84-r}\\\\left(-15^{\\\\frac{1}{12}}\\\\right)^{r})), string(latex({ }^{84} C_{r} ~ 17^{\\\\frac{84-r}{3}}(-1)^{r} ~ 15^{\\\\frac{r}{12}})), string(latex((-1)^{r} ~ { }^{84} C_{r} ~ 17^{28-\\\\frac{r}{3}} ~ 15^{\\\\frac{r}{12}}))]),equating(latex(=))),string(The possible non-negative integral values of 'latex(r)' for which latex(\\\\dfrac{r}{3}) and latex(\\\\dfrac{r}{12}) are integer, where latex(r \\\\leq 84),  are latex(r=0),  latex(12),  latex(24),  latex(36),  latex(......),  latex(84).),string(latex(\\\\therefore) There are latex(8) rational terms in the binomial expansion and remaining latex(85- 8=77) terms are irrational terms.),string(Hence, the first option is correct.)]",
     "[string(We have,),string(latex(\\\\lparen x+ 25 \\\\rparen^{60} +\\\\lparen x- 25 \\\\rparen^{60} = a_{0}+a_{1} x+a_{2} x^{2} +..... . .+ a_{60} x^{60} )),string(latex(\\\\therefore a_{0}+a_{1} x+a_{2} x^{2} +..... . .+ a_{60} x^{60} )),string(latex(= \\\\lbrack \\\\lparen ^{60}C_{0} x^{60} + ^{60}C_{1} x^{59} 25 + ^{60}C_{2} x^{58} 25^{2} + \\\\dots + ^{60}C_{60} 25^{60} \\\\rparen + \\\\lparen ^{60}C_{0} x^{60} - ^{60}C_{1} x^{59} 25 + ^{60}C_{2} x^{58} 25^{2} - \\\\dots + ^{60}C_{60} 25^{60} \\\\rparen \\\\rbrack)),string(latex(= 2 \\\\lbrack ^{60}C_{0} x^{60} + ^{60}C_{2} x^{58} \\\\cdot 25^{2} + ^{60}C_{4} x^{56} \\\\cdot 25^{4} + \\\\dots + ^{60}C_{60} \\\\cdot  25^{60} \\\\rbrack )),string(By comparing coefficients, we get),string(latex( a_{8} = 2 ^{60}C_{52} \\\\lparen 25 \\\\rparen ^{52};~ a_{6} = 2 ^{60}C_{54} \\\\lparen 25 \\\\rparen^{54} ) ),evaluation_expression(lhs([string(latex(\\\\dfrac{a_{8}}{a_{6}}))]),rhs([string(latex( \\\\dfrac{2 \\\\lparen ^{60}C_{8} \\\\rparen \\\\lparen 25 \\\\rparen^{52}}{2 \\\\lparen ^{60}C_{6} \\\\rparen \\\\lparen 25 \\\\rparen ^{54}} = \\\\dfrac{2 \\\\cdot 60\\\\cdot59\\\\cdot58\\\\cdot57\\\\cdot56\\\\cdot55\\\\cdot54\\\\cdot53 \\\\cdot \\\\lparen 25 \\\\rparen^{52} \\\\cdot 1\\\\cdot2\\\\cdot3\\\\cdot4\\\\cdot5\\\\cdot6 }{1\\\\cdot2\\\\cdot3\\\\cdot4\\\\cdot5\\\\cdot6\\\\cdot7\\\\cdot8 \\\\cdot 2 \\\\cdot  60\\\\cdot59\\\\cdot58\\\\cdot57\\\\cdot56\\\\cdot55 \\\\cdot \\\\lparen 25 \\\\rparen ^{54} } \\\\quad \\\\lbrack \\\\because~ ^{60}C_{52} ~=~  ^{60}C_{8}) and latex(^{60}C_{54} ~=~ ^{60}C_{6} \\\\rbrack)),string(latex(\\\\dfrac{60\\\\times59\\\\times58\\\\times57\\\\times56\\\\times55\\\\times54\\\\times53 \\\\times \\\\lparen 25 \\\\rparen^{52} \\\\times 1\\\\times2\\\\times3\\\\times4\\\\times5\\\\times6 }{1\\\\times2\\\\times3\\\\times4\\\\times5\\\\times6\\\\times7\\\\times8 \\\\times 60\\\\times59\\\\times58\\\\times57\\\\times56\\\\times55 \\\\times \\\\lparen 25 \\\\rparen ^{54} } = \\\\dfrac{2558620845 }{50063860 \\\\times 25^{2} }  = 0.08))])),string(Hence, the fourth option is correct.)]",
     "[string(The amount of markup can be found with the following equation.),string(Markup rate latex(\\times) wholesale price latex(=) amount of markup),string(Since markup rate is a percentage, we have to convert it into a decimal first.),string(So, latex(45 \\%=\\dfrac{45}{100}=0.45)),string(Now, using the formula and substituting the values, we get latex(0.45 \\times \\$ 113=\\$ 50.85)),string(Therefore, the amount of markup on the headphones is latex(\\$ 50.85).)]",
     "[string(The amount of markdown can be found with the following equation.),string(Markdown rate latex(\\times) original price latex(=) amount of markdown),string(Since the markdown rate is a percentage, we have to convert it into a decimal first.),string(So, latex(20 \\%=\\dfrac{20}{100}=0.20)),string(Now, using the formula and substituting the values, we get latex(0.20 \\times \\$ 18=\\$ 3.60)),string(Therefore, the amount of markdown for the book is latex(\\$ 3.60).)]",
     "[string(To find the amount of commission made, use the following formula Commission rate latex(\\times) retail price latex(=) amount of commission made Since the commission rate is a percentage, we have to convert it into a decimal first. So, latex(6 \\%=\\dfrac{6}{100}=0.06)),string(Now, using the formula and substituting the values, we get latex(0.06 \\times \\$ 764=\\$ 45.84)),string(Therefore, the amount of commission Sophia makes by selling a computer is latex(\\$ 45.84).)]",
     "[,string(We have to convert the percentage of tax into a decimal first.),string(latex(4.6 \\%=\\dfrac{4.6}{100}=0.046)),string(latex(3.65 \\%=\\dfrac{3.65}{100}=0.0365)),string(Since both sales tax rates apply to latex(\\$ 220), we can add the two rates.),string(latex(0.046+0.0365=0.0825)),string(latex(0.0825 \\times \\$ 220=\\$ 18.15)),string(Emma pays latex(\\$ 18.15) in sales tax for her smartwatch purchase.),]",
     ]

print(constraintSolver(specific_string_arr[4],generic_string_arr[4]))

  