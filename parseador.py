from bs4 import BeautifulSoup
import re

def limpiar_html(texto_html):
    soup = BeautifulSoup(texto_html, "html.parser")

    # Encabezados h1-h3 → #, ##, ###
    for i in range(1, 4):
        for tag in soup.find_all(f"h{i}"):
            text = tag.get_text(strip=True)
            tag.replace_with(f"{'#' * i} {text}")

    # Negrita
    for strong in soup.find_all(["strong", "b"]):
        strong.replace_with(f"**{strong.get_text(strip=True)}**")

    # Cursiva
    for em in soup.find_all(["em", "i"]):
        em.replace_with(f"*{em.get_text(strip=True)}*")

    # Subrayado (opcional)
    for u in soup.find_all("u"):
        u.replace_with(f"__{u.get_text(strip=True)}__")

    # Tachado
    for s in soup.find_all(["s", "del", "strike"]):
        s.replace_with(f"~~{s.get_text(strip=True)}~~")

    # Código en línea
    for code in soup.find_all("code"):
        code.replace_with(f"`{code.get_text(strip=True)}`")

    # Bloques de código
    for pre in soup.find_all("pre"):
        pre.replace_with(f"```\n{pre.get_text(strip=True)}\n```")

    # Citas
    for blockquote in soup.find_all("blockquote"):
        lines = blockquote.get_text().splitlines()
        quoted = "\n".join(f"> {line.strip()}" for line in lines if line.strip())
        blockquote.replace_with(quoted)

    # Imágenes
    for img in soup.find_all("img"):
        alt = img.get("alt", "imagen")
        src = img.get("src", "")
        img.replace_with(f"[Imagen: {alt}]({src})" if src else f"[Imagen: {alt}]")

    # HR
    for hr in soup.find_all("hr"):
        hr.replace_with("\n---\n")

    # Listas
    for li in soup.find_all("li"):
        li.replace_with(f"• {li.get_text(strip=True)}")

    # Eliminar enlaces pero mantener el texto
    for a in soup.find_all("a"):
        a.unwrap()

    # Tablas básicas (sin formato elegante)
    for table in soup.find_all("table"):
        filas = []
        for row in table.find_all("tr"):
            celdas = [cell.get_text(strip=True) for cell in row.find_all(["td", "th"])]
            filas.append(" | ".join(celdas))
        texto_tabla = "\n".join(filas)
        table.replace_with(texto_tabla)

    # <br>
    for br in soup.find_all("br"):
        br.replace_with("\n")

    # Obtener texto y limpiar
    texto = soup.get_text(separator="\n")
    texto = re.sub(r"\n+", "\n", texto)
    texto = "\n".join(line.strip() for line in texto.splitlines())
    texto = "\n".join(line for line in texto.splitlines() if line)

    # Eliminar repeticiones consecutivas
    resultado = []
    prev = None
    for line in texto.split("\n"):
        if line != prev:
            resultado.append(line)
        prev = line

    return "\n".join(resultado)

def split_text(text, max_length=2000):
    chunks = []
    while len(text) > max_length:
        # Busca el último salto de línea antes del límite para no cortar a mitad de palabra
        split_pos = text.rfind('\n', 0, max_length)
        if split_pos == -1:
            split_pos = max_length
        chunks.append(text[:split_pos])
        text = text[split_pos:].lstrip('\n')
    chunks.append(text)
    return chunks