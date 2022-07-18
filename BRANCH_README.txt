IMPLEMENTATION CHANGE

This branch changes the way the evaluation report implementation.
Capturing process resource information and writing it to a report file is now done
by creating a report generating object, that initializes the conditions and functionality for both evaluating 
and adding the evaluation information.

In this implementation, most of the logic happens in the newly created module: report_generator.py