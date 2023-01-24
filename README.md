# Any-audio-transcribe-2txt
This script will help: 
1) to recognize speech from any audio format and any length audio file. 
2) Enhance audio quality for better results. 
3) Write recognized speech into txt file

How it works:
1) Run scrpit;
2) Type the root to a file you would like to transcribe;
3) Script detects the format of the initial file. If it isn't 'Wav' -converts to wav;
4) Using sox library the script tries to enhance audio quality of the initial audio for better recognition results;
5) Script detects the length of the file: if it is longer than 1 min – the file will be splited into chunks to meet limitations of speech recognition library (speech2text works only for files with the duration <1 min);
6) After the spliting each chunk is being recognised separately;
7) Results of the recognition of each chunk are being writen into one txt file with the same name as the initial audio file.
