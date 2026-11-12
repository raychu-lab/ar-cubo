# AR Cubo

Demo mínima de realidad aumentada en el navegador: un cubo de 20 cm flotando en el espacio real, visto a través de la cámara del móvil.

**URL:** https://raychu-lab.github.io/ar-cubo/

![QR](qr.png)

## Cómo abrirlo

### Android (Chrome)
1. Escanea el QR o abre la URL en **Chrome** (hace falta tener instalado *Google Play Services for AR*, que viene en casi todos los móviles recientes).
2. Pulsa **Start AR** y acepta el permiso de cámara.
3. Mueve el móvil despacio apuntando al suelo o a una mesa hasta que aparezca el anillo turquesa.
4. Toca la pantalla: el cubo aparece unos 30 cm por encima de la superficie, girando y flotando, con una sombra suave debajo. Si vuelves a tocar, se mueve a otro sitio.

### iPhone (Safari)
Safari no tiene WebXR AR, así que la página lo detecta y muestra un visor 3D (`<model-viewer>`).
1. Abre la URL en **Safari** (o escanea el QR con la cámara).
2. Pulsa **Ver en AR**: se abre *AR Quick Look* de Apple y puedes colocar el cubo en el suelo.
   En Quick Look el cubo se queda quieto sobre la superficie; flotar y girar solo funciona en Chrome para Android.

En un ordenador se ve el visor 3D sin AR.

## Archivos
| Archivo | Qué es |
|---|---|
| `index.html` | Toda la página: three.js + WebXR (`immersive-ar` + hit-test) y el visor de respaldo para iPhone. Sin paso de compilación. |
| `cube.glb` | El cubo (54 caras, ~5 KB): bordes biselados, degradado violeta → turquesa y bordes más claros con algo de emisión. |
| `make_cube.py` | Script de Blender que genera `cube.glb`. |
| `qr.png` | QR con la URL. |

Regenerar el cubo (en macOS Blender no está en el PATH):
```bash
/Applications/Blender.app/Contents/MacOS/Blender --background --python make_cube.py
```

## Usar tus propios modelos de Blender
1. Modela en **metros** (1 unidad = 1 m) con el origen en el centro del objeto.
2. Exporta como **glTF Binary (.glb)**, con las texturas incluidas.
3. Sustituye `cube.glb`, o cambia `MODEL_URL` al principio del script de `index.html` y el `src` del `<model-viewer>`.
4. En `index.html` puedes ajustar `HOVER` (altura sobre la superficie), `BOB` (amplitud de la flotación) y `SPIN_SPEED` (giro).

## Probar en local
WebXR exige HTTPS (o `localhost`), así que para probar en el móvil lo más fácil es subir los cambios a GitHub Pages. En el ordenador:
```bash
python3 -m http.server 8000
```
