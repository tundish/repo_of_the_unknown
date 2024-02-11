title: #3: The fundamentals of a framework
date: 2024-02-09 18:00
author: tundish
tags: balladeer, rotu, releases
category: Blog
status: published
summary: Starting to imagine plotlines.

Features
========

[Balladeer](https://github.com/tundish/balladeer) is a very flexible library.
You can use it to create all sorts of web multimedia.
In the realm of Interactive Fiction, it enables:

+ point-and-click games, of the [Ren'Py](https://www.renpy.org/) kind.
+ hyperlink text, similar to [Twine](https://twinery.org/) pieces.
+ parser-based adventures, which otherwise might require [Inform](https://ganelson.github.io/inform-website/).

In return for that flexibility, there's a little work to do up front to establish
a project. The exact structure of a project will vary from author to author depending
on their preferred workflow.


Assets
------

Balladeer works as a Web stack. The design of your interface will be captured in CSS files.
Alongside that styling, you may need other assets like images and fonts.

Scenes
------

25 in total

Code
----

Single module. Rely on World build from spec.


~~~
rotu
├── assets
│   ├── fonts
│   │   ├── Lora-Bold.woff2
│   │   ├── Lora-Regular.woff2
│   │   ├── OpenSans-BoldItalic.woff2
│   │   ├── OpenSans-Bold.woff2
│   │   ├── OpenSans-ExtraBoldItalic.woff2
│   │   ├── OpenSans-ExtraBold.woff2
│   │   ├── OpenSans-Italic.woff2
│   │   ├── OpenSans-LightItalic.woff2
│   │   ├── OpenSans-Light.woff2
│   │   ├── OpenSans-Regular.woff2
│   │   ├── OpenSans-SemiBoldItalic.woff2
│   │   └── OpenSans-SemiBold.woff2
│   ├── basics.css
│   ├── layout.css
│   ├── object.css
│   └── styles
│       ├── style_01.css
│       ├── style_02.css
│       └── style_03.css
├── scenes
│   ├── 00
│   │   ├── 0.scene.toml
│   │   └── a.scene.toml
│   ├── 01
│   │   └── a.scene.toml
│   ├── 02
│   │   └── a.scene.toml
│   └── 24
│       └── a.scene.toml
├── main.py
└── __init__.py
~~~

