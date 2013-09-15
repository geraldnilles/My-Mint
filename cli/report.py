#-----------------
# Account CLI
#
# Parses account CLI commands
#-------------------

import argparse
import mymint.db
import mymint.report

def parse(arg_list):
	parser = argparse.ArgumentParser(description="Report Generator")
	parser.add_argument("-d","--db", required=True, metavar="database.json")

	args = parser.parse_args(arg_list)


	db = mymint.db.db(args.db)
	mymint.report.generate(db)
	
	
	
