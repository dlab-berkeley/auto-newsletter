# auto-newsletter
Automating the creation of the newsletter.

## Goals
The goal is to create a set of scripts that automatically generates the weekly newsletter based on information from the D-Lab website. The scripts should:
* pull the upcoming training information for the following two weeks
    - title
    - date
    - instructor
    - indicate whether or not registration is full
    - a link directed to the training registration
    - training description
* create a plain text file with the scraped information embedded
* this script will generate the newsletter from the Friday in the current week to the Friday 2 weeks later.
