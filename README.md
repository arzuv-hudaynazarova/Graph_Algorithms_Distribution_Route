# Algorithm_Analyses_and_Desin
# Graph Dijikstra Algorithms
# İhtiyaçlara göre dağıtım rotası


Bu örnek kodda, ihtiyaç malzemeleri dağıtımı için bir planlama uygulaması oluşturulmaktadır. Bu uygulama, Leaflet.js kütüphanesi kullanılarak bir harita üzerinde rastgele lokasyonların oluşturulmasını, her bir lokasyon için rastgele ihtiyaçların belirlenmesini ve bu lokasyonların adres bilgileri ve ihtiyaçları ile birlikte harita üzerinde gösterilmesini sağlar.

Kodun genel yapısı şu şekildedir:

HTML dosyasında, Leaflet.js kütüphanesi için gerekli CSS ve JS dosyaları dahil edilir. Ayrıca, bir div öğesi oluşturulur ve bu öğeye bir id özelliği (map) atanır.

JavaScript dosyasında, bir merkez noktası ve yarıçap belirlenerek rastgele lokasyonlar oluşturmak için bir fonksiyon (generateRandomLocations()) tanımlanır. Bu fonksiyon, belirtilen merkez noktası ve yarıçap kullanılarak, belirli bir sayıda (locationCount) rastgele konumlar oluşturur.

Lokasyonlar üzerinde gösterilecek işaretleyici simgesi ve özellikleri belirlemek için bir icon nesnesi oluşturulur.

Rastgele lokasyonlar, Leaflet.js kütüphanesi kullanılarak bir harita üzerinde işaretleyici olarak gösterilir. Her bir işaretleyiciye, konumun id özelliği içeren bir pop-up penceresi eklenir.

Her bir konum için bir adres bilgisi almak için bir fonksiyon (getAddress()) tanımlanır. Bu fonksiyon, Nominatim API'sini kullanarak bir koordinatın adres bilgisini alır.

Rastgele ihtiyaçlar oluşturmak için bir fonksiyon (generateRandomNeeds()) tanımlanır. Bu fonksiyon, her bir lokasyon için, önceden belirlenmiş bir ihtiyaç malzemesi listesinden (stock) rastgele ihtiyaçlar oluşturur.

Her bir lokasyon için, getAddress() fonksiyonu kullanılarak adres bilgisi alınır ve lokasyonun ihtiyaçları ile birlikte harita üzerinde işaretleyici olarak gösterilir.


İki koordinat arasındaki mesafeyi hesaplamak için bir fonksiyon (calculateDistance()) tanımlanır. Bu fonksiyon, Haversine formülü kullanılarak iki nokta arasındaki mesafeyi hesaplar.

Yukarıdaki işlemlerin tamamı async/await yapısı kullanılarak gerçekleştirilir. Bu sayede, işlemler sırayla ve arka arkaya gerçekleştirilir ve herhangi bir hata oluştuğunda bu hatalar yakalanabilir.

Sonuç olarak, bu örnek kod, Leaflet.js kütüphanesi kullanarak harita üzerinde rastgele lokasyonların oluşturulmasını, bu lokasyonların adres bilgileri ve ihtiyaçları ile birlikte gösterilmesini ve ihtiyaç malzemeleri dağıtımı için bir planlama uygulaması oluşturulmasını sağlar. Bu uygulama, gerçek hayatta ihtiyaç duyulan malzemelerin daha hızlı ve etkili bir şekilde dağıtılmasına yardımcı olabilir.


