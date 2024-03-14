# Contributing

As this is an open source project, forks and PRs are welcome! Please review some of the practices used below when contributing.
Contributing and branching work a bit different to what the norm is, please read carefully how it is done here. The long of the short is that all PR should be merged into the `dev` branch, and NOT `master`.

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

## Branching dev repos 

There are two main branches at any given point in time. These branches may only be pulled. These are:

- master
- dev

On creating a pull request for merging into dev or master, change reviews must be requested. 

### master

This is the clean golden source branch. 
Feature development will typically be merged into `dev` branch first.
The `master` branch is exclusively merged into from the `dev` branch. 

### dev

This is the release branch for merging tested and stable code.
Production builds (or better called realeases) on pypi are built from this branch. 
Although the branch is open for merging into, it should still be done with communication throughout the team. 

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

In case of changes to dev, a git rebase will bring your branch up to date with master and avoid conflicts. For example:

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
