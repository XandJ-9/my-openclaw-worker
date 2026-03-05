Add-Type -AssemblyName System.Windows.Forms
$screens = [Windows.Forms.Screen]::AllScreens
$bounds = $screens[0].Bounds
$bmp = New-Object Drawing.Bitmap $bounds.Width, $bounds.Height
$graphics = [Drawing.Graphics]::FromImage($bmp)
$graphics.CopyFromScreen($bounds.X, $bounds.Y, 0, 0, $bounds.Size)
$bmp.Save('C:\Users\18352\.openclaw\workspace\screenshot.png')
$graphics.Dispose()
$bmp.Dispose()
Write-Host "Screenshot saved to screenshot.png"
