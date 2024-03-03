import tsplib95
import numpy as np
from tqdm import tqdm
class TspToMatrix():

  def __init__(self, file_dir):
    # content is the list of the lines of the tsp file

    self.problem = tsplib95.load(file_dir)

    self.name, self.matrix = self.get_matrix()


  def get_matrix(self):

    edge_weight_type = self.problem.edge_weight_type
    dim = self.problem.dimension
    name = self.problem.name

    if edge_weight_type == "EXPLICIT":
      if self.problem.edge_weight_format == "FULL_MATRIX":
        matrix = self.problem.edge_weights
      else:
        values = []
        for w in self.problem.edge_weights:
          values.extend(w)
        edge_weight_format = self.problem.edge_weight_format
        matrix = self.full_matrix(values, dim, edge_weight_format, name)

    else:
        node_coords = self.problem.node_coords
        matrix = self.compute_matrix(node_coords, dim, edge_weight_type, name)
    return name, matrix


  def compute_matrix(self, coords, dim, edge_weight_type, name):
    dist_matrix = [[0] * dim for _ in range(dim)]
    pbar = tqdm(range(dim),desc="Computing {}".format(name))
    for i in pbar:
      for j in range(i + 1, dim):
        dist = self.distance(coords[i + 1], coords[j + 1], edge_weight_type)
        dist_matrix [i][j] = dist
        dist_matrix [j][i] = dist
    return dist_matrix

  def distance(self, cord1, cord2, edge_weight_type):

    x1, y1 = cord1
    x2, y2 = cord2

    if edge_weight_type == "EUC_2D":
      return np.sqrt((x1 - x2)**2 + (y1 - y2)**2)
    elif edge_weight_type == "CEIL_2D":
      return np.round(np.sqrt((x1 - x2)**2 + (y1 - y2)**2))
    elif edge_weight_type == "GEO":
      lat1, lon1 = np.radians(cord1)
      lat2, lon2 = np.radians(cord2)
      R = 6371  # Radius of the Earth
      return R * np.arccos(np.sin(lat1) * np.sin(lat2) + np.cos(lat1) * np.cos(lat2) * np.cos(lon2 - lon1))
    elif edge_weight_type == "ATT":
      return np.round(np.sqrt((x1 - x2)**2 + (y1 - y2) ** 2) / 10)

  def full_matrix(self, values, dim, format, name):

    matrix = [[0] * dim for _ in range(dim)]
    cnt = 0
    pbar = tqdm(range(dim),desc="Computing {}".format(name))

    for i in pbar:
      for j in range(dim):
        if format == "UPPER_ROW" and j > i:
          matrix[i][j] = values[cnt]
          matrix[j][i] = values[cnt]
          cnt += 1
        elif format == "LOWER_ROW" and j < i:
          matrix[i][j] = values[cnt]
          matrix[j][i] = values[cnt]
          cnt += 1
        elif format == "LOWER_DIAG_ROW" and j <= i:
          matrix[i][j] = values[cnt]
          matrix[j][i] = values[cnt]
          cnt += 1
        elif format == "UPPER_DIAG_ROW" and j >= i:
          matrix[i][j] = values[cnt]
          matrix[j][i] = values[cnt]
          cnt += 1
    return matrix

  def return_matrix(self):
    return np.array(self.matrix)
  def print_matrix(self):
    print(self.matrix)


#Tspfolder = 'TspRes/'

#example_file = "gr17.tsp"
#example = TspToMatrix(Tspfolder + example_file)
