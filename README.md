Here we solve the network flows optimization problem propused by AIMMS in https://download.aimms.com/aimms/download/manuals/AIMMS3_OM.pdf using OR-Tools graph library of Python.

In this problem, we have two sources, located in Arnhem and Gouda, and six customers, located in London, Berlin, Maastricht, Amsterdam, Utrecht and The Hague. For reasons of efficiency, deliveries abroad are only made by one source. So that, Arnhem delivers to Berlin and Gouda to London.

The limits of production/supply for each source, the demand for each customer and the transportation costs between each source and customer are known. In this problem, the goal is to satisfy the customers’ demand while minimizing transportation costs.

We can represent this problem as a bipartite graph where the nodes can be divided into two disjoint sets such that all arc connect a node in one set to a node in another set and there are no arcs between nodes in the same set.

In main.py, we can find the problem formulation (you can see more details in https://developers.google.com/optimization/flow/mincostflow), the way to solve it and a way to print the solution.

We have four data file in 'data' folder that we can use to try the code:
* data_0.json. This is the base case.
* data_1.json. Using the base case, we move one ton of supply capacity from Gouda to Arnhem and the objective function improves in 0.2 euros.
* data_2.json. Using the base case, we increase the demand in London in one ton, we increase one ton of supply capacity in Gouda (Gouda is the only source for London) and we increase this arc capacity in one ton. Then the objective function gets worse in 2.5 euros.
* data_3.json. Using the base case, we increase the demand in Berlin in one ton, we increase one ton of supply capacity in Gouda (Arnhem is the only source for Berlin) and we increase the arc capacity between Arnhem and Berlin in one ton. Then the objective function gets worse in 2.7 euros.
* data_4.json. Using the base case, we fixed a transportation between Arnhem and Amsterdam equal to one ton, in order to do that we reduce the capacity between Gouda and Arnhem in one ton. Then the objective function gets worse in 0.6 euros.