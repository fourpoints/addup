### Setup
- In `addup.py`, change `file_to_read` to your addup-file, and change `file_to_write` to choose a name for your HTML-file.  
- If you're using spaces instead of tabs, change the `indent` input in the `Filereader` constructor. (Note: this will currently not work for `+("file.extension")`-loaded files).  
- To add a new customized tag, include an entry in `custom_tags.json`.

### Syntax

#### Example file
```
+doctype(html)
+html:
  +head:
    +title: Ipsum lorem
    +meta(charset = "utf-8")

  +body: //comment
    +Section:
      +h3: heading
      +p:
        sample text sample text sample
        sample text sample +b(text sample
        text) sample text
      +br
      +ul:
        +li: +a(href = "example.com"):(link name)
        +li: +a(href = "example.com"):(link name)
```
```html
<!doctype html>
<html>
<head>
  <title>Ipsum lorem</title>
  <meta charset="utf-8">
</head>
<body><!--comment-->
  <div class="section">
    <h3>heading</h3>
    <p>
      sample text sample text sample
      sample text sample <b>text sample
      text</b> sample text
    </p>
    <br>
    <ul>
      <li><a href="example.com">link name</a></li>
      <li><a href="example.com">link name</a></li>
    </ul>
</body>
</html>
```

#### +tag
`+tag(attribute="value"):(content)` creates opening and closing tags around the indented block. Note that `+ tag` will be ignored by the interpreter. The `tag` must be followed by a space/newline ("` `", "`\n`") or an opening bracket ("`(`").
```
+div: text
  text
text
```
```html
<div>text
  text
<div>
text
```


#### attributes
`+tag(attribute="value")` are comma-separated entries. This will be converted to `<tag attribute="value"></tag>`.

##### .class and #id
`+span.hello#world` Multiple classes and ids may be added by using CSS selector style syntax. This will be converted to `<span class="hello" id="world"></span>`

#### inline vs block
the following addup text
```
+div:
  all text in the indented block will be wrapped in <div></div> tags.
  +span:(all text inside brackets will be wrapped in  <span></span> tags)
```
will be converted to
```html
<div>
  all text in the indented block will be wrapped in <div></div> tags.
  <span>all text inside brackets will be wrapped in  <span></span> tags</span>
</div>
```


#### //comment
`//comment` creates an inline comment. (Multi-line comments are not supported.)
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

#### Code
`` `(lang) content` `` is highlighted with pygments

#### Math
`$(align) math$` is sconverted to an aligned mathml. Simple and complex math may also be used `$x+y$`, and will be rendered in MathML using mumath. The syntax is latex-like, with some minor quirks (read: ~~bugs~~ features).


#### +style and +script will escape all addup-syntax
So you don't have to worry about your JavaScript-comments becoming HTML-styled. You can also use +css and +js to directly write the content of the css and js files to the html file.

#### +read(file = "name.ext")
`+read(file = "file.extension")` will start reading from another file, allowing you to easily combine multiple files into a single output file.  
file.txt:
```txt
ipsum lorem
```
addup file:
```
+div:
  +read(file="file.txt", tag="span")
```
HTML output:
```
<div>
  <span>ipsum lorem</span>
</div>
```
The content will be enclosed by a tag of choice or `<div></div>` if none are specified.

<!--#### custom tags
Make more meaningful names to your tags by making customized names with attributes of your choice. Why not make a `+bold` tag, instead of the less meaningful `b`, or a `section` tags if you find yourself using many `div`s with a `section` class?  
There is no need to make these distinguishable from standard HTML-tags. The simpler the better.  
Custom tags must be defined using lower case letters in the json-file, but tags in your addup-file are case-insensitive.
`custom_tags.json`:
```json
{
"italic":
{
	"lang" : "HTML",
	"tags" :
	[
		{
			"html5tag"    : "i"
		}
	]
},
  
"section":
{
	"lang" : "HTML",
	"tags" :
	[
		{
			"html5tag"  : "div",
			"attributes" :
			{
				"class" : "section"
			}
		}
	]
}
}
```
-->

### Conventions
- tabs <> spaces  
- underscore\_case > camelCase  
- green > blue
