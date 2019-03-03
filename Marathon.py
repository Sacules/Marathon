#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import midi

"""
Created on Sat Feb 23 08:03:51 2019

Marathon is a program to automatically create a 50% microrhythm between two
rhythmic patterns in MIDI.

Maraton takes a MIDI file by the name "marathon_in.mid" located in the same
folder as itself containing two MIDI tracks of same length and number of notes.
Marathon then creates the file "marathon_out.mid" by calculating the average
duration of each note pair in the two tracks and copying the channel, velocity,
and pitch pattern of the first track.

As of February 26, 2019, Marathon can also generate microrhythms for you,
without having to feed it a MIDI file. You can select from 6 different
rhythmic classes (like Swing Feel, Gnawa Triplet, or Brazilian 16ths), and
apply a morph value of your desire to create a microrhythm. For this feature
the program will output a file by the name "marathon_out.mid" that contains
the rhythmic pattern placed by default on C4 (note 60).

As of February 26, 2019, Marathon can also generate microrhythms for you,
without having to feed it a MIDI file. You can select from 6 different
rhythmic classes (like Swing Feel, Gnawa Triplet, or Brazilian 16ths), and
apply a morph value of your desire to create a microrhythm. For this feature
the program will output a file by the name "marathon_out.mid" that contains
the rhythmic pattern placed by default on C4 (note 60).

As of February 27, 2019, Marathon can also generate custom microrhythms
without the need for MIDI input. You can select preset "99" and write your
two rhythm tracks using text commands. Marathon accepts note length (from
whole to thirty-second notes), dots (up to 3), and tuplet feel (Marathon
is very flexible regarding tuplets, as they don't need to be whole to be
accepted). The syntax is "ndx/y":
* n is the note value
* d is the place for dots
* x/y is the tuplet space (it must be two integers separated by "/")
* Each note must be separated by a space or dash ("-") for tied notes

You can then choose a morph value and a number of repetitions, and then
the program will export the completed MIDI track as "marathon_out.mid".

Known issues:

    —Does not work properly with chords and multiple voices on one track.
    —May behave unexpectedly with time signatures or tempo changes and other
        more complex actions.

Suggestions:

    —Create simple MIDI files with a DAW to feed the program.
    —Create monophonic tracks. If you want multiphonic results, I suggest you
        create a MIDI file for each voice. Remember to write the same number of
        notes in each track if you want similar results. You can then manually
        recombine the different output files into one track on a DAW.
    —Tempo or time signature change, note bends, and other more complex actions
        are to be avoided for better results. You can apply those changes
        manually on the output track.

@author: DaveTremblay
"""


def presetSwing(morph, repeats):
    """TODO: Docstring for presetSwing.

    Args:
        morph: TODO
        repeats: TODO

    Returns: TODO

    """
    file_out = "marathon_out.mid"

    # straight
    notes1 = [0, 960, 0, 960]

    # phrased
    notes2 = [0, 1440, 0, 480]

    fm = 1
    rm = 960

    pat = midi.Pattern(format=int(fm), resolution=int(rm))
    tra = midi.Track()
    pat.append(tra)

    # pattern weight (must add up to 1.0)
    w1 = 1-float(morph)/100
    w2 = float(morph)/100

    # rounding correction
    rc = 0

    for n in range(int(repeats)):
        e = 0
        for event in notes2:
            tick1 = int(notes1[e])
            tick2 = int(notes2[e])

            # rounding correction
            rc += (w1 * tick1) + (w2 * tick2) - float(int(w1 * tick1) + (w2 * tick2))

            if rc % 1 < -0.5:
                tickm = int((w1 * tick1) + (w2 * tick2)) + int(rc) - 1
                rc = 0
            elif rc % 1 >= 0.5:
                tickm = int((w1 * tick1) + (w2 * tick2)) + int(rc) + 1
                rc = 0
            else:
                tickm = int((w1 * tick1) + (w2 * tick2)) + int(rc)
                rc = 0

            noteon = midi.NoteOnEvent(tick=0, channel=0, data=[60, 70])
            tra.append(noteon)
            noteoff = midi.NoteOffEvent(tick=tickm, channel=0, data=[60, 0])
            tra.append(noteoff)

            e += 1

        else:
            e += 1

    trackend = midi.EndOfTrackEvent(tick=1)
    tra.append(trackend)
    midi.write_midifile(file_out, pat)


