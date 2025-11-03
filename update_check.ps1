# Activate venv
.venv\Scripts\activate

# Check for updates
Write-Host "`nChecking for package updates...`n" -ForegroundColor Green
pip list --outdated --format=columns

Write-Host "`nTo update a package, run: pip install --upgrade <package-name>`n" -ForegroundColor Yellow