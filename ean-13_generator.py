import random

def generate_ean13():
    data = [random.randint(0, 9) for _ in range(12)]
    
    checksum = 0
    for i, num in enumerate(data):
        if i % 2 == 0:
            checksum += num
        else:
            checksum += num * 3
    
    checksum_digit = (10 - (checksum % 10)) % 10
    data.append(checksum_digit)
    
    return ''.join(map(str, data))



barcode = generate_ean13()
print("Generated EAN-13 Barcode:", barcode)
