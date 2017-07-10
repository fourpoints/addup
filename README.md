# Markplus
Interpreter from whitespace dependent markplus to html.

Example  
```
<!doctype html>
+html
  +head
    +title(sample page)
    +meta(charset = "utf-8")
    
  +body
    //this is a one line comment
    +div(id = "wrapper")
      +h3 this is a title
      +a(href = "example.com")(this is a link)
      this is just text +b(and this is bold text)
      \ is an \+b(escape char)
      [[is+an+unformatted+line]]
      +ul
        +li item 1
        +li item 2
      @div
      wraps around the rest of the block
    the block ends above this line
```

```html
<!doctype html>
<html>
  <head>
    <title> sample page</title>
    <meta charset="utf-8" />
  </head>
  <body>
    <!--this is a one line comment-->
    <div id="wrapper">
      <h3> this is a title</h3>
      <a href="example.com">this is a link</a>
      this is just text <b>and this is bold text</b>
      is an +b(escape char)
      is+an+unformatted+line
      <ul>
        <li> item 1</li>
        <li> item 2</li>
      </ul>
      <div>
      wraps around the rest of the block
      </div>
    the block ends above this line
    </div>
  </body>
</html>
```

In addition to these features, markplus also allows you to
* Define custom tags, so instead of typing `+div(class="head")`, you may define a `+Head`-tag in custom_tags.py
* Read from multiple files. By writing `+("file.extension")` the interpreter will start reading from another file, allowing you to combine multiple files into a single html-file.

Future updates:
- Support for the `<pre>`-tag
- Convert `+h3 title` to `<h3>title</h3>` instead of (current) `<h3> title</h3>`

