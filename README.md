# doneright
This program is written in Python and was tested on Python 3.6. It uses some libraries that might need to be installed, such as: selenium, yaml
Unfortunately, I did not manage to adapt my program to be able to use xml format and think of a good use for exit codes.
To run the program, open terminal and type:
python testfile1 testfile2 ... testfilen
It will be producing output to the console and will exit with an exit code 0 or 1. 0 represents OK, 1 represents assertion error.
The test plan provided is very basic, the first test script tries to search for modules containing the word "computer" on QMUL website, but fails to do so (succeeds if you manually scroll down the page). The second script, however, uses another method for searching for modules and succeeds in doing so. The second test tries submitting an empty form and succeeds in doing so. Both JSON and YAML files contain the same tests 
PS:I feel a bit ashamed submitting this as this program is not the one I can be proud of, but this was something completely new to me and I think I learned a lot.
