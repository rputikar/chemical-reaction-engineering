# Course Website: Chemical Reaction Engineering 

Github repository For chemical reaction engineering course.
[The website can be found here.](https://cre.smilelab.dev/)

## Getting Started on windows 10

I use powershell in windows terminal.

Clone the repository.

```powershell
gh repo clone rputikar/chemical-reaction-engineering
```

## Quarto related stuff

Set up python virtual environment and activate it.

```powershell
python -m venv _env 

.\_env\Scripts\Activate.ps1
```

Install packages required to run juypter from Quarto

```powershell
python -m pip install -r requirements.txt
```

## Render all files to html

```powershell
quarto render
```

## Tools

### git and github cli

Use `winget` (Windows Package Manager) simplifies the installation process.

1. **Install Git**:
   ```powershell
   winget install Git.Git
   ```

2. **Install GitHub CLI**:
   ```powershell
   winget install GitHub.cli
   ```

3. **Verify Installations**:
   ```powershell
   git --version

   gh --version
   ```

4. **Authenticate with GitHub CLI**:
   ```powershell
   gh auth login
   ```

5. **Set Git Credentials**:
   ```powershell
   git config --global user.name "Your GitHub Username"

   git config --global user.email "Your GitHub Email"
   ```

Git and GitHub CLI are ready for use in PowerShell.


### Quarto

Quarto is an open-source scientific and technical publishing system.

Follow installation instructions at [quarto.org](https://quarto.org/)

### Python3

Python is a programming language that lets you work more quickly and integrate
your systems more effectively.

Python should be already installed on your machine. Check with

```
python --version
```

If you get an error, install python.

```
winget install Python.Python.3.10
```
### Jupyter

Project Jupyter is a non-profit, open-source project, born out of the IPython
Project in 2014 as it evolved to support interactive data science and
scientific computing across all programming languages.

Jupyter will be installed via requirements.txt.


