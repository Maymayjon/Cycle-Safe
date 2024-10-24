import math
import numpy as np
from scipy.stats import linregress

class car_coord:
    def __init__ (self, x, y, w, h, age=0, increasing = False, color=(255,255,255), name = "Unnamed"):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.age = age
        self.increasing = increasing
        self.last_update = age
        self.history = {
            age:(x,y,w,h)
        }
        self.color = color
        self.name = name



    def __str__ (self):
        return f"C:({self.x},{self.y})\nw: {self.w} \nh:{self.h} \na:{self.age}"


    def get_box(self):
        return (self.x, self.y, self.w, self.h)


    def incr_age(self):
        self.age += 1


    def set_coord(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.history[self.age] = (x, y, w, h)
        self.last_update=self.age


    def print_history(self):
        keys = list(self.history.keys())
        keys.sort()
        for k in keys:
            print(k, ":", self.history[k])

    def compare(self, other_x, other_y, other_w, other_h, radius =25):
        if(self.contains(other_x, other_y, other_w, other_h)):
            return True
        d = math.sqrt((self.x-other_x)**2+(self.y-other_y)**2)
        return d<=radius
    
    def contains(self, other_x, other_y, other_w, other_h):
        left = self.x - self.w//2
        right = self.x + self.w//2
        top = self.y - self.h//2
        bottom = self.y + self.h//2

        # other_left = other_x - other_w//2
        # other_right = other_x + other_w//2
        # other_top = other_y - other_h//2
        # other_bottom = other_y + other_h//2

        
        return left <= other_x and right >= other_x and top <= other_y and bottom >= other_y
            

    #
    # def check_increasing(self):
    #     wa = 0
    #     ha = 0
    #     for h in self.history:
    #         l = list(self.history[h])
    #         wa+=l[2]
    #         ha+=l[3]
    #     wa = wa/len(self.history)
    #     ha = ha/len(self.history)
    #     start_term = list(self.history[0])
    #     # print("increasing")
    #     if wa-start_term[2]>5 and ha-start_term[3]>5:
    #         print("increasing")


    def check_increasing(self):

        # Create an array of indices to use as x values
        size = []

        for h in self.history:
            l = list(self.history[h])
            size.append(l[2]*l[3])



        sizes = np.arange(len(size))


        # Perform linear regression
        slope, intercept, r_value, p_value, std_err = linregress(sizes, size)
        sizet = slope > 1

        # slope, intercept, r_value, p_value, std_err = linregress(hx, ha)
        # ht = slope > 0

        if sizet:
            self.increasing = True
        else:
            self.increasing = False


#
# c1= car_coord(2, 3, 3, 2)
#
# print(c1)
# c1.incr_age()
# print(c1)
# c1.print_history()
# print("--")
#
# c1.set_coord(6,4,4,4)
# c1.print_history()
# c1.incr_age()
#
# print("--")
#
# c1.set_coord(4,3,5,6)
# c1.print_history()
# c1.incr_age()
#
# print("--")
# # print(c1.compare(100,100))
# # print(c1.compare(5,5))
#
#
# c1.set_coord(4,3,5,6)
# c1.print_history()
# c1.incr_age()
#
# print("--")
#
#
# c1.set_coord(4,3,5,6)
# c1.print_history()
# c1.incr_age()
#
# print("--")
#
#
# c1.check_increasing()






# Example usage
# numbers = [1, 2, 3, 4, 5]
# print(has_increasing_trend(numbers))  # Output: True
#
# numbers = [1, 3, 2, 4, 5]
# print(has_increasing_trend(numbers))  # Output: True
#
# numbers = [5, 4, 3, 2, 1]
# print(has_increasing_trend(numbers))  # Output: False