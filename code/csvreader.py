"""
    
"""

import csv
from area import area

def main():
    
    new_area = area()
    empty_area = new_area.area

    with open('wijk1.csv') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            bottom,left = row['bottom_left_xy'].split(",")
            top,right  = row['top_right_xy'].split(",")
            print(f"{bottom} , {left} - {top} , {right}")

            for i range(bottom,top):
                for j range(left,right):
                    empty_area = empty_area[i][j]


    # print(empty_area)



if __name__ == "__main__":
    main()