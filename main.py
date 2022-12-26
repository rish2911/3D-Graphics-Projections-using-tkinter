import draw_utils as draw
import sys
import os

if __name__ == "__main__":
    
        # main function to take the file path and implementation to be run
        try:
            user_input = input("Enter the path of your file with extension: \n")
            part = int(input("Which part of the assessment do you want to see? , press 1 or 2 \n"))
            if part==1:
                dummy = draw.DrawPolygon(user_input)
            elif part==2:
                dummy = draw.ColourPolygon(user_input)
            else:
                print("Wrong input, press 1 or 2, \n")
                sys.exit(1)

        except:
            print('Wrong input try again \n')