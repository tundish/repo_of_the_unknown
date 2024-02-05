title: #3: Planning
date: 2023-10-30 09:00
author: tundish
tags: python, balladeer, game jam
category: Blog
status: draft
summary: Pushed for time. In need of a strategy.

Brevity
-------

OK, a ten-day Jam will give me about 24 hours of working time. Not very much, so I need to be organised.
I want to be able to jot down scraps of dialogue whenever they occur to me during my working day.
I'll arrange and edit them in the evenings.

Clever coding will cost me. No time to debug.

So mostly linear story, with some variations driven by player choices.

Story will be mostly on rails, with some parse exploration.

I want to signpost two or three explicit missions for the player to tackle.
I can use Balladeer's parser to implement questions/answers and an Ask/Say syntax.

There's a trick I discovered a while ago that will come in useful.
Populate list data for input text.

500 cues of SpeechMark?

* [Conversation Trees](https://balladeer.readthedocs.io/en/latest/conversation.html)

tghing

~~~ TOML

[ALAN]
type = "Narrator"

[BETH]
type = "CatOwner"

[CONVERSATION]
type = "Conversation"

[[_]]
if.CONVERSATION.state = 0
if.CONVERSATION.tree = false
s="""
<ALAN> What shall we do?
"""

[[_]]
if.CONVERSATION.state = 1
if.CONVERSATION.tree = false
s="""
<ALAN> Let"s practise our conversation skills.
<ALAN.branching> Maybe now"s a good time to ask {BETH.name} a question.
    1. Ask about the weather
    2. Ask about pets
    3. Ask about football
<ALAN> I"ll let you carry on for a bit.
"""

[_.1]
s="""
<BETH> Well, you never know what"s it"s going to do next, do you?
<BETH.returning> I"ve never seen anything like it!
"""

[_.2]
s="""
<BETH.branching> I"ve got two lovely cats.
    1. Ask about Charlie
    2. Ask about Doodles
"""

[_.2.1]
s="""
<BETH> Charlie is the elder cat. He"s a Marmalade. Very laid back.
"""

[_.2.2]
s="""
<BETH.returning@CONVERSATION> Oh my goodness, Doodles. Always up to mischief!
"""

[_.3]
s="""
<BETH> I don"t know anything about football at all.
"""

[[_]]
if.CONVERSATION.state = 3
if.CONVERSATION.tree = false
s="""
<ALAN> OK. Conversation over.
"""
~~~
