# HANDOFF – Marcador Voleibol Alevín

## Estado actual (PWA completada)
- `index.html`: app única, 100% offline (sin CDN). Dígitos LED de 7 segmentos en SVG propio, fibra de carbono, marcos metálicos.
- `manifest.webmanifest`: display fullscreen, landscape, iconos PNG.
- `sw.js`: cache-first (subir `VERSION` al cambiar archivos).
- `make_icons.py` → genera `icons/` (192, 512, maskable).
- `Marcador Táctil de Voleibol.pdf`: requisitos originales (chat Gemini).

## Reglas implementadas
3 sets obligatorios a 25 con diferencia de 2, cambio de campo automático al siguiente set, rally point.

## Funciones
Toque = +1 · Deshacer real (historial de snapshots) · Cambiar campo · Reiniciar (set / todo) · Nombres editables · Persistencia en `localStorage` · Pantalla completa (botón) · Pantalla encendida ON/OFF (preferencia guardada).

## Despliegue / instalación
La PWA necesita HTTPS (o localhost). Opciones: GitHub Pages / Netlify / Cloudflare Pages, o local `python -m http.server 8080`.
En Android/Chrome: menú ⋮ → "Instalar aplicación". Instalada abre en pantalla completa y horizontal. iOS no soporta Fullscreen API en Safari; usar "Añadir a pantalla de inicio".

## Pendiente (opcional)
Indicador de saque, pitido sintético, compartir resultado.

## Calendario 3ª Femenino GB
- Fuente: https://fedexvoleibol.com/calendario-tercera-femenino-gb (iframe: https://resultados.fedexvoleibol.com/calendar.php?grupo=147)
- Guardado en `calendario/` (CSV, MD y raw.html). Actualizar: `python calendario_gb.py`.

## Cambios 07/11 (tarde)
- Equipo A renombrado: Zurbarán → **Salesianos** (migración automática del nombre guardado).
- Gestos por marcador: toque o deslizar ↓ = +1, deslizar ↑ = −1 (cada lado independiente; el deshacer global sigue disponible).
- Logo nuevo (marcador LED rojo/azul + balón) generado con `make_icons.py`. SW `marcador-v4`.
