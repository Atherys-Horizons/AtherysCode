# Run this from the base AtherysScript project to generate documentation for github wiki

#Set up variables for the spinner
i=0
fileCount=0
sp='/-\|'
n=${#sp}

# Make directory and remove any files from it so that we don't keep appending to files
# Redirect error for removing file
json="module.json"
echo "Snippets" > "$json"
echo "{" >> "$json"

# We use process substitution so that the library variables can be retrieved after the loop
while read -r line ; do

	# Trim grep result down to just the name of the function and the class name 
	sig=$(echo "$line" | grep -o '(.*)' | sed -e 's/"//g' | tr -d "()" | sed 's/, new//g')
	words=( $sig )

	# Get the name of the function and trim
	name="$(echo "${words[1]}" | tr -d '[:space:]')"

	# Get the name of the class
	lineList=( $line )
	file=$(echo "${lineList[0]}" | sed 's%/[^/]*$%/%')

	# Names for files to write to - one is a temporary one to be concatenated on afterwards
	library=docs/$(basename "${lineList[0]}" | sed -e 's/.java//' -e 's/://')
	libraryToC="$library.temp"
	classFile="$(find "$1" -name "$name.java")"
	echo "$classFile"
	parent=$(basename "$(dirname "$classFile")")

	# Grep file for method information
	params=$(grep -E -m 1 'apply|accept|get' "$classFile" | grep -o '(.*)')
	fullSig=$(grep -E 'apply|accept|get' "$classFile")
	fullSig=( $fullSig )
	returnType=${fullSig[1]}

	jsName=${words[0]}
	jsNameLower="${jsName,,}"

	# Append method for table of contents
	echo "* [$jsName](#$jsNameLower)" >> "$libraryToC"

	# Append method information to file
	echo "	\"$name\": {" >> "$json" 
	echo "		\"prefix\": \"${words[0]}\"," >> "$json"
	echo "		\"body\": \"${words[0]}$params\"," >> "$json" 
	echo "		\"description\": \" \"" >> "$json" 
	echo "	}," >> "$json"

	# Increase file count for spinner
	((fileCount++))

	# Show spinner and number of files
	printf '\r%s' "${sp:i++%n:1}" 
	printf "Files processed: $fileCount"
	sleep 0.02
done < <(grep -r 'Library.put' "$1")


printf '\n'
