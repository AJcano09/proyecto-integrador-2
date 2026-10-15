# Documentación oficial de ExploraNica

El documento contiene portada, preliminares y ocho capítulos: formulación, investigación documental, emprendimiento, modelado del proceso, implementación, resultados, impacto y cierre académico.

## Compilación

Desde la raíz del proyecto, ejecutar `./src/compilar.ps1`. El resultado se genera en `build/main.pdf`. El script utiliza Tectonic instalado o la copia portátil de `tmp/tectonic/tectonic.exe`.

También se puede compilar desde `src` con:

```powershell
tectonic main.tex --outdir ../build --keep-logs
```

En Overleaf, subir los archivos del paquete y seleccionar `main.tex`.

## Organización

- `main.tex`: configuración y composición del documento.
- `portada.tex` y `preliminares.tex`: presentación académica.
- `capitulos/`: contenido de los ocho capítulos.
- `entradas-originales.tex`: entradas de índice de los capítulos 1-4.
- `assets/fondos.pdf`: elementos gráficos de la maquetación.
- `assets/evidencias/`: recursos de interfaz.
- `ARQUITECTURA.md`: organización técnica del sistema.

Los capítulos 5-8 utilizan títulos, tablas y referencias de LaTeX. El índice se genera automáticamente. Para regenerar las entradas de los capítulos 1-4 se utiliza `integrar_documento.py` con el PDF de referencia en la raíz del proyecto.

## Sistema

ExploraNica utiliza .NET 10, Windows Forms, ASP.NET Core, Entity Framework Core y PostgreSQL. Repositorio oficial: https://github.com/AJcano09/explora-nicaragua.
