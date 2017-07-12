### Setup
In `markup+.py`, change `file_to_read` to your +Markup-file, and change `file_to_write` to choose a name for your HTML-file.
If you're using spaces instead of tabs, change the `indent` input in the `Filereader` constructor. (Note: this will currently not work for `+("file.extension")`-loaded files).
To add a new customized tag, include an entry in `custom_tags.py`.

### Syntax

#### Example file
```
<!doctype html>
@html
+head
  +title Ipsum lorem
  +meta(charset = "utf-8")

+body //comment
  +Section
    +h3 heading
    sample text sample text sample
    sample text sample +b(text sample
    text) sample text +br
    +ul
     +li +a(href = "example.com")(link name)
     +li +a(href = "example.com")(link name)
```

```html
<!doctype html>
<html>
<head>
  <title>Ipsum lorem</title>
  <meta charset="utf-8" />
</head>
<body><!--comment-->
  <div class="section">
    <h3>heading</h3>
    sample text sample text sample
    sample text sample <b>text sample
    text</b> sample text <br/>
    <ul>
      <li><a href="example.com">link name</a></li>
      <li><a href="example.com">link name</a></li>
    </ul>
</body>
</html>
```

#### +tag
`+tag` creates opening and closing tags around the indented block. Note that `+ tag` will be ignored by the interpreter.
```
+div text
  text
text
```
```html
<div>text
  text
<div>
text
```

#### @tag (may be removed)
`@tag` creates opening and closing tags around the rest of the block on the same level.
```
+div
  text
  @div text
  text
```
```html
<div>
  text
  <div> text
  text
  </div>
</div> 
```

#### //comment
`//comment` creates an inline comment. (Multi-line comments are not (yet?) supported.)
```
//this is a comment
```
```html
<!--this is a comment-->
```

#### \escape_char
`\escape_char` escapes the next character
```
text \+div \//
```
```html
tetxt +div //
```

#### [[escape line]]
`[[escape line]]` escapes the content of the brackets. Will only work on a single line.
```
text [[+div //]]
```
```html
text +div //
```

#### +style and +script will escape all +Markup-syntax
So you don't have to worry about your JavaScript-comments becoming HTML-styled.

#### +("file.extension")
`+("file.extension")` will start reading from another file, allowing you to easily combine multiple files into a single output file.  
`color.css`:
```css
#red {color: red}
```
```
+style
  +("color.css")
```
```
<style>
  #red {color: red}
</style>
```

#### custom tags
Make more meaningful names to your tags by making customized names with attributes of your choice. Why not make a `+Bold` tag, instead of the less meaningful `b`, or a `Section` tags if you find yourself using many `div`s with a `section` class?  
It is recommended that you use capital letters for custom tags, to easily distinguish them from HTML5 tags.
`custom_tags.py`:
```python
"Bold":
  {
    "html5tag" : "b"
  },
  
"Section":
  {
    "html5tag"    : "div",
    "attributes"  :
    {
      "class" : "section",
      "id"    : "red"
    }
  },
```
