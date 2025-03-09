#### basic understanding

Cut command in unix is a tool to select/extract a chunk of text from a particular file (or stdin). We can do that by specifiying the range where the text is in the file. We can also specify specific characters. 

1-3 specifies range[1,3]
1,3 specifies 1st and 3rd character to be extracted 

cut -c 1-3 textfile -> takes character from 1 to 3 of all lines in textfile 
cut -b 1,3 textfile -> takes 'byte' 1 & 3 from all lines in textfile 
cut -d "," f1,2 -> takes list item 1 & 2 from all lines split to list with delimeter "," (csv use case) . Note: the default delimeter is \t 


Note: There's a wierd thing that cut does when the field asked for doesn't exists - if the text is suppressable, it returns the whole string. If not, then only it returns the empty string 

```
$ echo a.b.c | cut -d. -f3
c
$ echo a.b | cut -d. -f3

$ echo a | cut -d. -f3
a

```


Read more - `man cut`


## Cut tool build using python 

https://codingchallenges.fyi/challenges/challenge-cut

### To install, just run 

`cd cut-tool` 

`pip install .` 

### To run tests 

The test file has all the tests mentioned on the challenge. Note: we need to install this first because we're testing the shell commands directly here.

`cd cut-tool`

`pytest`

