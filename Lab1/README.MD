# Lab 1 - Expert Systems


## Table of contents
* [Introduction](#introduction)
* [Technologies](#technologies)
* [How to run the program](#how-to-run-the-program)
* [Available commands](#available-commands)
* [Examples of use](#examples-of-use)
* [Bibliography and resources](#bibliography-and-resources)


## Introduction
This repository contains the code for the Laboratory 1 for the Fundamentals of Artificial Intelligence course at Technical University of Moldova.
This laboratory presents an interactive Expert System based on Goal Trees(And/Or Trees), that is capable of distinguishing between locals of the Luna-City (the "Loonies") and 5 different types of tourists. The system uses Goal Trees (And/Or trees), implementing forward chaining as well as backward chaining algorithms.
The forward chaining allows to determine the type of tourists based on dfferent characteristics (or facts), such as clothes, language, nr of legs and arms, hair and skin color and others. The backward chain allows to see the facts about a type of tourist, given a hypothesis.

## Technologies
Project is created with:
* Python 3
* Docker

## How to run the program
To run this project locally, open a terminal and run with python3 the file main.py. Make sure to have python3 installed:

```$ python3 main.py```

To run in docker:

```$ docker build -t lab1 . ```

```$ docker run -it --rm --name lab1-run lab1```

## Available commands
- help()                 - shows help
- clear_and_restart()    - clears the facts and restarts the system
- exit()                 - exit the program
- show_facts()           - prints the existing available facts
- show_answer()          - prints the answer based on the  existing available facts
- tell_me_about()        - will show facts about a type of tourist using backward chaining


## Examples of use

Showing available facts:

![S1](https://github.com/mdiannna/Labs_UTM_AI/blob/main/Lab1/screenshots/image1.png?raw=true)

Using the forward chaining algorithm:

![S3](https://github.com/mdiannna/Labs_UTM_AI/blob/main/Lab1/screenshots/image3.png?raw=true)

Using the backward chaining algorithm:
![S2](https://github.com/mdiannna/Labs_UTM_AI/blob/main/Lab1/screenshots/image2.png?raw=true)



## Bibliography and resources
- UTM Fundamentals of Artificial Intelligence Course
- [MIT Artificial Intelligence Course](https://ocw.mit.edu/courses/electrical-engineering-and-computer-science/6-034-artificial-intelligence-fall-2010/index.htm)
