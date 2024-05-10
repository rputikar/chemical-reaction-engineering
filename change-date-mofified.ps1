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
  $updated = $false
    
  # Get file's date write time, only considering the date part
  $fileLastWriteTime = (Get-Item $file.FullName).LastWriteTime.Date

  # Attempt to find and parse the last-updated date from the file
  $lastUpdatedLine = $content | Where-Object { $_ -match '^date-modified: (.*)$' }
  $fileNeedsUpdate = $true

  if ($lastUpdatedLine)
  {
    $lastUpdatedDateStr = $lastUpdatedLine -replace '^date-modified: (.*)$', '$1'
    try
    {
      $lastUpdatedDate = [DateTime]::ParseExact($lastUpdatedDateStr, "yyyy-MM-dd", $null)

      if ($fileLastWriteTime -le $lastUpdatedDate)
      {
        $fileNeedsUpdate = $false
      }
    } catch
    {
      Write-Warning "Failed to parse date-modified date for $($file.FullName)"
    }
  }

  if ($fileNeedsUpdate)
  {
    # Your update logic goes here. Make sure to set $updated = $true if changes are made.
        
    # Example: Updating the last-updated field
    $lastUpdatedIndex = [array]::IndexOf($content, $lastUpdatedLine)
    if ($lastUpdatedIndex -ne -1)
    {
      $content[$lastUpdatedIndex] = "date-modified: " + $fileLastWriteTime.ToString("yyyy-MM-dd")
      $updated = $true
    } else
    {
      $content += "date-modified: " + $fileLastWriteTime.ToString("yyyy-MM-dd")
      $updated = $true
    }
        
    if ($updated)
    {
      $content | Set-Content $file.FullName
      Write-Output "Updated file: $($file.FullName)"
    }
  }
}
