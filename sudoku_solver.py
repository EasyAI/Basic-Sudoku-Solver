#! /usr/bin/env python

"""
Soduku Rules
- each column, row and box must contain numbers 1-9 without overlapping

"""

sodukuPuzzle = [
	[0, 0, 0, 7, 2, 0, 1, 0, 4],
	[7, 0, 1, 0, 0, 9, 8, 6, 0],
	[2, 9, 4, 0, 8, 1, 0, 0, 7],
	[8, 0, 6, 5, 0, 0, 0, 4, 3],
	[0, 0, 9, 1, 6, 0, 2, 7, 0],
	[5, 7, 0, 9, 3, 0, 0, 0, 8],
	[9, 2, 0, 4, 0, 7, 0, 8, 0],
	[0, 8, 3, 0, 9, 6, 7, 0, 0],
	[0, 6, 0, 0, 0, 3, 4, 2, 9]]

boxRow = 3
boxes = 9

template = [
	[0,1,2],
	[3,4,5],
	[6,7,8]]

boxAdjacent = [[1,2,3,6], [0,2,4,7], [0,1,5,8], [0,4,5,6], [1,3,5,7], [2,3,4,8], [0,3,7,8], [1,4,6,8], [2,5,6,7]]


def main():

	print_game(sodukuPuzzle)
	solving_algorithm(sodukuPuzzle)


def solving_algorithm(sodukuPuzzle):
	"""
	This script uses a type of wildcard mask to determin where to place a number in the puzzle.
	"""
	count = 0
	unSolvedPuzzle = sodukuPuzzle
	solved = False

	while not(solved):
		numFreq = [9, 9, 9, 9, 9, 9, 9, 9, 9]
		## numFreq is used to fin out how many time a number has occured

		blocksSimple = slice_boxes(unSolvedPuzzle)
		blocksComplex = []
		for block in blocksSimple:
			blocksComplex.append(build_block(block, style='complex'))

		## This checks every block to see how many time a number has been used.
		for i, box in enumerate(blocksSimple):
			for num in range(1, 10): 
				if num not in box:
					numFreq[num-1]-=1

		## This checks if the table has been filled.
		if sum(numFreq)/len(numFreq) == 9:
			solved = True
			break
		else:
			lastFreq = 0
			## This checks what number shows up the most and will then use it.
			for currNum, freq in enumerate(numFreq):
				if freq != 9:
					if freq > lastFreq:
						lastFreq = freq
						iValue = currNum+1

		for currBlockID, box in enumerate(blocksSimple):
			if not(iValue in box):
				## This goes over and checks if the current block has a specific number, if not the bot will try and place it in the block.
				adjBlockLocs = []
				currBlockLoc = get_val_loc(template, currBlockID)

				## Used to get the block locations of each adjacent block to the current one.
				for blockID in boxAdjacent[currBlockID]:
					adjBlockLocs.append(get_val_loc(template, blockID))

				blockWildcard = get_wildcard(currBlockLoc, adjBlockLocs, blocksComplex, iValue)

				numberOfOpen = 0
				## This is used to check if there is a sutible location to place a number based on the block wildcard.
				for row in blockWildcard:
					for element in row:
						if element != 'x':
							numberOfOpen += 1

				if numberOfOpen == 1:
					toPlace = get_val_loc(blockWildcard, '')
					if blocksComplex[currBlockID][toPlace[0]][toPlace[1]] == 0:
						blocksComplex[currBlockID][toPlace[0]][toPlace[1]] = iValue

				## This will just turn complex blocks back into block lists
				blocksSimple[currBlockID] = build_block(blocksComplex[currBlockID], style='simple')

		## This just rebuilds puzzle a new.
		unSolvedPuzzle = rebuild_puzzle(blocksSimple)

	print_game(unSolvedPuzzle)


def get_wildcard(currBlockLoc, adjBlockLocs, blocks, value):
	""" This gets a wildcard that will then be used to determin where to place the newest value. """
	blockWildcard = [
		['','',''], 
		['','',''], 
		['','','']]

	for position in adjBlockLocs:
		blockID = template[position[0]][position[1]]
		valueLoc = get_val_loc(blocks[blockID], value)

		if position[0] == currBlockLoc[0]:
			## If the block is on the same row as the current block.
			for i in range(3):
				if valueLoc != None:
					if blockWildcard[valueLoc[0]][i] != 'x':
						blockWildcard[valueLoc[0]][i] += 'x'

		elif position[1] == currBlockLoc[1]:
			## If the block is in the same column as the current block.
			for i in range(3):
				if valueLoc != None:
					if blockWildcard[i][valueLoc[1]] != 'x':
						blockWildcard[i][valueLoc[1]] += 'x'

		## Once checking what colums/rows are free the script then coveres every square with a number already in it.
		blockID = template[currBlockLoc[0]][currBlockLoc[1]]
		for i, row in enumerate(blocks[blockID]):
			for x, element in enumerate(row):
				if element != 0 and blockWildcard[i][x] == '':
					blockWildcard[i][x] = 'x'

	return(blockWildcard)


def get_val_loc(table, value):
	""" This is used to get a location of a specific value within a block/table. """
	valLoc = None
	for row in table:
		if value in row:
			valLoc = [table.index(row), row.index(value)]

	return(valLoc)


def build_block(block, style=None):
	""" This turns an 1d list of blocks into a 2d block. """
	builtBlock = []
	
	for row in range(3):
		if style == 'complex':
			rowStart = row*3
			rowEnd = (row*3)+3
			builtBlock.append(block[rowStart:rowEnd])

		elif style == 'simple':
			builtBlock += block[row]

	return(builtBlock)


def slice_boxes(puzzle):
	""" This turns the puzzle into simple block list. """
	boxeData = [[],[],[],[],[],[],[],[],[]]
	boxNum = 0
	
	for br in range(boxRow):
		row = br * 3
		for x in range(3):
			for i in range(row, row+3):
				boxeData[boxNum] += puzzle[i][x*3:x*3+3]

			boxNum += 1

	return(boxeData)


def rebuild_puzzle(slice_boxes):
	""" This is used to rebuild the puzzle. """
	blockNum = 0
	rebuiltPuzzle = []

	for blockRow in range(3):
		rowStart = blockRow * 3
		rowEnd = blockRow * 3 + 3
		for x in range(3):
			puzzleRow = []
			startVal = x*3
			endVal = (x*3)+3

			for i in range(rowStart, rowEnd):
				puzzleRow += slice_boxes[i][startVal:endVal]

			rebuiltPuzzle.append(puzzleRow)

	return(rebuiltPuzzle)


def print_game(puzzle):
	boxRow = 3
		
	print("###############################")
	for br in range(boxRow):
		row = br * 3
		
		for i in range(row, row+3):
			print("#" + str(puzzle[i][:3]) + "#" + (str(puzzle[i][3:6])) + "#" + str(puzzle[i][6:9]) + "#")
		print("###############################")


if __name__ == "__main__":
	main()
