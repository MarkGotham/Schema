"""
===============================
Bass To Form Function (bassToFormFunction.py)
===============================

Mark Gotham and Lenz Weinreich, 2022


LICENCE:
===============================

Creative Commons Attribution-ShareAlike 4.0 International License
https://creativecommons.org/licenses/by-sa/4.0/


ABOUT:
===============================

Produces a plausible form functional analysis (first order only)
given only a harmonic analysis alone (not even the score).

"""

# ------------------------------------------------------------------------------

from music21 import roman, spanner, stream
import unittest
from itertools import groupby

import formFunctionTables


# ------------------------------------------------------------------------------

class FormFunctionInPractice(formFunctionTables.FormFunctionInTheory):
    """
    The formFunctionTables.FormFunctionInTheory objects define a schema _in principle_.

    This FormFunctionInPractice class works with an actual manifestation
    in the practice of a specific harmonic analysis.
    """

    def __init__(self, rns: list):
        self.rns = rns
        self.bassScaleDegrees = [x.bassScaleDegreeFromNotation() for x in rns]
        self.figures = [x.figuresNotationObj.numbers for x in rns]
        # NB: self.functionalLabel from self.formFunctionInTheory.functionalLabel
        self.index = -1
        self.uncondensedRns = []
        self.formFunctionInTheory = None
        self.getFormalFunction()
        self.functionalLabel = None
        if self.formFunctionInTheory:
            self.functionalLabel = self.formFunctionInTheory.functionalLabel
        self.pedalPoint = None

        self.duration = None
        if self.formFunctionInTheory:
            self.getDuration()

    def getFormalFunction(self):
        """
        Assesses a group of 3 or 4 harmonies and
        compares it with the function.
        """

        if len(self.rns) == 3:
            data = formFunctionTables.global3
        elif len(self.rns) == 4:
            data = formFunctionTables.global4
        else:
            data = []  # TODO shouldn't happen: raise ValueError('Invalid number of RNs.')

        for thisFormFunctionInTheory in data:
            if thisFormFunctionInTheory.bassScaleDegrees == self.bassScaleDegrees:
                counter = 0
                found = True
                for fig in thisFormFunctionInTheory.requiredFigures:
                    if fig and fig not in self.figures[counter]:
                        found = False
                    counter += 1
                if found:
                    self.formFunctionInTheory = thisFormFunctionInTheory

    def getDuration(self):
        self.duration = sum([x.quarterLength for x in self.rns])


allFFInPractice = []


def fillScoreWithMedial(rns: list):
    """
    Covers the score with `*Medial?*` as a proxy for unassigned.
    TODO: replace with rn.isAssigned or similar.

    :param rns: List of Roman Numerals
    :return:
    """
    for rn in rns:
        rn.addLyric('*Medial?*')


def writeAllInformationInAnalysis(allFFInPractice: list,
                                  analysis: stream.Part):
    """
    Writes all information (slurs, Labels) 
    of a given List of FormFunctionsInPractice 
    to the score.

    :param allFFInPractice: a list of to write FormFunctionInPractice objects
    :param analysis: analysis (stream.Part object)
    :return:
    """
    for index in range(len(allFFInPractice)):
        writeInformationInScore(allFFInPractice, index, analysis)


def writeInformationInScore(allFFInPractice: list,
                            index: int,
                            analysis: stream.Part):
    """
    Writes slur and Label for one given (index) FormFunctionInPractice in a given analysis

    :param allFFInPractice: a list of FormFunctionInPractice objects to write
    :param index: index of a FormFunctionObject in the List
    :param analysis: analysis (stream.Part object)
    :return:
    """
    trailingPedal = trailingPedalPoint(allFFInPractice, index)

    if trailingPedal != -1:
        # if there is a Trailing Pedal Point it will be the next FormFunction in the List
        rnStart = allFFInPractice[index].uncondensedRns[0]
        rnEnd = allFFInPractice[index].uncondensedRns[trailingPedal]
        if allFFInPractice[index].formFunctionInTheory:
            prolOrCad = allFFInPractice[index].formFunctionInTheory.prolMedCadStream
            insertSlur(analysis, rnStart, rnEnd, prolOrCad)
            lyricAdd(rnStart, allFFInPractice[index].formFunctionInTheory.functionalLabel)
    else:
        rnStart = allFFInPractice[index].uncondensedRns[0]
        rnEnd = allFFInPractice[index].uncondensedRns[
            len(allFFInPractice[index].uncondensedRns) - 1]

        if allFFInPractice[index].formFunctionInTheory:
            prolOrCad = allFFInPractice[index].formFunctionInTheory.prolMedCadStream
            insertSlur(analysis, rnStart, rnEnd, prolOrCad)
            lyricAdd(rnStart, allFFInPractice[index].formFunctionInTheory.functionalLabel)

    removeTrailingMedialLyric(allFFInPractice[index])


