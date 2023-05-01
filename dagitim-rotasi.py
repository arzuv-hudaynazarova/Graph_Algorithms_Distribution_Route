"""  Bu uygulamada, belirtilen koşulları sağlayacak şekildedir. Kod şu şekildedir:

1. Stok listesi oluşturma.
2. İhtiyaçları toplamıyla birlikte noktaları sıralama
3. Merkez noktadan belirli bir yarıçap ve nokta sayısıyla örnek noktalar oluşturma
4. Noktalara rastgele ihtiyaçlar atama
5. OpenStreetMap API'den veri çekme
6. Noktalar arasındaki mesafeyi hesaplama (Haversine formülü kullanarak)
7. Dijkstra algoritması ile en kısa yolları hesaplama
8. Harita üzerinde noktaları ve rotaları görselleştirme
İhtiyaçlar en çok ihtiyacın duyulduğu yere en kısa zamanda dağıtılacak şekilde sıralanmıştır. 
Harita üzerinde belirlenen karayolu rotası ya da drone rotası, en kısa yolları hesaplamak için Dijkstra algoritması kullanılarak belirlenmiştir.
Harita üzerinde noktalar ve rotalar görselleştirdim.

Kodun sonunda, my_map.save('map.html') satırı ile harita "map.html" adlı bir dosya olarak kaydedilir. """


import heapq
import requests
import networkx as nx
import folium
from folium import Popup
import math
import random

# Stok listesi
stock_list = [
    {'priority': 1, 'type': 'Sağlık Malzemesi', 'stock': 100},
    {'priority': 2, 'type': 'Temel Gıda', 'stock': 100},
    {'priority': 3, 'type': 'Isınma Gereci', 'stock': 70},
    {'priority': 4, 'type': 'Giyecek', 'stock': 70},
]


# İhtiyaçları toplamıyla birlikte sıralama
def sort_points_by_needs(points):
    points_needs_sum = [(i, sum(point['needs'])) for i, point in enumerate(points)]
    heapq.heapify(points_needs_sum)
    sorted_points = [points[i] for i, _ in heapq.nlargest(len(points), points_needs_sum)]
    return sorted_points


# Örnek merkez nokta koordinatları (Aydın, Kuşadası)
center_lat = 37.892747
center_lon = 27.298976
radius = 1.5  # km
count = 15


def generate_points(center_lat, center_lon, radius, count):
    points = []
    angle_diff = 360 / count

    for i in range(count):
        angle = math.radians(i * angle_diff)
        lat = center_lat + (radius * math.sin(angle) / 110.574)
        lon = center_lon + (radius * math.cos(angle) / (111.320 * math.cos(math.radians(center_lat))))
        points.append({'lat': lat, 'lon': lon, 'needs': [100, 100, 70, 70]})

    return points


# Belirtilen alanda noktaları oluşturma
points = generate_points(center_lat, center_lon, radius, count)



