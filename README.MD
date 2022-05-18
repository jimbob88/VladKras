# VladKrasLanguage

## What does this do?

This is a transpiled language that can be converted to Mallard-80 BASIC. For example, example2.vkl can be converted from this to that:

```
sub other {
     printAt(6, 1, "I love programming");
}

sub main {
    clearScreen();
    enableCursor();
    disableCursor();
    printAt(1, 2, "Hello World");
    resetCursor();
    var name$ = "James";
    var lastName$ = askInput("What is your last name? ");
    var fl = 1.0;
    var i = 1;
    Print("Hello " + name$ + lastName$);


    for(var j = 0, |j < 19|, j++) {
        Print(j);
    }

    while |i > 0| {
        if |i == 0| {
            Print("Hello");
            i += 1;
        } else {
            Print("No");
            i -= 1;
        }
    }
    call other;
}
```

to:
```basic
10 escape$=CHR$(27)
20 clear$=escape$+"E"
30 home$=escape$+"H"
40 move$=escape$+"Y"
50 con$=e$+"e"
60 coff$=e$+"f"
70 '
80 GOSUB 130
90 REM SUB:other
100 PRINT move$;CHR$(6+32);CHR$(1+32);
110 PRINT "I love programming";
120 RETURN
130 REM SUB:main
140 PRINT clear$;
150 PRINT con$;
160 PRINT coff$;
170 PRINT move$;CHR$(1+32);CHR$(2+32);
180 PRINT "Hello World";
190 PRINT home$;
200 name$ = "James"
210 INPUT "What is your last name? ", reservedInputValue1$
220 lastName$ = reservedInputValue1$
230 fl = 1.0
240 i = 1
250 PRINT "Hello "+name$+lastName$
260 j = 0
270 WHILE j<19
280 PRINT j
290 j= j + 1
300 WEND
310 WHILE i>0
320 IF i=0 THEN  GOSUB 350 ELSE  GOSUB 390
330 WEND GOSUB 90
340 RETURN
350 REM SUB:reservedIfStatement1
360 PRINT "Hello"
370 i= i + 1
380 RETURN
390 REM SUB:reservedElseStatement1
400 PRINT "No"
410 i= i - 1
420 RETURN
```

## Why does this exist?
The problem this software was created to solve was the way subroutines and if statements are written in Mallard-80. Because there is no way to define a subroutine like in VB:

```
[modifiers] Sub SubName[(parameterList)]
    ' Statements of the Sub procedure.
End Sub
```

You have to instead use line numbers and write something like this:

```
10 IF x = 0 THEN GOSUB 1000 ELSE GOSUB 1200
1000 PRINT "HELLO WORLD"
1010 RETURN
1200 PRINT "NO"
1210 RETURN
```

When written like this the problem isn't instantly obvious, but the problem is two-fold: The if statement can only contain 1 line, and the subroutines have to have a specific number attached to them. This makes writing code for Mallard BASIC extremely long winded, so this code hopes to improve the performance of that coding by instead allowing users to write something like this:

```
if |x == 0| {
    Print('Hello World');
} else {
    Print('No');
}
```

This is much more legible than the previous example as you can read it from Left-Right rather than reading up and down your code.

## So, I have converted some code, how do I add it to a `.dsk` file?

1. Download a copy of [CPCDiskXP](http://www.cpcmania.com/cpcdiskxp/cpcdiskxp.htm) (despite the name it fully works on Windows 10)
2. Run `CPCDiskXP.exe`
3. Press "Disk Editor"
4. Press "New"
5. Select your format as: "PCW/+3DOS - Single Side - 42 Tracks - 32 Dir. Entries - 189K"
6. Drag and drop your ".bas" file to the list
7. Press Save
8. Voila!

## Using the converter
1. Install the requirements to allow full features
```
$ #Linux
$ python3 -m venv
$ source venv/bin/activate
$ pip install -r requirements.txt
```

or
```
> :: Windows
> python3 -m venv
> venv\Scripts\activate
> pip install -r requirements.txt
```

2. View the help/docs
```
> python3 main.py -h
usage: main.py [-h] -f FILE [-t] [-T] [-i]

A system for transpiling VladKras -> Mallard-86

optional arguments:
  -h, --help            show this help message and exit
  -f FILE, --file FILE  The file to transpile `--file example.vkl`
  -t, --transpile       Whether or not to transpile the file
  -T, --treeify         Whether or not to create a tree from the dataset
  -i, --image           Whether or not to export a tree image
```

3. Transpile an example and create a fancy diagram
```
> python3 main.py -f examples/example2.vkl -i
```



## What's with the name?
This is a reference to one of the directors of [The Slowest Train](https://en.wikipedia.org/wiki/The_Slowest_Train)