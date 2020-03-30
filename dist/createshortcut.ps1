<#
  Description:  Create a Shortcut
  Usage:
      createshortcut.ps1 <shortcut_path> <target_path> <target_args> <icon_file>

      <shortcut_path> - path to where the shortcut will be created
      <target_path> - path to the target of the shortcut
      <target_args> - command line arguments for the target (if multiple must be in quotes)
      <icon_file> - full path to .ico file
#>

$ShortcutPath = $args[0]
$TargetPath = $args[1]
$TargetArgs = $args[2]
$IconLocation = $args[3]
$IconArrayIndex = 0
$WindowStyle = 7          # Start window minimized

$Shell = New-Object -ComObject ("WScript.Shell")
$Shortcut = $Shell.CreateShortcut($ShortcutPath)
$Shortcut.TargetPath = $TargetPath
$Shortcut.Arguments = $TargetArgs
$Shortcut.WindowStyle = $WindowStyle
$Shortcut.IconLocation = "$IconLocation, $IconArrayIndex"
$Shortcut.Save()