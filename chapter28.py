#wrapper

# def extragreeting(func):
#   def wrapper():
#     print("hello from NYC team")
#     func()
#     print("thankyou viisit again")

#   return  wrapper

# @extragreeting
# def greetings():
#   print("good morning")

# greetings()

#args and **kwargs
# def addition(a , b):
#   return a + b

# print(addition(20 , 30 , 40)) #gives error

#args
# def addition(*args):
#   s = 0
#   for i in args:
#     s = s + i
#   return s

# print(addition(20 , 30 , 50 , 39 , 5 , 78,  0,  78 ,6))

# def info(**kwargs):
#   return kwargs

# print(info(name = "Akarsh" , age = 24 , profession = "Data scientist"))


# def extragreeting(func):
#   def wrapper(*args , **kwargs):
#     print("hello from NYC team")
#     func(*args , **kwargs)
#     print("thankyou viisit again")

#   return  wrapper

# @extragreeting
# def addition(*args):
#   s = 0
#   for i in args:
#     s = s + i

#   print(s)

# addition(20 , 3  , 8 ,  5 , 6 , 8 , 8  , 3)

#one liner if else statement
# a = 20 

# # if a % 2 == 0:
# #   print("even")
# # else:
# #   print("odd")

# #ternary operation
# print("even number") if a % 2 == 0 else print("odd number")

#List comprehension
# a = [1 , 2 , 3 , 4 , 5 , 6 , 7 , 8 , 9 , 12 , 13]

# b = [i for i in a if i % 2 == 0]

# # for i in a:
# #   if i % 2 == 0:
# #     b.append(i)

# print(b)

#lambda function

# def check(a):
#   if a % 2 == 0:
#     print("even number")
#   else:
#     print("odd number")

# check(12)

# check = lambda x: print("even") if x % 2 == 0 else print("odd number")
# check(12)

# addition = lambda a,b : print(a + b)
# addition(10 , 20)

#map

# a = ["Sarthak" , "harsh" , "vedant" , "Akarsh"]

# lengths = list(map(len , a))
# print(lengths)

# temp_cel = [0 , 20 , 30 , 35]

# # def converter(a):
# #   far = (a * 9/5) + 32
# #   return far

# #temp_far = list(map(converter , temp_cel))
# temp_far = list(map(lambda x : (x * 9/5) + 32 , temp_cel))
# print(temp_far)  

#filter
# m = [35 , 80 , 80 , 21 , 12 , 45 , 78]

# passed = list(filter(lambda x : x >= 40 , m))
# #passed = list(map(lambda x : x >= 40 , m)) #returns list in true and false : [False, True, True, False, False, True, True]

# print(passed)

#zip

name = ['sarthak' , "Akarsh" , "harsh" , "vedant"]

marks = [12 , 90 , 42 , 6]

result = list(zip(name , marks))
print(result)