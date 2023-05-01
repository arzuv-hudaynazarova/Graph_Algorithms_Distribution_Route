<!DOCTYPE html>
<html>
<head>
  <title>Dağıtım Rotası</title>
  <link rel="stylesheet" href="https://unpkg.com/leaflet@1.7.1/dist/leaflet.css" integrity="sha512-xodZBNTC5n17Xt2atTPuE1HxjVMSvLVW9ocqUKLsCC5CXdbqCmblAshOMAS6/keqq/sMZMZ19scR4PsZChSR7A==" crossorigin=""/>
  <script src="https://unpkg.com/leaflet@1.7.1/dist/leaflet.js" integrity="sha512-XQoYMqMTK8LvdxXYG3nZ448hOEQiglfqkJs1NOQV44cWnUrBc8PkAOcXy20w0vlaXaVUearIOBhiXZ5V3ynxwA==" crossorigin=""></script>
  <style>
    #map {
      height: 100%;
      width: 100%;
    }
    html, body {
      height: 100%;
      margin: 0;
      padding: 0;
    }
  </style>
</head>
<body>
  <div id="map"></div>
  <script>
    
   // Lokasyon bilgileri
    const locations = [
      { id: 1, lat: 37.892747, lon: 27.298976, needs: [10, 5, 2, 3] },
      { id: 2, lat: 37.880624, lon: 27.309730, needs: [8, 10, 4, 2] },
      { id: 3, lat: 37.871681, lon: 27.320380, needs: [6, 8, 3, 1] },
      { id: 4, lat: 37.864895, lon: 27.343111, needs: [4, 7, 5, 4] },
      { id: 5, lat: 37.851215, lon: 27.363872, needs: [8, 9, 1, 2] },
      { id: 6, lat: 37.846049, lon: 27.378192, needs: [7, 10, 3, 3] },
      { id: 7, lat: 37.838957, lon: 27.388764, needs: [5, 6, 4, 1] },
      { id: 8, lat: 37.820459, lon: 27.411769, needs: [9, 8, 2, 4] },
      { id: 9, lat: 37.829072, lon: 27.420015, needs: [3, 7, 5, 2] },
      { id: 10, lat:37.808091, lon: 27.427245, needs: [2, 6, 3, 3] },
      { id: 11, lat: 37.791718, lon: 27.438112, needs: [1, 5, 4, 1] },
      { id: 12, lat: 37.786293, lon: 27.450480, needs: [4, 4, 5, 4] },
      { id: 13, lat: 37.766529, lon: 27.462147, needs: [6, 3, 2, 2] },
      { id: 14, lat: 37.750019, lon: 27.473570, needs: [7, 2, 3, 3] },
      { id: 15, lat: 37.733975, lon: 27.475515, needs: [9, 1, 4, 1] },
      { id: 16, lat: 37.727215, lon: 27.474972, needs: [7, 3, 3, 1] },
      { id: 17, lat: 37.714141, lon:  27.48118, needs: [5, 5, 1, 4] },
      { id: 18, lat: 37.706453, lon: 27.518912, needs: [6, 4, 2, 3] },
    ];
  

    // Stok bilgileri 
     const stock = [
     { priority: 1, type: 'Sağlık Malzemesi', stock: 100 },
     { priority: 2, type: 'Temel Gıda', stock: 100 },
     { priority: 3, type: 'Isınma Gereci', stock: 70 },
     { priority: 4, type: 'Giyecek', stock: 70 },
   ];
  

   // Merkez koordinatları
   const center = [37.892747, 27.298976];
   // Haritayı başlatma
   const map = L.map('map').setView(center, 11);

   // 1.5 km çapında daireler için yarıçap
   const circleRadius = 1500; 

  // Lokasyonları haritada göstermek için daireler çiziyoruz
  locations.forEach(location => {
    L.circle([location.lat, location.lon], {
      color: 'red',
      fillColor: '#f03',
      fillOpacity: 0.5,
      radius: circleRadius
    }).addTo(map);
  });


  // Haversine formülü ile koordinatlar arası mesafe hesaplama
   function haversineDistance(lat1, lon1, lat2, lon2) {
    const R = 6371; 
    const dLat = (lat2 - lat1) * Math.PI / 180;
    const dLon = (lon2 - lon1) * Math.PI / 180;
    const a =
      Math.sin(dLat / 2) * Math.sin(dLat / 2) +
      Math.cos(lat1 * Math.PI / 180) *
        Math.cos(lat2 * Math.PI / 180) *
        Math.sin(dLon / 2) *
        Math.sin(dLon / 2);
    const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
    return R * c;
  }
  
  

  // Haritayı başlatma

     L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
     attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
     }).addTo(map);

     

     // Koordinatlardan adres bilgisi alma
    async function getAddress(lat, lon) {
      const url = `https://nominatim.openstreetmap.org/reverse?format=json&lat=${lat}&lon=${lon}&zoom=18&addressdetails=1`;
      const response = await fetch(url);
      const data = await response.json();
      return data.display_name;
    }


    // Adres bilgilerini alıp, lokasyonları haritaya işaretleme
    (async () => {
      for (const location of locations) {
        const address = await getAddress(location.lat, location.lon);
        location.address = address;
        const marker = L.marker([location.lat, location.lon]).addTo(map);
        const popupContent = `
          <h3>Lokasyon: ${location.id}</h3>
          <p>
            Adres: ${location.address}<br>
            Sağlık Malzemesi: ${location.needs[0]}<br>
            Temel Gıda: ${location.needs[1]}<br>
            Isınma Gereci: ${location.needs[2]}<br>
            Giyecek: ${location.needs[3]}
          </p>
        `;
        marker.bindPopup(popupContent);
      }
    })();

    // Mesafe matrisi oluşturma
    const distanceMatrix = locations.map((location1) =>
    locations.map((location2) =>
      haversineDistance(location1.lat, location1.lon, location2.lat, location2.lon)
    )
    );

    // Dijkstra algoritması ile en kısa yol bulma
    function dijkstra(graph, source) {
    const visited = [];
    const distances = [];
    const previous = [];

    for (let i = 0; i < graph.length; i++) {
      distances[i] = Infinity;
      visited[i] = false;
      previous[i] = null;
    }

    distances[source] = 0;

    for (let i = 0; i < graph.length; i++) {
      let minValue = Infinity;
      let minIndex = -1;

      for (let v = 0; v < distances.length; v++) {
        if (!visited[v] && distances[v] < minValue) {
          minValue = distances[v];
          minIndex = v;
        }
      }

      if (minValue === Infinity) {
        break;
      }

      visited[minIndex] = true;

      for (let e = 0; e < graph[minIndex].length; e++) {
        const neighbor = graph[minIndex][e];
        const alt = minValue + neighbor;

        if (alt < distances[e]) {
          distances[e] = alt;
          previous[e] = minIndex;
        }
      }
    }

    return {
      distances: distances,
      previous: previous
    };
    }

    const graph = distanceMatrix.map(row => row.map(distance => distance));
    const result = dijkstra(graph, 0);

    // Malzeme dağıtım planı oluşturma
    const distributionPlan = distributeStock(stock, locations, result.distances);
    console.log(distributionPlan);

    
    // En kısa yolu çizmek için polyline oluşturuyoruz
    const shortestPath = [];
    let currentNode = destIndex;
    while (currentNode !== null) {
    shortestPath.unshift(coordinates[currentNode]);
    currentNode = result.previous[currentNode];
    }

    const polyline = L.polyline(shortestPath, {color: 'blue'}).addTo(map);

    // En kısa yolun uzunluğunu ve süresini hesaplayarak ekranda gösteriyoruz
    const shortestDistance = result.distances[destIndex] / 1000; // km olarak
    const shortestDuration = shortestDistance / averageSpeed; // saat olarak
    const infoDiv = document.createElement("div");
    infoDiv.innerHTML = `
    <h2>En Kısa Rota Bilgisi</h2>
    <p>Toplam Mesafe: ${shortestDistance.toFixed(2)} km</p>
    <p>Tahmini Süre: ${shortestDuration.toFixed(2)} saat</p>
    `;
    document.body.appendChild(infoDiv);
  
        
</script>
</body>
</html>
