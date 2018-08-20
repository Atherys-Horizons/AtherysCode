# Run this from the base AtherysScript project to generate VS Code snippets
# Open file for writing
echo "//Atherys Snippets for VS Code" > atherys.json
echo "{" >> atherys.json

# Grep for where the functions are created for their name
grep -r 'library.put' src/main/java/com/atherys/script/js/library/ | while read -r line ; do

	# Trim grep result down to just the name of the function and the class name 
	sig=$(echo "$line" | grep -o '(.*)' | sed -e 's/"//g' | tr -d "()" | sed 's/, new//g')
	words=( $sig )
	# Get the name of the function and trim
	name="$(echo "${words[1]}" | tr -d '[:space:]')"
	# Get the name of the file
	lineList=( $line )
	file=$(echo "${lineList[0]}" | sed 's%/[^/]*$%/%')
	file="$file$name.java"
	# Grep file for method signature
	params=$(grep -E 'apply|accept' "$file" | grep -o '(.*)')

	# Remove words that start with capitals (class names) and everything that isn't a letter
	# These are the two parameter names
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

	# Append to file
	echo "	\"$name\": {" >> atherys.json
	echo "		\"prefix\": \"${words[0]}\"," >> atherys.json
	echo "		\"body\": \"${words[0]}$params\"," >> atherys.json
	echo "		\"description\": \" \"" >> atherys.json
	echo "	}," >> atherys.json
done

echo "}" >> atherys.json
