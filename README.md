# 🏐 Marcador Voleibol Alevín (PWA)

Marcador táctil deportivo para partidos de voleibol categoría **Alevín**, pensado para usarse en el móvil en horizontal y **100 % sin conexión**.

👉 **Abrir marcador:** https://kapi21.github.io/marcador-voley/  
📅 **Calendario 3ª Femenino GB (FEDEXVB):** [`calendario/calendario_3F_GB.md`](calendario/calendario_3F_GB.md)

---

## ✨ Características

- **Reglamento Alevín (RFEVB):** se juegan obligatoriamente **3 sets a 25 puntos** con diferencia de 2 (resultados posibles: `3-0` o `2-1`) y sistema **punto directo** (*rally point*).
- **Gestos por marcador:**
  - **Tocar** o **deslizar hacia abajo (`↓`)** → **+1 punto**.
  - **Deslizar hacia arriba (`↑`)** → **−1 punto** (para corregir cada marcador por separado).
  - Botón **Deshacer** en la barra superior con historial completo.
- **Indicador de saque (balón):** aparece en la esquina inferior derecha del marcador que saca y cambia de lado automáticamente con cada punto. Al `0-0` permite elegir quién abre el set tocando el balón tenue; en los sets siguientes alterna automáticamente.
- **Cambio de campo:** automático al pasar de set y manual con el botón **Campo**.
- **Nombres editables:** toca el nombre de cualquier equipo para cambiarlo; se guarda automáticamente.
- **Pitido sintético (WebAudio):** 2 pitidos al fin de set y 3 al fin de partido, sin archivos de audio externos. Botón **Sonido ON/OFF**.
- **Pantalla siempre encendida (Wake Lock):** botón **Pantalla ON/OFF** con preferencia recordada.
- **Pantalla completa:** botón **Completa / Salir** y apertura directa a pantalla completa al instalar la PWA.
- **100 % offline:** dígitos LED de 7 segmentos en SVG propio, sin CDN ni fuentes externas, y estado persistido en `localStorage`.

---

## 📱 Instalación en el móvil (PWA)

1. Abre **https://kapi21.github.io/marcador-voley/** en Chrome (Android) o Safari (iOS).
2. En Android: menú `⋮` → **Instalar aplicación**. En iOS: **Compartir** → **Añadir a pantalla de inicio**.
3. Ábrela desde el icono: arrancará en horizontal, a pantalla completa y funcionará aunque no haya cobertura en el pabellón.

---

## 🗂️ Estructura del repositorio

| Ruta | Descripción |
|---|---|
| [`index.html`](index.html) | Aplicación completa (HTML + CSS + SVG LED + JS). |
| [`manifest.webmanifest`](manifest.webmanifest) | Manifiesto PWA (fullscreen, horizontal, iconos). |
| [`sw.js`](sw.js) | Service Worker *cache-first* para uso sin conexión. |
| [`icons/`](icons/) | Iconos PWA (`192`, `512` y `maskable`). |
| [`make_icons.py`](make_icons.py) | Script para regenerar los iconos (`python make_icons.py`). |
| [`calendario/`](calendario/) | Calendario y resultados de 3ª Femenino GB (`.md`, `.csv` y `raw.html`). |
| [`calendario_gb.py`](calendario_gb.py) | Script para actualizar el calendario desde FEDEXVB (`python calendario_gb.py`). |
| [`HANDOFF.md`](HANDOFF.md) | Notas técnicas y registro de cambios del proyecto. |
