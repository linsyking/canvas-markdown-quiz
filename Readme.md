# Canvas-markdown-quiz

Add markdown support for Canvas LMS quizzes.

## Quick Start

### Markdown Writing

Following `test.md`, create your own quiz markdown file, like `quiz1.md`.

The structure of this md file should be like this:

```md
---
(Some quiz configs)
---

# Your Title

(Your description)

---

(Block 1)

---

(Block 2)

---

...

---

(Block n)
```

Quiz config should be formatted as YAML, and the options are available at [this page](https://canvas.instructure.com/doc/api/quizzes.html#method.quizzes/quizzes_api.create). You don't have to set title and description parameter in this config.

---

Each block is a question, and it should be like this:

````md

---

```yaml
question_type: multiple_choice_question
points_possible: 1
answers:
    -
        answer_text: "Option 1"
        answer_weight: 100
    -
        answer_text: "Option 2"
        answer_weight: 0
---

Question description goes here.

```cpp
#include <stdio.h>

int main(){
    printf("Hello World!");
}
```
---
````

Quiz question config should be formatted as YAML, and the options are available at [this page](https://canvas.instructure.com/doc/api/quiz_questions.html#method.quizzes/quiz_questions.create). You don't have to set the text parameter in this config.

### Quiz Generator

1. Clone this repo

```sh
git clone https://github.com/linsyking/canvas-markdown-quiz.git
```

2. Install Dependencies

```sh
# using pip for python

pip install markdown canvasapi

# If you use pip3 for python3
pip3 install markdown canvasapi
```

3. Modify Configs

Edit `config.py`, change these three values:

```py
CANVAS_API_URL = "<Your canvas url>"

CANVAS_API_KEY = "<Your canvas key>"

COURSE_ID = 1 # Change this to your course id
```

4. Run command

```sh
# using python

python ./generate.py <md filename>

# If you use python3
python3 ./generate.py <md filename>
```

## Snapshot

![](img/result.png)

## TO-DOs

Latex support is not implemented because Canvas LMS doesn't allow js script to be included in the quiz content, so I am trying to figure out other solutions.

