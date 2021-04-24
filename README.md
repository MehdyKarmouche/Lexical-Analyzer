# Lexical-Analyzer
This is a lexical analyzer or a lexer of our language written in Python. The aim of our lexer is to turn the input text file into a token stream.

## Implementation choices
#### Python:
We chose Python because most of the team members are used to write code in it. Moreover, Python offers the re module (regular expressions or RegEx) which is very useful for us in this part of the project. We did not opt for java (JLex) because we don't have much experience in it and Python is much faster in development time. Python 3 was a  good option between C and Java.  

## User Manual:

To download and install python3 go to:
```
https://www.python.org/downloads/
```
To install the dependencies:
```
pip3 install -r requirements.txt
```

To run the lexer:
```
python runner.py
```
Once running, the user gets prompted to enter the input file name / path:

- If the input file name is `stdin`, our lexer switches to the shell / interactive mode. Commands can then be entered line by line in the command line (after `lexer >`).
  
- If the input file name is other than `stdin` (e.g `script.mg`), then our lexer is in script mode. It will analyze whichever commands are inside the file specified.
The file needs to be in the same directory as the file *runner.py*.




