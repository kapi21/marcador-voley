# HANDOFF – VoleyLED (Marcador Voleibol Alevín)

## Estado actual (PWA completada)
- `index.html`: app única, 100% offline (sin CDN). Dígitos LED de 7 segmentos en SVG propio, fibra de carbono, marcos metálicos.
- `manifest.webmanifest`: display fullscreen, landscape, iconos PNG.
- `sw.js`: cache-first (subir `VERSION` al cambiar archivos).
- `make_icons.py` → genera `icons/` (192, 512, maskable).
- `README.md`: documentación principal del repositorio.

## Reglas implementadas
3 sets obligatorios a 25 con diferencia de 2, cambio de campo automático al siguiente set, rally point.

## Funciones
Toque = +1 · Deshacer real (historial de snapshots) · Cambiar campo · Reiniciar (set / todo) · Nombres editables · Persistencia en `localStorage` · Pantalla completa (botón) · Pantalla encendida ON/OFF (preferencia guardada).

## Despliegue / instalación
La PWA necesita HTTPS (o localhost). Opciones: GitHub Pages / Netlify / Cloudflare Pages, o local `python -m http.server 8080`.
En Android/Chrome: menú ⋮ → "Instalar aplicación". Instalada abre en pantalla completa y horizontal. iOS no soporta Fullscreen API en Safari; usar "Añadir a pantalla de inicio".

## Cambios 07/11 (VoleyLED + Calendario Alevín Salesianos + Fix PWA WebAPK)
- App renombrada a **VoleyLED** en `manifest.webmanifest`, `index.html`, `README.md` y `HANDOFF.md`.
- Botón **Partidos Alevín** en la barra inferior que abre una ventana con los partidos pendientes de **E.D. SALESIANOS A** (categoría únicamente **ALEVÍN**) de la liga 3ª Femenino GB, con botón **Cargar** para precargar rival y lado de campo.
- Sincronización triple con FEDEXVB (`calendario/salesianos_alevin.json`, consulta en directo y GitHub Actions cada 6 h en `.github/workflows/update-calendar.yml`).
- Fix de colisión de `id` en `manifest.webmanifest` (`"id": "/marcador-voley/"`, `"start_url": "/marcador-voley/"`, `"scope": "/marcador-voley/"`) con otras PWAs del mismo dominio `kapi21.github.io` (`LISTIA`, `OpenRadioFM`) + botón verde **Instalar** directo en la barra superior (`beforeinstallprompt`). SW `marcador-v8`.

## Calendario 3ª Femenino GB
- Fuente: https://fedexvoleibol.com/calendario-tercera-femenino-gb (iframe: https://resultados.fedexvoleibol.com/calendar.php?grupo=147)
- Guardado en `calendario/` (CSV, MD y raw.html). Actualizar: `python calendario_gb.py`.

## Cambios 07/11 (tarde)
- Equipo A renombrado: Zurbarán → **Salesianos** (migración automática del nombre guardado).
- Gestos por marcador: toque o deslizar ↓ = +1, deslizar ↑ = −1 (cada lado independiente; el deshacer global sigue disponible).
- Logo nuevo (marcador LED rojo/azul + balón) generado con `make_icons.py`. SW `marcador-v4`.

## Cambios 07/11 (saque y sonido)
- Indicador de saque: balón en la esquina inferior derecha del marcador que saca. Punto directo: saca quien gana el punto. Saque inicial: set 1 elegible tocando el balón al 0-0 (por defecto Salesianos); sets siguientes alternan. Tocar el balón en cualquier momento corrige quién saca (con deshacer).
- Pitido sintético (WebAudio) al acabar set (2 pitidos) y partido (3). Botón Sonido ON/OFF (preferencia guardada).
- Textos de ayuda más abajo y marcador con más margen. SW `marcador-v5`.
