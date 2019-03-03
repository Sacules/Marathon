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

def Marathon(preset, comm1, comm2, morph, repeats, file):    
    #Custom File
    if str(preset) == "1":
        file_in = filename
        file_out = "marathon_out.mid"
    
        read_1 = midi.read_midifile(file_in)
        
        track1 = str(read_1).split("midi.Track(\\")[2]
        track2 = str(read_1).split("midi.Track(\\")[3]
        
        notes1 = str(track1).split("),")
        notes2 = str(track2).split("),")
        
        if len(notes1)-1 == len(notes2):
            
            fm = str(read_1).split("format=")[1].split(", resolution")[0]
            rm = str(read_1).split("resolution=")[1].split(", tracks")[0] 
        
            pat = midi.Pattern(format=int(fm), resolution=int(rm))
            tra = midi.Track()
            pat.append(tra)
            
            #pattern weight (must add up to 1.0)
            w1 = 1-float(morph)/100
            w2 = float(morph)/100
            
            #rounding correction
            rc = 0
            
            for n in range(int(repeats)):
                e = 0
                for event in notes2:
                    if "Note" in str(event):
                        tick1 = int(notes1[e].split("tick=")[1].split(", channel")[0])
                        tick2 = int(notes2[e].split("tick=")[1].split(", channel")[0])
                        
                        #rounding correction
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
                        
                        cm = int(notes1[e].split("channel=")[1].split(", data")[0])
                        if "NoteOff" in str(event):
                            dm1on = notes1[e-1].split("data=[")[1].split(", ")[0]
                            dm1off = notes1[e].split("data=[")[1].split(", ")[0]
                            dm2on = notes1[e-1].split("data=[")[1].split(", ")[1].split("]")[0]
                            dm2off = notes1[e].split("data=[")[1].split(", ")[1].split("]")[0]
                        elif "NoteOn" in str(event):
                            dm1on = notes1[e].split("data=[")[1].split(", ")[0]
                            dm1off = notes1[e-1].split("data=[")[1].split(", ")[0]
                            dm2on = notes1[e].split("data=[")[1].split(", ")[1].split("]")[0]
                            dm2off = notes1[e-1].split("data=[")[1].split(", ")[1].split("]")[0]
            
                        noteon = midi.NoteOnEvent(tick=0, channel=cm, data=[int(dm1on), int(dm2on)])
                        tra.append(noteon)
                        noteoff = midi.NoteOffEvent(tick=tickm, channel=cm, data=[int(dm1off), int(dm2off)])
                        tra.append(noteoff)
                                    
                        e += 1
                        
                    else:
                        e += 1
                
            trackend = midi.EndOfTrackEvent(tick=1)
            tra.append(trackend)
            midi.write_midifile(file_out, pat)
        
        else:
            print("Error: The number of notes in the two tracks is different.")
            quit()
            
    #Swing
    elif str(preset) == "2":

        file_out = "marathon_out.mid"
            
        #straight
        notes1 = [0,960,0,960]
        #phrased
        notes2 = [0,1440,0,480]
        
        fm = 1
        rm = 960
    
        pat = midi.Pattern(format=int(fm), resolution=int(rm))
        tra = midi.Track()
        pat.append(tra)
        
        #pattern weight (must add up to 1.0)
        w1 = 1-float(morph)/100
        w2 = float(morph)/100
        
        #rounding correction
        rc = 0
        
        for n in range(int(repeats)):
            e = 0
            for event in notes2:
                tick1 = int(notes1[e])
                tick2 = int(notes2[e])
                
                #rounding correction
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
        
    #Half-Swing
    elif str(preset) == "3":

        file_out = "marathon_out.mid"
            
        #straight
        notes1 = [0,1920,0,960,0,960]
        #phrased
        notes2 = [0,1920,0,1440,0,480]
        
        fm = 1
        rm = 960
    
        pat = midi.Pattern(format=int(fm), resolution=int(rm))
        tra = midi.Track()
        pat.append(tra)
        
        #pattern weight (must add up to 1.0)
        w1 = 1-float(morph)/100
        w2 = float(morph)/100
        
        #rounding correction
        rc = 0
        
        for n in range(int(repeats)):
            e = 0
            for event in notes2:
                tick1 = int(notes1[e])
                tick2 = int(notes2[e])
                
                #rounding correction
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
        
    #West African Triplet
    elif str(preset) == "4":

        file_out = "marathon_out.mid"
            
        #straight
        notes1 = [0,480,0,480,0,480]
        #phrased
        notes2 = [0,720,0,360,0,360]
        
        fm = 1
        rm = 960
    
        pat = midi.Pattern(format=int(fm), resolution=int(rm))
        tra = midi.Track()
        pat.append(tra)
        
        #pattern weight (must add up to 1.0)
        w1 = 1-float(morph)/100
        w2 = float(morph)/100
        
        #rounding correction
        rc = 0
        
        for n in range(int(repeats)):
            e = 0
            for event in notes2:
                tick1 = int(notes1[e])
                tick2 = int(notes2[e])
                
                #rounding correction
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
        
    #Gnawa Triplet
    elif str(preset) == "5":

        file_out = "marathon_out.mid"
            
        #straight
        notes1 = [0,480,0,480,0,480]
        #phrased
        notes2 = [0,576,0,288,0,576]
        
        fm = 1
        rm = 960
    
        pat = midi.Pattern(format=int(fm), resolution=int(rm))
        tra = midi.Track()
        pat.append(tra)
        
        #pattern weight (must add up to 1.0)
        w1 = 1-float(morph)/100
        w2 = float(morph)/100
        
        #rounding correction
        rc = 0
        
        for n in range(int(repeats)):
            e = 0
            for event in notes2:
                tick1 = int(notes1[e])
                tick2 = int(notes2[e])
                
                #rounding correction
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
        
    #Brazilian 16ths
    elif str(preset) == "6":

        file_out = "marathon_out.mid"
            
        #straight
        notes1 = [0,240,0,240,0,240,0,240]
        #phrased
        notes2 = [0,320,0,160,0,160,0,320]
        
        fm = 1
        rm = 960
    
        pat = midi.Pattern(format=int(fm), resolution=int(rm))
        tra = midi.Track()
        pat.append(tra)
        
        #pattern weight (must add up to 1.0)
        w1 = 1-float(morph)/100
        w2 = float(morph)/100
        
        #rounding correction
        rc = 0
        
        for n in range(int(repeats)):
            e = 0
            for event in notes2:
                tick1 = int(notes1[e])
                tick2 = int(notes2[e])
                
                #rounding correction
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
        
    #Braff's Quintuplets
    elif str(preset) == "7":

        file_out = "marathon_out.mid"
            
        #straight
        notes1 = [0,192,0,192,0,192,0,192,0,192]
        #phrased
        notes2 = [0,274,0,137,0,137,0,275,0,137]
        
        fm = 1
        rm = 960
    
        pat = midi.Pattern(format=int(fm), resolution=int(rm))
        tra = midi.Track()
        pat.append(tra)
        
        #pattern weight (must add up to 1.0)
        w1 = 1-float(morph)/100
        w2 = float(morph)/100
        
        #rounding correction
        rc = 0
        
        for n in range(int(repeats)):
            e = 0
            for event in notes2:
                tick1 = int(notes1[e])
                tick2 = int(notes2[e])
                
                #rounding correction
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
        
    #Viennese Waltz
    elif str(preset) == "8":

        file_out = "marathon_out.mid"
            
        #straight
        notes1 = [0,960,0,960,0,960]
        #phrased
        notes2 = [0,720,0,1200,0,960]
        
        fm = 1
        rm = 960
    
        pat = midi.Pattern(format=int(fm), resolution=int(rm))
        tra = midi.Track()
        pat.append(tra)
        
        #pattern weight (must add up to 1.0)
        w1 = 1-float(morph)/100
        w2 = float(morph)/100
        
        #rounding correction
        rc = 0
        
        for n in range(int(repeats)):
            e = 0
            for event in notes2:
                tick1 = int(notes1[e])
                tick2 = int(notes2[e])
                
                #rounding correction
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
        
    #Text Command
    elif str(preset) == "99":

        file_out = "marathon_out.mid"
        
        note_length = {
                "w": 3840,
                "h": 1920,
                "q": 960,
                "e": 480,
                "s": 240,
                "t": 120
                }
        
        note_list1 = str(comm1).replace("-"," ").split(" ")
        note_list2 = str(comm2).replace("-"," ").split(" ")
        
        notes1 = []
        notes2 = []
        
        #notes
        for note in note_list1:
            notes1.append(int(0))
            notes1.append(int(note_length[str(note)[0]]))
        for note in note_list2:
            notes2.append(int(0))
            notes2.append(int(note_length[str(note)[0]]))

        #dots
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

        #tuplets
        pos = 1
        for note in note_list1:
            if "/" in str(note):
                tuplet_start = 0
                for char in str(note).split("/")[0]:
                    if char.isalpha() == True:
                        tuplet_start += 1
                    else:
                        break
                nom = int(str(note)[tuplet_start:len(note)].split("/")[0])
                tuplet_end = 0
                for char in str(note).split("/")[1]:
                    if char.isalpha() == False:
                        tuplet_end += 1
                    else:
                        break
                denom = int(str(note).split("/")[1][0:tuplet_end])
                notes1[pos*2-1] = int(notes1[pos*2-1]*(denom/nom))
            pos += 1
        pos = 1
        for note in note_list2:
            if "/" in str(note):
                tuplet_start = 0
                for char in str(note).split("/")[0]:
                    if char.isalpha() == True:
                        tuplet_start += 1
                    else:
                        break
                nom = int(str(note)[tuplet_start:len(note)].split("/")[0])
                tuplet_end = 0
                for char in str(note).split("/")[1]:
                    if char.isalpha() == False:
                        tuplet_end += 1
                    else:
                        break
                denom = int(str(note).split("/")[1][0:tuplet_end])
                notes2[pos*2-1] = int(notes2[pos*2-1]*(denom/nom))
            pos += 1

        notes1_f = []
        notes2_f = []
        
        #tying notes
        pos = 1
        for note in str(comm1).split(" "):
            notes1_f.append(0)
            ties = 0
            if "-" in str(note):
                ties += int(str(note).count("-"))
            tied_value = notes1[pos*2-1]
            posi = 0
            for n in range(ties-1):
                tied_value += int(notes1[posi*2+1])
                posi += 1
            notes1_f.append(tied_value)
            pos += 1         
        pos = 1
        for note in str(comm2).split(" "):
            notes2_f.append(0)
            ties = 0
            if "-" in str(note):
                ties += int(str(note).count("-"))
            tied_value = notes2[pos*2-1]
            posi = 0
            for n in range(ties-1):
                tied_value += int(notes2[posi*2+1])
                posi += 1
            notes2_f.append(tied_value)
            pos += 1      
              
        #length equalization
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
        
        #pattern weight (must add up to 1.0)
        w1 = 1-float(morph)/100
        w2 = float(morph)/100
        
        #rounding correction
        rc = 0
        
        for n in range(int(repeats)):
            e = 0
            for event in notes2_f:
                tick1 = int(notes1_f[e])
                tick2 = int(notes2_f[e])
                
                #rounding correction
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

                if "r" in str(comm1).split(" ")[e//2] or "r" in str(comm2).split(" ")[e//2]:
                    noteon = midi.NoteOnEvent(tick=0, channel=0, data=[0, 1])
                    tra.append(noteon)
                    noteoff = midi.NoteOffEvent(tick=tickm, channel=0, data=[0, 0])
                    tra.append(noteoff)
                else:
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
        
def main():
    preset = input("Choose preset \n\n1: Custom File\n2: Swing\n3: Half-Swing\n4: West African Triplet\n5: Gnawa Triplet\n6: Brazilian 16ths\n7: Braff's Quintuplet\n8: Viennese Waltz\n99: Text Command\n\nEnter number: ")
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
        morph = input("Enter morph value (0-100)\n\nExamples\n0: 1:1 Straight Quarter Notes\n29: ~4:3 Septuplet Feel\n40: 3:2 Quintuplet Feel\n50: 5:3 Eighth Feel\n66.7: 2:1 Triplet Feel \n85.7: ~5:2 Septuplet Feel\n100: 3:1 Hard Swing\n\nEnter number: ")
        repeats = input("How many repetitions do you want?: ")
        Marathon(preset, comm1, comm2, morph, repeats, file)
        
    elif str(preset) == "3":
        morph = input("Enter morph value (0-100)\n\nExamples\n0: 1:1 Straight Quarter Notes\n29: ~4:3 Septuplet Feel\n40: 3:2 Quintuplet Feel\n50: 5:3 Eighth Feel\n66.7: 2:1 Triplet Feel \n85.7: ~5:2 Septuplet Feel\n100: 3:1 Hard Swing\n\nEnter number: ")
        repeats = input("How many repetitions do you want?: ")
        Marathon(preset, comm1, comm2, morph, repeats, file)
        
    elif str(preset) == "4":
        morph = input("Enter morph value (0-100)\n\nExamples\n0: 1:1:1 Straight Triplet Notes\n50: Halfway Morph\n100: 2:1:1 16ths Gallop\n\nEnter number: ")
        repeats = input("How many repetitions do you want?: ")
        Marathon(preset, comm1, comm2, morph, repeats, file)
        
    elif str(preset) == "5":
        morph = input("Enter morph value (0-100)\n\nExamples\n0: 1:1:1 Straight Triplet Notes\n50: Halfway Morph\n100: 2:1:2 Quintuplet Feel\n\nEnter number: ")
        repeats = input("How many repetitions do you want?: ")
        Marathon(preset, comm1, comm2, morph, repeats, file)
        
    elif str(preset) == "6":
        morph = input("Enter morph value (0-100)\n\nExamples\n0: 1:1:1:1 Straight 16th Notes\n50: Halfway Morph\n100: 2:1:1:2 Sixtuplet Feel\n\nEnter number: ")
        repeats = input("How many repetitions do you want?: ")
        Marathon(preset, comm1, comm2, morph, repeats, file)   
        
    elif str(preset) == "7":
        morph = input("Enter morph value (0-100)\n\nExamples\n0: 1:1:1:1:1 Straight Quintuplets\n50: Halfway Morph\n100: 2:1:1:2:1 Septuplet Feel\n\nEnter number: ")
        repeats = input("How many repetitions do you want?: ")
        Marathon(preset, comm1, comm2, morph, repeats, file)
        
    elif str(preset) == "8":
        morph = input("Enter morph value (0-100)\n\nExamples\n0: 1:1:1 Straight Quarter Notes\n50: Halfway Morph\n65: Recommended Morph\n100: 3:5:4 16ths Feel\n\nEnter number: ")
        repeats = input("How many repetitions do you want?: ")
        Marathon(preset, comm1, comm2, morph, repeats, file)
        
    elif str(preset) == "99":
        comm1 = input("Enter text notation for track 1\n\nSeparate each note by a space, tied notes with a dash\n\nNotes\nw: whole note\nh: half note\nq: quarter note\ne: eighth note\ns: sixteenth note\nt: thirty-second note\n\nDots (after the note)\n.: dotted\n..: double dotted\n...: triple dotted\n\nTuplets (after note and dots)\nx/y: where x-tuplet notes are to be played in y non-tuplet notes\n\nRest (at the end)\nr\n\nEnter text command (track 1): ")
        comm2 = input("Enter text notation for track 2\n\nSeparate each note by a space, tied notes with a dash\n\nNotes\nw: whole note\nh: half note\nq: quarter note\ne: eighth note\ns: sixteenth note\nt: thirty-second note\n\nDots (after the note)\n.: dotted\n..: double dotted\n...: triple dotted\n\nTuplets (after note and dots)\nx/y: where x-tuplet notes are to be played in y non-tuplet notes\n\nRest (at the end)\nr\n\nEnter text command (track 2): ")
        if len(str(comm1).split(" ")) != len(str(comm2).split(" ")):
            print("Error: The number of notes in the two tracks is different.")
            raise SystemExit
        morph = input("Enter morph value (0-100): ")
        repeats = input("How many repetitions do you want?: ")
        Marathon(preset, comm1, comm2, morph, repeats, file) 


# Execute the main program if this file is not being imported as a module
if __name__ == "__main__":
    main()

     
    
