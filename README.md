# Rickled - Smart Python tools for working with YAML
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
Rickled is a versatile Python library and command-line tool that offers a wide range of functionalities for working with YAML and JSON data. Here's a brief summary of its key features:

1. **Serialization**: Rickled allows you to easily serialize Python objects to YAML format. This is particularly useful for converting Python data structures into a human-readable and easily shareable format.

2. **Schema Validation**: It provides the capability to validate YAML and JSON data against predefined schemas. This ensures that your data adheres to a specific structure or format, helping to maintain data consistency.

3. **Schema Generation**: You can generate schema definitions from existing YAML (or JSON) files. This is helpful when you want to formalize the structure of your data or for documentation purposes.

4. **Conversion between YAML and JSON**: Rickled offers seamless conversion between YAML and JSON formats. This facilitates data interchange between systems that use different serialization formats.

5. **Simple Web Server**: One unique feature of Rickled is its ability to create a basic web server from a YAML file. This means you can define endpoints, routes, and data sources purely by writing it as a YAML file, making it easy to prototype web services without extensive coding, or to create mock REST APIs.

In summary, Rickled is a powerful utility for working with YAML and JSON data in Python. It simplifies tasks like serialization, schema validation, schema generation, format conversion, and even enables quick web server prototyping using YAML configuration files. This tool is valuable for developers and data engineers working with structured data in a flexible and efficient manner.

# Usage

For usage examples see [examples](https://docs.zipfian.science/rickled/examples.html) page.

## Install

First install the tool (Python version >= 3.7):

```bash script
$ pip install rickled
```

Optionally the twisted web server can be installed alongside for the `serve` functionality.

```bash script
$ pip install rickled[twisted]
```

Furthermore, if SSL support is needed:

```bash script
$ pip install rickled[twisted,pyopenssl]
```

Check if the installation succeeded:

```bash script
$ rickle --help
```

## Schema tools

Two main schema tools exist, the `check` and the `gen` tools.

### Schema `check`

For checking the schema of input files, the `check` tool is used.

```bash script
$ rickle schema check --help
```

```bash script
$ rickle schema check -i test.yaml -c schema.yaml 
```

### Schema `gen`

Schema files can be generated from YAML files with the `gen` tool.

```bash script
$ rickle schema gen --help
```

```bash script
$ rickle schema gen -i test.yaml
```

This will generate a schema file called `test.schema.yaml`.


## Conversion tools

Rickled can also be used for bulk conversion from YAML to JSON or the other way around.

```bash script
$ rickle conv --help
```

To convert input files (or directories):

```bash script
$ rickle conv -i test.yaml -o test.json
```

For each input file the output file can be defined and the path suffix is used to infer the desired output type.

Alternatively the type can be specified with the `-t` flag.

## Serving via HTTP(s)

A nifty little use of this Python tool is the ability to host a webserver, using a YAML file.
 
```bash script
$ rickle serve --help
```

```bash script
$ rickle serve -f basic_example.yaml
```

This will start listening on http://localhost:8080, for requests using `GET`. 

# Contributing

As this is an open source project, forks and PRs are welcome! Please review some of the practices used below when contributing.

## Sauce layout

```
rickled
   |
   |- docs
   |  |- source
   |
   |- rickled
   |  |- __init__.py
   |  |- __version__.py
   |  |- cli.py
   |  |- net.py
   |  |- tools.py
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
