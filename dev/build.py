from os.path import join


def main(urd):
	imp = urd.build('import',               directory='biorxiv_medrxiv/biorxiv_medrxiv/pdf_json')
	imp = urd.build('import', previous=imp, directory='comm_use_subset/comm_use_subset/pdf_json')
	imp = urd.build('import', previous=imp, directory='custom_license/custom_license/pdf_json')
	imp = urd.build('import', previous=imp, directory='noncomm_use_subset/noncomm_use_subset/pdf_json')
	imp = urd.build('import', previous=imp, directory='comm_use_subset/comm_use_subset/pmc_json')
	imp = urd.build('import', previous=imp, directory='custom_license/custom_license/pmc_json')
	imp = urd.build('import', previous=imp, directory='noncomm_use_subset/noncomm_use_subset/pmc_json')

	filename = 'out.tsv'
	job = urd.build('csvexport',
		source=imp,
		filename=filename,
		separator='\t',
		chain_source=True,
		labels=('filename', 'sha', 'abstract', 'title', 'exabstract',),
		labelsonfirstline=True,
	)
	job.link_result(filename)  # create a link to the file in result_directory

	print()
	urd.joblist.print_exectimes()

	print("\nOutput filename: \"\x1b[1m%s\x1b[0m\"." % (job.filename(filename),))
	print("\nA link to the file is created in the result_directory,\ni.e. \"\x1b[1m%s\x1b[0m\"." %
	      (join(urd.info.result_directory, filename)))
	print("\n(Try \"\x1b[1max dsinfo %s\x1b[0m\" to get dataset information.)" % (imp,))