# İhtiyaçları belirleyen fonksiyon
def assign_needs(points, stock):
    max_needs = [stock_item['stock'] // len(points) for stock_item in stock]
    for point in points:
        point_needs = [random.randint(0, max_need) for max_need in max_needs]
        point['needs'] = point_needs


assign_needs(points, stock_list)

# OpenStreetMap API ile veri çekme
def get_osm_data(lat, lon, radius):
    overpass_url = "http://overpass-api.de/api/interpreter"
    overpass_query = f"""
     [out:json];
     (node({lat - radius},{lon - radius},{lat + radius},{lon + radius}););
     out body;
    """
    response = requests.get(overpass_url, params={'data': overpass_query})
    data = response.json()
    return data

# İhtiyaçları belirleyen fonksiyon
def assign_needs(points, stock):
    max_needs = [stock_item['stock'] // len(points) for stock_item in stock]
    for point in points:
        point_needs = [random.randint(0, max_need) for max_need in max_needs]
        point['needs'] = point_needs

assign_needs(points, stock_list)


# Noktalar arasındaki mesafe hesaplama
from math import radians, sin, cos, sqrt, atan2
def haversine(lat1, lon1, lat2, lon2):
    # Dünya yarıçapı (km)
    R = 6371

    # Enlem ve boylamları radyana çevirme
    lat1_rad = radians(lat1)
    lon1_rad = radians(lon1)
    lat2_rad = radians(lat2)
    lon2_rad = radians(lon2)

    # Enlem ve boylam farkları
    delta_lat = lat2_rad - lat1_rad
    delta_lon = lon2_rad - lon1_rad

    # Haversine formülü
    a = sin(delta_lat / 2) ** 2 + cos(lat1_rad) * cos(lat2_rad) * sin(delta_lon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    # Mesafeyi hesaplama ve sonucu kilometre cinsinden döndürme
    distance = R * c
    return distance


# Dijkstra algoritmasını kullanarak en kısa yol hesapladım
def calculate_shortest_paths(points):
    graph = nx.Graph()

    # Graf düğümleri ve kenarları oluşturdum
    for i, point1 in enumerate(points):
        for j, point2 in enumerate(points):
            if i != j:
                dist = haversine(point1['lat'], point1['lon'], point2['lat'], point2['lon'])
                graph.add_edge(i, j, weight=dist)

    # Dijkstra algoritması ile en kısa yolları hesapladım
    shortest_paths = {}
    for i in range(len(points)):
        shortest_paths[i] = nx.single_source_dijkstra_path(graph, i)

    # Graf düğümleri ve kenarları oluşturdum
    for i, point1 in enumerate(points):
        for j, point2 in enumerate(points):
            if i != j:
                dist = haversine(point1['lat'], point1['lon'], point2['lat'], point2['lon'])
                graph.add_edge(i, j, weight=dist)

    # Dijkstra algoritması ile en kısa yolları hesapladım
    shortest_paths = {}
    for i in range(len(points)):
        shortest_paths[i] = nx.single_source_dijkstra_path(graph, i)
        return shortest_paths



# harita üzerinde noktaları ve rotaları görseleştirme
def visualize_map(points, shortest_paths):
    map_center = (points[0]['lat'], points[0]['lon'])



for point in points:
    # Adres bilgisini almak için Nominatim API'sini kullanma
    response = requests.get(
        f"https://nominatim.openstreetmap.org/reverse?format=json&lat={point['lat']}&lon={point['lon']}&zoom=18&addressdetails=1")
    address = response.json().get('display_name', 'Adres bilgisi bulunamadı')



# Harita üzerinde noktaları ve rotaları görselleştirdim
def visualize_map(points, shortest_paths):
    map_center = (points[0]['lat'], points[0]['lon'])
    my_map = folium.Map(location=map_center, zoom_start=14)


    for point in points:
        # Adres bilgisini almak için Nominatim API'sini kullanma
        response = requests.get(f"https://nominatim.openstreetmap.org/reverse?format=json&lat={point['lat']}&lon={point['lon']}&zoom=18&addressdetails=1")
        address = response.json().get('display_name', 'Adres bilgisi bulunamadı')

        # İhtiyaç miktarları ve adresi birleştirme
        info = f"Adres: {address}<br>"
        for need, stock_item in zip(point['needs'], stock_list):
            info += f"{stock_item['type']}: {need}<br>"

        popup = Popup(info, max_width=250)
        folium.Marker(location=(point['lat'], point['lon']), popup=popup).add_to(my_map)

    for start, paths in shortest_paths.items():
        for path in paths.values():
            locations = [(points[i]['lat'], points[i]['lon']) for i in path]
            folium.PolyLine(locations, color="blue", weight=2.5, opacity=0.8).add_to(my_map)

    my_map.save('map.html')
    

def calculate_total_distance(shortest_paths):
    total_distance = 0
    for start, paths in shortest_paths.items():
        for path in paths.values():
            path_distance = sum(haversine(points[path[i]]['lat'], points[path[i]]['lon'],
                                          points[path[i + 1]]['lat'], points[path[i + 1]]['lon'])
                                for i in range(len(path) - 1))
            total_distance += path_distance



    return total_distance


def calculate_estimated_time(total_distance, speed=50):
    time = total_distance / speed  # saat cinsinden süre
    time_in_minutes = time * 60  # dakika cinsinden süre
    return time_in_minutes

shortest_paths = calculate_shortest_paths(points)

total_distance = calculate_total_distance(shortest_paths)
print(f"Toplam mesafe: {total_distance:.2f} km")

estimated_time = calculate_estimated_time(total_distance)
print(f"Tahmini süre: {estimated_time:.2f} dakika")


# OpenStreetMap API ile veri çekme
osm_data = get_osm_data(points[0]['lat'], points[0]['lon'], 0.01)

# En çok ihtiyacı olan noktaları sıralama
sorted_points = sort_points_by_needs(points)

# En kısa yolları hesaplama
shortest_paths = calculate_shortest_paths(points)

# Harita üzerinde görselleştirme
visualize_map(points, shortest_paths)
