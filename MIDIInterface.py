from music21 import converter as Converter
from music21.chord import Chord
from music21.instrument import Instrument
from music21.key import Key
from music21.tempo import MetronomeMark as Metronome
from music21.midi import MidiFile as MIDI
from music21.midi.translate import midiFileToStream as MIDItoStream
from music21.note import Note
from music21.note import Rest
from music21.meter import TimeSignature as Metric
from music21.stream import Part
from music21.stream import Voice

def ParseMIDI(FilePath = str()): #this function parse midi creating a list
    File = Converter.parse(FilePath) #file reading
    Stream = [Element for Element in File.recurse()] #stream list creation
    Parts = [Stream.index(Element) for Element in Stream if type(Element) == type(Part())] #getting indexes where to split
    Parts.append(len(Stream) - 1) #adding the lenght of the stream to indexes (to get the end index of last part)
    return [Stream[Start : End] for Start, End in zip(Parts[: -1], Parts[1 :])] #splitting stream in parts(instruments)

def GetOctaveRange(UnclassifiedStreamPart = []): #this function get minimum and the maximum octave in a parts in a unclassified stream part
    Min = 8 #minimun octave
    Max = 0 #maximum octave

    for Element in UnclassifiedStreamPart: #for loop for every element in the part
        if isinstance(Element, Note): #check if the element is a note
            if Element.octave > Max: #check if the octave of the note is higher of the max registered
                Max = Element.octave #changing the max octave
            if Element.octave < Min: #check if the octave of the note is lower of the max registered
                Min = Element.octave #changing the min octave
        if isinstance(Element, Chord): #check if the element is a chord
            for Item in Element.notes: #for loop for every note of the chord
                if Item.octave > Max: #check if the octave of the note is higher of the max registered
                    Max = Item.octave #changing the max octave
                if Item.octave < Min: #check if the octave of the note is lower of the max registered
                    Min = Item.octave #changing the min octave

    return [Min, Max]

def ClassifyElements(UnclassifiedStreamPart = []): #this function classify the elements inside the list
    ClassifiedStream = [] #list with classified elements with common property

    for Element in UnclassifiedStreamPart: #for loop for every element in the part
        Item = dict()
        #indentify the type and setting the properties
        if isinstance(Element, Note):
            Item['Type'] = 'Note'
            Item['Sound'] = Element.name
            Item['Octave'] = Element.octave
            Item['Duration'] = Element.quarterLength
            Item['Extra'] = 'None'
        elif isinstance(Element, Chord):
            Item['Type'] = 'Chord'
            Item['Sound'] = [Part.name for Part in Element.notes]
            Item['Octave'] = [Part.octave for Part in Element.notes]
            Item['Duration'] = Element.quarterLength
            Item['Extra'] = 'None'
        elif isinstance(Element, Rest):
            Item['Type'] = 'Rest'
            Item['Sound'] = 'None'
            Item['Octave'] = 'None'
            Item['Duration'] = Element.quarterLength
            Item['Extra'] = 'None'
        elif isinstance(Element, Instrument):
            Item['Type'] = 'Instrument'
            Item['Sound'] = 'None'
            Item['Octave'] = 'None'
            Item['Duration'] = 'None'
            Item['Extra'] = Element.partName
        elif isinstance(Element, Key):
            Item['Type'] = 'Key'
            Item['Sound'] = 'None'
            Item['Octave'] = 'None'
            Item['Duration'] = 'None'
            Item['Extra'] = Element
        elif isinstance(Element, Metric):
            Item['Type'] = 'Metric'
            Item['Sound'] = 'None'
            Item['Octave'] = 'None'
            Item['Duration'] = 'Note'
            Item['Extra'] = Element.ratioString
        elif isinstance(Element, Metronome):
            Item['Type'] = 'BPM'
            Item['Sound'] = 'None'
            Item['Octave'] = 'None'
            Item['Duration'] = 'Note'
            Item['Extra'] = Element.number
        elif isinstance(Element, Part):
            Item['Type'] = 'Part'
            Item['Sound'] = 'None'
            Item['Octave'] = 'None'
            Item['Duration'] = 'None'
            Item['Extra'] = Element

        if not isinstance(Element, Voice): #chek if not voice type (not actually playable)
            ClassifiedStream.append(Item) #adding element dictionary

    return ClassifiedStream

def ShiftOctave(ClassifiedStreamPart = [], OctaveRange = []): #this function shift the octave of single notes making them playable in the target program
    Shift = (min(OctaveRange) - 1, 0)[min(OctaveRange) == 1] #ternary operator to check if the min octave is not 1 and than computing the shift

    for Element in ClassifiedStreamPart: #for loop to shift every note in the part
        if Element['Type'] == 'Note': #checking if the element is a note
            Element['Octave'] -= Shift #lowering the octave of the note
        elif Element['Type'] == 'Chord': # check if the element is a chord
            Element['Octave'] = [Octave - Shift for Octave in Element['Octave']] #lowering the octave of the chord

    return ClassifiedStreamPart

