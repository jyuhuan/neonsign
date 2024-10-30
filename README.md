# NeonSign

## Overview

NeonSign is a Python library for making styled text in terminals. The library 
offers a modern, declarative syntax. You can simply describe the styles and 
effects your text should have, without having to work with terminal commands 
directly.


## Examples

<table>

<tr>
    <th>Example Code</th>
    <th>Result</th>
</tr>

<tr></tr>

<tr>
<td>

```python
from neonsign import s, Color

print(
    s('Hello, world!')
    .padded()
    .foreground(Color.BRIGHT_WHITE)
    .background(Color.BRIGHT_BLUE)
    .bold()
    .blinking()
)
```

</td>
<td>
<p>Blinking text:</p>
<img src="https://yuhuan.me/neonsign/_images/example-0.gif" style="width: 150px" />
</td>
</tr>

<tr></tr>

<tr>
<td>

```python
from neonsign import s, Color

print(
    s(
        s('Hello')
        .padded_left()
        .foreground(Color.BRIGHT_YELLOW),
        s('World')
        .padded_right()
        .foreground(Color.BRIGHT_BLUE)
    )
    .background(Color.BRIGHT_GREEN)
    .bold()
)
```

</td>
<td>
<p>Multicolored text with background:</p>
<img src="https://yuhuan.me/neonsign/_images/example-2.png" style="width: 120px" />
</td>
</tr>

<tr></tr>

<tr>

<td>

```python
from neonsign import s, Color

print(
    s(
        s('INFO')
        .padded()
        .foreground(Color.BLACK)
        .background(Color.BRIGHT_WHITE)
        .bold(),
        ' ',
        'An example message'
    )
)

print(
    s(
        s('WARN')
        .padded()
        .foreground(Color.BLACK)
        .background(Color.BRIGHT_YELLOW)
        .bold(),
        ' ',
        s('An example message')
        .foreground(Color.YELLOW)
    )
)

print(
    s(
        s('ERROR')
        .padded()
        .foreground(Color.BRIGHT_WHITE)
        .background(Color.BRIGHT_RED)
        .bold()
        .blinking(),
        ' ',
        s('An example message')
        .foreground(Color.RED)
    )
)
```

</td>

<td>
<p>Color-coded logger messages:</p>
<img src="https://yuhuan.me/neonsign/_images/example-1.gif" style="width: 259px" />
</td>
</tr>

</table>
