"""
===============================
Form Function Tables (formFunctionTables.py)
===============================
Mark Gotham and Thomas Posen, 2022


LICENCE:
===============================
Creative Commons Attribution-ShareAlike 4.0 International License
https://creativecommons.org/licenses/by-sa/4.0/


ABOUT:
===============================
Form Function terminology, organised first in tables then in objects.
See Caplin 1998.

TODO:
===============================
Add more options, e.g. 
1.
Altered scale degrees
- [[4,sharp4,5], (None, 6, None), 'Cadential', None, 'Half'],
- [[6,flat6,5], (None, 6, None), 'Cadential', None, 'Half'],
2.
(Perhaps) Sub-Dominant prolongations (only if more likely readings failed).
3.
(Perhaps) refactor to add attributes to each RN object, e.g.:
- .stageInFunction = 1
- .repetitionOfStageInFunction = 3
Note, would need to handle multiple entries.
4.
(Perhaps) subclasses on FormFunctionInTheory:
- classProlongation(FormFunctionInTheory):
- class Cadential(FormFunctionInTheory):
- class Sequence(FormFunctionInTheory):
"""

import unittest
import typing as t


# ------------------------------------------------------------------------------

class FormFunctionInTheory:

    def __init__(self,
                 bassScaleDegrees: tuple = (),
                 requiredFigures: tuple = (),
                 whatFunctionProlonged: t.Optional[str] = '',  # Note, only for prolongations
                 prolMedCadStream: str = '',
                 prolMedCadType: str = '',
                 ):
        self.bassScaleDegrees = bassScaleDegrees
        self.requiredFigures = requiredFigures
        self.whatFunctionProlonged = whatFunctionProlonged
        self.prolMedCadStream = prolMedCadStream
        self.prolMedCadType = prolMedCadType

        self.functionalLabel = ''
        self.shortLabel = ''

        self.makeFirstOrderLabel()

        # TODO 2nd, 3rd, ... Order
        # self.phraseFunctionLabel = None  # ['Initial', 'Medial', 'Cadential', None]
        # self.themeFunctionLabel = None  # ['Theme', None]
        # self.themeTypeLabel = None  # Sentence, Period, Hybrid

    def makeFirstOrderLabel(self):
        """
        Makes a label for the defined bass patterns.
        """
        if self.prolMedCadStream == 'Prolongation':
            self.functionalLabel = \
                f'{self.whatFunctionProlonged} {self.prolMedCadStream} with {self.prolMedCadType}'
            self.shortLabel = f'{self.whatFunctionProlonged[0]}-{self.prolMedCadType[0]}'
        elif self.prolMedCadStream == 'Cadential':
            self.functionalLabel = f'{self.prolMedCadType} {self.prolMedCadStream} Progression'
            self.shortLabel = f'Cad-{self.prolMedCadStream[0:4]}'
        else:
            raise ValueError


# ------------------------------------------------------------------------------

prolongation3 = [
    
    # Prolongations: Tonic, SD 1 -  Usually Rule of the Octave segments
    [[1, 2, 1], (5, 6, 5), 'Prolongation', 'Tonic', 'Neighbor, Upper'],
    [[1, 7, 1], (5, None, 5), 'Prolongation', 'Tonic', 'Neighbor, Lower'],
    [[1, 4, 3], (1, 4, 6), 'Prolongation', 'Tonic', 'Neighbor, Incomplete'],
    [[1, 5, 1], (5, 5, 5), 'Prolongation', 'Tonic', 'Harmonic'],  # Possible confusion with I-V-I
    [[1, 4, 1], (5, 5, 5), 'Prolongation', 'Tonic', 'Harmonic'],  # Possible confusion with I-V-I

    # Prolongations: Tonic, SD 3 - Usually Rule of the Octave segments
    [[3, 2, 3], (6, 6, 6), 'Prolongation', 'Tonic', 'Neighbor, Lower'],
    [[3, 4, 3], (6, 4, 6), 'Prolongation', 'Tonic', 'Neighbor, Upper'],

    # Prolongations: Tonic, Changing SD -  Usually Rule of the Octave segments
    [[1, 2, 3], (5, 6, 6), 'Prolongation', 'Tonic', 'Passing'],
    [[3, 2, 1], (6, 6, 5), 'Prolongation', 'Tonic', 'Passing'],
    [[1, 6, 3], (5, 5, 6), 'Prolongation', 'Tonic', 'Arpeggiating'],

    # Substitute
    [[1, 6, 1], (5, 5, 5), 'Prolongation', 'Tonic', 'Substitute'],

]


pedalProlongation3 = [

    # Prolongations: Pedals (T and D)
    # TODO S and relevance of pedals here ... currently handled separately - integration TODO
    [[1, 1, 1], (5, 4, 5), 'Prolongation', 'Tonic', 'Pedal'],  # end on 53 except concerto cadenza.
    [[5, 5, 5], (5, 4, 5), 'Prolongation', 'Dominant', 'Pedal'],

]


cadences3 = [

    # Cadences
    [[4, 5, 1], (None, 7, 5), 'Cadential', None, 'Authentic'],  # Note 7th.
    [[4, 5, 1], (None, 5, 5), 'Cadential', None, None],  # Note doesn't have 7th. TODO unclear.

    # Cadential Deviations (leaving scale-degree 5)
    [[5, 4, 3], (5, 4, 6), 'Cadential', None, 'Abandoned'],
    [[4, 5, 3], (None, 5, 6), 'Cadential', None, 'Evasion'],
    [[4, 5, 6], (None, 5, 5), 'Cadential', None, 'Deceptive Resolution'],

]


