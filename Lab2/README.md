# Code for Lab2 for the Fundamentals of AI Course at Technical University of Moldova, Flocking Behaviour



Note: run on https://py3.codeskulptor.org/ to run faster with python3!




!!! Each boid has direct access to the whole scene's geometric description, but flocking requires that it reacts only to flockmates within a certain small neighborhood around itself. The neighborhood is characterized by a distance (measured from the center of the boid) and an angle, measured from the boid's direction of flight. Flockmates outside this local neighborhood are ignored.

## Separation
we want this rule to give us a vector which when added to the current position moves a boid away from those near it.


## Bibliography
- https://en.wikipedia.org/wiki/Norm_(mathematics)
- https://math.wikia.org/ro/wiki/Norma_unui_vector
- https://stackoverflow.com/questions/534855/subtracting-2-lists-in-python
