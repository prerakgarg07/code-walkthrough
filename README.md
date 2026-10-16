# code-walkthrough

A Claude Code plugin for reading a codebase block by block. Claude writes a plain explanation and a verdict
(needed, could be simpler, not needed, fix) for each block, shows them beside the live code in a local page, and
answers the comments you leave there. It changes code only when you ask.

## Install

    /plugin marketplace add prerakgarg07/code-walkthrough
    /plugin install code-walkthrough@code-walkthrough

Then `/reload-plugins` (or restart Claude Code).

## Use

In any project, say "walk me through this code" or run `/code-walkthrough:walkthrough`. Claude writes the notes,
starts the page (http://localhost:8090 by default) and watches for your comments.

Notes and comments are kept in `.walkthrough/` inside your project; add it to `.gitignore`.

Needs Python 3 (standard library only).
