"""Genera entradas de índice para los capítulos de maquetación conservada."""
from pathlib import Path
from pypdf import PdfReader
import unicodedata

root=Path(__file__).resolve().parent
reader=PdfReader(root.parent/'v5-proyecto-integrador-II.pdf')
entries={}
for page,title in [(2,'Dedicatoria'),(3,'Agradecimientos'),(4,'Resumen'),(5,'Abstract')]:
    entries[page]=[r'\phantomsection\addcontentsline{toc}{chapter}{'+title+'}']
counters=[0,0,0]
def escape(s):
    return ''.join({'&':r'\&','%':r'\%','#':r'\#','_':r'\_'}.get(c,c) for c in unicodedata.normalize('NFKC',s))
def walk(items,level=0):
    for obj in items:
        if isinstance(obj,list):
            walk(obj,level+1);continue
        title=obj['/Title'].replace('.NET 8 y C#','.NET 10 y C#').replace('Patrón MVP (Model-View-Presenter)','Arquitectura por capas')
        if title=='Formulación del proyecto' and level==0:counters[:]=[1,0,0]
        elif level==0 and counters[0]:counters[0]+=1;counters[1:]=[0,0]
        elif level>0 and 1<=counters[0]<=4:
            counters[level]+=1
            for k in range(level+1,3):counters[k]=0
        if not 1<=counters[0]<=4:continue
        n=reader.get_destination_page_number(obj)+1
        kind=['chapter','section','subsection'][min(level,2)]
        number='.'.join(map(str,counters[:level+1]))
        line=r'\phantomsection\addcontentsline{toc}{'+kind+r'}{\protect\numberline{'+number+'}'+escape(title)+'}'
        entries.setdefault(n,[]).append(line)
walk(reader.outline)
(root/'entradas-originales.tex').write_text('\n'.join(r'\expandafter\def\csname entrada'+str(n)+r'\endcsname{'+''.join(lines)+'}' for n,lines in entries.items())+'\n',encoding='utf-8')
print('Entradas de índice originales:',sum(map(len,entries.values())))
