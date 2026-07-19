Write-Host "===== ACCOUNTS WITHOUT PASSWORD REQUIREMENT ====="
Get-ADUser -Filter 'PasswordNotRequired -eq $true' -Properties PasswordNotRequired

Write-Host "===== PRIVILEGED USERS ====="
$groups = "Domain Admins", "Enterprise Admins", "Administrators"

foreach ($group in $groups) {

Write-Host "=== $group ==="
Get-ADGroupMember -Identity $group -Recursive | Select-Object Name, SamAccountName

}
