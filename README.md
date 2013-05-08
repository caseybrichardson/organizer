organizer.py
=========

Python program that goes through a specified directory and moves files based on extension. The way it decides what to move is based on a user specified JSON file.

Example mapping file:

```javascript
{
    ".py" : "Python files",
    ".java" : "Java files",
    ".png" : "Pictures"
}
```

How to run:

```
python organizer.py -p /path/to/directory mappingFile
```

Note: You do not need to use the -p option. That flag just means to run the program in a different directory than the one you're currently in.
