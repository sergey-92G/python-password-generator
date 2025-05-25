# Используем стандартный интерпретатор
$python = "python"

function Create-Venv {
    if (-not (Get-Command $python -ErrorAction SilentlyContinue)) {
        Write-Host "Python interpreter '$python' not found in PATH." -ForegroundColor Red
        return
    }

    if (Test-Path ".venv") {
        Write-Host "Virtual environment already exists." -ForegroundColor Yellow
    } else {
        & $python -m venv .venv
        if ($LASTEXITCODE -eq 0) {
            Write-Host "Virtual environment created." -ForegroundColor Green
        } else {
            Write-Host "Failed to create virtual environment." -ForegroundColor Red
            return
        }
    }

    if (Test-Path ".\.venv\Scripts\Activate.ps1") {
        Write-Host "Activating environment..."
        & .\.venv\Scripts\Activate.ps1
    } else {
        Write-Host "Activation script not found." -ForegroundColor Red
    }
}

function Install-Requirements {
    if (-not (Test-Path ".venv")) {
        Write-Host "Virtual environment not found. Please create it first." -ForegroundColor Red
        return
    }
    if (-not (Test-Path "requirements.txt")) {
        Write-Host "requirements.txt not found." -ForegroundColor Yellow
        return
    }

    & .\.venv\Scripts\Activate.ps1
    python -m pip install --upgrade pip
    pip install -r requirements.txt
}

function Remove-Venv {
    if (Test-Path ".venv") {
        Remove-Item -Recurse -Force .venv
        Write-Host "Virtual environment deleted." -ForegroundColor Green
    } else {
        Write-Host "No virtual environment found." -ForegroundColor Yellow
    }
}

function Create-Requirements-FromFreeze {
    if (-not (Test-Path ".venv")) {
        Write-Host "Virtual environment not found. Please create it first." -ForegroundColor Red
        return
    }

    & .\.venv\Scripts\Activate.ps1
    pip freeze > requirements.txt
    Write-Host "requirements.txt generated from installed packages using pip freeze." -ForegroundColor Green
}

function Create-Requirements-FromImports {
    if (-not (Get-Command pipreqs -ErrorAction SilentlyContinue)) {
        Write-Host "pipreqs not found. Installing..." -ForegroundColor Yellow
        pip install pipreqs
    }

    pipreqs . --force --ignore .venv,__pycache__,.git
    Write-Host "requirements.txt generated from imports using pipreqs (excluding .venv, __pycache__, .git)." -ForegroundColor Green
}

function Check-PythonFiles {
    Write-Host "`nChecking .py files for syntax issues..." -ForegroundColor Cyan
    $files = Get-ChildItem -Path . -Recurse -Include *.py -File -ErrorAction SilentlyContinue |
             Where-Object { $_.FullName -notmatch '\\(\.venv|__pycache__|\.git)(\\|$)' }

    if ($files.Count -eq 0) {
        Write-Host "No Python files found." -ForegroundColor Yellow
        return
    }

    $errorCount = 0
    foreach ($file in $files) {
        $path = $file.FullName
        $result = & python -m py_compile "$path" 2>&1
        if ($LASTEXITCODE -ne 0) {
            Write-Host "❌ Syntax error in: $path" -ForegroundColor Red
            Write-Host "$result" -ForegroundColor DarkGray
            $errorCount++
        }
    }

    if ($errorCount -eq 0) {
        Write-Host "`n✅ All .py files are syntactically valid." -ForegroundColor Green
    } else {
        Write-Host "`n⚠️  Total files with errors: $errorCount" -ForegroundColor Yellow
    }
}
function Show-Menu {
    Clear-Host
    Write-Host "== Python Virtual Environment Manager =="

    Write-Host "`n Environment"
    Write-Host "  1. Create and activate virtual environment"
    Write-Host "  2. Install dependencies from requirements.txt"
    Write-Host "  3. Delete virtual environment"
    Write-Host "  4. Save requirements.txt from installed packages (pip freeze)"
    Write-Host "  5. Generate requirements.txt from code imports (pipreqs)"
    Write-Host "  6. Check .py files for syntax errors"
    Write-Host "  7. Exit"

    $choice = Read-Host "`nSelect an option (1-7)"

    switch ($choice) {
        "1" { Create-Venv }
        "2" { Install-Requirements }
        "3" { Remove-Venv }
        "4" { Create-Requirements-FromFreeze }
        "5" { Create-Requirements-FromImports }
        "6" { Check-PythonFiles }
        "7" {
            Write-Host "`nExiting..."
            return $false
        }
        default {
            Write-Host "`nInvalid selection."
        }
    }

    Pause
    return $true
}

# =================== MAIN LOOP ===================
do {
    $continue = Show-Menu
} while ($continue)
