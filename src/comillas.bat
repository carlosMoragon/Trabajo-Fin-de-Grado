@echo off
set "csvPath=C:\Users\cmora\Desktop\TFG\ESTE_ES_EL_TFG\src\Familias.csv"
set "outputPath=C:\Users\cmora\Desktop\TFG\ESTE_ES_EL_TFG\src\Familias_comillas.csv"


powershell -Command "
    $csvPath = '%csvPath%'
    $outputPath = '%outputPath%'
    $csvContent = Import-Csv -Path $csvPath
    
    $modifiedContent = $csvContent | ForEach-Object {
        $properties = $_.PSObject.Properties | ForEach-Object {
            '""' + $_.Value + '""'
        }
        
        [PSCustomObject]@{
            $properties.Name = $properties.Value
        }
    }
    
    $modifiedContent | Export-Csv -Path $outputPath -NoTypeInformation
"

echo El proceso ha terminado. El archivo modificado se guardó en: %outputPath%
pause