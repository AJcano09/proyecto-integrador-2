"""Reconstrucción tipográfica del PDF: texto LaTeX y fondo vectorial sin texto."""
from pathlib import Path
import re
import unicodedata
import pdfplumber
from pypdf import PdfReader, PdfWriter
from pypdf.generic import ContentStream

ROOT = Path(__file__).resolve().parent
SOURCE = ROOT.parent / 'v5-proyecto-integrador-II.pdf'
if (ROOT/'main.tex').exists() and '05-implementacion' in (ROOT/'main.tex').read_text(encoding='utf-8'):
    raise SystemExit('La edición integrada ya existe. Ejecutar la extracción en una copia separada para no sobrescribir los capítulos desarrollados.')

def escape(s):
    s = unicodedata.normalize('NFKC', s)
    mapping = {'\\': r'\textbackslash{}', '{': r'\{', '}': r'\}', '$': r'\$', '&': r'\&', '#': r'\#', '%': r'\%', '_': r'\_', '^': r'\textasciicircum{}', '~': r'\textasciitilde{}', '–': '--', '—': '---', '→': r'\ensuremath{\rightarrow}', '≥': r'\ensuremath{\geq}', '≤': r'\ensuremath{\leq}', '•': r'\textbullet{}', '✓': r'\ensuremath{\surd}', '×': r'\ensuremath{\times}'}
    return ''.join(mapping.get(c,c) for c in s)

reader = PdfReader(SOURCE)
writer = PdfWriter()
for p in reader.pages:
    writer.add_page(p)
    page = writer.pages[-1]
    content = ContentStream(page.get_contents(), writer)
    # Mantener tablas, líneas, diagramas e imágenes, retirando el texto de página.
    content.operations = [(args,op) for args,op in content.operations if op not in (b'Tj',b'TJ',b"'",b'"')]
    page.replace_contents(content)
with open(ROOT/'assets/fondos.pdf','wb') as f:
    writer.write(f)

groups = [(0,1,'portada'),(1,5,'preliminares'),(5,11,'indices'),(11,22,'capitulos/01-formulacion'),(22,33,'capitulos/02-investigacion'),(33,46,'capitulos/03-emprendimiento'),(46,59,'capitulos/04-modelado'),(59,67,'capitulos/05-analisis'),(67,68,'glosario')]
# Los límites reales se obtienen de los marcadores del PDF.
starts = []
for item in reader.outline:
    if isinstance(item,dict):
        starts.append((item['/Title'],reader.get_destination_page_number(item)))
chapters = [(t,n) for t,n in starts if t not in ('Dedicatoria','Agradecimientos','Resumen','Abstract','Glosario')]
first = chapters[0][1]
groups = [(0,1,'portada'),(1,5,'preliminares'),(5,first,'indices')]
names = ['01-formulacion','02-investigacion','03-emprendimiento','04-modelado','05-analisis']
end = next(n for t,n in starts if t == 'Glosario')
for i,((title,start),name) in enumerate(zip(chapters,names)):
    groups.append((start,chapters[i+1][1] if i+1<len(chapters) else end,'capitulos/'+name))
groups.append((end,len(reader.pages),'glosario'))

with pdfplumber.open(SOURCE) as doc:
    for start,stop,name in groups:
        result = ['% Texto editable; coordenadas en puntos PDF.']
        for index in range(start,stop):
            p = doc.pages[index]
            result += [f'% Página original {index+1}',r'\begin{pagina}{'+str(index+1)+'}']
            runs=[]
            for c in p.chars:
                font=c['fontname'].split('+')[-1]
                baseline=c['matrix'][5]
                if runs and runs[-1]['font']==font and abs(runs[-1]['size']-c['size'])<.01 and abs(runs[-1]['y']-baseline)<.1 and abs(runs[-1]['end']-c['x0'])<1:
                    runs[-1]['text']+=c['text']; runs[-1]['end']=c['x1']
                else:
                    runs.append(dict(font=font,size=c['size'],x=c['x0'],y=baseline,end=c['x1'],text=c['text']))
            for run in runs:
                style = r'\normalfont'
                if 'Mono' in run['font']: style += r'\ttfamily'
                if 'Bold' in run['font']: style += r'\bfseries'
                if 'Italic' in run['font']: style += r'\itshape'
                if 'Caps' in run['font']: style += r'\scshape'
                text=escape(run['text'])
                if run['font'].startswith('CMMI'): text=r'\ensuremath{'+text+'}'
                result.append(r'\texto{%.4f}{%.4f}{%.4f}{%s}{%s}'%(run['x'],run['y'],run['size'],style,text))
            result.append(r'\end{pagina}')
        (ROOT/(name+'.tex')).write_text('\n'.join(result)+'\n',encoding='utf-8')

preamble = r'''\documentclass[12pt,letterpaper]{article}
\usepackage[utf8]{inputenc}
\usepackage[T1]{fontenc}
\usepackage{lmodern}
\usepackage{textcomp,amsmath,amssymb}
\usepackage[paperwidth=612bp,paperheight=792bp,margin=0pt]{geometry}
\usepackage{graphicx,tikz}
\pagestyle{empty}
\setlength{\parindent}{0pt}
% Una página usa el fondo vectorial sin texto y texto LaTeX editable.
\newenvironment{pagina}[1]{\noindent\begin{tikzpicture}[remember picture,overlay,x=1bp,y=1bp]
\node[anchor=south west,inner sep=0] at (current page.south west) {\includegraphics[page=#1,width=612bp,height=792bp]{assets/fondos.pdf}};
}{\end{tikzpicture}\null\newpage}
\newcommand{\texto}[5]{\node[anchor=base west,inner sep=0pt,outer sep=0pt] at ([xshift=#1bp,yshift=#2bp]current page.south west) {{#4\fontsize{#3bp}{#3bp}\selectfont #5}};}
\begin{document}
'''
body='\n'.join(r'\input{'+n+'}' for _,_,n in groups)
(ROOT/'main.tex').write_text(preamble+body+'\n\\end{document}\n',encoding='utf-8')
(ROOT/'README.md').write_text('''# Reconstrucción LaTeX de Explora-Nicaragua

Compilar desde esta carpeta con `pdflatex main.tex` (dos veces si se agregan referencias). Compatible con Overleaf: subir toda esta carpeta y elegir main.tex.

La portada, preliminares, índices, cinco capítulos y glosario están separados. Todo el texto de página se recupera como texto LaTeX editable. Se conserva el diseño original mediante posiciones absolutas; al ampliar párrafos hay que ajustar sus coordenadas. Los índices conservan la paginación original y no se regeneran automáticamente. No es todavía una edición semántica con comandos chapter/section, tablas y bibliografía automáticas.

assets/fondos.pdf conserva los elementos gráficos originales (líneas, tablas, imágenes y diagramas), sin los operadores de texto de página. El texto interno de imágenes o formularios gráficos puede permanecer dentro de esos recursos.

reconstruir.py permite repetir la extracción con Python, pypdf y pdfplumber desde el PDF original situado dos carpetas arriba. No editar los .tex antes de regenerar: la extracción los reemplaza.
''',encoding='utf-8')
print('Reconstruidas',len(reader.pages),'páginas; archivos:',[n for _,_,n in groups])
