use context essentials2021
import s-exp as S

# A small expression-language interpreter developed as programming-languages
# coursework. The surface language supports arithmetic, equality, and if.
# Function values and applications are represented directly in the core AST.

data BinOpC:
  | plus-op-c
  | multiply-op-c
  | equal-op-c
end


data ExprC:
  | true-c
  | false-c
  | number-c(value :: Number)
  | binary-c(op :: BinOpC, left :: ExprC, right :: ExprC)
  | if-c(condition :: ExprC, then-branch :: ExprC, else-branch :: ExprC)
  | id-c(name :: String)
  | app-c(function :: ExprC, arguments :: List<ExprC>)
  | function-c(arguments :: List<String>, body :: ExprC)
end


data BinOpExt:
  | plus-op
  | multiply-op
  | equal-op
  | minus-op
end


data ExprExt:
  | true-ext
  | false-ext
  | number-ext(value :: Number)
  | binary-ext(op :: BinOpExt, left :: ExprExt, right :: ExprExt)
  | if-ext(condition :: ExprExt, then-branch :: ExprExt, else-branch :: ExprExt)
end


fun parse(expression :: S.S-Exp) -> ExprExt:
  cases (S.S-Exp) expression:
    | s-num(value) => number-ext(value)
    | s-sym(symbol) =>
      if symbol == "true":
        true-ext
      else if symbol == "false":
        false-ext
      else:
        raise("parse: unknown symbol")
      end
    | s-list(items) =>
      cases (List) items:
        | empty => raise("parse: empty expression")
        | link(operator, arguments) =>
          if arguments.length() < 2:
            raise("parse: expected at least two arguments")
          else:
            left = arguments.get(0)
            right = arguments.get(1)
            if operator.s == "+":
              binary-ext(plus-op, parse(left), parse(right))
            else if operator.s == "*":
              binary-ext(multiply-op, parse(left), parse(right))
            else if operator.s == "-":
              binary-ext(minus-op, parse(left), parse(right))
            else if (operator.s == "==") or (operator.s == "is"):
              binary-ext(equal-op, parse(left), parse(right))
            else if operator.s == "if":
              if arguments.length() == 3:
                if-ext(parse(left), parse(right), parse(arguments.get(2)))
              else:
                raise("parse: if expects three arguments")
              end
            else:
              raise("parse: unknown operator")
            end
          end
      end
    | else => raise("parse: unsupported expression")
  end
end


fun desugar(expression :: ExprExt) -> ExprC:
  cases (ExprExt) expression:
    | true-ext => true-c
    | false-ext => false-c
    | number-ext(value) => number-c(value)
    | binary-ext(operator, left, right) =>
      cases (BinOpExt) operator:
        | plus-op => binary-c(plus-op-c, desugar(left), desugar(right))
        | multiply-op => binary-c(multiply-op-c, desugar(left), desugar(right))
        | equal-op => binary-c(equal-op-c, desugar(left), desugar(right))
        | minus-op =>
          binary-c(
            plus-op-c,
            desugar(left),
            binary-c(multiply-op-c, number-c(-1), desugar(right)))
      end
    | if-ext(condition, then-branch, else-branch) =>
      if-c(desugar(condition), desugar(then-branch), desugar(else-branch))
  end
end


data Value:
  | number-v(value :: Number)
  | boolean-v(value :: Boolean)
  | closure-v(function :: ExprC%(is-function-c), environment :: List<Binding>)
end


data Binding:
  | binding(name :: String, value :: Value)
end


type Environment = List<Binding>
empty-environment = empty


fun lookup(name :: String, environment :: Environment) -> Value:
  cases (List) environment:
    | empty => raise("lookup: unknown identifier")
    | link(first, rest) =>
      if first.name == name:
        first.value
      else:
        lookup(name, rest)
      end
  end
end


fun extend-many(names :: List<String>, values :: List<Value>, environment :: Environment) -> Environment:
  cases (List) names:
    | empty =>
      cases (List) values:
        | empty => environment
        | else => raise("application: too many values")
      end
    | link(name, remaining-names) =>
      cases (List) values:
        | empty => raise("application: too few values")
        | link(value, remaining-values) =>
          link(
            binding(name, value),
            extend-many(remaining-names, remaining-values, environment))
      end
  end
end


fun numeric-operation(
    operation :: (Number, Number -> Number),
    left :: ExprC,
    right :: ExprC,
    environment :: Environment) -> Value:
  left-value = interpret(left, environment)
  right-value = interpret(right, environment)
  if is-number-v(left-value) and is-number-v(right-value):
    number-v(operation(left-value.value, right-value.value))
  else:
    raise("operation: expected numbers")
  end
end


fun equality-operation(left :: ExprC, right :: ExprC, environment :: Environment) -> Value:
  left-value = interpret(left, environment)
  right-value = interpret(right, environment)
  if is-number-v(left-value) and is-number-v(right-value):
    boolean-v(left-value.value == right-value.value)
  else:
    raise("equality: expected numbers")
  end
end


fun interpret(expression :: ExprC, environment :: Environment) -> Value:
  cases (ExprC) expression:
    | true-c => boolean-v(true)
    | false-c => boolean-v(false)
    | number-c(value) => number-v(value)
    | binary-c(operator, left, right) =>
      cases (BinOpC) operator:
        | plus-op-c => numeric-operation(lam(x, y): x + y end, left, right, environment)
        | multiply-op-c => numeric-operation(lam(x, y): x * y end, left, right, environment)
        | equal-op-c => equality-operation(left, right, environment)
      end
    | if-c(condition, then-branch, else-branch) =>
      condition-value = interpret(condition, environment)
      if is-boolean-v(condition-value):
        if condition-value.value:
          interpret(then-branch, environment)
        else:
          interpret(else-branch, environment)
        end
      else:
        raise("if: condition must be Boolean")
      end
    | id-c(name) => lookup(name, environment)
    | function-c(_, _) => closure-v(expression, environment)
    | app-c(function, arguments) =>
      function-value = interpret(function, environment)
      if is-closure-v(function-value):
        argument-values = arguments.map(lam(argument): interpret(argument, environment) end)
        call-environment = extend-many(
          function-value.function.arguments,
          argument-values,
          function-value.environment)
        interpret(function-value.function.body, call-environment)
      else:
        raise("application: expected a function")
      end
  end
end


fun run(source :: String) -> Value:
  interpret(desugar(parse(S.read-s-exp(source))), empty-environment)
end


check:
  run("(+ 23 (* 5 6))") is number-v(53)
  run("(- 10 3)") is number-v(7)
  run("(== 4 4)") is boolean-v(true)
  run("(if (== 2 3) 10 20)") is number-v(20)

  add-two = function-c(
    [list: "left", "right"],
    binary-c(plus-op-c, id-c("left"), id-c("right")))
  interpret(
    app-c(add-two, [list: number-c(1), number-c(2)]),
    empty-environment) is number-v(3)

  weighted-sum = function-c(
    [list: "x", "y", "weight"],
    binary-c(
      plus-op-c,
      id-c("x"),
      binary-c(multiply-op-c, id-c("y"), id-c("weight"))))
  interpret(
    app-c(weighted-sum, [list: number-c(1), number-c(2), number-c(3)]),
    empty-environment) is number-v(7)
end
