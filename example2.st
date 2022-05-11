sub main {
    clearScreen();
    enableCursor();
    disableCursor();
    printAt(1, 2, "Hello World");
    resetCursor();
    var name = "James";
    var lastName = askInput("What is your last name? ");
    Print("Hello " + name + lastName);
}