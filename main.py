import numpy as np
import pandas as pd
import json
from ortools.graph.python import min_cost_flow


def solve_problem_using_ortools_graph(data_file):
    """solve the problem using ortools graph and print results"""

    # Load data

    # Open json file with data
    f = open(data_file)

    # Returns the data as a dictionary
    data = json.load(f)

    # Close the file
    f.close()

    # Prepare data that the graph or the solution will use

    # Define four parallel arrays: sources, destinations, capacities and unit costs between each pair
    start_nodes = np.array(data["start_nodes"])
    end_nodes = np.array(data["end_nodes"])
    capacities = np.array(data["capacities"])
    unit_costs = np.array([item for item in data["unit_costs"]])

    # Define an array of supplies at each node
    supplies = data["supplies"]

    # Define a dict with the name for each source and destination
    # We will use them to write the results
    start_nodes_names = data["start_nodes_names"]
    end_nodes_names = data["end_nodes_names"]

    # Solve the problem

    # Instantiate a SimpleMinCostFlow solver
    smcf = min_cost_flow.SimpleMinCostFlow()

    # Add arcs, capacities and costs in bulk using numpy
    all_arcs = smcf.add_arcs_with_capacity_and_unit_cost(
        start_nodes, end_nodes, capacities, unit_costs
    )

    # Add supply for each node
    smcf.set_nodes_supplies(np.arange(0, len(supplies)), supplies)

    # Find the min cost flow
    status = smcf.solve()

    # Print the solution

    if status != smcf.OPTIMAL:
        print("There was an issue with the min cost flow input.")
        print("Status:", status)
        exit(1)

    solution_flows = smcf.flows(all_arcs)
    costs = solution_flows * unit_costs
    list_output_data = [
        {
            "Source": start_nodes_names[str(smcf.tail(arc))],
            "Customer": end_nodes_names[str(smcf.head(arc))],
            "Capacity": smcf.capacity(arc),
            "Shipped": flow,
            "Cost": cost
        } for arc, flow, cost in zip(all_arcs, solution_flows, costs)
    ]
    df_output_data = pd.DataFrame(list_output_data)

    print("Status:", status)
    print("")
    print("Minimum cost:", sum(df_output_data["Cost"]))
    print("")
    print("Flows:")
    print(df_output_data)


# Solve some transportation problems

# Base case
solve_problem_using_ortools_graph("./data/data_0.json")

# Sensibility analysis - sources
# Using the base case, we move one ton of supply capacity from Gou to Arn and
# the objetive function improves in 0.2 euros
# solve_problem_using_ortools_graph("./data/data_1.json")

# Sensibility analysis - customers - 1
# Using the base case, we increase the demand in Lon in one ton,
# we increase one ton of supply capacity in Gou (Gou is the only source for Lon)
# and we increase this arc capacity in one ton.
# Then the objetive function gets worse in 2.5 euros
# solve_problem_using_ortools_graph("./data/data_2.json")

# Sensibility analysis - customers - 2
# Using the base case, we increase the demand in Ber in one ton,
# we increase one ton of supply capacity in Gou (Arn is the only source for Ber)
# and we increase the arc capacity between Arn and Ber in one ton.
# Then the objetive function gets worse in 2.7 euros
# solve_problem_using_ortools_graph("./data/data_3.json")

# Sensibility analysis - routes
# Using the base case, we fixed a transportation between Arn and Ams equal to one ton,
# in order to do that we reduce the capacity between Gou and Arn in one ton.
# The objetive function gets worse in 0.6 euros
# solve_problem_using_ortools_graph("./data/data_4.json")
