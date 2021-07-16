To run the code simply execute 

```
python3 {path_to}/adaptive.py
``` 

The graphs for average cost vs generation number should pop up as long as the machine executed on has matplotlib installed. 


In order to test the non-DEAP implementation add a call to the function `run_trials()` at the bottom. This function compares c=0.6, 0.8, 1 for the (1+1)-ES algorithm. 

In order to test the DEAP implementation add a call to the function `run_trials(c={c_value})` at the bottom. This function compares the deap implementation with the non-DEAP implementation for the provided c value. 