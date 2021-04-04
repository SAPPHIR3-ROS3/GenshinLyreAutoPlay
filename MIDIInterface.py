from music21 import converter as Converter
from music21.chord import Chord
from music21.instrument import partitionByInstrument as Instruments
from music21.tempo import MetronomeMark as Metronome
from music21.midi import MidiFile as MIDI
from music21.midi.translate import midiFileToStream as MIDItoStream
from music21.note import Note
from music21.note import Rest

if __name__ == '__main__':
    File = Converter.parse('Songs\Bad Apple!.mid')

    for Element in File.recurse()[: -1]:
        if type(Element) == type(Note()):
            print([Element.nameWithOctave, Element.quarterLength])
        elif type(Element) == type(Chord()):
            print([[Part.nameWithOctave for Part in Element.notes], Element.quarterLength])
        elif type(Element) == type(Rest()):
            print([' ', Element.quarterLength])
        elif type(Element) == type(Metronome()):
            print(['BPM', Element.number])
        else:
            print(Element)
