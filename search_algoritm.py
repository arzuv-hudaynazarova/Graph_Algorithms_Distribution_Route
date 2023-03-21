# Alice in Wonderland dosyasını açıp okuyoruz
with open('alice_in_wonderland.txt', 'r') as file:
    data = file.read().replace('\n', ' ')

# Aranacak kelimeleri bir diziye yerleştiriyoruz
words = ['upon', 'sigh', 'Dormouse', 'jury-box', 'swim']

# Arama yapmak için bir sözlük oluşturuyoruz
word_counts = {word: 0 for word in words}

# Sözlükteki her kelime için dosyayı arıyoruz
for word in words:
    lowercase_word = word
    # Kelimenin kaç kez geçtiğini sayıyoruz
    count = data.count(lowercase_word)
    # Sözlüğe kelimenin sayısını kaydediyoruz
    word_counts[word] = count

# Sonuçları yazdırıyoruz
for word, count in word_counts.items():
    print(f"{word}: {count}")
