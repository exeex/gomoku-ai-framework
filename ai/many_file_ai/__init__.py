from .easy_ai import Ai

"""
*** A demo about how to packaging multiple .py files in 1 module ***


If you don't add this line in __init__.py, you must import the Ai in the way:

``` from ai.many_file_ai.easy_ai import Ai ```

This will not be accepted in the Ai competition.


this line would packaging the Ai class to be imported in this way:

``` from ai.many_file_ai import Ai ```

This one is acceptable.

"""