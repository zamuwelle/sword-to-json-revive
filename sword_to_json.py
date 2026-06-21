from pysword.modules import SwordModules
import argparse, json

def generate_dict(source_file, bible_version):
	modules = SwordModules(source_file)
	found_modules = modules.parse_modules()

	if bible_version not in found_modules:
		raise SystemExit(
			f"'{bible_version}' not found in {source_file}.\n"
			f"Available module key(s): {list(found_modules.keys())}"
		)

	bible = modules.get_bible_from_module(bible_version)
	book_structure = bible.get_structure().get_books()
	books = book_structure['ot'] + book_structure['nt']

	bib = {'books': []}
	for book in books:
		chapters = []
		for chapter in range(1, book.num_chapters + 1):
			texts = bible.get_iter(books=[book.name], chapters=[chapter])
			verses = [
				{
					'verse': v,
					'chapter': chapter,
					'name': f"{book.name} {chapter}:{v}",
					'text': t,
				}
				for v, t in enumerate(texts, start=1)
			]
			chapters.append({
				'chapter': chapter,
				'name': f"{book.name} {chapter}",
				'verses': verses,
			})
		bib['books'].append({'name': book.name, 'chapters': chapters})

	return bib

def write_json(bible_dict, output_file):
	with open(output_file, 'w') as outfile:
		json.dump(bible_dict, outfile, indent='\t')

def main():
	parser = argparse.ArgumentParser()
	parser.add_argument('--source_file', required=True)
	parser.add_argument('--bible_version', required=True)
	parser.add_argument('--output_file', required=True)
	args = parser.parse_args()
	bible_dict = generate_dict(args.source_file, args.bible_version)
	write_json(bible_dict, args.output_file)

if __name__ == "__main__":
	main()