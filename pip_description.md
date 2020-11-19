# Pickle Rick
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
.---.  _       .-.   .-.          .---.  _       .-.   
: .; ::_;      : :.-.: :          : .; ::_;      : :.-.
:  _.'.-. .--. : `'.': :   .--.   :   .'.-. .--. : `'.'
: :   : :'  ..': . `.: :_ ' '_.'  : :.`.: :'  ..': . `.
:_;   :_;`.__.':_;:_;`.__;`.__.'  :_;:_;:_;`.__.':_;:_;
                                        
by Zipfian Science                               
```
Python tools for creating a different type of pickling by [Zipfian Science](https://zipfian.science/).

Pickle Rick is a lightweight tool for loading and writing very small Python objects to YAML or JSON representations.
This is especially useful for creating YAML config files and serialising them as Python objects.
Works great in interactive Python environments like notebooks.

For documentation, see [docs](http://docs.zipfian.science/pickle-rick/index.html).

Source on [GitHub](https://github.com/Zipfian-Science/pickle-rick).
## Install

```shell script
$ pip install pickle-rick
```

## And use

```python
from pickle_rick import PickleRick
```

Using an example YAML file:

```yaml
BASIC:
  text: test
  dictionary:
    one: 1
    two: 2
  number: 2
  list:
    - one
    - two
    - four
    - name: John
      age: 20
  USERNAME:
    type: env
    load: USERNAME
  callable_lambda:
    type: lambda
    load: "lambda: print('hell world!')"
  datenow:
    type: lambda
    import:
      - "from datetime import datetime as dd"
    load: "lambda: print(dd.utcnow().strftime('%Y-%m-%d'))"
  test_function:
    type: function
    name: test_function
    args:
      x: 7
      y: null
      s: hello world
      any:
        - 1
        - hello
    import:
      - "math"
    load: >
      def test(x, y, s, any):
        print(math.e)
        iii = 111
        print(iii)
        print(x,s)
        if y:
          print(type(y))
        else:
          print(y)
        for i in any:
          print(i)
```

Then use Rick:

```python
>> from pickle_rick import PickleRick

>> config = PickleRick('./config.yaml', deep=True, load_lambda=True)

>> config.BASIC.callable_lambda()
'hell world!'
```

## Release

- Date: {pypi_metdata_release_date}
- Version: {pypi_metdata_version_number}