def presetHalfSwing(morph, repeats):
    """TODO: Docstring for presetHalfSwing.

    Args:
        morph: TODO
        repeats: TODO

    Returns: TODO

    """

    file_out = "marathon_out.mid"

    # straight
    notes1 = [0, 1920, 0, 960, 0, 960]
    # phrased
    notes2 = [0, 1920, 0, 1440, 0, 480]

    fm = 1
    rm = 960

    pat = midi.Pattern(format=int(fm), resolution=int(rm))
    tra = midi.Track()
    pat.append(tra)

    # pattern weight (must add up to 1.0)
    w1 = 1-float(morph)/100
    w2 = float(morph)/100

    # rounding correction
    rc = 0

    for n in range(int(repeats)):
        e = 0
        for event in notes2:
            tick1 = int(notes1[e])
            tick2 = int(notes2[e])

            # rounding correction
            rc += (w1 * tick1) + (w2 * tick2) - float(int(w1 * tick1) + (w2 * tick2))

            if rc % 1 < -0.5:
                tickm = int((w1 * tick1) + (w2 * tick2)) + int(rc) - 1
                rc = 0
            elif rc % 1 >= 0.5:
                tickm = int((w1 * tick1) + (w2 * tick2)) + int(rc) + 1
                rc = 0
            else:
                tickm = int((w1 * tick1) + (w2 * tick2)) + int(rc)
                rc = 0

            noteon = midi.NoteOnEvent(tick=0, channel=0, data=[60, 70])
            tra.append(noteon)
            noteoff = midi.NoteOffEvent(tick=tickm, channel=0, data=[60, 0])
            tra.append(noteoff)

            e += 1

        else:
            e += 1

    trackend = midi.EndOfTrackEvent(tick=1)
    tra.append(trackend)
    midi.write_midifile(file_out, pat)


def presetWestAfricanTriplet(morph, repeats):
    """TODO: Docstring for presetWestAfricanTriplet.

    Args:
        morph: TODO
        repeats: TODO

    Returns: TODO

    """

    file_out = "marathon_out.mid"

    # straight
    notes1 = [0, 480, 0, 480, 0, 480]
    # phrased
    notes2 = [0, 720, 0, 360, 0, 360]

    fm = 1
    rm = 960

    pat = midi.Pattern(format=int(fm), resolution=int(rm))
    tra = midi.Track()
    pat.append(tra)

    # pattern weight (must add up to 1.0)
    w1 = 1-float(morph)/100
    w2 = float(morph)/100

    # rounding correction
    rc = 0

    for n in range(int(repeats)):
        e = 0
        for event in notes2:
            tick1 = int(notes1[e])
            tick2 = int(notes2[e])

            # rounding correction
            rc += (w1 * tick1) + (w2 * tick2) - float(int(w1 * tick1) + (w2 * tick2))

            if rc % 1 < -0.5:
                tickm = int((w1 * tick1) + (w2 * tick2)) + int(rc) - 1
                rc = 0
            elif rc % 1 >= 0.5:
                tickm = int((w1 * tick1) + (w2 * tick2)) + int(rc) + 1
                rc = 0
            else:
                tickm = int((w1 * tick1) + (w2 * tick2)) + int(rc)
                rc = 0

            noteon = midi.NoteOnEvent(tick=0, channel=0, data=[60, 70])
            tra.append(noteon)
            noteoff = midi.NoteOffEvent(tick=tickm, channel=0, data=[60, 0])
            tra.append(noteoff)

            e += 1

        else:
            e += 1

    trackend = midi.EndOfTrackEvent(tick=1)
    tra.append(trackend)
    midi.write_midifile(file_out, pat)


def presetGwanaTriplet(morph, repeats):
    """TODO: Docstring for presetGwanaTriplet.

    Args:
        morph: TODO
        repeats: TODO

    Returns: TODO

    """

    file_out = "marathon_out.mid"

    # straight
    notes1 = [0, 480, 0, 480, 0, 480]
    # phrased
    notes2 = [0, 576, 0, 288, 0, 576]

    fm = 1
    rm = 960

    pat = midi.Pattern(format=int(fm), resolution=int(rm))
    tra = midi.Track()
    pat.append(tra)

    # pattern weight (must add up to 1.0)
    w1 = 1-float(morph)/100
    w2 = float(morph)/100

    # rounding correction
    rc = 0

    for n in range(int(repeats)):
        e = 0
        for event in notes2:
            tick1 = int(notes1[e])
            tick2 = int(notes2[e])

            # rounding correction
            rc += (w1 * tick1) + (w2 * tick2) - float(int(w1 * tick1) + (w2 * tick2))

            if rc % 1 < -0.5:
                tickm = int((w1 * tick1) + (w2 * tick2)) + int(rc) - 1
                rc = 0
            elif rc % 1 >= 0.5:
                tickm = int((w1 * tick1) + (w2 * tick2)) + int(rc) + 1
                rc = 0
            else:
                tickm = int((w1 * tick1) + (w2 * tick2)) + int(rc)
                rc = 0

            noteon = midi.NoteOnEvent(tick=0, channel=0, data=[60, 70])
            tra.append(noteon)
            noteoff = midi.NoteOffEvent(tick=tickm, channel=0, data=[60, 0])
            tra.append(noteoff)

            e += 1

        else:
            e += 1

    trackend = midi.EndOfTrackEvent(tick=1)
    tra.append(trackend)
    midi.write_midifile(file_out, pat)


