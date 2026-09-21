from pathlib import Path
from PIL import Image


# ==========================================
# UBICACIÓN DE LAS IMÁGENES
# ==========================================

ruta_entrada = Path(
    r"C:\Users\nicog\OneDrive\Documentos\proyecto imagenes\imagenes_restauradas"
)

ruta_salida = Path(
    r"C:\Users\nicog\OneDrive\Documentos\proyecto imagenes\imagenes_descontaminadas"
)

ruta_salida.mkdir(parents=True, exist_ok=True)


# ==========================================
# PROCESAMIENTO DE IMÁGENES
# ==========================================

imagenes_procesadas = 0
maximo_imagenes = 2

extensiones_validas = (".jpg", ".jpeg", ".png")


print("==========================================")
print("     DESCONTAMINACIÓN DE IMÁGENES RGB")
print("==========================================")
print("Dimensiones requeridas: 512x512")
print("Ruido tratado: Sal y pimienta")
print("Filtro utilizado: Mediana 3x3")
print("Imágenes a procesar: 2")
print("")


# ==========================================
# RECORRER LAS IMÁGENES
# ==========================================

for imagen_archivo in ruta_entrada.iterdir():

    # Detener cuando se hayan procesado 2 imágenes
    if imagenes_procesadas >= maximo_imagenes:
        break

    # Comprobar que sea una imagen válida
    if imagen_archivo.suffix.lower() not in extensiones_validas:
        continue

    print("Procesando imagen:", imagen_archivo.name)


    # ==========================================
    # ABRIR Y CONVERTIR LA IMAGEN A RGB
    # ==========================================

    imagen = Image.open(imagen_archivo).convert("RGB")

    ancho, alto = imagen.size


    # ==========================================
    # COMPROBAR DIMENSIONES
    # ==========================================

    if (ancho, alto) != (512, 512):

        print("  Imagen ignorada: dimensiones diferentes a 512x512")
        continue

    print("  Formato: RGB")
    print("  Dimensiones: 512x512")
    print("  Aplicando filtro de mediana 3x3...")


    # ==========================================
    # CREAR IMAGEN PARA EL RESULTADO
    # ==========================================

    resultado = Image.new("RGB", imagen.size)


    # ==========================================
    # FILTRO DE MEDIANA 3x3
    # ==========================================

    for fila in range(1, alto - 1):

        for columna in range(1, ancho - 1):

            valores_r = []
            valores_g = []
            valores_b = []


            # ------------------------------------------
            # OBTENER LOS 9 PÍXELES DE LA VENTANA 3x3
            # ------------------------------------------

            for desplazamiento_y in (-1, 0, 1):

                for desplazamiento_x in (-1, 0, 1):

                    r, g, b = imagen.getpixel(
                        (
                            columna + desplazamiento_x,
                            fila + desplazamiento_y
                        )
                    )

                    valores_r.append(r)
                    valores_g.append(g)
                    valores_b.append(b)


            # ------------------------------------------
            # ORDENAR LOS VALORES
            # ------------------------------------------

            valores_r.sort()
            valores_g.sort()
            valores_b.sort()


            # ------------------------------------------
            # OBTENER LA MEDIANA
            # ------------------------------------------

            pixel_nuevo = (
                valores_r[4],
                valores_g[4],
                valores_b[4]
            )


            # ------------------------------------------
            # GUARDAR EL NUEVO PÍXEL
            # ------------------------------------------

            resultado.putpixel(
                (columna, fila),
                pixel_nuevo
            )


    # ==========================================
    # CONSERVAR LOS BORDES DE LA IMAGEN
    # ==========================================

    # Borde superior e inferior

    for posicion in range(ancho):

        resultado.putpixel(
            (posicion, 0),
            imagen.getpixel((posicion, 0))
        )

        resultado.putpixel(
            (posicion, alto - 1),
            imagen.getpixel((posicion, alto - 1))
        )


    # Borde izquierdo y derecho

    for posicion in range(alto):

        resultado.putpixel(
            (0, posicion),
            imagen.getpixel((0, posicion))
        )

        resultado.putpixel(
            (ancho - 1, posicion),
            imagen.getpixel((ancho - 1, posicion))
        )


    # ==========================================
    # GUARDAR IMAGEN DESCONTAMINADA
    # ==========================================

    archivo_salida = ruta_salida / imagen_archivo.name

    resultado.save(archivo_salida)

    imagenes_procesadas += 1

    print("  Resultado: imagen descontaminada correctamente")
    print("  Guardada en:", archivo_salida)
    print("")


# ==========================================
# RESULTADOS OBTENIDOS
# ==========================================

print("==========================================")
print("       PROCESAMIENTO FINALIZADO")
print("==========================================")

print("Imágenes procesadas:", imagenes_procesadas)
print("Formato de las imágenes: RGB")
print("Dimensiones: 512x512")
print("Ruido tratado: Sal y pimienta")
print("Filtro utilizado: Mediana 3x3")
print("")

print("Los resultados obtenidos se encuentran en:")

print(ruta_salida)

print("==========================================")