def removeTrailingMedialLyric(formFunctionInPracticeObject: FormFunctionInPractice):
    """
    Removes all '*Medial?*' Labels of a given FormFunctionInPractice from the analysis

    :param formFunctionInPracticeObject: FormFunctionInPractice Object
    :return:
    """
    for rn in formFunctionInPracticeObject.uncondensedRns:
        if '*Medial?*' in rn.lyric:
            rn.lyric = rn.lyric.replace('*Medial?*', '')


def lyricAdd(rn: roman.RomanNumeral,
             lyric: str):
    """
    Adds a lyric in to a given RN. If '*Medial?*' was contained in the lyric, '*Medial?*' will be replaced by the
    new value.

    :param rn: RomanNumeral
    :param lyric: a String lyric
    :return:
    """
    if '*Medial?*' in rn.lyric:
        rn.lyric = rn.lyric.replace('*Medial?*', '')
    rn.addLyric(lyric)


def trailingPedalPoint(allFFInPractice: list,
                       indexOfAll: int):
    """
    If there is a trailing PedalPoint in the RNs,
    return the index relative to the phrase without the pedalpoint.
    If there is no trailing PedalPoint return -1

    :param allFFInPractice: a List of FormFunctionInPractice objects
    :param indexOfAll: index of current FFIP Objects in that List
    :return: index of Trailing Pedal Point relative to FFIP Start
    """
    # last FormFunction can't have a trailing FormFunction
    if indexOfAll == len(allFFInPractice) - 1:
        return -1

    currentRns = allFFInPractice[indexOfAll]
    potentialPedalPoint = allFFInPractice[indexOfAll + 1]
    endIndexOfToBeTestedRns = len(currentRns.uncondensedRns) + currentRns.index
    endIndexOfPotentialPedalPoint = len(
        potentialPedalPoint.uncondensedRns) + potentialPedalPoint.index

    # Pedal Point is at the End of a larger FormFunctionInPractice -> trailing
    if (endIndexOfToBeTestedRns == endIndexOfPotentialPedalPoint) and \
            ('Pedal' in allFFInPractice[indexOfAll + 1].functionalLabel):
        return potentialPedalPoint.index - currentRns.index
    return -1


def appendFormFunction(rns: list,
                       start: int,
                       end: int,
                       label: str,
                       condensedRns):
    """
    Appends a FormFunctionInPractice Object, 
    built from the condensedRns, 
    to the global list allFFInPractice.

    :param rns: list of Roman Numerals
    :param start: startIndex in List of to build FFIP
    :param end: endIndex in List of to build FFIP
    :param label: label that will be assigned to FFIP
    :param condensedRns: collapsed Roman Numerals
    :return:
    """
    f = FormFunctionInPractice(condensedRns)
    if len(condensedRns) != end - start + 1:
        f.uncondensedRns = rns[start:(end + 1)]
    else:
        f.uncondensedRns = f.rns
    f.index = start
    if label:
        f.functionalLabel = label
    if not existsInFormFunctionList(f):
        allFFInPractice.append(f)


def existsInFormFunctionList(f: FormFunctionInPractice) -> bool:
    """
    Returns True iff
    a given FormFunctionInPractice Object is contained
    in the global List allFFInPractice.

    :param f: a FormFunctionInPractice object
    :return: bool
    """
    for formFunction in allFFInPractice:
        if pedalPointInPedalPoint(f, formFunction):
            return True
        if formFunction.index == f.index:
            if f.functionalLabel == formFunction.functionalLabel:
                return True
    return False


