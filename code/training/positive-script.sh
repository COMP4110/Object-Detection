IFS=$'\n'
files=$(find . -iname "*.jpg" -type f)
i=1
for file in $files; do
	echo "$file"
	mv "$file" "ball_$i.jpg"
	i=$((i+1))
done