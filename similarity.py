#!/usr/bin/env python2.7

import pprint
import re
import string
import sys
import unicodedata

import numpy as np
import pandas as pd

'''
k_shingle(String, Int) -> List[String]
Converts the given document into a set of k-shingles (length-k substrings).

@param doc: Text document to be converted
@param k: Length of resulting k-shingles
'''
def k_shingle(doc, k):
	
	res = []
	for i in range(len(doc)):
		j = i + k
		if (j == len(doc) - 1): break
		res.append(doc[i:j])
		
	return list(set(res))

'''
normalize(String) -> String
Standardizes the encoding, punctuation, and case of the given string before similarity analysis.

@param line: Text string to be normalized
'''
def normalize(line):

	newline = "".join((char for char in line if char not in string.punctuation)) # Strip punctuation
	newline = unicodedata.normalize("NFD", unicode(newline, 'utf-8')) # Strip accents
	newline = newline.encode("ascii", "ignore") # Normalize character encoding, ignoring invalid characters
	newline = newline.decode("utf-8")
	newline = re.sub(r"[\t\r]*", "", newline).strip() # Strip tab, return, and trailing newline characters
	newline = newline.lower() # Normalize case

	return newline

'''
generate_matrix(Dict[String, String]) -> DataFrame[Int]
Generates a binary matrix between each document name and the shingles across all documents, with each cell containing a 1 if a given shingle is present in that document, and a 0 otherwise.

@param docs: Dictionary object mapping document names to their text contents
'''
def generate_matrix(docs):

	doc_shingles = {doc: k_shingle(docs[doc], sys.argv[1]) for doc in docs.keys()} # Map from document names to corresponding k-shingles
	shingles = list(set(sum([doc_shingles[doc] for doc in doc_shingles], []))) # Set of total unique k-shingles
	s_indices = {i: shingle for i, shingle in enumerate(shingles)} # Map from unique index to each k-shingle
	d_indices = {i: doc for i, doc in enumerate(docs.keys())} # Map from unique index to each document name

	nrow = len(shingles)
	ncol = len(doc_shingles)
	C = np.zeros((nrow, ncol)) # Initialize characteristic (binary) matrix

	for row in range(len(C)):
		for col in range(len(C[row])):
			if (s_indices[row] in doc_shingles[d_indices[col]]): C[row][col] = 1

	dfC = pd.DataFrame(C, columns = docs.keys(), index = shingles) # Convert matrix to DataFrame object

	return dfC

'''
compute_sims(DataFrame[Int]) -> Dict[String, Dict[String, Float]]
Calculates similarities between all documents and returns their relative scores as a nested dictionary object.

@param df: Binary matrix DataFrame output from generate_matrix()
'''
def compute_sims(df):

	sims = {}
	for doc1 in df.columns:
		for doc2 in df.columns:
			numerator = np.sum((df[doc1] == 1) & (df[doc2] == 1)) # Number of shingles present in both documents
			denominator = np.sum((df[doc1] == 1) | (df[doc2] == 1)) # Number of shingles present in either document
			sim = (float(numerator) / denominator) # Cast to avoid integer division
			sim = float("{:0.3f}".format(sim)) # Truncate and preserve value
			if (doc1 not in sims): sims[doc1] = {doc2: sim}
			else: sims[doc1].update({doc2: sim})

	return sims

'''
main(None) -> None
Accepts a positive integer K representing the desired K-shingle length and any number of documents as command-line arguments, and prints the final similarity scores between each document.
K should be specified as the first argument, followed by the document filenames to be analyzed; if no documents are given, the default set of files will be used.
'''
def main():

	if (len(sys.argv) == 1 or not sys.argv[1].isdigit() or int(sys.argv[1]) < 1): # Validate K value
		print("Missing or invalid K value")
		sys.exit(-1)
	else:
		print("Computing document similarities for K = {k}:".format(k = sys.argv[1]))
		sys.argv[1] = int(sys.argv[1])

	docs = None # Initialize map from document names to contents
	def_files = ["awaken.txt", "BB.txt", "DQ.txt", "odyssey.txt", "niebla.txt"] # Default fileset
	
	if (len(sys.argv) == 2):
		print("No documents specified, using default set...")
		docs = {def_files[i]: "" for i in range(len(def_files))}
	else:
		docs = {sys.argv[i]: "" for i in range(2, len(sys.argv))}

	for doc in docs:
		with open("data/" + doc) as f:
			for line in f:
				docs[doc] += normalize(line)
	
	matrix = generate_matrix(docs)
	scores = compute_sims(matrix)
	pprint.pprint(scores)

	sys.exit(0)

if (__name__ == "__main__"): main()

