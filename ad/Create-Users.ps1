$users = Import-Csv "C:\Users\admin\Desktop\Users.csv"
$created = 0
$skipped = 0
$errors = 0

foreach ($row in $users) {
    $found = Get-ADUser -Filter "SamAccountName -eq '$($row.UserName)'"
    if ($found){
        Write-Host "User $($row.UserName) exists"
        $skipped++
    } else {
        Write-Host "User $($row.UserName) does not exist - creating user"
        $password = ConvertTo-SecureString $row.Password -AsPlainText -Force
        $path = "OU=$($row.OU),DC=lab,DC=local"
        try {New-ADUser -Name "$($row.FirstName) $($row.LastName)" -SamAccountName $row.UserName -Path $path -AccountPassword $password -Enabled $true
	$created++
    	}
        catch {
             $_.Exception.Message
             $errors++
        }
    }
}

Write-Host "Created users: $($created)"
Write-Host "User creation skipped: $($skipped)"
Write-Host "Nummber of errors: $($errors)"