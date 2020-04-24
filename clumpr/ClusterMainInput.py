# ClumsterMainInput.py
# Dave Makhervaks, March 2020
# Main input function for ClumperMain

def getInput(d, t, l, k, args):
    """ 
    :param d <float> - the cost of a duplication
    :param t <float> - ^^ transfer
    :param l <float> - ^^ loss
    :param k <float>: number of clusters
    :param relev_params: relevant parameters
    :param args <dict str->str> - dictionary that contains all parameters needed 
    to compute, save, and/or output the PDV
    :return inputs <dict str->str> - all input from user for computing and saving the PDV
    """

    inputs = {}
    inputs.update(args)
    getMutuallyExclusiveInput(inputs)
    getOptionalInput(inputs)

    return inputs

#TODO: Add better docstrings!!!
def getMutuallyExclusiveInput(inputs):
    """
    This method is for interactively asking for arguments that are mutually exclusive 
    :param inputs: dictionary of arguments where key is parameter name and value is parameter value.
    """

    # Specifies how far down to go when finding splits
    # requires, d or n!
    while True:
        depth_or_n = input("Please type 'd' if you want to enter depth, or 'n' for nmprs")
        if (depth_or_n not in ('d', 'n')):
            print("Please enter 'd' or 'n'")
        else:
            break

    if (depth_or_n == 'd'):
        while True:
            depth = input("How far down the graph to consider even splits.")
            try:
                inputs["depth"] = int(depth)
                break
            except ValueError:
                print("Depth must be an integer number. Please try again.")
    else:
        while True:
            nmprs = input("How many MPRs to consider.")
            try:
                inputs["nmprs"] = int(nmprs)
                break
            except ValueError:
                print("NMPRs must be an integer number. Please try again.")

    # What visualizations to produce
    # does not require visualization
    while True:
        vis_type = input("Please type 'p' for visualizing using PDV, 'h' for histograms, and 'n' for none.")
        if (vis_type not in ('p','h','n')):
            print("Please enter 'p', 'h', or 'n'")
        else:
            break

    if (vis_type == 'p'):
        inputs["pdv-vis"] = True
    elif (vis_type == 'h'):
        inputs["support-vis"] = True
        
    
    # Which objective function to use
    # requires, p or s!
    while True:
        score = input("Please type 'p' for using weighted average distance to evaluate clusters, or 's' for using weighted event support")
        if (score not in ('p','s')):
            print("Please enter 'p' or 's'")
        else:
            break

    if (score == 'p'):
        inputs["pdv"] = True
    else:
        inputs["support"] = True


def getOptionalInput(inputs):
    """ 
    :param inputs: dictionary of arguments where key is parameter name and value is parameter value.

    """
    bool_params = ("medians")
    for param in bool_params:
        if param not in inputs:
            inputs[param] = True


    print("Enter additional input in the form <parameter name> <value>")
    print("Enter 'Done' when you have no additional input to enter.")
    print("Enter '?' if you would like to see additional input options.")
    while True:
        user_input = input(">> ").split()
        param = user_input[0]
        value = None
        if len(user_input) > 1:
            value = " ".join(user_input[1:])

        if param == "Done":
            break
        elif param == "?":
            print_usage()
        elif param in bool_params:
            if value[0] in ('y', 'Y', 'n', 'N'):
                inputs[param] = value[0] in ('y', 'Y')
            else:
                print("Value must begin with Y, y, N, or n.  Please try again.")
        else:
            print("That is not a valid parameter name. Please try again.")
            
def print_usage():
    """
    Print information on all optional parameter inputs.
    """
    data = [
        ("medians", "Whether or not to print out medians for each cluster."),
    ]
    col_width = max(len(x) for x,y in data) + 2
    for name, hint in data:
        print(name.ljust(col_width) + " " + hint)
