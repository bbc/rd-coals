#!/usr/bin/python3
#
#    | bit | hex | code | LED | Btn | Acc | Radio |        |
#    |  -  |  -  |  -   |  -  |  -  |  -  |   -   | intro  |
#    |  -  |  -  |  -   |  -  |  -  |  -  |   -   | use    |
#    |  -  |  -  |  -   |  -  |  -  |  -  |   -   | modify |
#    |  -  |  -  |  -   |  -  |  -  |  -  |   -   | create |
#    |  -  |  -  |  -   |  -  |  -  |  -  |   -   | core   |
#    |  -  |  -  |  -   |  -  |  -  |  -  |   -   | embed  |
#
# btn == buttons
# acc = acceleromter
# embed = embed tech into things
# 

template = """\
id: %(idtag)s
title: %(title)s
name: %(resource_name)s
url: %(url)s
depends_resource: fill_me_in
updated: April 2018
template: mainpanel
source_form: markdown
pipeline_stage: unstarted
---
WHO WHAT WHY WHERE WHEN HOW

WHO
    Who needs to know this?

WHAT
    What must the learner understand prior to this resource?
    What must the learner understand at the end of this resource?

HOW
    What is the relevant "How" question for this resource. Answer it.
    (Probably tells them "how to do this thing")

WHY 
    Why do they need to know this ?
    What is the learner able to do at the end of this resource?
    Why does this matter to then?

WHERE
    HERE: What example can we give the user?
    THERE: Where can they find more information?

WHEN
    When will they find this useful ?

* Write the questions for this resource.                 --> QUESTION OUTLINES WRITTEN
* Write answers for the questions.                       --> ANSWER OUTLINES WRITTEN
* Arranges the answers into a useful interesting order   --> ANSWERS REARRANGED
* Simplify the langange                                 --> LANGUAGE SIMPLIFIED
* CONCEPTS ARISING
"""

counter = 0
for functionality in "bit hex code led btn acc radio".split():
    for level in "intro use modify create core embed".split():
        counter +=1
        filename = functionality + "_" + level + ".md"
        meta = {"idtag" : functionality + "_" + level + "_" + str(counter),
                "title" : functionality + " " + level,
                "resource_name" : functionality + " " + level + " " + str(counter),
                "url": "http://microbit.org/resources/als/"+functionality + "_" + level + "_" + str(counter)
                }
        print(filename, meta)
        merged = template % meta
        concept_lines  = "concept: " + functionality + "\n"
        concept_lines += "concept: " + functionality + "_" + level + "\n"
        f = open(filename, "w")
        f.write(concept_lines)
        f.write(merged)
        f.close()
