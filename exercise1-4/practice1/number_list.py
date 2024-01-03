
with open('number_list.txt', 'w') as my_file:
  number_list=[f"{n}\n" for n in range(50,101)]
  my_file.writelines(number_list)
  
with open('number_list.txt', 'r') as my_file: 
  print(my_file.readlines())