# NeonSign

NeonSign is a Python library for styling terminal text and creating simple 
text-based user interfaces, offering a modern declarative syntax.

With NeonSign, you can simply describe the colors, effects and layout your 
terminal text should have, without having to work with terminal color commands 
or box drawing characters manually.

Feature highlights:

- **Style a string** using colors and text effects. Best for highlighting a few 
  words in a single line,

- **Style a block of text** using colors, effects and layouts. Best for printing
  contents organized as a list, table, or  

- **Create a simple text-based UI**, when you need interactivity. For an early 
  prototype of the text user interface (TUI) feature, see 
  [here](#neonsign-ui-prototype). 


## Examples

### Styled text strings

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
<img src="https://yuhuan.me/neonsign/_images/example-0.gif" width=150px />
</td>
</tr>


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
<img src="https://yuhuan.me/neonsign/_images/example-1.gif" width=259px />
</td>
</tr>

</table>


### Styled text blocks

<table>

<tr><td><img src="https://yuhuan.me/neonsign/_images/example-10.png" style="width: 500px" /></td></tr>
<tr><td><img src="https://yuhuan.me/neonsign/_images/example-12.png" style="width: 310px" /></td></tr>
<tr><td><img src="https://yuhuan.me/neonsign/_images/example-13.png" style="width: 250px" /></td></tr>

</table>





<a id="neonsign-ui-prototype"></a>
### Text-based UI (early prototype)

<img src="https://yuhuan.me/neonsign/_images/example-20.gif" width=400px />