def presetBrazilianSixteens(morph, repeats):
    """TODO: Docstring for presetBrazilianSixteens.

    Args:
        morph: TODO
        repeats: TODO

    Returns: TODO

    """

    file_out = "marathon_out.mid"

    # straight
    notes1 = [0, 240, 0, 240, 0, 240, 0, 240]
    # phrased
    notes2 = [0, 320, 0, 160, 0, 160, 0, 320]

    fm = 1
    rm = 960

    pat = midi.Pattern(format=int(fm), resolution=int(rm))
    tra = midi.Track()
    pat.append(tra)

    # pattern weight (must add up to 1.0)
    w1 = 1-float(morph)/100
    w2 = float(morph)/100

    # rounding correction
    rc = 0

    for n in range(int(repeats)):
        e = 0
        for event in notes2:
            tick1 = int(notes1[e])
            tick2 = int(notes2[e])

            # rounding correction
            rc += (w1 * tick1) + (w2 * tick2) - float(int(w1 * tick1) + (w2 * tick2))

            if rc % 1 < -0.5:
                tickm = int((w1 * tick1) + (w2 * tick2)) + int(rc) - 1
                rc = 0
            elif rc % 1 >= 0.5:
                tickm = int((w1 * tick1) + (w2 * tick2)) + int(rc) + 1
                rc = 0
            else:
                tickm = int((w1 * tick1) + (w2 * tick2)) + int(rc)
                rc = 0

            noteon = midi.NoteOnEvent(tick=0, channel=0, data=[60, 70])
            tra.append(noteon)
            noteoff = midi.NoteOffEvent(tick=tickm, channel=0, data=[60, 0])
            tra.append(noteoff)

            e += 1

        else:
            e += 1

    trackend = midi.EndOfTrackEvent(tick=1)
    tra.append(trackend)
    midi.write_midifile(file_out, pat)


def presetBraffsQuintuplets(morph, repeats):
    """TODO: Docstring for presetBraffsQuintuplets.

    Args:
        morph: TODO
        repeats: TODO

    Returns: TODO

    """

    file_out = "marathon_out.mid"

    # straight
    notes1 = [0, 192, 0, 192, 0, 192, 0, 192, 0, 192]
    # phrased
    notes2 = [0, 274, 0, 137, 0, 137, 0, 275, 0, 137]

    fm = 1
    rm = 960

    pat = midi.Pattern(format=int(fm), resolution=int(rm))
    tra = midi.Track()
    pat.append(tra)

    # pattern weight (must add up to 1.0)
    w1 = 1-float(morph)/100
    w2 = float(morph)/100

    # rounding correction
    rc = 0

    for n in range(int(repeats)):
        e = 0
        for event in notes2:
            tick1 = int(notes1[e])
            tick2 = int(notes2[e])

            # rounding correction
            rc += (w1 * tick1) + (w2 * tick2) - float(int(w1 * tick1) + (w2 * tick2))

            if rc % 1 < -0.5:
                tickm = int((w1 * tick1) + (w2 * tick2)) + int(rc) - 1
                rc = 0
            elif rc % 1 >= 0.5:
                tickm = int((w1 * tick1) + (w2 * tick2)) + int(rc) + 1
                rc = 0
            else:
                tickm = int((w1 * tick1) + (w2 * tick2)) + int(rc)
                rc = 0

            noteon = midi.NoteOnEvent(tick=0, channel=0, data=[60, 70])
            tra.append(noteon)
            noteoff = midi.NoteOffEvent(tick=tickm, channel=0, data=[60, 0])
            tra.append(noteoff)

            e += 1

        else:
            e += 1

    trackend = midi.EndOfTrackEvent(tick=1)
    tra.append(trackend)
    midi.write_midifile(file_out, pat)


