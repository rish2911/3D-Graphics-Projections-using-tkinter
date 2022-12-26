from tkinter import *
import numpy as np
import math as mp
import import_object as io

"""Assume that the observer is an infinite distance from the canvas. = Orthographic Projections"""

class MatrixTransformations():
    """
    Base Class for 3D consrtruction and transformations (rotation plus translation)
    """ 
    def __init__(self):
        #empty constructor can be used in future
        pass
    
    # function to translate given points using given inputs
    def translation(self, x:float, y:float, x_delta:float, y_delta:float)->float:
        return x+x_delta, y+y_delta

    # function to multiply given list of matrices (used in calculating 3D rotations)
    def mat_mul(self, list_of_mat:list)->np.array:
        dummy = np.eye(list_of_mat[0].shape[0], list_of_mat[0].shape[1])
        for i in list_of_mat:
            dummy = np.dot(dummy,i)
        return dummy

    # 3D rotation matrix with default angle parameters as zeros
    def rotation_matrix(self, ang_x:float=0, ang_y:float=0, ang_z:float=0, input:np.array=None)->mat_mul:
        rot_matrix_x = np.array([[1, 0, 0],
                     [0, mp.cos(ang_x), -mp.sin(ang_x)], 
                    [0, mp.sin(ang_x), mp.cos(ang_x)]])
        
        rot_matrix_y = np.array([[mp.cos(ang_y), 0, mp.sin(ang_y)], 
                        [0, 1, 0], 
                        [-mp.sin(ang_y), 0, mp.cos(ang_y)]])

        rot_matrix_z = np.array([[mp.cos(ang_z), mp.sin(ang_z), 0],
                        [-mp.sin(ang_z), mp.cos(ang_z), 0], 
                        [0, 0, 1]])
        
        rot_mat = [rot_matrix_x, rot_matrix_y, rot_matrix_z, input]
        
        return self.mat_mul(rot_mat)


class DrawPolygon(MatrixTransformations):
    """
    Child class for creating a polygon using mathematical transformations
    """ 
    def __init__(self, path:str)->None:
      
    
        #calling the required functions to draw polygon
        self.initialise_poly(path)
        self.get_polygon(self.poly_.edges_)
        self.mouse_binder(self.poly_.edges_)
        self.root_.mainloop()

    def initialise_poly(self, path:str)->None:
          # object of import data class with required data       
        self.poly_ = io.import_object(path)
        #base class constructor initialisation by default(no usage in this case)
        super().__init__()
        # object of tkinter library
        self.root_ = Tk()
        self.window_ = None
        self.vertices_ = None
        self.vertices_ = np.transpose(self.poly_.coordinates_)

        #reference for mouse initial location
        self.x_last = 0
        self.y_last = 0
        #lambda function for scaling angles of rotation
        self.multiple = lambda d: d*0.01

        # colecting screen size to scale object dimensions
        self.height_ = self.root_.winfo_screenheight()
        self.width_ = self.root_.winfo_screenwidth()
        self.get_windows()
        self.scale_ = self.get_scale()
    
    #creating and unpacking the canvas according to screen size
    def get_windows(self)->None:
        self.window_ = Canvas(self.root_, width=self.width_, height=self.height_, background='white', confine=True)
        self.window_.pack()
    
    # function to calculate scale
    def get_scale(self)->None:
        w = self.window_.winfo_reqwidth()
        h = self.window_.winfo_reqheight()
        j = 0
        scale = (w+h)/2 #default scale

        #finds the number of iterations depending upon the largest coordinate value
        iterations = int(np.max(np.abs(self.vertices_[:2,:]))/2)
        for k in range(iterations+1):
            for i in range(len(self.vertices_[0])):
                        # checking if the current scale sends any of the coordinate outside the frame
                        if scale*self.vertices_[0][i]>w or scale*self.vertices_[1][i]>h or scale*self.vertices_[0][i]<0 or scale*self.vertices_[1][i]<0:
                            j+=2
                            scale = (w+h)/((2*j))
        return scale

    #method to actually create the polygon
    def get_polygon(self, arg:list)->None:
        #deleting the previous points/lines
        self.window_.delete(ALL)

        # getting the width and height for translating the top left (0,0) to center of canvas
        width, height = self.window_.winfo_reqwidth()/2, self.window_.winfo_reqheight()/2      
        
        # translation of vertices and drawing lines using create line function in tkinter canvas (code referenced from examples)
        for i in range(len(arg)):
            self.window_.create_line(self.translation(self.scale_*self.vertices_[0][arg[i][0]], self.scale_*self.vertices_[1][arg[i][0]], width, height), \
                self.translation(self.scale_*self.vertices_[0][arg[i][1]], self.scale_*self.vertices_[1][arg[i][1]], width, height),fill = 'blue')

            self.window_.create_oval(self.translation(self.scale_*self.vertices_[0][arg[i][0]], self.scale_*self.vertices_[1][arg[i][0]], width, height), \
                self.translation(self.scale_*self.vertices_[0][arg[i][0]], self.scale_*self.vertices_[1][arg[i][0]], width, height), outline='blue', width=5)

            self.window_.create_oval(self.translation(self.scale_*self.vertices_[0][arg[i][1]], self.scale_*self.vertices_[1][arg[i][1]], width, height), \
                self.translation(self.scale_*self.vertices_[0][arg[i][1]], self.scale_*self.vertices_[1][arg[i][1]], width, height), outline='blue', width=5)

    #function to locating the mouse coordinates using binder
    def get_mousecoordinates(self, event:Event)->None:
        self.x_last = event.x
        self.y_last = event.y

    # function to calculate the difference in mouse motion
    def get_mousemovement(self, event:Event, arg:list)->None:
        x_change = self.y_last - event.y 
        y_change = self.x_last - event.x

        # transforming vertices with the calculated changes in x and y 
        self.vertices_ = self.rotation_matrix(ang_x=self.multiple(-x_change), ang_y = self.multiple(y_change), input= self.vertices_)
        # re-drawing polygon with new points
        self.get_polygon(arg)
        # getting mouse coordinates again to recalculate motion
        self.get_mousecoordinates(event)

    # function to bind mouse to get the coordinates and its chnage in motion (a set of callback functions)
    # referenced from tkinter tutorial
    def mouse_binder(self, edge:list)->None:
        self.window_.bind("<Button-1>", self.get_mousecoordinates)
        self.window_.bind("<B1-Motion>", lambda event, arg = edge: self.get_mousemovement(event, arg))



