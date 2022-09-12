from core.herramientas import Herramientas as her



while True:
    opcion = input("Indicame el mensaje a cifrar")
    
    if opcion == "salir":
        break
    cifrado = her.cifrado_sha1(opcion)
    print(f"Longitud: {len(cifrado)} caracteres: {cifrado}")
