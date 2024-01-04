class Height(object):
  def __init__(self, feet, inches):
    self.feet = feet
    self.inches = inches

  # the following method will override the str() method for object
  # and replace "<__main__.Height object at 0x000001E6A7AAE790>" by
  # whatever we want to be more readable.
  def __str__(self):
    output = str(self.feet) + " feet and " + str(self.inches) + " inches."
    return output
  
  def __add__(self, other):
    # convert heights in inches
    a_height_inches = (self.feet * 12) + self.inches
    b_height_inches = (other.feet * 12) + other.inches

    # Adding a + b
    sum_height = a_height_inches + b_height_inches

    # Convert to feet and inches
    sum_height_feet = sum_height // 12
    sum_height_inches = sum_height - (sum_height_feet * 12)

    # Return output as new object
    output = Height(sum_height_feet, sum_height_inches)
    return output

  def __sub__(self, other):
    # convert heights in inches for self
    a_total_inches = (self.feet * 12) + self.inches

    # convert heights in inches for other
    b_total_inches = (other.feet * 12) + other.inches

    # Substract a - b
    total_height_inches = a_total_inches - b_total_inches

    # Convert to feet and inches
    total_height_feet = (total_height_inches // 12)
    total_height_inches = total_height_inches - (total_height_feet * 12)

    # return total as new object
    output = Height(total_height_feet, total_height_inches)
    return output
  
  def __lt__(self, other):
    # convert in inches
    a_total_inches = (self.feet * 12) + self.inches
    b_total_inches = (other.feet * 12) + other.inches
    # compare and return true or false 
    return a_total_inches < b_total_inches
  
  def __le__(self, other):
    # convert in inches
    a_total_inches = (self.feet * 12) + self.inches
    b_total_inches = (other.feet * 12) + other.inches
    # compare and return true or false 
    return a_total_inches <= b_total_inches
  
  def __gt__(self, other):
    # Convert into inches
    a_total_inches = (self.feet * 12) + self.inches
    b_total_inches = (other.feet * 12) + other.inches
    # Compare and return true or false
    return a_total_inches > b_total_inches
  
  def __ge__(self, other):
    # Convert into inches
    a_total_inches = (self.feet * 12) + self.inches
    b_total_inches = (other.feet * 12) + other.inches
    # Compare and return true or false
    return a_total_inches >= b_total_inches
  
  def __eq__(self, other):
    # Convert to inches
    a_total_inches = (self.feet * 12) + self.inches
    b_total_inches = (other.feet * 12) + other.inches
    # Compare and return True or False
    return a_total_inches == b_total_inches
  
  def __ne__(self, other):
    # Convert to inches
    a_total_inches = (self.feet * 12) + self.inches
    b_total_inches = (other.feet * 12) + other.inches
    # Compare and return True or False
    return a_total_inches != b_total_inches
  


tom_height = Height(5, 10)
bob_height = Height(5, 10)

print("Tom's height = ", tom_height)
print("Bob's height = ", bob_height)
print("Tom + Bob's heights = ", tom_height + bob_height)
print("Tom - Bob's heights = ", tom_height - bob_height)
print(tom_height < bob_height)
print(tom_height > bob_height)
print(tom_height == bob_height)

print("")
print("Practice 3 test results...")
print(Height(4, 6) > Height(4, 5))
print(Height(4, 5) >= Height(4, 5))
print(Height(5, 9) != Height(5, 10))
print('')

print("Test sorted....")
a = Height(4, 10)
b = Height(5, 6)
c = Height(7, 1)
d = Height(5, 5)
e = Height(6, 7)
f = Height(5, 6)

heights = [a, b, c, d, e, f]

heights = sorted(heights, reverse=True)
for height in heights:
    print(height)


