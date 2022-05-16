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
    var i = 0;
    Print("Hello " + name$ + lastName$);

    var j = 0;
    for(j = 0, |j < 19|, j++) {
        Print(j);
    }

    while |true| {
        if |i == 0| {
            Print("Hello");
            i += 1;
        } else {
            Print("No");
            i -= 1;
        }
        break;
    }
    call other;
}