title: #3: The fundamentals of a framework
date: 2024-02-09 18:00
author: tundish
tags: balladeer, rotu, releases
category: Blog
status: published
summary: Establishing a prototype.

Features
========

[Balladeer](https://github.com/tundish/balladeer) is a very flexible library.
You can use it to create all sorts of web multimedia.
In the realm of Interactive Fiction, it enables:

+ point-and-click games, of the [Ren'Py](https://www.renpy.org/) kind.
+ hyperlink text, similar to [Twine](https://twinery.org/) pieces.
+ parser-based adventures, which otherwise might require [Inform](https://ganelson.github.io/inform-website/).

In return for that flexibility, there's a little work to do up front to establish
a project. The exact structure will vary according to need.
Nevertheless, here are the basic elements.


Assets
------

Balladeer works as a Web stack. The design of your interface will be implemented in CSS files.
Alongside that styling, you may need other assets like images and fonts.

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
~~~

Scenes
------

A full-length story will need between 20 and 25 scene folders, each with at least one scene file inside.
Why this number? That will be the topic of future posts.

Just imagine these folders like the vertebrae along the spine of your story. And since we don't yet
have a full story, our initial prototype will consist of a title card, opening sequence, and then straight
to end credits.

~~~
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
~~~

Code
----

To begin with you won't need much code; just a single *main* module.
I'll explain the contents in a future post.

~~~
└── main.py
~~~

Next time, I think, we'll talk about how the scene files link together.
