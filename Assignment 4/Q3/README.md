To run the code simply execute 

```
python3 {path_to}/multiplexer.py
``` 

> Note for this to work the machine needs to have deap installed

```
pip3 install deap
```

The graphs for Best iteration finess vs generation number should pop up as long as the machine executed on has matplotlib installed. 


In order to test the multiplexer GA add a call to `plot_multiplexer({num_select_bits}, {num_generations})` to the bottom of the code and execute. 

In order to test the 16-middle-3 GA add a call to `plot_middle({num_generations})` to the bottom of the code and execute. 