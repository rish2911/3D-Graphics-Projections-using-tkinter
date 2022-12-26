import numpy as np
import math as mp
import pandas as pd
import sys

class import_object():
    """
    Class for importing data from the given file
    """
    def __init__(self, filepath:str=None) -> None:
        # a check on the input path
        if filepath!=None:
            self.filepath_ = filepath
        else:
            print('Provide a file path please \n')
            sys.exit(0)
        
        # initialisation of class variables
        self.data_arr_ = None
        self.edges_ = None
        self.faces_ = None
        self.coordinates_ = None
        self.vert_id_ = None

        # calling the function with the constructor
        self.data_conversion()
        self.data_extractor()
        pass

    #the function to extract input data into numpy array
    def data_conversion(self)->None:
        try:
            csv_data = pd.read_csv(self.filepath_, sep = " ", header=None)
            self.data_arr_ = csv_data.to_numpy()
        except:
            print("Could not convert data using pd data frames, checks for whitespaces., exiting!!! \n")
            sys.exit(0)
    
    # extracting the data in given format, number of faces, edges and vertices
    def data_extractor(self)->None:
        #getting the data from first row of input file
        numOfVertex, numOfFaces = self.data_arr_[0,0].split(',')

        #checking the consistency in number of faces and vertex mentioned
        if (int(numOfFaces)+int(numOfVertex)+1)!=self.data_arr_.shape[0]:
            print('The num of faces and vertices not as mentioned, exiting!!! \n')
            sys.exit(0)
        else:
            numOfFaces, numOfVertex = int(numOfFaces), int(numOfVertex)
        self.coordinates_ = np.empty([int(numOfVertex), 3])
        self.vert_id_  = list()
        vertices = self.data_arr_[1:int(numOfVertex)+1, :]
        faces = self.data_arr_[int(numOfVertex)+1:]
        self.edges_ = list()
        self.faces_ = list()

        #extrcating the vertex ids and coordinates
        for i in range(int(numOfVertex)):
            try:
                v_id, x, y, z = vertices[i,0].split(',')
                self.coordinates_[i] = [float(x), float(y), float(z)]
                
                ## checking if the vertex ids are unique
                if v_id in  self.vert_id_ :
                    print('Vertex ids are not consistent, exiting!!! \n')
                    sys.exit(0)
                else:
                    self.vert_id_ .append(int(v_id))
            except:
                print('Coordinates are not consistent or float, exiting!!! \n')
                sys.exit(0)

        # extracting the faces data
        for i in range(len(faces)):
            try:
                vertex1, vertex2, vertex3 = faces[i][0].split(',')
                if int(vertex1)==int(vertex2) or int(vertex1)==int(vertex2) or int(vertex1)==int(vertex2):
                    print('3D face cannot be drawn between same vertex ids \n')
                    sys.exit(0)
                else:
                    self.faces_.append([int(vertex1)-1, int(vertex2)-1, int(vertex3)-1])
                # appending edges if edges are not in the list
                if (int(vertex1)-1, int(vertex2)-1) not in self.edges_:
                    self.edges_.append((int(vertex1)-1, int(vertex2)-1))
                if (int(vertex1)-1, int(vertex3)-1) not in self.edges_:
                    self.edges_.append((int(vertex1)-1, int(vertex3)-1))
                if (int(vertex2)-1, int(vertex3)-1) not in self.edges_:
                    self.edges_.append((int(vertex2)-1, int(vertex3)-1))
            except:
                print('Faces are not consistent or integers, exiting!!! \n')
                sys.exit(0)

        print("input coordinates are",  self.coordinates_)
        print("input vertex ids are", self.vert_id_)
        print("input edges are", self.edges_)
        print("input face list is", self.faces_)