def presetVienesseWaltz(morph, repeats):
    """TODO: Docstring for presetVienesseWaltz.

    Args:
        morph: TODO
        repeats: TODO

    Returns: TODO

    """

    file_out = "marathon_out.mid"

    # straight
    notes1 = [0, 960, 0, 960, 0, 960]
    # phrased
    notes2 = [0, 720, 0, 1200, 0, 960]

    fm = 1
    rm = 960

    pat = midi.Pattern(format=int(fm), resolution=int(rm))
    tra = midi.Track()
    pat.append(tra)

    # pattern weight (must add up to 1.0)
    w1 = 1-float(morph)/100
    w2 = float(morph)/100

    # rounding correction
    rc = 0

    for n in range(int(repeats)):
        e = 0
        for event in notes2:
            tick1 = int(notes1[e])
            tick2 = int(notes2[e])

            # rounding correction
            rc += (w1 * tick1) + (w2 * tick2) - float(int(w1 * tick1) + (w2 * tick2))

            if rc % 1 < -0.5:
                tickm = int((w1 * tick1) + (w2 * tick2)) + int(rc) - 1
                rc = 0
            elif rc % 1 >= 0.5:
                tickm = int((w1 * tick1) + (w2 * tick2)) + int(rc) + 1
                rc = 0
            else:
                tickm = int((w1 * tick1) + (w2 * tick2)) + int(rc)
                rc = 0

            noteon = midi.NoteOnEvent(tick=0, channel=0, data=[60, 70])
            tra.append(noteon)
            noteoff = midi.NoteOffEvent(tick=tickm, channel=0, data=[60, 0])
            tra.append(noteoff)

            e += 1

        else:
            e += 1

    trackend = midi.EndOfTrackEvent(tick=1)
    tra.append(trackend)
    midi.write_midifile(file_out, pat)


