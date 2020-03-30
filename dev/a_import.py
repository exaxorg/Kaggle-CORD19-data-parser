from json import loads
from glob import glob
from os.path import join


options = dict(directory='')

datasets = ('previous',)


def parse(data):
	# "data" is a dict corresponding to each file's json-data.
	sha = data['paper_id']
	title = data['metadata']['title']
	abstract = data.get('abstract', ())
	if abstract:
		# typle of text paragraphs
		abstract = tuple(element['text'] for element in data['abstract'])
	body = data['body_text']
	# tuple of (section title, paragraph text) for each paragraph in body
	body = tuple((element['section'], element['text']) for element in body)
	bib = {key: val['title'] for key, val in data['bib_entries'].items()}
	ref = {key: val['text'] for key, val in data['ref_entries'].items()}
	back = tuple(element['text'] for element in data['back_matter'])
	return {
		'sha': sha,
		'title': title,
		'abstract': abstract,
		'body': body,
		'bib': bib,
		'ref': ref,
		'back': back,
	}


def prepare(job):
	# prepare() is run first, then "analysis()", and then "synthesis()", if they exist.
	path = join(job.input_directory, options.directory)
	filenames = sorted(glob(join(path, '*.json')))
	assert len(filenames) > 0, 'No json-files in directory \"%s\"' % (path,)
	# create a datasetwriter instance
	dw = job.datasetwriter(previous=datasets.previous, filename=path)  # path, since no single filename exists
	dw.add('sha', 'unicode')
	dw.add('title', 'unicode')
	dw.add('abstract', 'json')			# (text, ...)
	dw.add('body', 'json')				# ((section, text), ...)
	dw.add('bib', 'json')				# {ref:title, ...}
	dw.add('ref', 'json')				# {ref:text, ...}
	dw.add('back', 'json')				# (text, ...)
	dw.add('filename', 'unicode')
	dw.add('exabstract', 'unicode')	# lowercase joined string
	return filenames, dw


def analysis(prepare_res, sliceno, slices):
	# analysis() is parallelised into "slices" processes.  "sliceno" is the unique process id.
	filenames, dw = prepare_res  # output from prepare()
	filenames = filenames[sliceno::slices]  # pick a (1/slices)-fraction of all filenames for this slice
	for fn in filenames:
		with open(fn, 'rt') as fh:
			data = loads(fh.read())
		v = parse(data)
		example_cleaned_abstract = '\\n'.join(x.lower().replace('\n', '\\n') for x in v['abstract'])
		dw.write(v['sha'], v['title'], v['abstract'], v['body'], v['bib'], v['ref'], v['back'], fn,
			example_cleaned_abstract,
		)