def GetOctaves(ClassifiedStreamPart = []): #this function get the minimum and maximum octave in a classified in a classified stream part
    Min = 8 #minimun octave
    Max = 0 #maximum octave

    for Element in ClassifiedStreamPart: #for loop for every element in the part
        if Element['Type'] == 'Note': #check if the element is a note
            if Element['Octave'] > Max: #check if the octave of the note is higher of the max registered
                Max = Element['Octave'] #changing the max octave
            if Element['Octave'] < Min: #changing the max octave
                Min = Element['Octave'] #changing the min octave
        elif Element['Type'] == 'Chord': #check if the element is a chord
            for Item in Element['Octave']: #for loop for every note of the chord
                if Item > Max: #check if the octave of the note is higher of the max registered
                    Max = Item #changing the max octave
                if Item < Min: #check if the octave of the note is lower of the max registered
                    Min = Item #changing the min octave
    return [Min , Max]

def GetMostActiveOctave(ClassifiedStreamPart = [], Octaves = []): #this function get the octave with most note counted on
    Octaves = [Octave for Octave in range(min(Octaves), max(Octaves) + 1)] #generating actual octave range from min to max
    NotesCount = {Octave : 0  for Octave in Octaves} #dictionary octave : note count
    MostActive = 0

    for Element in ClassifiedStreamPart: #for loop for every note in the stream part
        if Element['Type'] == 'Note': #check if the element is a note
            NotesCount[Element['Octave']] += 1 #increase note count relative to selected octave
        elif Element['Type'] == 'Chord': #check if the element is a chord
            for Item in Element['Octave']: #for loop for every note of the chord
                NotesCount[Item] += 1 #increase note count relative to selected octave

    for Notes in NotesCount: #for loop for every octave in stream part
        if NotesCount[Notes] > MostActive: #check if octave note count is the highest
            MostActive = Notes #changing most active octave

    return MostActive

def CutStream(ClassifiedStreamPart = [], Octaves = [], MostActiveOctave = int()): #this function cut the least active octaves of 
    Octaves = [Octave for Octave in range(min(Octaves), max(Octaves) + 1)] #generating actual octave range from min to max (sorted)
    CuttedOctaves = [] #list with the ***most*** active octaves of stream part

    if MostActiveOctave == max(Octaves): #checking if the most active octave is in last pace of the list
        CuttedOctaves = Octaves[-3 :] #setting the range as last 3
    elif MostActiveOctave == min(Octaves): #checking if the most active octave is in first place
        CuttedOctaves = Octaves[: 3] #setting the range a first 2
    else: #the most active octave is in the middle
        CuttedOctaves = Octaves[(MostActiveOctave - 1) - 1 : (MostActiveOctave - 1) + 2] # setting the range as 1 before and 2 after

    for Element in ClassifiedStreamPart[:]: #for loop for every note in a copy of the stream (for normal iteration)
        if Element['Type'] == 'Note': #check if the element is a note
            if not Element['Octave'] in CuttedOctaves: #checking if the octave of the note is in the selected range
                ClassifiedStreamPart.remove(Element) #removing the element for the real stream part
        elif Element['Type'] == 'Chord': #check if the element is a chord
            for Item in Element['Octave'][:]: #for loop for every note of a copy of the chord
                if not Item in CuttedOctaves: #checking if the octave of the note is in the selected range
                    Index = Element['Octave'].index(Item) #getting the index of octave and note
                    Element['Octave'].pop(Index) #popping the octave by index
                    Element['Sound'].pop(Index) #popping the note by index

            if len(Element['Sound']) == 0: #checking if (after the loop) the chord has no notes
                ClassifiedStreamPart.remove(Element) #romoving the empty chord

    return ClassifiedStreamPart

if __name__ == '__main__':
    Stream = ParseMIDI('Songs/Necrofantasia 6.mid')
    OctaveRange = [GetOctaveRange(SubStream) for SubStream in Stream]
    ComputedStream = [ClassifyElements(SubStream) for SubStream in Stream]
    ShiftedStream = [ShiftOctave(SubStream, Octaves) for SubStream, Octaves in zip(ComputedStream, OctaveRange)]
    ShiftedOctaves = [GetOctaves(SubStream) for SubStream in ShiftedStream]
    MostActiveOctaves = [GetMostActiveOctave(SubStream, Octave) for SubStream, Octave in zip(ShiftedStream, ShiftedOctaves)]
