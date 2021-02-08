# The full Knowledge Database description

## The Rules Initially Provided to the Expert System

| Types of tourists/locals  | Rules                                            |
| ------------------------- | --------------------------------------------     |
| Loonie (Local)            |                                                  |
|                           |Speaks Loonian language                           |
|                           | Has gray skin                                    |
|                           | Has 2 legs and 2 arms                            |   
|                           | Does not wear a mask                             |
|                           | Wears sunglases                                  |
|                           | Walks fast                                       |   
|                           | Has red hair                                     |   
| Earthy (Comes from Earth) |                                                  |
|                           | Wears a mask                                     |
|                           | Wears a spacesuit                                |
|                           | Has yellow or pink or white or brown skin        |
|                           | Speaks English                                   |
|                           | Has 2 legs and 2 arms                            |   
|                           | Walks slow                                       |
| Martian  (Comes from Mars)|                                                  | 
|                           | Wears a mask                                     |
|                           | Has green skin                                   |
|                           | Does not wear a spacesuit                        |
|                           | Wears shiny clothes                              |
|                           | Speaks Martian language                          |
|                           | Has 4 legs and 4 arms                            |
|                           | Wears sunglasses                                 |
| Jupiterian(Comes from Jupiter) |                                             |
|                           | Has orange hair                                  |
|                           | Weights very much                                |
|                           | Has orange skin                                  |
|                           | Wears yellow clothes                             |
|                           | Speaks Jupiterian language                       |
|                           | Has 4 legs and 2 arms                            |
|                           | Wears sunglasses                                 |
|                           | Walks fast                                       |   
| Callistian (Comes from Callisto) |                                           |
|                           | Is slim                                          |
|                           | Has orange skin                                  |
|                           | Wears yellow clothes                             |
|                           | Speaks Jupiterian language or Callistian dialect |
|                           | Has 2 legs and 2 arms                            |
|                           | Wears sunglases                                  |
|                           | Walks slow                                       |   
| Asteroidian (Comes from an asteroid)|                                        |
|                           | Has gray skin                                    |
|                           | Has gray hair                                    |
|                           | Is slim                                          |
|                           | Wears shiny clothes                              |
|                           | Communicates with high pitched sounds            |
|                           | Has 4 legs and 4 arms                            |
|                           | Walks fast                                       |   


## The intermediate rules that were created


| Types of creatures        | Intermediate Rules                               |
| ------------------------- | --------------------------------------------     |
| Air breather              | '(?x) wears a mask' AND '(?x) wears a spacesuit' |
| Humanoid like             |     '(?x) has 2 legs' AND '(?x) has 2 arms'      |
| Insectoid like            |     '(?x) has 4 legs' AND '(?x) has 2 arms'      |
| Spider like               |     '(?x) has 4 legs' AND '(?x) has 4 arms'      |