class ColourPolygon(DrawPolygon):
    """
    Derived Class of draw polygon to fill colours and implement shading
    """

    # similar constructor as base class
    def __init__(self, path: str)->None:
        # super function to get the data from base class
        super().initialise_poly(path)
        self.ListOfFaces_ = self.poly_.faces_

        # polymorphised base class functions
        self.get_polygon(self.poly_.edges_)
        self.mouse_binder(self.poly_.edges_)
        self.root_.mainloop()


    # function to perform gradient in the colours (referenced from tkinter community examples)
    def get_colors(self, start, end, limit, factor=180):

        # starting rgb values for colour code given
        (red_start,green_start,blue_start) = self.window_.winfo_rgb(start)
        # ending rgb values for colour code given
        (red_end,green_end,blue_end) = self.window_.winfo_rgb(end)

        # factorisation of transition of colours as the angle changes from 0 to 180 degrees
        # when limit = 0, final colours
        # when limit = factor, start colours
        delta_red = int((red_end - ((red_end-red_start) * (2*limit/factor))))
        delta_green = int((green_end - ((green_end-green_start) * (2*limit/factor))))
        delta_blue = int((blue_end - ((blue_end-blue_start) * (2*limit/factor))))

        #new colour produced
        color = "#%4.4x%4.4x%4.4x" % (delta_red,delta_green,delta_blue)
        return color


    # similar poygon function for drawing faces and colouring it
    def get_polygon(self, edges):
        self.window_.delete(ALL)
        width, height = self.window_.winfo_reqwidth()/2,  self.window_.winfo_reqheight()/2

        list_of_triangs = []
   
        for i in range(len(self.ListOfFaces_)):

            #collecting vertices which are drawing a face/plane
            vx1,vy1,vz1 = self.vertices_[0][self.ListOfFaces_[i][0]],self.vertices_[1][self.ListOfFaces_[i][0]],\
                self.vertices_[2][self.ListOfFaces_[i][0]]

            vx2,vy2,vz2 = self.vertices_[0][self.ListOfFaces_[i][1]], self.vertices_[1][self.ListOfFaces_[i][1]],\
                self.vertices_[2][self.ListOfFaces_[i][1]]

            vx3,vy3,vz3 = self.vertices_[0][self.ListOfFaces_[i][2]], self.vertices_[1][self.ListOfFaces_[i][2]],\
                self.vertices_[2][self.ListOfFaces_[i][2]]

            
            vert_a = np.array([vx1, vy1, vz1])
            vert_b = np.array([vx2, vy2, vz2])
            vert_c = np.array([vx3, vy3, vz3])

            #unit vector z
            z_unit = np.array([0, 0, 1])

            # normal to the plane/face using cross product and its unit vector
            normal_ = np.cross((vert_a-vert_b),(vert_b-vert_c))
            unit_vect = normal_/np.linalg.norm(normal_)  

            # angle is the cos inverse of the dot product of normal to the face and z unit vector
            output = np.abs(np.dot(unit_vect,z_unit))/(np.linalg.norm(unit_vect)*np.linalg.norm(z_unit))      
            val = np.rad2deg(np.arccos(output))
            
            # normalized between 0 to 360 degrees
            if val<0:
                val=360+val
            
            # colour gradient to vary when the angle b/w normal and z unit
            # varies from 0 to 90 degrees
            if val<90:
                clr = self.get_colors("#00005F", "#0000FF", val)
            else:
                clr = "#00005F"
            
            
            iter = 0

            ##checking if the polygon being created lies inside the previous polygon using the summation of triangles
            """
            If a point P lies inside the triangle ABC, Area(APB + APC + BPC) = Area(ABC) 

            Output is not as expected for some reason!!!
            """
            for triangs in list_of_triangs:
                ans1 = ColourPolygon.isInside(triangs[0][0], triangs[0][1], triangs[1][0], triangs[1][1], triangs[2][0], triangs[2][1], vx1, vy1)
                ans2 = ColourPolygon.isInside(triangs[0][0], triangs[0][1], triangs[1][0], triangs[1][1], triangs[2][0], triangs[2][1], vx2, vy2)
                ans3 = ColourPolygon.isInside(triangs[0][0], triangs[0][1], triangs[1][0], triangs[1][1], triangs[2][0], triangs[2][1], vx3, vy3)
                if ans1 and ans2 and ans3:
                    break
                else:
                    iter+=1
                    continue
            
            """uncomment this line to see the implementation of above algorithm"""
            # if iter==len(list_of_triangs) or len(list_of_triangs)==0:
            list_of_triangs.append([vert_a,vert_b,vert_c])
            self.window_.create_polygon(self.translation( self.scale_*vx1,  self.scale_*vy1,  width, height), \
                self.translation( self.scale_*vx2,  self.scale_*vy2,  width, height), \
                    self.translation( self.scale_*vx3,  self.scale_*vy3,  width, height), fill=clr)

            self.window_.create_oval(self.translation(self.scale_*self.vertices_[0][edges[i][0]], self.scale_*self.vertices_[1][edges[i][0]],  width, height), \
                self.translation(self.scale_*self.vertices_[0][edges[i][0]], self.scale_*self.vertices_[1][edges[i][0]],  width, height), outline='blue', width=5)

            self.window_.create_oval(self.translation(self.scale_*self.vertices_[0][edges[i][1]], self.scale_*self.vertices_[1][edges[i][1]],  width, height), \
                self.translation(self.scale_*self.vertices_[0][edges[i][1]], self.scale_*self.vertices_[1][edges[i][1]],  width, height), outline='blue', width=5)


    #same as above with faces added
    def mouse_binder(self, edges):

        self.window_.bind("<Button-1>", self.get_mousecoordinates)
        self.window_.bind("<B1-Motion>", lambda event, arg1 = edges, arg2 = self.ListOfFaces_: self.get_mousemovement(event, arg1, arg2))

    #same as above with faces added
    def get_mousemovement(self, event, edges, ListOfFaces):
        x_change = self.y_last - event.y 
        y_change = self.x_last - event.x 
        self.vertices_ = self.rotation_matrix(ang_x =self.multiple(-x_change), ang_y=self.multiple(y_change), input=self.vertices_)
        self.get_polygon(edges)
        self.get_mousecoordinates(event)

    #static methods to check if a point is inside the plane or face
    @staticmethod
    def area(x1, y1, x2, y2, x3, y3):
        return abs((x1 * (y2 - y3) + x2 * (y3 - y1)
                + x3 * (y1 - y2)) / 2.0)

    @staticmethod
    def isInside(x1, y1, x2, y2, x3, y3, x, y):
        
        # Calculate area of triangle ABC
        A = ColourPolygon.area(x1, y1, x2, y2, x3, y3)
    
        # Calculate area of triangle PBC
        A1 = ColourPolygon.area(x, y, x2, y2, x3, y3)
        
        # Calculate area of triangle PAC
        A2 = ColourPolygon.area(x1, y1, x, y, x3, y3)
        
        # Calculate area of triangle PAB
        A3 = ColourPolygon.area(x1, y1, x2, y2, x, y)
        
        # Check if sum of A1, A2 and A3
        # is same as A
        if(A == A1 + A2 + A3):
            return True
        else:
            return False


