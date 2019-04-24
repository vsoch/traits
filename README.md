# Traits

[Gordon Allport](https://en.wikipedia.org/wiki/Gordon_Allport#Allport.27s_trait_theory) was one of the first "trait psychologists" who made a massive list of 14,535 words "that could describe a person," and grouped them into three trait levels: Cardinal traits, Central traits, and Secondary traits (see link for more details). From this list, [William Cattell](https://en.wikipedia.org/wiki/James_McKeen_Cattell) at Duke University then reduced this set [down to 171](doc/cattell_1943.pdf), and then did further [factor analysis](http://www.jstor.org/stable/1417576?seq=1#page_scan_tab_contents) to derive approximately 30 clusters. This work eventually developed into the [16 factor model](https://en.wikipedia.org/wiki/16PF_Questionnaire) that is well known today.

Harder to find are the original 14,535 (I have yet to find them), and the list of 171 in a machine accessible format. This repository is a first attempt to make these traits more accessible to interested researchers. It currently includes the [list of 171](data/tsv/cattell_personality_171.tsv), and the same data with [the opposites parsed out]() and a tool to search / view / query will be released shortly.

The previous demo has been taken down, but you can build a demo container:

```bash
$ docker build -t vanessa/flask-traits .
```

or run one provided:

```bash
$ docker run -p 5000:5000 vanessa/flask-traits
```
