"""Descarga y guarda el calendario 3ª Femenino GB (FEDEXVB) en calendario/.
Uso: python calendario_gb.py        (vuelve a ejecutarlo para actualizar resultados)
Genera: calendario/calendario_3F_GB.csv, calendario/calendario_3F_GB.md, calendario/salesianos_alevin.json, calendario/raw.html
"""
import csv, datetime, html, json, os, re, urllib.request

URL = "https://resultados.fedexvoleibol.com/calendar.php?grupo=147"
FUENTE = "https://fedexvoleibol.com/calendario-tercera-femenino-gb"
OUT = "calendario"
os.makedirs(OUT, exist_ok=True)

raw = urllib.request.urlopen(urllib.request.Request(URL, headers={"User-Agent": "Mozilla/5.0"})).read().decode("utf-8", "replace")
open(f"{OUT}/raw.html", "w", encoding="utf-8").write(raw)

t = re.sub(r"(?s)<(script|style)[^>]*>.*?</\1>", "", raw)
t = re.sub(r"(?i)</(tr|p|h\d|li|div)>", "\n", t)
t = re.sub(r"(?i)</t[dh]>", " | ", t)
t = html.unescape(re.sub(r"<[^>]+>", "", t))
lines = [re.sub(r"\s+", " ", l).strip() for l in t.split("\n")]
lines = [l for l in lines if l]

rows, jornada, i = [], "", 0
while i < len(lines):
    l = lines[i]
    m = re.match(r"JORNADA (\d+)", l)
    if m:
        jornada = m.group(1); i += 1; continue
    m = re.match(r"(\d{4}/\d\d/\d\d) \| (.+?) \| (\d+ - \d+|vs) \| (.+?) \|$", l)
    if m and i + 1 < len(lines):
        fecha, local, res, visit = m.groups()
        d = lines[i + 1].rstrip("|").strip()
        dia, _, resto = d.partition(" | ")
        mm = re.match(r"([A-ZÁÉÍÓÚ]+)(?: \(([^)]*)\))?(?: (\d{1,2}[:.]\d{2}|Pdte-[^\s]+))? ?(.*)", resto)
        cat, sets, hora, lugar = (mm.groups() if mm else (resto, "", "", ""))
        hora = (hora or "").replace(".", ":")
        rows.append([jornada, fecha.replace("/", "-"), dia, hora, cat, local, res, visit, sets or "", lugar.strip()])
        i += 2; continue
    i += 1

head = ["Jornada", "Fecha", "Día", "Hora", "Categoría", "Local", "Resultado", "Visitante", "Sets", "Pabellón"]
with open(f"{OUT}/calendario_3F_GB.csv", "w", newline="", encoding="utf-8-sig") as f:
    w = csv.writer(f, delimiter=";"); w.writerow(head); w.writerows(rows)

def tabla(rs):
    s = "| " + " | ".join(head) + " |\n|" + "---|" * len(head) + "\n"
    return s + "".join("| " + " | ".join(r) + " |\n" for r in rs)

md = f"# Calendario 3ª Femenino GB – FEDEXVB\n\nFuente: {FUENTE}\n\nDatos: {URL}\n\n"
for j in sorted({r[0] for r in rows}, key=int):
    md += f"## Jornada {j}\n\n" + tabla([r for r in rows if r[0] == j]) + "\n"
mio = [r for r in rows if re.search(r"ALBUERA|ZURBARAN|SALESIANOS", " ".join([r[5], r[7], r[9]]).upper())]
md += "## Filtro: La Albuera / Salesianos / IES Zurbarán\n\n" + tabla(mio)
open(f"{OUT}/calendario_3F_GB.md", "w", encoding="utf-8").write(md)

alevin_salesianos = [
    {
        "jornada": int(r[0]),
        "fecha": r[1],
        "dia": r[2],
        "hora": r[3],
        "local": r[5],
        "resultado": r[6],
        "visitante": r[7],
        "sets": r[8],
        "pabellon": r[9],
        "pendiente": r[6].strip().lower() == "vs",
    }
    for r in rows
    if r[4].upper() == "ALEVIN" and ("E.D. SALESIANOS A" in (r[5].upper(), r[7].upper()))
]
payload = {
    "equipo": "E.D. SALESIANOS A",
    "categoria": "ALEVIN",
    "fuente": FUENTE,
    "iframe": URL,
    "actualizado": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
    "partidos": alevin_salesianos,
}
open(f"{OUT}/salesianos_alevin.json", "w", encoding="utf-8").write(json.dumps(payload, ensure_ascii=False, indent=2))
print(len(rows), "partidos guardados en", OUT, "|", sum(p["pendiente"] for p in alevin_salesianos), "pendientes Alevín Salesianos")