def textCommand(morph, repeats, comm1, comm2):
    """TODO: Docstring for textCommand.

    :arg1: TODO
    :returns: TODO

    """

    file_out = "marathon_out.mid"

    note_length = {
        "w": 3840,
        "h": 1920,
        "q": 960,
        "e": 480,
        "s": 240,
        "t": 120
    }

    note_list1 = str(comm1).replace("-", " ").split(" ")
    note_list2 = str(comm2).replace("-", " ").split(" ")

    notes1 = []
    notes2 = []

    # notes
    for note in note_list1:
        notes1.append(int(0))
        notes1.append(int(note_length[str(note)[0]]))
    for note in note_list2:
        notes2.append(int(0))
        notes2.append(int(note_length[str(note)[0]]))

    # dots
    pos = 1
    for note in note_list1:
        if len(str(note)) == 2:
            if str(note)[1] == ".":
                notes1[pos*2-1] += int(notes1[pos*2-1]/2)
        if len(str(note)) == 3:
            if str(note)[2] == ".":
                notes1[pos*2-1] += int(notes1[pos*2-1]/2)
                notes1[pos*2-1] += int(notes1[pos*2-1]/6)
        if len(str(note)) == 4:
            if str(note)[3] == ".":
                notes1[pos*2-1] += int(notes1[pos*2-1]/2)
                notes1[pos*2-1] += int(notes1[pos*2-1]/6)
                notes1[pos*2-1] += int(notes1[pos*2-1]/14)
        pos += 1
    pos = 1
    for note in note_list2:
        if len(str(note)) == 2:
            if str(note)[1] == ".":
                notes2[pos*2-1] += int(notes2[pos*2-1]/2)
        if len(str(note)) == 3:
            if str(note)[2] == ".":
                notes2[pos*2-1] += int(notes2[pos*2-1]/2)
                notes2[pos*2-1] += int(notes2[pos*2-1]/6)
        if len(str(note)) == 4:
            if str(note)[3] == ".":
                notes2[pos*2-1] += int(notes2[pos*2-1]/2)
                notes2[pos*2-1] += int(notes2[pos*2-1]/6)
                notes2[pos*2-1] += int(notes2[pos*2-1]/14)
        pos += 1

    # tuplets
    pos = 1
    for note in note_list1:
        if "/" in str(note):
            tuplet_start = str(note).count(".")+1
            nom = int(str(note)[tuplet_start:len(note)].split("/")[0])
            denom = int(str(note)[tuplet_start:len(note)].split("/")[1])
            notes1[pos*2-1] = int(notes1[pos*2-1]*(denom/nom))
        pos += 1
    pos = 1
    for note in note_list2:
        if "/" in str(note):
            tuplet_start = str(note).count(".")+1
            nom = int(str(note)[tuplet_start:len(note)].split("/")[0])
            denom = int(str(note)[tuplet_start:len(note)].split("/")[1])
            notes2[pos*2-1] = int(notes2[pos*2-1]*(denom/nom))
        pos += 1

    notes1_f = []
    notes2_f = []

    # tying notes
    pos = 1
    for note in str(comm1).split(" "):
        notes1_f.append(0)
        ties = 0
        if "-" in str(note):
            ties += int(str(note).count("-"))
        tied_value = notes1[pos*2-1]
        for n in range(ties):
            tied_value += int(notes1[pos*2+1])
            pos += 1
        notes1_f.append(tied_value)
        pos += 1
    pos = 0
    for note in str(comm2).split(" "):
        notes2_f.append(0)
        ties = 0
        if "-" in str(note):
            ties += int(str(note).count("-"))
        tied_value = notes2[pos*2-1]
        for n in range(ties):
            tied_value += int(notes2[pos*2+1])
            pos += 1
        notes2_f.append(tied_value)
        pos += 1

    # length equalization
    T1 = 0
    for note in notes1_f:
        T1 += int(note)
    T2 = 0
    for note in notes2_f:
        T2 += int(note)
    ratio = T1/T2
    pos = 0
    for note in notes2_f:
        notes2_f[pos] = int(note*ratio)
        pos += 1

    fm = 1
    rm = 960

    pat = midi.Pattern(format=int(fm), resolution=int(rm))
    tra = midi.Track()
    pat.append(tra)

    # pattern weight (must add up to 1.0)
    w1 = 1-float(morph)/100
    w2 = float(morph)/100

    # rounding correction
    rc = 0

    for n in range(int(repeats)):
        e = 0
        for event in notes2:
            tick1 = int(notes1_f[e])
            tick2 = int(notes2_f[e])

            # rounding correction
            rc += (w1 * tick1) + (w2 * tick2) - float(int(w1 * tick1) + (w2 * tick2))

            if rc % 1 < -0.5:
                tickm = int((w1 * tick1) + (w2 * tick2)) + int(rc) - 1
                rc = 0
            elif rc % 1 >= 0.5:
                tickm = int((w1 * tick1) + (w2 * tick2)) + int(rc) + 1
                rc = 0
            else:
                tickm = int((w1 * tick1) + (w2 * tick2)) + int(rc)
                rc = 0

            noteon = midi.NoteOnEvent(tick=0, channel=0, data=[60, 70])
            tra.append(noteon)
            noteoff = midi.NoteOffEvent(tick=tickm, channel=0, data=[60, 0])
            tra.append(noteoff)

            e += 1

        else:
            e += 1

    trackend = midi.EndOfTrackEvent(tick=1)
    tra.append(trackend)
    midi.write_midifile(file_out, pat)


def Marathon(preset, comm1, comm2, morph, repeats, file):
    # Custom File
    if str(preset) == "1":
        presetCustomFile(morph, repeats, file)

    # Swing
    elif str(preset) == "2":
        presetSwing(morph, repeats)

    # Half-Swing
    elif str(preset) == "3":
        presetHalfSwing(morph, repeats)

    # West African Triplet
    elif str(preset) == "4":
        presetWestAfricanTriplet(morph, repeats)

    # Gnawa Triplet
    elif str(preset) == "5":
        presetGwanaTriplet(morph, repeats)

    # Brazilian 16ths
    elif str(preset) == "6":
        presetBrazilianSixteens(morph, repeats)

    # Braff's Quintuplets
    elif str(preset) == "7":
        presetBraffsQuintuplets(morph, repeats)

    # Viennese Waltz
    elif str(preset) == "8":
        presetVienesseWaltz(morph, repeats)

    # Text Command
    elif str(preset) == "99":
        textCommand(morph, repeats, comm1, comm2)


