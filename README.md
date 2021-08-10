# K-Shingles
Sample implementation of basic K-Shingling similarity analysis, written in Python 2.7. This program will take any number of text documents and calculate the similarity of their contents based on the substrings present in each one.

## Usage
`similarity.py`

This file is meant to be run on the command-line in the same directory as the `data/` folder, where any documents to be analyzed should be stored for easy use. This folder contains some sample documents with various character encodings that will be used by the program automatically if none are specified:
* `BB.txt`, Kate Chopin's *Beyond the Bayou* (english)
* `DQ.txt`, Miguel de Cervantes' *The Ingenious Gentleman Don Quixote of La Mancha* (spanish)
* `niebla.txt`, Miguel de Unamuno's *Niebla* (spanish)
* `awaken.txt`, Kate Chopin's *The Awakening* (english)
* `odyssey.txt`, Homer's *The Odyssey* (english, translated by Samuel Butler)

*Note*: This code was created with `.txt` files in mind, although similar formats may still be parsed correctly (`.rtf`, `.csv`, etc.)

To use the program, run `python similarity.py <K> [docs]`:
* K: Positive integer representing length of K-Shingles to use. Typical values will range from [3, 5], depending on the content.
* docs: Space-separated list of document filenames to use (optional, otherwise will default to fileset above).
