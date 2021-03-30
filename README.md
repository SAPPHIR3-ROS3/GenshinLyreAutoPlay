# GenshinLyreAutoPlay
### this script will convert and play (almost) every song on the lyre in Performace function of Genshin Impact  
---
## Disclaimer
* I will not take responsibility to any in-game ban or restriction (do it at your own risk)
    * Even if the script has a (sort of) bypass that tries to avoid Macro-Detection you can still be restricted  
    and/or banned
* in the Genshin Impact [Terms of Service](https://genshin.mihoyo.com/en/company/terms) is specified not to third-party program as follows (do it at your risk):
```
...
2.  Rules of Usage
...
3)  You acknowledge and confirm that you may not, either directly or indirectly, do or attempt to do any of the following action with respect to any or all of the miHoYo Services:
...
iii.  Infringe contractual rights, personal and property rights, intellectual property rights and other rights and interests (including the rights of privacy, publicity or trade secret) of miHoYo or third-parties;
iv.  Develop, use or distribute any software, script code, plug-in unit, programs or applications that may cause an unfair competitive advantage;
...
viii.  Use illegal or inappropriate methods that may interrupt the operation of or otherwise exploit any of the miHoYo Services without authorization, including but not limited to extracting source code, hacking, cracking, distributing counterfeit software, complaining of false information, uploading or transmitting files (or attempting to do so) that contain viruses, Trojan horses, worms, time bombs, corrupted files or other unauthorized programs;
...
x.  Allow or assist any third-parties to do any of the above.
...
9.  Inappropriate User Behaviors
...
2)  You are prohibited from engaging in, directly or indirectly:
...
iii.  use of cheating programs or other malicious game programs;
...
3)  We reserve the right, but are not obligated, to attention or be involved in disputes between users. Depending on the relevant situation, miHoYo may take action, including but not limited to, sending a warning, blocking communications, suspending, off-lining, banning or terminating your Account temporarily or permanently, blocking login, deleting game files or otherwise take actions in our sole discretion. We reserve and maintain the final rights to interpret and take actions according to relevant circumstances of your inappropriate behaviors. If your rights are violated by other users, we will assist you in providing the necessary materials to defend your rights.
...
```
* in the Genshin Impact Performance function disclaimer is specified play your personal song or have relevant right to play a song as follows (do it at your own risk):
```
When using the Performace function, make sure that you use an original composition or have the relevant rights to use the melody you are playing in order to avoid harming the rights of any third parties and to avoid any actions in breach of or incompatible with our Terms of Service. Otherwise we may have to your use of this function
```
---
## Requirements
######  this script require ***Python*** and ***ffmpeg*** to be installed and function properly to execute 
---
## Steps
* import your songs (needed to be done once for every song)
  * Drop your songs in `/Songs` folder
  * the songs in folder will be converted in .wav (better sound translation)
  * the .wav files will be converted in .mid (MIDI files will give the instructions to play the songs)
  * the MIDI files will be mapped to Genshin Impact Performace Mode (Lyre) compatible keys sequences
  * the MIDI files will be translated in C Major in order to remove (most of) the notes alterations (A#, C# ecc.)
  * the keys sequence will exported and saved in `/MappedSongs`
* play the imported songs
  * open Genshin Impact
  * go on Performance function
  * start this script
  * choose between the listed songs the song you want to play (refresh is the song you want is not listed)
  * click the play button
  * return on Genshin Impact (on Performance function)
  * after a few seconds the song will start to play
  * to stop the song while playing press the EscapeButton
  * enjoy your lyre playing your songs