def pedalPointInPedalPoint(fNew: FormFunctionInPractice, fOld: FormFunctionInPractice):
    """
    If a pedal Point is contained in another PedalPoint (probably never) return true
    else false

    :param fNew: a FormFunctionInPractice object
    :param fOld: a FormFunctionInPractice object
    :return:
    """
    if 'Pedal' in fNew.functionalLabel and 'Pedal' in fOld.functionalLabel:
        startOldFormFunction = fOld.index
        endOLdFormFunction = fOld.index + len(fOld.uncondensedRns)
        startNewFormFunction = fNew.index
        endNewFormFunction = fNew.index + len(fNew.uncondensedRns)
        if startOldFormFunction <= startNewFormFunction and endOLdFormFunction >= endNewFormFunction:
            return True
        return False


def insertSlur(thisPart: stream.Part,
               rn1: roman.RomanNumeral,
               rn2: roman.RomanNumeral,
               prolongationOrCadence: str = 'Prolongation'):
    """
    Add slurs to the analysis to indicate granular Prolongation or Cadential motions.

    :param thisPart:
    :param rn1: first Roman numeral of the span in question (start)
    :param rn2: last ***form defining*** Roman numeral of the span in question (end)
    :param prolongationOrCadence:
    :return:
    """
    # Slur
    sl = spanner.Slur(rn1, rn2)
    # TODO: placement doesn't currently work
    if prolongationOrCadence == 'Prolongation':
        sl.placement = 'below'
    elif prolongationOrCadence == 'Cadential':
        sl.placement = 'above'
    else:
        raise ValueError('prolongationOrCadence must be "Prolongation" or "Cadential".')
    # TODO add case of 'Medial'

    thisPart.insert(sl)


def splitter(text):
    """
    Splits a given Text into segments of the same character and return that list.
    Example: "112233334111" will be split into -> ['11','22','3333','4','111']

    :param text: in our case, a sequence of bass notes
    :return:
    """
    return ','.join(''.join(group) for key, group in groupby(text)).split(',')


def reduceRnsToLengthX(rnsList: list,
                       listLength: int,
                       startIndex: int) -> tuple:
    """
    returns a Tuple containing:
    at 0th position: RNs List of given length "listLength" which might be a reduced RNs version
    which collapses sequential RNs which share the same bass note.
    Example: bass line: 15551 listLength: 3 reduced to: 151
    at 1st position: the new Index in the rnsList the program has to skip
    at 2nd position: a Pedal Point, if contained in the looked at RNs

    :param rnsList: List of Roman Numerals
    :param listLength: length of the reduction
    :param startIndex: index of start Roman Numeral
    :return:
    """
    counter = startIndex + 1
    while counter < (len(rnsList)):
        bassLineList = [str(x.bassScaleDegreeFromNotation()) for x in
                        rnsList[startIndex:counter + 1]]
        bassLineString = ''.join(bassLineList)
        bassLineSplit = splitter(bassLineString)
        if len(bassLineSplit) > listLength:  # go explicitly one step too far
            break
        else:
            counter += 1

    rnsInterval = rnsList[startIndex:counter]
    bassLineList = [str(x.bassScaleDegreeFromNotation()) for x in rnsList[startIndex:counter]]
    bassLineString = ''.join(bassLineList)
    bassLineSplit = splitter(bassLineString)

    pedalPointsList = getPotentialPedalPoints(rnsInterval, bassLineSplit, startIndex)
    # pedalPointObjects = createFormFunctionObjectsFromIndicesTuple(pedalPointsList, rnsList)
    
    finalRns = getRnsOutOfbassLine(rnsInterval, bassLineSplit)
    indexRnTuple = (finalRns, startIndex + len(bassLineList), pedalPointsList)
    return indexRnTuple


# TODO: implement:
# def createFormFunctionObjectsFromIndicesTuple(pedalPointsList: list, rns: list):
#     """
#     Current use case for PedalPoints, but could be expanded.
#     returns the a List of created FormFunctionInPractice Objects from a List,
#     containing Start and End Indices
#     :param pedalPointsList: List of created FormFunctionInPractice Objects
#     :return: list
#     """


def getRnsOutOfbassLine(allRnsList: list, bassLineList: list):
    """
    takes the first Roman Numeral of each bassLine segement and appends it to a list
    Example: given bassLineList: ['11','22','3333','4','111']
    return the RomanNumerals at postions 0,2,4,8,10 in a list

    :param allRnsList:
    :param bassLineList: a list of bassnotes such as ['11','22','3333','4','111']
    :return:
    """
    finalRnList = []
    index = 0
    for bassLine in bassLineList:
        finalRnList.append(allRnsList[index])
        index += len(bassLine)
    return finalRnList


