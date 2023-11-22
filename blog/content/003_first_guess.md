title: #3: Panicking
date: 2023-10-30 09:00
author: tundish
tags: python, balladeer, game jam
category: Blog
status: published
summary: There"s a lot needs doing.

Conversation
------------

We begin in the cab of a van. Player is young. just starting to help in a company of repo men.
No phone coverage.

Story will be mostly on rails, with some parse exploration.

Missions/Tasks nee questions/answers ans Ask/Say syntax.

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
