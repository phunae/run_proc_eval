IMPLEMENTATION CHANGE

This branch mainly changes how the report file is being recorded:
- the information is written 5 report records at a time
- the file is alternatively opened for writting and then closed
(as opossed to the first implementation, where the information was all written in RAM
and only at the end of the target process would the information be written all at once to the file report)

Capturing process resource information and writing it to a report file is now done
by creating a report generating object, that initializes the conditions and separates the functionality for evaluating 
and adding the evaluation information to the report file.

In this implementation, most of the logic happens in the newly created module: report_generator.py