def getPotentialPedalPoints(rnsInterval: list, bassLineSplit: list, pieceIndex: int):
    """
    Returns all pedalpoints of a given bassLineSplit as Tuples (startIndex, endIndex) in a list

    :param rnsInterval: the Roman Numerals that map to the bassLine
    :param bassLineSplit: list of bassLines such as ['11','22','3333','4','111']
    :param pieceIndex: current index of the progress of the whole piece
    :return:
    """
    indexStart = 0
    indexEnd = 0
    pedalPointsList = []
    for bassNoteCluster in bassLineSplit:
        indexEnd = indexEnd + len(bassNoteCluster)
        rnsSubList = rnsInterval[indexStart: indexEnd]
        indexOfSubListInActualPiece = indexStart + pieceIndex
        potentialPedalPoint = getPotentialPedalPoint(rnsSubList, indexOfSubListInActualPiece)
        if potentialPedalPoint:
            pedalPointsList.append(potentialPedalPoint)
        indexStart = indexEnd
    return pedalPointsList


def getPotentialPedalPoint(rnsSubList: list, index: int):
    """
    Returns a pedalpoint as a Tuple in the form (startIndex, endIndex)

    :param rnsSubList: Roman Numerals that must be checked for pedalpoint
    :param index: current index of the progress of the whole piece
    :return:
    """
    indexEssentialMiddlePart = getEssentialPedalPart(rnsSubList)
    indexPedalPointEnd = findEndPedalPoint(rnsSubList)
    if indexEssentialMiddlePart != -1 and indexPedalPointEnd != -1:  # end exists so find the middle
        return index, index + indexPedalPointEnd  # relative Index of start and end of pedal point
    else:
        return None


def findEndPedalPoint(rnsSubList: list, mustIncludeFig: int = 5):
    """
    Find the end of a pedal passage.
    endMustInclude defined the figures that must be in the final chord (usually 5).

    :param rnsSubList: a list of Roman numerals.
    :param mustIncludeFig: a number that must be included in the figured bass.
    :return:
    """

    index = len(rnsSubList) - 1
    while index >= 0:  # search form back to front for speed
        if mustIncludeFig in rnsSubList[index].figuresNotationObj.numbers:
            break
        index -= 1
    return index  # if index -1 there is no PedalPoint because it doesnt end


def getEssentialPedalPart(rnsSubList: list, mustIncludeFig: int = 4):
    """
    Other point in a pedal passage (NB: not the end).

    Like findEndPedalPoint, but within,
    hence require (mustIncludeFig) 4 (i.e., 64) not 5 (i.e., 53).

    :param rnsSubList: a list of Roman numerals.
    :param mustIncludeFig: a number that must be included in the figured bass.
    :return:
    """

    index = len(rnsSubList) - 1
    while index >= 0:  # search form back to front
        # print(rnsSubList[index].figuresNotationObj.numbers)
        if mustIncludeFig in rnsSubList[index].figuresNotationObj.numbers:
            break
        index -= 1
    return index  # if index -1 there is no PedalPoint because it doesnt end

# # TODO
# def generateHigherOrder(listofFormFunctionInPracticeObjects: list):


# ------------------------------------------------------------------------------

class Test(unittest.TestCase):
    def testBassPattern(self):
        """
        One test case for a hypothetical set of RNs.
        """

        rn1 = roman.RomanNumeral('I')
        rn2 = roman.RomanNumeral('V43')
        rn3 = roman.RomanNumeral('I6')
        rn4 = roman.RomanNumeral('IV')
        rn5 = roman.RomanNumeral('V')

        test3 = FormFunctionInPractice([rn1, rn2, rn3])
        self.assertEqual(test3.functionalLabel, 'Tonic Prolongation with Passing')

        test4 = FormFunctionInPractice([rn1, rn2, rn3, rn4])
        self.assertEqual(test4.functionalLabel, None)

        test5 = FormFunctionInPractice([rn1, rn2, rn3, rn4, rn5])
        self.assertEqual(test5.functionalLabel, None)  # TODO should prob. be self.assertRaises


# -----------------------------------------------------------------------------

if __name__ == '__main__':
    unittest.main()
