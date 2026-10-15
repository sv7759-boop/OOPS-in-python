# class car:
#   a = 12 #attribute

#   def hello():
#     print("how are you") #Method

# #you can acess attribute and
# #methods after acessing the class

# print(car.a) #acessing attribute
# car.hello()  #accesing methods

# class Bags:
#   name = "NotYourCollege"

#   def details(self):
#     print("This is the company who creates bag")

# reebok = Bags() #object
# campus = Bags() #object

# print(reebok.name)
# print(campus.name)

# reebok.details()

# class Bags:
#   def __init__(self , material , zips , pockets):
#     self.material = material
#     self.zips = zips
#     self.pockets = pockets

# reebok = Bags("leather" , 3 , 2)
# campus = Bags("polyster" , 2 , 3)

# print(reebok.material)
# print(campus.material)

#types of attributes and methods

# class Animal:
#   a = 12 #class attribute

#   def __init__(self , name):
#       self.name = name #object/instance attribute

#   def hello(self): #instance/object method , captures the location of obj
#     print(f"how are you my name is {self.name}")

#   @classmethod
#   def details(cls): #class method , captures location of class
#      print(f"how are you my number is {cls.a}")

#   @staticmethod
#   def speak():
#      print("hello how are you I am a static method")

# obj = Animal("lion")
# obj.name = "Tiger"

# print(obj.name)

# obj.details()

# obj.speak()


#inheritance
# class Animal: #parent class
#    a = 12
   
#    def __init__(self , name):
#       self.name = name

#    def details(self):
#       print(f"hello your name is {self.name}")

# class Humans(Animal): #child class
#    pass

# obj = Animal("lion")

# obj2 = Humans("Harsh")
# obj2.details()
# print(obj2.a)

# #your child class object has all the powers to acess
# #the attribute of parent class


#multilevel inheritance
# class BagFactory:
#   def __init__(self , material , zips ,  pockets):
#     self.material = material
#     self.zips = zips
#     self.pockets = pockets

#   def details(self):
#     print("Your bag details are :")
#     print(self.material)
#     print(self.zips)
#     print(self.pockets)

# class Reebok(BagFactory):
#   def __init__(self, material, zips, pockets , color):
#     super().__init__(material, zips, pockets)
#     self.color = color

#   def details(self):
#     print(self.color)
#     return super().details()

# class Campus(Reebok):
#   def __init__(self, material, zips, pockets, color , size):
#     super().__init__(material, zips, pockets, color)
#     self.size = size
  
# bag1 = BagFactory("leather" , 3 , 4)
# bag2 = Reebok("polyster" , 4 , 2 , "Blue")

#multiple inheritance

# class Animal:
#   def __init__(self , name):
#     self.name = name

# class Humans:
#   def __init__(self , id):
#     self.id = id

# class Robots(Humans , Animal):
#   def __init__(self, id , name):
#     Humans.__init__(id)
#     Animal.__init__(name)


# robo = Robots(12 , "Akshay")

# polymorphism

# def hello():
#   print("how are you ")

# def hello():
#   print("What are you doing")

# hello()

# class animal:
#   def speak(self):
#     print('Animals will not speak')

# class humans:
#   def speak(self):
#     print("we are humans we can speak")

# obj = animal()

# obj2 = humans()

# obj.speak()
# obj2.speak()

#Ways to achive polymorphism in python

#method overriding (we need inheritance)

# class Animal:
#   a = 12
#   def __init__(self , name):
#     self.name = name

#   def details(self):
#     print(f"Your name is {self.name}")

# class Humans(Animal):
#   b = 12
#   def __init__(self, name):
#     super().__init__(name)

#   def details(self):
#     print(f"your info is {self.name} and this is all we have")


# obj = Humans("harry")

# obj.details()

#when we are doing inheritance and parent and child classes have same method name so the child class method will override your parent class method

#method overloading
#method overloading does not exist in python

# class hello:
#   def speak(self , a):
#     print(f"how are you")

#   def speak(self , a , b):
#     print("how are you")

#in python 2nd function overrides the 1st function

#encapsulation


# class Factory:
# #  __name = "kia" #private class attributr
#   a = 12 #public class attribute
# # we use ( __ ) to make any attribute private that it can not be accesed or changed directly . it can be acessed or modified through method.


#   def __init__(self , type , tyre , color):
#     self.type = type  #public object attritude
#     self.__tyre = tyre #private object attribute
#     self.color = color

#   def __detail(self):
#     print("hello your details are : ")

# class hello(Factory):
#   print(Factory.a)



# obj = Factory("sedan" , "MRF" , "black")

#calling private attribute by  calling the attribute in class method and
# then calling the method by creating the object

# class hello:
#   __a = 12

#   @classmethod
#   def info(cls):
#     print(cls.__a)

# obj = hello()

# obj.info()

#abstraction

# from abc import ABC , abstractmethod

# class enforce(ABC):
#   @abstractmethod
#   def enginestart():
#     pass

# class bike(enforce):
#   def enginestart():
#       pass

# class car(enforce):
#   def enginestart():
#       pass


# class trucks:
#   pass

# obj1 = bike()
# obj2 = car()
# obj3 = trucks()

#Dunder methods

# class Animal:
#   def __init__(self , name):
#     self.name = name

#   def __str__(self):
#     return f"hello my name is {self.name}"

# obj = Animal("Lion")
# obj2 = Animal("Giraffe")
# print(obj2)

# class numbers:
#   def __init__(self , num):
#     self.num = num

#   def __add__(self , other):
#     return self.num + other.num

#   def __eq__(self, value):
#     return self.num == value.num
  
# num1 = numbers(20)
# num2 = numbers(30)

# print(num1 + num2 )

# a = 12
# b = 12

# print(a + b)
# print(type(a))

# print(dir(int))
