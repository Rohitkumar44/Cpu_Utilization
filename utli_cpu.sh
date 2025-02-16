$SMTP_SERVER = "smtp.gmail.com"
$SMTP_PORT = 587
$EMAIL_FROM = "rohit2024cs@gmail.com"
$EMAIL_TO = "itz4rohit@gmail.com"
$EMAIL_SUBJECT = "High CPU Usage Alert"

# Secure Credentials
$SecurePassword = ConvertTo-SecureString "mailpassword" -AsPlainText -Force
$Credential = New-Object System.Management.Automation.PSCredential ("rohit2024cs@gmail.com", $SecurePassword)

# Send Email Function
function Send-Email {
    param (
        [string]$ProcessName,
        [string]$CPUUsage
    )

    $BODY = "Warning: High CPU usage detected.`nProcess: $ProcessName`nCPU Usage: $CPUUsage%"

    Send-MailMessage -SmtpServer $SMTP_SERVER -Port $SMTP_PORT -UseSsl `
                     -From $EMAIL_FROM -To $EMAIL_TO -Subject $EMAIL_SUBJECT `
                     -Body $BODY -Credential $Credential
    Write-Host "Email sent for $ProcessName using $CPUUsage% CPU."
}