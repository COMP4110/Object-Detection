# cat info_filtered.dat | awk '{ print $1 }' | cut -d\/ -f2 | cut -d_ -f1 | sort | uniq

word_lookup = {}
with open('words.txt', 'r') as words:
    for word_info in words.readlines():
        parts = word_info.partition('\t')
        word_lookup[parts[0]] = parts[2].strip()

found_words = {}

with open('info.dat', 'r') as dat_file:
    for line in dat_file.readlines():
        search_word = line.strip().rpartition('/')[2].partition('_')[0]
        search_word_description = word_lookup[search_word]
        found_words[search_word] = search_word_description

for search_word, search_word_description in found_words.iteritems():
    print search_word, search_word_description
