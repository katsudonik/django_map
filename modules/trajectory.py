import folium
import numpy as np
import math

def get_center(points):
  return [( np.max(points[:,0]) + np.min(points[:,0]) ) / 2, ( np.max(points[:,1]) + np.min(points[:,1]) ) / 2]

def get_width(points):
  return np.max([( np.max(points[:,0]) - np.min(points[:,0]) ),  ( np.max(points[:,1]) - np.min(points[:,1]) )])

def get_zoom_rate(width):
  return math.log(5*width/9500, 0.5)

def get_map(center, zoom):
  return folium.Map(location=center, zoom_start=zoom)

def append_polyline(m, points):
  folium.PolyLine(points, color='blue').add_to(m)

def append_marker(m, point, color):
  folium.Marker(location=point, icon=folium.Icon(color=color)).add_to(m)

# actual_points = [[latitude, longitude]] (ndarray)
def get_trajectory_map(actual_points, start_point, goal_point):
    calc_points = np.append(actual_points, [start_point, goal_point], axis=0)
    center = get_center(calc_points)
    zoom = get_zoom_rate(get_width(calc_points))
    m = get_map(center, zoom)
    append_polyline(m, actual_points.tolist())
    append_marker(m, start_point, 'blue')
    append_marker(m, goal_point, 'red')
    return m

def get_map_html(m):
    return m.get_root().render()

