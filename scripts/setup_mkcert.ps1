# PowerShell script to install mkcert and generate trusted SSL certificates on Windows

# Define mkcert download URL and destination
$mkcertUrl = "https://github.com/FiloSottile/mkcert/releases/latest/download/mkcert-v1.4.4-windows-amd64.exe"
$mkcertExe = "$env:USERPROFILE\mkcert.exe"

Write-Host "Downloading mkcert..."
Invoke-WebRequest -Uri $mkcertUrl -OutFile $mkcertExe

Write-Host "Adding mkcert to PATH temporarily for this session..."
$env:PATH += ";$env:USERPROFILE"

Write-Host "Installing local CA..."
& $mkcertExe -install

Write-Host "Generating certificates for localhost and 127.0.0.1..."
& $mkcertExe localhost 127.0.0.1

Write-Host "Certificates generated:"
Write-Host " - localhost+127.0.0.1.pem"
Write-Host " - localhost+127.0.0.1-key.pem"

Write-Host "You can now run your Django development server with:"
Write-Host "python manage.py runsslserver --certificate localhost+127.0.0.1.pem --key localhost+127.0.0.1-key.pem"
