$exportPath = "$env:USERPROFILE\Desktop\report.txt"

$os = Get-CimInstance Win32_OperatingSystem
$cs = Get-CimInstance Win32_ComputerSystem

$report = [PSCustomObject]@{
    ComputerName = $cs.Name
    OS           = $os.Caption
    Version      = $os.Version
    LastBoot     = $os.LastBootUpTime
    RAMinGB      = [math]::Round($cs.TotalPhysicalMemory/1GB, 2)
}

$ld = Get-CimInstance Win32_LogicalDisk | Where-Object { $_.DriveType -eq 3 }

$output = foreach ($i in $ld) {

    [PSCustomObject]@{

        DiskName = $i.DeviceID
        DiskSizeGB = [math]::Round($i.Size/1GB, 2)
        DiskFreeSpaceGB = [math]::Round($i.FreeSpace/1GB, 2)
    }
}

$report | Format-List
$output | Format-Table

$report | Out-File $exportPath
$output | Out-File $exportPath -Append
