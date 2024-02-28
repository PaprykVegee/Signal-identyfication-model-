import numpy as np
import random

class SortFile():
    def __init__(self, file):
        self.file = file

    # Open file method
    def open_file(self, file_path):
        with open(file_path, 'r') as file:
            X_cord = []
            Y_cord = []
            Z_cord = []
            for row in file:
                # Split row on 3 element because it is separated by whitespace
                column = row.split()
                if len(column) >= 3:  # Check the length of column
                    X_cord.append(column[0])
                    Y_cord.append(column[1])
                    Z_cord.append(column[2])

        # remove a base error
        max_Z = max(Z_cord)
        min_Z = min(Z_cord)
        adv = (float(max_Z) + float(min_Z))/2
        Z_cord_n = [float(i) - adv for i in Z_cord]
        Z_cord = Z_cord_n

        return X_cord, Y_cord, Z_cord
        
    # Solver
    def circle_mean(self, X_cord, Y_cord):
        sub_length = len(X_cord) // 6
        # X sublist
        X_sublist = [X_cord[i: i + sub_length] for i in range(0, len(X_cord), sub_length)]

        # Y sublist
        Y_sublist = [Y_cord[i: i + sub_length] for i in range(0, len(Y_cord), sub_length)]
    
        # taking point to circular approximation 
        points = []
        for i in range(len(X_sublist)-1):     
            point = []
            for j in range(4):
                for k in range(0, 3, 3):
                    random_idx = random.randint(0, len(X_sublist[i]) - 1)
                    X_val = X_sublist[i+k][random_idx]
                    Y_val = Y_sublist[i+k][random_idx]
                    point.append([float(X_val), float(Y_val)])

            points.append(point)

        points = np.array(points)

        # Flatten the points array
        flattened_points = points.reshape(-1, 2)

        # Calculate the mean center
        center_estimate = np.mean(flattened_points, axis=0)
        # center_estimate = [0, 0]
        # Calculate the mean radius 
        radius_estimate = np.mean(np.sqrt(np.sum((flattened_points - center_estimate) ** 2, axis=1)))

        return center_estimate, radius_estimate

