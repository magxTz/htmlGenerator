# htmlGenerator
a simple python program that convert a  3 quoted string into html codes, suppose you want to send an email(HTML formated email specifically) from your python script
then this piece shit is there for you, 
# how to format your string(triple quotes string)
in order to use this, the input string must be a multiline string(a triple quote string), the context is detemined by the intents
# tags
each tag ends with colon (:)
forexample head: ,body: ,p: ,img: ,div: ,input: ,button: ,h1: , h2: ,h3: ,h4: ,h5: etc
# attributes
equal sign (=) placed between attribute and its value
example
color=red
background-coloor=white
border-radius=10px
text-align=center

#Example
ht_string='''
head:
    text=hello world
    color=blue
body:
    p:
      text=this is a paragraph
      color=indigo
      background-color=beige
      font-size=50px
      border-radius=15px
      text-align=center
    img:
        src=malisaAG.jpg
        height=100px
        width=100px
        border-radius=10px
    h1:
        text={msg}
        color=blue
        background-color=beige
    button:
        text={button_text}
        border-radius=10px
        color=black
        background-color=indigo
        height=50px
    h2:
        text={txt2}
        color=orange
        background-color=blue
        text-align=center
    div:
        text=hello
        color=orange
        border-radius=5px
        width=200px
        height=100px
        text-align=center
        h1:
            text=another h1 tag
        h1:
            text=another h1 tag
'''

