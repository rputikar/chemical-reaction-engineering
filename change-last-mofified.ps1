$pathToFiles = if ($args.Length -gt 0)
{ $args[0] 
} else
{ Get-Location 
}

if (-not (Test-Path $pathToFiles))
{
  Write-Error "The provided path does not exist."
  exit
}

$qmdFiles = Get-ChildItem -Path $pathToFiles -Filter *.qmd -Recurse

foreach ($file in $qmdFiles)
{
  $content = Get-Content $file.FullName
    
  $dateLineIndex = $content | Select-String -Pattern "^date:" | Select-Object -ExpandProperty LineNumber | ForEach-Object { $_ - 1 }
  if ($dateLineIndex -ne $null)
  {
    # Capture the current date from the 'date' line and reformat
    $currentDateMatch = $content[$dateLineIndex] -match "^date: (.*)$"
    if ($currentDateMatch)
    {
      $currentDateStr = $matches[1]
      try
      {
        $currentDate = [DateTime]::Parse($currentDateStr)
        $newDateStr = $currentDate.ToString("yyyy-MM-dd")
        $content[$dateLineIndex] = "date: $newDateStr"
      } catch
      {
        Write-Warning "Could not parse the date in file $($file.FullName)"
      }
    }
  }

  # Get the last modified date and format it
  $lastModifiedDate = (Get-Item $file.FullName).LastWriteTime.ToString("yyyy-MM-dd")
  $lastModifiedLine = "last-modified: $lastModifiedDate"

  # Check if 'last-modified' exists
  $lastModifiedExists = $content -match '^last-modified:'
    
  if ($lastModifiedExists)
  {
    # If 'last-modified' exists, update it
    $content = $content -replace "(?<=^last-modified: ).*","$lastModifiedDate"
  } elseif ($dateLineIndex -ne $null)
  {
    # If 'date' exists but 'last-modified' doesn't, add it right after 'date'
    $content = $content[0..$dateLineIndex] + $lastModifiedLine + $content[($dateLineIndex + 1)..($content.Length - 1)]
  } else
  {
    # If 'date' doesn't exist, append 'last-modified' at the end
    $content += $lastModifiedLine
  }

  # Write the updated content back to the file
  $content | Set-Content $file.FullName
  Write-Output "Updated file: $($file.FullName)"
}

