# print('Welcome to the Addition or substraction Script...')

a = float(input('Please enter the first number : '))
b = float(input('Please enter the second number : '))
sign = input('Please enter + or - : ')

if sign == '+':
  print('The Total is : '+ str(a+b))
elif sign == "-":
  print('The Total is : '+ str(a-b))
else:
  print('Incorrect entry. Sorry.')

