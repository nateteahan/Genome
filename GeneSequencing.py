#!/usr/bin/python3
from Matrix import *

from which_pyqt import PYQT_VER
if PYQT_VER == 'PYQT5':
	from PyQt5.QtCore import QLineF, QPointF
elif PYQT_VER == 'PYQT4':
	from PyQt4.QtCore import QLineF, QPointF
else:
	raise Exception('Unsupported Version of PyQt: {}'.format(PYQT_VER))

import math
import time

# Used to compute the bandwidth for banded version
MAXINDELS = 3

# Used to implement Needleman-Wunsch scoring
MATCH = -3
INDEL = 5
SUB = 1

class GeneSequencing:

	def __init__( self ):
		pass

	def align( self, sequences, table, banded, align_length):
		self.banded = banded
		self.MaxCharactersToAlign = align_length
		results = []

		for i in range(len(sequences)):
			jresults = []
			for j in range(len(sequences)):

				if(j < i):
					s = {}
				else:
					sequence_one = sequences[i][:align_length]
					sequence_two = sequences[j][:align_length]

					if banded:
						if (i == 0 or i == 1) and j > 1:
							score = float("inf")
							alignment1, alignment2 = "No alignment possible", "No alignment possible"
						elif i > 1 and (j == 0 or j == 1):
							score = float("inf")
							alignment1, alignment2 = "No alignment possible", "No alignment possible"
						else:
							matrix = Restricted(sequence_one, sequence_two)
							alignment1, alignment2 = matrix.compute_alignment()
							# alignment1 = alignment1[:99]
							# alignment2 = alignment2[:99]
							score = matrix.get_final_score()

					else:
						matrix = Matrix(sequence_one, sequence_two)

						alignment1, alignment2 = matrix.compute_alignment()
						# alignment1 = alignment1[:99]
						# alignment2 = alignment2[:99]
						score = matrix.get_final_score()

					s = {'align_cost':score, 'seqi_first100':alignment1, 'seqj_first100':alignment2}
					table.item(i,j).setText('{}'.format(int(score) if score != math.inf else score))
					table.update()	
				jresults.append(s)
			results.append(jresults)
		return results


