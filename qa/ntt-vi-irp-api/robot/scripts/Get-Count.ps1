# A simple script to keep track of counters. Used to ensure BCDL numbers are only used once in a Robot Framework test.

param (
    [string] $COUNTER_NAME,   # Example: BCDL
    [int]    $COUNTER_VALUE   # Example: 1000000
)

Set-Variable -Name "MEMORY_FOLDER"       -Value "${HOME}\.counts"
if (-Not (Test-Path -Path ${MEMORY_FOLDER} -PathType Container)){
    New-Item -Path "${MEMORY_FOLDER}" -ItemType Directory
}

# If no number was given on the command-line, get it from a memory file
${MEMORY_FILE} = "${MEMORY_FOLDER}\${COUNTER_NAME}.txt"
if (${COUNTER_VALUE} -eq 0)
{
    # If no memory file, prompt for a number
    if (-Not (Test-Path -Path ${MEMORY_FILE} -PathType Leaf)){
        Write-Host "You must give a starting number to search. For example '1000000' to starting iterating."
        exit(3)
    }
    else {
        $FILE_CONTENT = Get-Content -Path ${MEMORY_FILE}
        $INTEGER = [int]${FILE_CONTENT}
        Set-Variable -Name "COUNTER_VALUE" -Value ${INTEGER}
        ${COUNTER_VALUE}=${COUNTER_VALUE}+1
    }
}

${COUNTER_VALUE} | Out-File -FilePath ${MEMORY_FILE}

${COUNTER_VALUE}