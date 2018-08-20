# Run this with the AtherysScript directory as an argument to generate snippets.

SECONDS=0
#Set up variables for the spinner
i=0
fileCount=0
sp='/-\|'
n=${#sp}

# Open file for writing
json="$2"
echo "//Atherys Snippets for VS Code" > "$json"
echo "{" >> "$json"

while read -r line ; do
	# Trim grep result down to just the name of the function and the class name 
	sig=$(echo "$line" | grep -o '(.*)' | sed -e 's/"//g' | tr -d "()" | sed 's/, new//g')
	words=( $sig )
	jsName="${words[0]}"

	# Get the name of the function and trim
	name="$(echo "${words[1]}" | tr -d '[:space:]')"

	# Get the name of the file
	lineList=( $line )
	classFile="$(find "$1" -name "$name.java")"

	# If the file isn't found, it's probably an event function
	if [[ $classFile = "" ]]; then
		isEvent=1
	else
		 # Grep file for method signature, only the first result
		 params=$(grep -E -m1 'apply|accept|get' "$classFile" | grep -o '(.*)')

		 # Remove words that start with capitals (class names) and everything that isn't a letter
		 # These are the parameter names
		 parameters=$(echo "$params" | sed -r -e 's/\b[A-Z]\w*//g' -e 's/[^ a-zA-Z]//g')

		 params="("
		 num=1
		 parameters=( $parameters )
		 # Loop through parameters and format for snippet: ${1:parameter}
		 for param in ${parameters[@]}; do
			 params="$params$"{"$num:$param"}""
			 if [[ "$num" -lt ${#parameters[@]} ]]; then
				 params="$params, "
			 fi
			 ((num++))
		 done
		 params="$params)"
	fi

	# Append to file
	printf "	\"$name\": {\n" >> "$json"
	printf "    \"prefix\": \"$jsName\",\n" >> "$json"
	if [[ $isEvent = 1 ]]; then
		printf "%s\n" "    \"body\": [" "     \"(function() {\"," "     \"\$0\"," "     \"}\"" "    ]," >> "$json"
	else   
		printf "    \"body\": \"$jsName$params\",\n" >> "$json"
	fi
	printf "    \"description\": \" \"\n" >> "$json"
	printf "	},\n" >> "$json"

	# Increase file count for spinner
	((fileCount++))

	# Reset isEvent
	isEvent=0

	# Show spinner and number of files
	printf '\r%s' "${sp:i++%n:1}" 
	printf "Files processed: $fileCount"
# Grep for where the functions are created for their name
done < <(grep -r -i 'library.put' "$1")

echo "}" >> "$json"
printf "\n"
echo "Time taken: $SECONDS seconds."
