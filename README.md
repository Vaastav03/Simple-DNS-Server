To run the program use the command-
    python lab2-cs20b060.py startportnumber input_filename
Instructions-
    Use the portnumbers greater than 1023 and makesure that 
    the portnumbers startportnum+53 to startportnumber +62 are free,
    else it would return an error that the given address is already in use.
Testing-
    1)Testing the domain names that are present in the input file. 
    Here we have to recieve the DNS mapping that matches with the one in the input.
    2)If we are giving a valid domain name that is not present in the input file
    then it should print "No DNS Record Found".
    3)If we enter an invalid domain name then we should get the invalid server message.
    4)If we enter bye as the user input the all the processes should be killed and the
    program should be terminated giving a prompt message.
    5)After termination, test for the killing of the processes by using the command
    "lsof -i:portnumber" where the portnumber is from startportnum+53 to startportnum+62,
    it should not show any process running in that port. 