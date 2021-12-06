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
   |- 
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
$ pip install pickle-rick
```

## Branching dev repos 

There are three main branches at any given point in time. These branches may only be pulled. These are:

- master
- release
- dev

On creating a pull request for merging into dev or master, change reviews must be requested. 

### master

This is the production branch and is considered the golden version. Production builds are deployed from this branch. Feature development will typically be pulled into the `release` branch first but bug fixes can be directly pulled into master. 

### release

This is considered the pre-release branch and needs to be squeaky clean of dead and experimental code. New feature development will be merged into this branch for future releases. This branch is also not considered as a testing ground for new developments. 

### dev

This is the playground branch for experimental coding and testing. Although the branch is open for merging, it should still be done with communication throughout the team. This branch is also regularly updated from `master` or `release`. 

## Feature development branches

Feature development requires branches to be created and pushed remotely. When creating a new branch, the following naming convention should be followed:

> XXX_AA_description

Explanation: 
- XXX: the TASK ticket number
- AA: the initials of the dev
- Description: short text describing the work or feature development

Example:

> 420_JK_new_genetic_programming

This describes that this branch is concerned with ticket 420, it is being developed by JK (John Khoza) and that the nature of development is building a new idea in EA.

These branches have to be created from a local up to date `master` or `release` branch, depending on where you start off a new development. Branches have to be pushed to the remote branch:  

`420_JK_new_genetic_programming[local] -> 420_JK_new_genetic_programming[remote]`

Merge requests into master, dev, or release from feature development branches will be reviewed by a requested team member.

## Branching and keeping up to date

Example of branching:

```shell script
$ git checkout master
$ git pull
$ git branch XXX_AA_description
$ git checkout XXX_AA_description
$ git commit
$ git push origin XXX_AA_description
```

In case of changes to master/dev, a git rebase will bring your branch up to date with master and avoid conflicts. For example:

```shell script
$ git checkout master
$ git pull
$ git checkout XXX_AA_description
$ git merge master
```
Alternatively, but not recommended:

```shell script
$ git checkout master
$ git pull
$ git checkout XXX_AA_description
$ git rebase master
```

## .gitignore

This is rather crucial to keep the repository clean. When any artefacts or files are created during development that don’t relate to run time code, please add these to the `.gitignore` file so that they are not added automatically. With that said, please commit the .gitignore file itself!


© [Zipfian Science](https://zipfian.science) 2020
