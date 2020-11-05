# html-parser

## formatting rules

- ```<b>TEXT</b>``` is marked as ```**TEXT**```
- ```<i>TEXT</i>``` is marked as ```_TEXT_```
- ```<a href="linked-path">TEXT</a>``` is marked as ```[TEXT](linked-path)```
- ```<img src="linked-path"/>``` is marked as ```[[linked-path]]```

## special formatting rules

- ```<h2>YYYY-MM-DD</h2>``` is marked in the name of the file as in ```YYYY-MM-DD.txt```
- ```<h3>hh:mm</h3>``` is marked as ```hh:mm DD/MM/YYYY``` (**F5** in Notepad)
- ```<p>``` is marked by the begging of text
- ```</p>``` is marked by a) EOF or b) any empty line like:

> ```hey, another line!```
>
> ``` ```
> 
> ```wow, this must be the next paragraph```

- ```<p><b>{</b> Note:``` is marked as ```{NOTE_START```
- ```<b>}</b></p>``` is marked as ```NOTE_END}```