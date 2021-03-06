.. _quickstart:

Quick Start
===========

In this tutorial we will be covering the basics of using Slash to write and run tests. 

The Test Class
--------------

For anyone familiar with ``unittest``'s interface, the easiest way to get started is with the ``slash.Test`` base class::

    import slash

    class MyTest(slash.Test):
        def test_something(self):
            pass # <-- test logic here!

Running Tests
-------------

We can save this as a Python file, for instance as ``my_test.py``. Then we can run it using the ``slash run`` command::

    $ slash run my_test.py

The above runs the test in your file, and reports the result at the end. If all went well, you should see 1 successful execution.

Debugging
---------

You can make slash enter a debugger when exceptions are encountered, by specifying the ``--pdb`` flag to ``slash run``.

Slash will try to use either ``pudb`` or ``ipdb`` if they can be invoked. Otherwise, the default ``pdb`` is invoked for debugging.
