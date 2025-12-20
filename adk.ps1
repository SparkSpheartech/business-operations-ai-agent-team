$adkPath = "C:\Users\shaza\AppData\Local\Packages\PythonSoftwareFoundation.Python.3.11_qbz5n2kfra8p0\LocalCache\local-packages\Python311\Scripts\adk.exe"
if (-not (Test-Path $adkPath)) {
    Write-Error "ADK executable not found at $adkPath"
    exit 1
}

# Pass all arguments to adk
& $adkPath $args
