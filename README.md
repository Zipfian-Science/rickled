# Rickled
```
                                      ....                                      
                                &((((((((((((((%,                               
                              #(*,*((//(((((((((((%.                            
                            ,((*,&,    .,.(#(((#((((%                           
                           /((((((/(/////(/###(((((((%                          
                           #(((((/(/(((//(/(/(((((((((%                         
                          .((((#     #/#.    %#((((((((%                        
                          ,(((/       #       %((((((((#*                       
                          ,((((*     #(/     &((((((((((%                       
                          ,((((%(((((/#/((//(#((((#((((##,                      
                          ((%(@@&///@%/(/@//@@(#(##((((((/                      
                          %&@@@@@@@,&,@&@@@@@@@@#&(((((((&                      
                          ##&&@@@@@@@@@@@&#(##@&#%#((((((#                      
                          #(###(#&.(*#*&/#*&%#(%(##(((((((,                     
                          %((#(((//(/(/(///((#((((((((((((/                     
                          %/#((((//////////(((((((((((((((#                     
                          %((((((///////////((((((((((((((@                     
                          %((((((//////////(((((((((((((((#                     
                          #((((((/(//////(/((((((((#(((((((                     
                          #((((((/////(((/((((((((((##/((#(.                    
                          %((((((//////(/(((((((((((##/((((.                    
                          #((((((//(///((((((((((((##((((((.                    
                          #(((((((((//(((((((((((((((((((((                     
                         *(((((((///(//(((((((((((((((((((#                     
                         (((#(((/////////(((((((((((((((((%                     
                         %((((((////////((((((((((((((((((@                     
                        *(((((((/////////(((((((((((((((((/                     
                        &(((((((/(///(((((#(((((((((((((((                      
                       *((((((((/////((((((((((((((((((((&                      
                       (((((((((///((/(((((((((((((((((((/                      
                      %(((((((#////(/(((((((((((((((((((#.                      
                     .#((((((((///((((((((((((((((#((((((                       
                     *(/#(((((((/(/((((((((((((((((((((#.                       
                     %((/(((((/(/(/(((((((((((((((###((..                       
                     #(((((/##((/((((((((((((((((###((..                        
                     #(((((((((((((((((((((#(#(((((((,,                         
                    .#(((((((((((((((((((((((((###((/.                          
                     #((((((((((((((((((((((((((((((                            
                     *(((((#(/#(//((((((((((((((((..                            
                      &(//##(//(//((//((((((((((#                               
                       *///(//////////(((((///#                                 
                         *#//////////(///(#/                                     

 _______      _          __       __               __  
|_   __ \    (_)        [  |  _  [  |             |  ] 
  | |__) |   __   .---.  | | / ]  | | .---.   .--.| |  
  |  __ /   [  | / /'`\] | '' <   | |/ /__\\/ /'`\' |  
 _| |  \ \_  | | | \__.  | |`\ \  | || \__.,| \__/  |  
|____| |___|[___]'.___.'[__|  \_][___]'.__.' '.__.;__] 
                                                       

by Zipfian Science                               
```
Python tools for creating pickles in a different way.

## Sauce layout

```
rickled
   |
   |- docs
   |  |- source
   |
   |- rickled
   |  |- __init__.py
   |
   |- tests
   |  |- integration
   |  |- placebos
   |  |- unittest
   |
   |- deploy.py
   |- run_tests.py
   |- setup.py
```
## Run tests

To run unit tests, use the helper script `run_tests.py`.

```shell script
# To see available options
$ python run_tests.py -h
```

## Deploying

To build and deploy to PyPi, use the helper script `deploy.py`.

```shell script
# To see available options
$ python deploy.py -h
```

## Install and use

Once deployed, the package can be installed via pip.

```shell script
$ pip install rickled
```

## Branching dev repos 

There are two main branches at any given point in time. These branches may only be pulled. These are:

- master
- dev

On creating a pull request for merging into dev or master, change reviews must be requested. 

### master

This is the production branch and is considered the golden version. 
Production builds are deployed from this branch. 
Feature development will typically be pulled into the `dev` branch first but bug fixes can be directly pulled into master. 

### dev

This is the pre-release branch for merging tested and stable code. 
Although the branch is open for merging, it should still be done with communication throughout the team. 

## Feature development branches

Feature development requires branches to be created and pushed remotely. When creating a new branch, the following naming convention should be followed:
All feature branches are pulled into `dev`. 

> AA_description

Explanation: 
- AA: the initials of the dev
- Description: short text describing the work or feature development

Example:

> JK_new_genetic_programming

This describes that this branch is being developed by JK (John Khoza) and that the nature of development is building a new idea in EA.

These branches have to be created from a local up to date `dev` branch, depending on where you start off a new development. 
Branches have to be pushed to the remote branch:  

`JK_new_genetic_programming[local] -> JK_new_genetic_programming[remote]`

Merge requests into dev from feature development branches will be reviewed by a requested team member.

## Branching and keeping up to date

Example of branching:

```shell script
$ git checkout dev
$ git pull
$ git checkout -b AA_description
$ git commit
$ git push origin AA_description
```

In case of changes to master/dev, a git rebase will bring your branch up to date with master and avoid conflicts. For example:

```shell script
$ git checkout dev
$ git pull
$ git checkout AA_description
$ git merge dev
```
Alternatively, but not recommended:

```shell script
$ git checkout dev
$ git pull
$ git checkout AA_description
$ git rebase dev
```

## .gitignore

This is rather crucial to keep the repository clean. 
When any artefacts or files are created during development that don’t relate to run time code, please add these to the `.gitignore` file so that they are not added automatically. 
With that said, please commit the .gitignore file itself!


© [Zipfian Science](https://zipfian.science) 2022
