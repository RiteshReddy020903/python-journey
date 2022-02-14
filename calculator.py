# -*- coding: utf-8 -*-
"""
Created on Mon Feb 14 15:12:33 2022

@author: RITESH REDDY
"""

first = input("Enter first number : ")
second = input("Enter second number : ")
first = int(first)
second = int(second)
print("----press keys for operator (+,-,*,/,%)----------")
operator = input("Enter operator : ")

if operator == "+":
   print(first + second)
elif operator == "-":
   print(first - second)
elif operator == "*":
   print(first * second)
elif operator == "/":
   print(first / second)
elif operator == "%":
   print(first % second)
else:
   print("Invalid Operation")
