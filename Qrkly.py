import requests
import time

# İncelenecek ürün numaraları ve aranacak anahtar kelimeler. Test icin start_product = 569
start_product = 1
end_product = 17200
keywords = ['titan', 'titan (holo)', 'ibuypower', 'katowice 2014', '(holo) | katowice 2015', '(holo) | cologne 2014', '(holo) | dreamhack 2014', 'harp of war (holo)', 'king on the field', 'winged defuser', 'howling dawn', 'crown (foil)']

for product_id in range(start_product, end_product + 1):
    url = f"https://gw.bynogame.com/steam-listings/v2/listings?limit=1000&page=1&filters=Product:{product_id}&Sort=Price:1;Score:-1"
    ### print(f"\nKontrol edilen urun numarasi: {product_id} ")
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            # Veriler "data" altında "result" listesi içerisinde geliyor.
            results = data.get('data', {}).get('result', [])
            for listing in results:
                # Sticker isimlerini, eğer boş ise boş liste olarak alıyoruz.
                sticker_names = listing.get('stickerNames', [])
                # Eğer sticker_names string olarak gelirse listeye çevirelim.
                if isinstance(sticker_names, str):
                    sticker_names = [sticker_names]
                
                # Aranacak anahtar kelimelerin varlığını kontrol edelim.
                matching_keywords = [kw for kw in keywords 
                                     if any(kw in sticker.lower() for sticker in sticker_names)]
                
                if matching_keywords:
                    # Ürün adını "product" altındaki "marketHashName" alanından çekiyoruz.
                    product_name = listing.get('product', {}).get('marketHashName', 'İsim Yok')
                    price = listing.get('price', 'Fiyat Yok')
                    print(f"\nKontrol edilen urun numarasi: {product_id}\n**********************************************\nESLESME BULUNDU: {product_name}\nFiyat: {price}\nStickerlar: {sticker_names}\n\nAnahtar Kelime(ler): {', '.join(matching_keywords)}\n**********************************************\n")
        else:
            print(f"Urun Numarasi {product_id} icin istek hatasi: {response.status_code}")
    except Exception as e:
        print(f"Urun Numarasi {product_id} icin hata: {e}")
    
    # Siteden banlanmayı önlemek için 2 saniye gecikme ekleniyor.
    time.sleep(1)