def main():
    presets_string = """
Choose preset:

1: Custom File
2: Swing
3: Half-Swing
4: West African Triplet
5: Gnawa Triplet
6: Brazilian 16ths
7: Braff's Quintuplet
8: Viennese Waltz
99: Text Command
"""
    print(presets_string)
    preset = input("\nEnter number: ")
    comm1 = ""
    comm2 = ""
    morph = ""
    repeats = ""
    file = ""

    if str(preset) == "1":
        filename = input("Enter file (See Readme for instructions): ")
        morph = input("Enter morph value (0-100): ")
        repeats = input("How many repetitions do you want?: ")
        file = open(filename)
        Marathon(preset, comm1, comm2, morph, repeats, file)

    elif str(preset) == "2":
        morph_examples = """
Enter morph value (0-100)

Examples
0: 1:1 Straight Quarter Notes
29: ~4:3 Septuplet Feel
40: 3:2 Quintuplet Feel
50: 5:3 Eighth Feel
66.7: 2:1 Triplet Feel
85.7: ~5:2 Septuplet Feel
100: 3:1 Hard Swing
"""
        print(morph_examples)
        morph = input("\nEnter number: ")
        repeats = input("How many repetitions do you want?: ")
        Marathon(preset, comm1, comm2, morph, repeats, file)

    elif str(preset) == "3":
        morph_examples = """
Enter morph value (0-100)

Examples
0: 1:1 Straight Quarter Notes
29: ~4:3 Septuplet Feel
40: 3:2 Quintuplet Feel
50: 5:3 Eighth Feel
66.7: 2:1 Triplet Feel
85.7: ~5:2 Septuplet Feel
100: 3:1 Hard Swing
"""
        print(morph_examples)
        morph = input("\nEnter number: ")
        repeats = input("How many repetitions do you want?: ")
        Marathon(preset, comm1, comm2, morph, repeats, file)

    elif str(preset) == "4":
        morph_examples = """
Enter morph value (0-100)

Examples
0: 1:1:1 Straight Triplet Notes
50: Halfway Morph
100: 2:1:1 16ths Gallop
"""
        print(morph_examples)
        morph = input("\nEnter number: ")
        repeats = input("How many repetitions do you want?: ")
        Marathon(preset, comm1, comm2, morph, repeats, file)

    elif str(preset) == "5":
        morph_examples = """
Enter morph value (0-100)

Examples
0: 1:1:1 Straight Triplet Notes
50: Halfway Morph
100: 2:1:2 Quintuplet Feel
"""
        print(morph_examples)
        morph = input("\nEnter number: ")
        repeats = input("How many repetitions do you want?: ")
        Marathon(preset, comm1, comm2, morph, repeats, file)

    elif str(preset) == "6":
        morph_examples = """
Enter morph value (0-100)

Examples
0: 1:1:1:1 Straight 16th Notes
50: Halfway Morph
100: 2:1:1:2 Sixtuplet Feel
"""
        print(morph_examples)
        morph = input("\nEnter number: ")
        repeats = input("How many repetitions do you want?: ")
        Marathon(preset, comm1, comm2, morph, repeats, file)

    elif str(preset) == "7":
        morph_examples = """
Enter morph value (0-100)

Examples
0: 1:1:1:1:1 Straight Quintuplets
50: Halfway Morph
100: 2:1:1:2:1 Septuplet Feel
"""
        print(morph_examples)
        morph = input("\nEnter number: ")
        repeats = input("How many repetitions do you want?: ")
        Marathon(preset, comm1, comm2, morph, repeats, file)

    elif str(preset) == "8":
        morph_examples = """
Enter morph value (0-100)

Examples
0: 1:1:1 Straight Quarter Notes
50: Halfway Morph
65: Recommended Morph
100: 3:5:4 16ths Feel
"""
        print(morph_examples)
        morph = input("\nEnter number: ")
        repeats = input("How many repetitions do you want?: ")
        Marathon(preset, comm1, comm2, morph, repeats, file)

    elif str(preset) == "99":
        text_notation = """
Separate each note by a space, tied notes with a dash

Notes
w: whole note
h: half note
q: quarter note
e: eighth note
s: sixteenth note
t: thirty-second note

Dots (after the note)
.: dotted
..: double dotted
...: triple dotted

Tuplets (after note and dots)
x/y: where x-tuplet notes are to be played in y non-tuplet notes
"""
        print("Enter text notation for track 1")
        print(text_notation)
        comm1 = input("Enter text command (track 1): ")
        print("you entered:", comm1)

        print("Enter text notation for track 2")
        comm2 = input("Enter text command (track 2): ")

        if len(comm1.split(" ")) != len(comm2.split(" ")):
            print("Error: The number of notes in the two tracks is different.")
            raise SystemExit

        morph = input("Enter morph value (0-100): ")
        repeats = input("How many repetitions do you want?: ")
        Marathon(preset, comm1, comm2, morph, repeats, file)


# Execute the main program if this file is not being imported as a module
if __name__ == "__main__":
    main()
