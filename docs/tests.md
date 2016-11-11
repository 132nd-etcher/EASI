[TOC]

# Footnotes

Footnotes[^1] have a label[^@#$%] and the footnote's content.

# Admonition

!!! Note "optional explicit title within double quotes"

    Any number of other indented markdown elements.
    
    This is the second paragraph.

# Definition lists

Apple
:   Pomaceous fruit of plants of the genus Malus in 
    the family Rosaceae.
    
!!! note

    You should note that the title will be automatically capitalized.
    
!!! danger "Don't try this at home"

    ...

!!! important "A title anyway"

    This is a admonition box without a title.

Orange
:   The fruit of an evergreen tree of the genus Citrus.

# Abbreviations

The HTML specification 
is maintained by the W3C.

*[HTML]: Hyper Text Markup Language
*[W3C]:  World Wide Web Consortium

# Fenced Code Blocks

~~~~~~~~~~~~~~~~~~~~
a one-line code block
~~~~~~~~~~~~~~~~~~~~

~~~~{.python}
# python code
~~~~

~~~~.html
<p>HTML Document</p>
~~~~

```python
# more python code
```

~~~~{.python hl_lines="1 3"}
# This line is emphasized
# This line isn't
# This line is emphasized
~~~~

```python hl_lines="1 3"
# This line is emphasized
# This line isn't
# This line is emphasized
```

First Header  | Second Header
------------- | -------------
Content Cell  | Content Cell
Content Cell  | Content Cell

[^1]: This is a footnote content.
[^@#$%]: A footnote on the label: "@#$%".