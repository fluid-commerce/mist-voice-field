#!/bin/bash
set -e
cd "$(dirname "$0")/.."
R="node tools/record-stage.mjs"
F=assets/footage
FLAT="http://localhost:5231/index.html?embed=1"
STAGE="http://localhost:5231/stage.html"
$R $F/flat-hook.webm      "$FLAT" 9  1080 1920 "key('q')" '[[3,"key(\"w\")"]]'
$R $F/flat-listening.webm "$FLAT" 9  1080 1920 "key('w')" '[]'
$R $F/flat-thinking.webm  "$FLAT" 10 1080 1920 "key('w')" '[[1.5,"key(\"l\");key(\"l\");key(\"l\");key(\"e\")"]]'
$R $F/flat-answer.webm    "$FLAT&layout=answer" 17 1080 1920 "key('r')" '[]'
$R $F/flat-idle.webm      "$FLAT" 8  1080 1920 "key('q')" '[]'
$R $F/stage-wide.webm     "$STAGE" 9  1080 1920 "key('h');key('n');window.__stage.setView(0);key('w')" '[]'
$R $F/stage-presenter.webm "$STAGE" 11 1080 1920 "key('h');key('n');window.__stage.setView(2);key('w')" '[]'
$R $F/stage-low.webm      "$STAGE" 9  1080 1920 "key('h');key('n');window.__stage.setView(4);key('w')" '[]'
$R $F/stage-answer.webm   "$STAGE" 9  1080 1920 "key('h');key('n');window.__stage.setView(1);key('l');key('l');key('l');key('r')" '[]'
echo ALL_DONE
