param([string]$Tectonic = 'tectonic')
$ErrorActionPreference = 'Stop'
if (-not (Get-Command $Tectonic -ErrorAction SilentlyContinue)) {
    $localCompiler = Join-Path $PSScriptRoot '../tmp/tectonic/tectonic.exe'
    if (Test-Path -LiteralPath $localCompiler) {
        $Tectonic = (Resolve-Path -LiteralPath $localCompiler).Path
    } else {
        throw 'Instala Tectonic o indica su ruta mediante -Tectonic.'
    }
}
Push-Location $PSScriptRoot
try {
    $outputDirectory = Join-Path $PSScriptRoot '../build'
    New-Item -ItemType Directory -Force -Path $outputDirectory | Out-Null
    & $Tectonic 'main.tex' '--outdir' $outputDirectory '--keep-logs'
    if ($LASTEXITCODE -ne 0) { throw 'Falló la compilación LaTeX.' }
    Write-Output "PDF generado: $(Join-Path $outputDirectory 'main.pdf')"
} finally {
    Pop-Location
}