prolongation4 = [

    # Prolongations: Tonic, SD 1
    [[1, 2, 7, 1], (5, 6, None, 5), 'Prolongation', 'Tonic', 'Neighbor, Double'],
    [[1, 7, 2, 1], (5, None, 6, 5), 'Prolongation', 'Tonic', 'Neighbor, Double'],
    # [[1,4,7,1], (5, 4, None, 5), 'Prolongation', 'Tonic', None],  # TBC

    # Prolongations: Tonic, SD 3
    [[3, 4, 2, 3], (6, 4, 6, 6), 'Prolongation', 'Tonic', 'Neighbor, Double'],
    [[3, 2, 4, 3], (6, 6, 4, 6), 'Prolongation', 'Tonic', 'Neighbor, Double'],

    # Prolongations: Tonic, Changing SD
    [[1, 2, 4, 3], (5, 6, 4, 6), 'Prolongation', 'Tonic', 'Cambiata'],
    [[1, 2, 4, 3], (5, 6, 4, 6), 'Prolongation', 'Tonic', 'Cambiata'],
    [[3, 2, 7, 1], (6, 6, None, 5), 'Prolongation', 'Tonic', 'Cambiata'],

]


cadences4 = [

    # Cadence
    [[3, 4, 5, 1], (6, None, None, 5), 'Cadential', None, 'Complete'],
    [[4, 5, 5, 1], (None, 4, 5, 5), 'Cadential', None, 'Incomplete'],

]


# TODO: sequences
# NB: generic intervals
# NB: do not segment analysis by 'modulation' and do complete incomplete triads
# NB: interval from chord to next (hence same number of intervals and figures)

# sequencePatternList = [
#     # See https://musescore.com/fourscoreandmore/scores/5350121
#     # 6-6
#     [(1, 2), (5, 6), '6-6- Ascending'],
#     [(-2, -2), (5, 6), '6-6- Descending'],
#     # 5-6
#     [(1, 2), (5, 6), '5-6- Alternation Ascending'],
#     [(-2, -2), (5, 6), '5-6- Alternation Descending'],
#     # 7-6
#     [(1, 2), (7, 6), '7-6- Alternation Ascending'],
#     [(-2, -2), (7, 6), '7-6- Alternation Descending'],
#     # Circle of fifths
#     [(4, -5), (5, 5), 'Descending circle of fifths'],  # Bass: C, F, B
#     [(-3, 2), (5, 6), 'Zigzag: descending circle of fifths'],  # Bass: C, A, B
#     [(1, 5, 1, -4), (4, 3, 4, 3), '4-3- Ascending circle of fifths'],  # Bass: C, C, G, G
#     # 2-3
#     [(1, 2), (9, 8), '2-3- Alternation Ascending'],
#     [(-2, 1), (2, 3), '7-6- Alternation Descending'],  # Sic (-2, 1): bass sus.
# ]


# ------------------------------------------------------------------------------

def makeListOfFormFunctionObjects(data: list = prolongation3):
    """
    Converts a lists of lists into lists of FormFunctionInTheory objects.
    """
    out_data = []
    for entry in data:
        f = FormFunctionInTheory(bassScaleDegrees=entry[0],
                                 requiredFigures=entry[1],
                                 prolMedCadStream=entry[2],
                                 whatFunctionProlonged=entry[3],  # Currently for all. TBC
                                 prolMedCadType=entry[4]
                                 )
        out_data.append(f)
    return out_data


# ------------------------------------------------------------------------------

global3 = makeListOfFormFunctionObjects(prolongation3 + pedalProlongation3 + cadences3)
global4 = makeListOfFormFunctionObjects(prolongation4 + cadences4)


# ------------------------------------------------------------------------------

class Test(unittest.TestCase):
    def testFirstOrderNaming(self):
        """
        Test that we have only used a fixed and small collection of terms.        
        """
        
        for item in global3:
        
            self.assertIn(item.prolMedCadStream,
                          ['Prolongation',
                           'Sequence',
                           'Cadential']
                          )
            self.assertIn(item.whatFunctionProlonged,
                          ['Tonic',
                           'Pre-Dominant',
                           'Subdominant',
                           'Dominant',
                           None]
                          )

            if item.prolMedCadStream == 'Prolongation':
                self.assertIn(item.prolMedCadType,
                              ['Neighbor',
                               'Neighbor, Upper',
                               'Neighbor, Lower',
                               'Neighbor, Incomplete',
                               'Neighbor, Double',
                               'Pedal',
                               'Passing',
                               'Substitute',
                               'Arpeggiating',
                               'Harmonic',
                               'Cambiata',
                               None]
                              )
            elif item.prolMedCadStream == 'Cadential':
                self.assertIn(item.prolMedCadType,
                              ['Complete',
                               'Incomplete',
                               'Authentic',
                               'Inauthentic',
                               'Embellished',
                               'Expanded',
                               'Abandoned',
                               'Evasion',
                               'Deceptive Resolution',
                               None]
                              )
            else:
                raise ValueError


# -----------------------------------------------------------------------------

if __name__ == '__main__':
    unittest.main()
