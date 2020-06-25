# empress_gui.py

import tkinter as tk
from tkinter import messagebox
from pathlib import Path
import os
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.backend_bases import MouseEvent, key_press_handler
import empress
import ReconInput
from empress.reconcile.recon_vis.utils import dict_to_tree
from empress.reconcile.recon_vis import tree

class App(tk.Frame):

    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.master = master
        # Configure the master frame 
        master.grid_rowconfigure(0, weight=1)
        master.grid_rowconfigure(1, weight=2)
        master.grid_columnconfigure(0, weight=1)
        master.grid_columnconfigure(1, weight=1)

        # Create a logo frame on top of the master frame 
        self.logo_frame = tk.Frame(master)
        # sticky="nsew" means that self.logo_frame expands in all four directions (north, south, east and west) 
        # to fully occupy the allocated space in the grid system (row 0 column 0&1)
        self.logo_frame.grid(row=0, column=0, columnspan=2, sticky="nsew")
        self.logo_frame.grid_propagate(False)

        # Add logo image
        photo = tk.PhotoImage(file="./assets/jane_logo_thin.gif")
        label = tk.Label(self.logo_frame, image=photo)
        label.place(x=0, y=0)
        label.image = photo

        # Create an input frame on the left side of the master frame 
        self.input_frame = tk.Frame(master)
        self.input_frame.grid(row=1, column=0, sticky="nsew")
        self.input_frame.grid_rowconfigure(0, weight=1)
        self.input_frame.grid_rowconfigure(1, weight=1)
        self.input_frame.grid_rowconfigure(2, weight=1)
        self.input_frame.grid_rowconfigure(3, weight=1)
        self.input_frame.grid_rowconfigure(4, weight=1)
        self.input_frame.grid_rowconfigure(5, weight=1)
        self.input_frame.grid_rowconfigure(6, weight=1)
        self.input_frame.grid_columnconfigure(0, weight=1)
        self.input_frame.grid_propagate(False)

        # Create an output frame on the right side of the master frame
        self.output_frame = tk.Frame(master)
        self.output_frame.grid(row=1, column=1, sticky="nsew")
        self.output_frame.grid_rowconfigure(0, weight=1)
        self.output_frame.grid_rowconfigure(1, weight=1)
        self.output_frame.grid_rowconfigure(2, weight=1)
        self.output_frame.grid_columnconfigure(0, weight=1)
        self.output_frame.grid_propagate(False)

        # "Load files" button 
        # Load in three input files (two .nwk and one .mapping)
        # and display the number of leaves in each tree and the entry boxes for setting DTL costs (next step)
        self.recon_input_file_option = tk.StringVar(self.input_frame) 
        self.recon_input_file_option.set("Load files")
        self.options = ["Load host tree file", "Load parasite tree file", "Load mapping file"]
        self.load_files_dropdown = tk.OptionMenu(self.input_frame, self.recon_input_file_option, *self.options, command=self.load_input_files)
        self.load_files_dropdown.configure(width=15)
        self.load_files_dropdown.grid(row=0, column=0)
        # Force a sequence of loading host tree file first, and then parasite tree file, and then mapping file
        self.load_files_dropdown['menu'].entryconfigure("Load parasite tree file", state = "disabled")
        self.load_files_dropdown['menu'].entryconfigure("Load mapping file", state = "disabled")

        # "View tanglegram" button
        self.view_tanglegram_btn = tk.Button(self.input_frame, text="View tanglegram", state=tk.DISABLED, width=18)
        self.view_tanglegram_btn.grid(row=1, column=0)

        # "View cost space" button 
        # Pop up a matplotlib graph for the cost regions
        self.view_cost_space_btn = tk.Button(self.input_frame, text="View cost space", command=self.plot_cost_regions, state=tk.DISABLED, width=18)
        self.view_cost_space_btn.grid(row=2, column=0)

        # "Compute reconciliations" button 
        # Display reconciliation results(numbers) and three options(checkboxes) for viewing graphical analysis
        self.compute_reconciliations_btn = tk.Button(self.input_frame, text="Compute reconciliations", command=self.display_recon_information, state=tk.DISABLED, width=18)
        self.compute_reconciliations_btn.grid(row=3, column=0)

        # "View solution space" button
        self.view_solution_space_btn = tk.Button(self.input_frame, text="View solution space", command=self.open_window_solution_space, state=tk.DISABLED, width=18)
        self.view_solution_space_btn.grid(row=4, column=0)

        # "View reconciliations" button
        self.view_reconciliations_btn = tk.Button(self.input_frame, text="View reconciliations", command=self.open_window_reconciliations, state=tk.DISABLED, width=18)
        self.view_reconciliations_btn.grid(row=5, column=0)

        # "View p-value histogram" button
        self.view_pvalue_histogram_btn = tk.Button(self.input_frame, text="View p-value histogram", command=self.open_window_pvalue_histogram, state=tk.DISABLED, width=18)
        self.view_pvalue_histogram_btn.grid(row=6, column=0)

        # Create an input information frame in self.output_frame
        # to display the numbers of tips for host and parasite trees
        self.input_info_frame = tk.Frame(self.output_frame)
        self.input_info_frame.grid(row=0, column=0, sticky="nsew")
        self.input_info_frame.grid_rowconfigure(0, weight=1)
        self.input_info_frame.grid_rowconfigure(1, weight=1)
        self.input_info_frame.grid_rowconfigure(2, weight=1)
        self.input_info_frame.grid_columnconfigure(0, weight=1)
        self.input_info_frame.grid_propagate(False)

        # Creates a frame for setting DTL costs in self.output_frame
        self.costs_frame = tk.Frame(self.output_frame)
        self.costs_frame.grid(row=1, column=0, sticky="nsew")
        self.costs_frame.grid_rowconfigure(0, weight=1)
        self.costs_frame.grid_rowconfigure(1, weight=1)
        self.costs_frame.grid_rowconfigure(2, weight=1)
        self.costs_frame.grid_columnconfigure(0, weight=1)
        self.costs_frame.grid_columnconfigure(1, weight=1)
        self.costs_frame.grid_propagate(False) 

        # Creates a frame for showing reconciliation results as numbers in self.output_frame
        self.recon_nums_frame = tk.Frame(self.output_frame)
        self.recon_nums_frame.grid(row=2, column=0, sticky="nsew")
        self.recon_nums_frame.grid_rowconfigure(0, weight=1)
        self.recon_nums_frame.grid_rowconfigure(1, weight=1)
        self.recon_nums_frame.grid_rowconfigure(2, weight=1)
        self.recon_nums_frame.grid_rowconfigure(3, weight=1)
        self.recon_nums_frame.grid_rowconfigure(4, weight=1)
        self.recon_nums_frame.grid_columnconfigure(0, weight=1)
        self.recon_nums_frame.grid_columnconfigure(1, weight=7)
        self.recon_nums_frame.grid_propagate(False)

        # To overwrite everything when user loads in new input files 
        # (always starting from the host tree file)
        self.host_tree_info = tk.Label(self.input_info_frame)
        self.parasite_tree_info = tk.Label(self.input_info_frame)
        self.mapping_info = tk.Label(self.input_info_frame)

        self.dup_label = tk.Label(self.costs_frame)
        self.dup_entry_box = tk.Entry(self.costs_frame)
        self.trans_label = tk.Label(self.costs_frame)
        self.trans_entry_box = tk.Entry(self.costs_frame)
        self.loss_label = tk.Label(self.costs_frame)
        self.loss_entry_box = tk.Entry(self.costs_frame)
        self.dup_input = tk.DoubleVar()
        self.dup_input.set(1.00)
        self.trans_input = tk.DoubleVar()
        self.trans_input.set(1.00)
        self.loss_input = tk.DoubleVar()
        self.loss_input.set(1.00)

        self.recon_MPRs_label = tk.Label(self.recon_nums_frame)
        self.num_MPRs_label = tk.Label(self.recon_nums_frame)
        self.recon_cospeci_label = tk.Label(self.recon_nums_frame)
        self.recon_dup_label = tk.Label(self.recon_nums_frame)
        self.recon_trans_label = tk.Label(self.recon_nums_frame)
        self.recon_loss_label = tk.Label(self.recon_nums_frame)

        self.num_cluster_input = tk.IntVar()
        self.num_cluster = None

        self.recon_info_displayed = False
        self.recon_input = ReconInput.ReconInput()
        App.recon_graph = None
        App.clusters_list = []
        App.medians = None

        self.cost_space_window = None
        self.view_solution_space_window = None
        self.view_reconciliations_window = None
        self.view_pvalue_histogram_window = None

    def reset(self, event):
        """Reset when user loads in a new input file (can be either of the three options)."""
        App.recon_graph = None 
        App.clusters_list = []
        App.medians = None
        # Reset self.recon_input so self.view_cost_space_btn can be disabled
        self.recon_input = ReconInput.ReconInput()
        self.view_cost_space_btn.configure(state=tk.DISABLED)
        self.view_tanglegram_btn.configure(state=tk.DISABLED)

        if event == "Load host tree file":
            self.load_files_dropdown['menu'].entryconfigure("Load parasite tree file", state = "normal")

            # Read in host tree file after reseting everything
            self.recon_input.read_host(self.host_file_path)

            self.host_tree_info.destroy() 
            self.parasite_tree_info.destroy()
            self.mapping_info.destroy()

        elif event == "Load parasite tree file":
            self.load_files_dropdown['menu'].entryconfigure("Load mapping file", state = "normal")

            # Read in host and parasite tree files after reseting everything
            self.recon_input.read_host(self.host_file_path)
            self.recon_input.read_parasite(self.parasite_file_path)

            self.parasite_tree_info.destroy()
            self.mapping_info.destroy()

        elif event == "Load mapping file":
            # Read in host and parasite trees and mapping files after reseting everything
            self.recon_input.read_host(self.host_file_path)
            self.recon_input.read_parasite(self.parasite_file_path) 
            self.recon_input.read_mapping(self.mapping_file_path)

            self.mapping_info.destroy()

        # Reset dtl costs so self.compute_reconciliations_btn can be disabled
        self.dup_cost = None
        self.trans_cost = None
        self.loss_cost = None
        self.dup_input.set(1.00)
        self.trans_input.set(1.00)
        self.loss_input.set(1.00)
        self.compute_reconciliations_btn.configure(state=tk.DISABLED)
        self.view_solution_space_btn.configure(state=tk.DISABLED)
        self.view_reconciliations_btn.configure(state=tk.DISABLED)
        self.view_pvalue_histogram_btn.configure(state=tk.DISABLED)

        # Reset the rest
        self.dup_label.destroy()
        self.dup_entry_box.destroy()
        self.trans_label.destroy()
        self.trans_entry_box.destroy()
        self.loss_label.destroy()
        self.loss_entry_box.destroy()

        self.recon_MPRs_label.destroy()
        self.num_MPRs_label.destroy()
        self.recon_cospeci_label.destroy()
        self.recon_dup_label.destroy()
        self.recon_trans_label.destroy()
        self.recon_loss_label.destroy()

        self.num_cluster_input = tk.IntVar()
        self.num_cluster_input.set(1)
        self.num_cluster = None

        self.recon_info_displayed = False
        
        if self.cost_space_window is not None and self.cost_space_window.winfo_exists() == 1:
            self.cost_space_window.destroy()

        if self.view_solution_space_window is not None and self.view_solution_space_window.winfo_exists() == 1:
            self.view_solution_space_window.destroy()

        if self.view_reconciliations_window is not None and self.view_reconciliations_window.winfo_exists() == 1:
            self.view_reconciliations_window.destroy()

        if self.view_pvalue_histogram_window is not None and self.view_pvalue_histogram_window.winfo_exists() == 1:
            self.view_pvalue_histogram_window.destroy()

    def load_input_files(self, event):
        """
        Load in two .nwk files for the host tree and parasite tree, and one .mapping file. Display the number of tips for 
        the trees and a message to indicate the successful reading of the tips mapping.
        """ 
        # Clicking on "Load host tree file" 
        if self.recon_input_file_option.get() == "Load host tree file":
            # initialdir is set to be the current working directory
            input_file = tk.filedialog.askopenfilename(initialdir=os.getcwd(), title="Select a host file")
            if Path(input_file).suffix == '.nwk':
                # Try to read in host tree file
                self.recon_input.read_host(input_file)
                self.host_file_path = None
                if self.recon_input.host_tree is not None:
                    self.host_file_path = input_file
                    # Force a sequence of loading host tree file first, and then parasite tree file, and then mapping file
                    self.load_files_dropdown['menu'].entryconfigure("Load parasite tree file", state = "disabled")
                    self.load_files_dropdown['menu'].entryconfigure("Load mapping file", state = "disabled")
                    # Reset everything every time user successfully loads in a new host tree file
                    self.reset("Load host tree file")      
                    host_tree_tips_number = self.compute_tree_tips("host tree")
                    self.host_tree_info = tk.Label(self.input_info_frame, text="Host: " + str(host_tree_tips_number) + " tips")
                    self.host_tree_info.grid(row=0, column=0, sticky="w")
                else: 
                    messagebox.showinfo("Warning", "The input file cannot be read.")          
            else:
                messagebox.showinfo("Warning", "Please load a '.nwk' file.")

        # Clicking on "Load parasite tree file" 
        elif self.recon_input_file_option.get() == "Load parasite tree file":
            # initialdir is set to be the current working directory
            input_file = tk.filedialog.askopenfilename(initialdir=os.getcwd(), title="Select a parasite file")
            if Path(input_file).suffix == '.nwk': 
                # Try to read in parasite tree file
                self.recon_input.read_parasite(input_file)
                self.parasite_file_path = None
                if self.recon_input.parasite_tree is not None:
                    self.parasite_file_path = input_file
                    # Reset every time user successfully loads in a new parasite tree file
                    self.reset("Load parasite tree file")
                    parasite_tree_tips_number = self.compute_tree_tips("parasite tree")
                    self.parasite_tree_info = tk.Label(self.input_info_frame, text="Parasite/symbiont: " + str(parasite_tree_tips_number) + " tips")
                    self.parasite_tree_info.grid(row=1, column=0, sticky="w")
                else: 
                    messagebox.showinfo("Warning", "The input file cannot be read.")          
            else:
                messagebox.showinfo("Warning", "Please load a '.nwk' file.")

        # Clicking on "Load mapping file" 
        elif self.recon_input_file_option.get() == "Load mapping file":
            # initialdir is set to be the current working directory
            input_file = tk.filedialog.askopenfilename(initialdir=os.getcwd(), title="Select a mapping file")
            if Path(input_file).suffix == '.mapping': 
                # Try to read in mapping file
                self.recon_input.read_mapping(input_file)
                self.mapping_file_path = None
                if self.recon_input.phi is not None:
                    self.mapping_file_path = input_file
                    # Reset every time user successfully loads in a new mapping file
                    self.reset("Load mapping file")
                    self.mapping_info = tk.Label(self.input_info_frame, text="Tip mapping has been read successfully.")
                    self.mapping_info.grid(row=2, column=0, sticky="w")

                    # Enables the next step, setting DTL costs
                    if self.recon_input.complete(): 
                        self.view_tanglegram_btn.configure(state=tk.NORMAL)
                        self.view_cost_space_btn.configure(state=tk.NORMAL)
                        self.dtl_cost()
                else: 
                    messagebox.showinfo("Warning", "The input file cannot be read.")          
            else:
                messagebox.showinfo("Warning", "Please load a '.mapping' file.")

    def compute_tree_tips(self, tree_type):
        """Compute the number of tips for the input host tree and parasite tree."""
        if tree_type == "host tree":
            host_tree_object = dict_to_tree(self.recon_input.host_tree, tree.TreeType.HOST)
            return len(host_tree_object.leaf_list())
        elif tree_type == "parasite tree":
            parasite_tree_object = dict_to_tree(self.recon_input.parasite_tree, tree.TreeType.PARASITE)
            return len(parasite_tree_object.leaf_list())

    def plot_cost_regions(self):
        """Plot the cost regions using matplotlib and embed the graph in a tkinter window."""
        self.view_solution_space_btn.configure(state=tk.DISABLED)
        self.view_reconciliations_btn.configure(state=tk.DISABLED)
        self.view_pvalue_histogram_btn.configure(state=tk.DISABLED)

        # Creates a new tkinter window 
        self.cost_space_window = tk.Toplevel(self.master)
        self.cost_space_window.geometry("550x550")
        self.cost_space_window.title("Matplotlib Graph - Cost regions")
        # Creates a new frame
        plt_frame = tk.Frame(self.cost_space_window)
        plt_frame.pack(fill=tk.BOTH, expand=1)
        plt_frame.pack_propagate(False)
        cost_regions = empress.compute_cost_regions(self.recon_input, 0.5, 10, 0.5, 10)  
        #cost_regions.draw_to_file('./examples/cost_poly.png')  # draw and save to a file
        fig = cost_regions.draw()  # draw to figure (creates matplotlib figure)
        canvas = FigureCanvasTkAgg(fig, plt_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        # The toolbar allows the user to zoom in/out, drag the graph and save the graph
        toolbar = NavigationToolbar2Tk(canvas, plt_frame)
        toolbar.update()
        canvas.get_tk_widget().pack(side=tk.TOP)
        # Updates the DTL costs using the x,y coordinates clicked by the user inside the graph 
        # Otherwise pops up a warning message window
        fig.canvas.callbacks.connect('button_press_event', self.get_xy_coordinates)

    def get_xy_coordinates(self, event):
        """Update the DTL costs when user clicks on the matplotlib graph, otherwise pop up a warning message window."""
        if event.inaxes is not None:
            self.dup_input.set(round(event.xdata, 2))
            self.trans_input.set(round(event.ydata, 2))
            self.loss_input.set("1.00")
            # Enables the next step, viewing reconciliation result
            self.dup_cost = event.xdata
            self.trans_cost = event.ydata
            self.loss_cost = 1.00
            self.update_compute_reconciliations_btn()
        else:
            messagebox.showinfo("Warning", "Please click inside the axes bounds.")

    def dtl_cost(self):
        """Set DTL costs by clicking on the matplotlib graph or by entering manually."""  
        self.dup_label = tk.Label(self.costs_frame, text="Duplication:")
        self.dup_label.grid(row=0, column=0, sticky="w")
        # %P = value of the entry if the edit is allowed
        # see https://stackoverflow.com/questions/4140437/interactively-validating-entry-widget-content-in-tkinter
        dup_vcmd = (self.register(self.validate_dup_input), '%P')
        # self.dup_input is tk.DoubleVar(), initialized to be 1.00
        self.dup_entry_box = tk.Entry(self.costs_frame, width=3, validate="all", textvariable=self.dup_input, validatecommand=dup_vcmd)
        self.dup_entry_box.grid(row=0, column=1, sticky="w")

        self.trans_label = tk.Label(self.costs_frame, text="Transfer:")
        self.trans_label.grid(row=1, column=0, sticky="w")
        # %P = value of the entry if the edit is allowed
        # see https://stackoverflow.com/questions/4140437/interactively-validating-entry-widget-content-in-tkinter
        trans_vcmd = (self.register(self.validate_trans_input), '%P')
        # self.trans_input is tk.DoubleVar(), initialized to be 1.00
        self.trans_entry_box = tk.Entry(self.costs_frame, width=3, textvariable=self.trans_input, validate="all", validatecommand=trans_vcmd)
        self.trans_entry_box.grid(row=1, column=1, sticky="w")

        self.loss_label = tk.Label(self.costs_frame, text="Loss:")
        self.loss_label.grid(row=2, column=0, sticky="w")
        # %P = value of the entry if the edit is allowed
        # see https://stackoverflow.com/questions/4140437/interactively-validating-entry-widget-content-in-tkinter
        loss_vcmd = (self.register(self.validate_loss_input), '%P')
        # self.loss_input is tk.DoubleVar(), initialized to be 1.00
        self.loss_entry_box = tk.Entry(self.costs_frame, width=3, validate="all", textvariable=self.loss_input, validatecommand=loss_vcmd)
        self.loss_entry_box.grid(row=2, column=1, sticky="w")
    
    def validate_dup_input(self, input_after_change: str):
        try:
            val = float(input_after_change)
            if val >= 0:
                self.dup_cost = val
                #self.dup_entry_box.configure(highlightbackground="blue", highlightcolor="blue")
            else:
                self.dup_cost = None   
                #self.dup_entry_box.configure(highlightbackground="red", highlightcolor="red")
                #messagebox.showinfo("Warning", "The input number should be non-negative.")    
        except ValueError:
            self.dup_cost = None
            #self.dup_entry_box.configure(highlightbackground="red", highlightcolor="red")
            #messagebox.showinfo("Warning", "The input should be a number.")
        
        self.update_compute_reconciliations_btn()
        return True # return True means allowing the change to happen

    def validate_trans_input(self, input_after_change: str):
        try:
            val = float(input_after_change)
            if val >= 0:
                self.trans_cost = val
            else:
                self.trans_cost = None   
                messagebox.showinfo("Warning", "The input number should be non-negative.")    
        except ValueError:
            self.trans_cost = None
            messagebox.showinfo("Warning", "The input should be a number.")
        
        self.update_compute_reconciliations_btn()
        return True # return True means allowing the change to happen
    
    def validate_loss_input(self, input_after_change: str):
        try:
            val = float(input_after_change)
            if val >= 0:
                self.loss_cost = val
            else:
                self.loss_cost = None   
                messagebox.showinfo("Warning", "The input number should be non-negative.")    
        except ValueError:
            self.loss_cost = None
            messagebox.showinfo("Warning", "The input should be a number.")

        self.update_compute_reconciliations_btn()
        return True # return True means allowing the change to happen

    def update_compute_reconciliations_btn(self):
        """When the dtl costs inputs are all valid."""
        if self.dup_cost is not None and self.trans_cost is not None and self.loss_cost is not None:
            # Enable the next button
            self.compute_reconciliations_btn.configure(state=tk.NORMAL)
            self.view_solution_space_btn.configure(state=tk.DISABLED)
            self.view_reconciliations_btn.configure(state=tk.DISABLED)
            self.view_pvalue_histogram_btn.configure(state=tk.DISABLED)
            
            if self.view_solution_space_window is not None and self.view_solution_space_window.winfo_exists() == 1:
                self.view_solution_space_window.destroy()

            if self.view_reconciliations_window is not None and self.view_reconciliations_window.winfo_exists() == 1:
                self.view_reconciliations_window.destroy()
            
            if self.view_pvalue_histogram_window is not None and self.view_pvalue_histogram_window.winfo_exists() == 1:
                self.view_pvalue_histogram_window.destroy()
        else:
            self.compute_reconciliations_btn.configure(state=tk.DISABLED)

    def display_recon_information(self):
        """Display reconciliation results in numbers and further viewing options for graphical analysis."""
        # Compute App.recon_graph
        App.recon_graph = empress.reconcile(self.recon_input, self.dup_cost, self.trans_cost, self.loss_cost)
        self.num_MPRs = App.recon_graph.n_recon
        if self.recon_info_displayed == False:
            # Shows reconciliation results as numbers
            self.recon_MPRs_label = tk.Label(self.recon_nums_frame, text="Number of MPRs: ")
            self.recon_MPRs_label.grid(row=0, column=0, sticky="w")
            self.num_MPRs_label = tk.Label(self.recon_nums_frame, text=self.num_MPRs)
            self.num_MPRs_label.grid(row=0, column=1, sticky="w")
            self.recon_cospeci_label = tk.Label(self.recon_nums_frame, text="# Cospeciations:")
            self.recon_cospeci_label.grid(row=1, column=0, sticky="w")
            self.recon_dup_label = tk.Label(self.recon_nums_frame, text="# Duplications:")
            self.recon_dup_label.grid(row=2, column=0, sticky="w")
            self.recon_trans_label = tk.Label(self.recon_nums_frame, text="# Transfers:")
            self.recon_trans_label.grid(row=3, column=0, sticky="w")
            self.recon_loss_label = tk.Label(self.recon_nums_frame, text="# Losses:")
            self.recon_loss_label.grid(row=4, column=0, sticky="w")
            self.recon_info_displayed = True
        else:
            self.num_MPRs_label.destroy()
            self.num_MPRs_label = tk.Label(self.recon_nums_frame, text=self.num_MPRs)
            self.num_MPRs_label.grid(row=0, column=1, sticky="w")

        if self.view_solution_space_window is not None and self.view_solution_space_window.winfo_exists() == 1:
            self.view_solution_space_window.destroy()

        if self.view_reconciliations_window is not None and self.view_reconciliations_window.winfo_exists() == 1:
            self.view_reconciliations_window.destroy()

        if self.view_pvalue_histogram_window is not None and self.view_pvalue_histogram_window.winfo_exists() == 1:
            self.view_pvalue_histogram_window.destroy()

        # Creates a new tkinter window 
        self.set_num_cluster_window = tk.Toplevel(self.master)
        self.set_num_cluster_window.geometry("300x200")
        self.set_num_cluster_window.title("Set the number of clusters")
        # Creates a new frame
        self.set_num_cluster_frame = tk.Frame(self.set_num_cluster_window)
        self.set_num_cluster_frame.pack(fill=tk.BOTH, expand=tk.YES)
        self.set_num_cluster_frame.pack_propagate(False)
        
        self.num_cluster_label = tk.Label(self.set_num_cluster_frame, text="Number of clusters:")
        self.num_cluster_error = tk.Label(self.set_num_cluster_frame, text="")
        num_cluster_vcmd = (self.register(self.validate_num_cluster_input), '%P')
        # self.num_cluster_input is tk.IntVar(), initialized to be 1
        self.num_cluster_entry_box = tk.Entry(self.set_num_cluster_frame, width=2, textvariable=self.num_cluster_input, validate="all", validatecommand=num_cluster_vcmd)
        self.num_cluster_label.grid(row=0, column=0, sticky="e")
        self.num_cluster_entry_box.grid(row=0, column=1, sticky="w")
        self.num_cluster_error.grid(row=0, column=2)
        self.enter_num_cluster_btn = tk.Button(self.set_num_cluster_frame, text="Enter", command=self.enable_results_analysis_btns)
        self.enter_num_cluster_btn.grid(row=1, column=0)

    def validate_num_cluster_input(self, input_after_change: str):
        try:
            val = int(input_after_change)
            if val >= 1 and val <= self.num_MPRs:
                self.num_cluster = val
            else:
                self.num_cluster = None   
                self.num_cluster_error.config(text="invalid", fg="red")    
        except ValueError:
            self.num_cluster = None
            self.num_cluster_error.config(text="number", fg="red")
        
        if self.num_cluster is not None:
            self.num_cluster_error.config(text="valid", fg="green")
            self.compute_recon_solutions()
        return True # return True means allowing the change to happen

    def enable_results_analysis_btns(self):
        """
        """
        if self.num_cluster is not None:
            self.view_solution_space_btn.configure(state=tk.NORMAL)
            self.view_reconciliations_btn.configure(state=tk.NORMAL)
            self.view_pvalue_histogram_btn.configure(state=tk.NORMAL)
            self.set_num_cluster_window.destroy()

    def compute_recon_solutions(self):
        """Compute cluster histograms and median reconciliations and store them in variables for drawing later."""
        # Compute all clusters from 1 to self.num_cluster
        # and store them in a list called App.clusters_list
        # App.clusters_list[0] contains App.recon_graph.cluster(1) and so on
        # Each App.clusters_list[num] is a list of ReconGraph
        App.clusters_list = []
        for num in range(self.num_cluster):
            App.clusters_list.append(App.recon_graph.cluster(num+1))

        # Compute medians for a specific self.num_cluster
        App.medians = []
        if self.num_cluster == 1:
            App.medians.append(App.recon_graph.median())
        else:
            clusters = App.recon_graph.cluster(self.num_cluster)
            for i in range(len(clusters)):
                App.medians.append(clusters[i].median())
        
        if self.view_solution_space_window is not None and self.view_solution_space_window.winfo_exists() == 1:
            self.view_solution_space_window.destroy()

        if self.view_reconciliations_window is not None and self.view_reconciliations_window.winfo_exists() == 1:
            self.view_reconciliations_window.destroy()
        
        if self.view_pvalue_histogram_window is not None and self.view_pvalue_histogram_window.winfo_exists() == 1:
            self.view_pvalue_histogram_window.destroy()

    def open_window_solution_space(self):
        """    
        """
        self.view_solution_space_window = tk.Toplevel(self.master)
        self.view_solution_space_window.geometry("900x900")
        self.view_solution_space_window.title("View reconciliation space")
        SolutionSpaceWindow(self.view_solution_space_window)

    def open_window_reconciliations(self):
        """
        """
        self.view_reconciliations_window = tk.Toplevel(self.master)
        self.view_reconciliations_window.geometry("900x900")
        self.view_reconciliations_window.title("View reconciliations")
        ReconciliationsWindow(self.view_reconciliations_window)
    
    def open_window_pvalue_histogram(self):
        """Compute the p-value histogram."""
        App.p_value_histogram = App.recon_graph.draw_stats()
        self.view_pvalue_histogram_window = tk.Toplevel(self.master)
        self.view_pvalue_histogram_window.geometry("700x700")
        self.view_pvalue_histogram_window.title("p-value Histogram")
        PValueHistogramWindow(self.view_pvalue_histogram_window)

# View reconciliation space 
class SolutionSpaceWindow(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master        
        self.frame = tk.Frame(master)
        self.frame.pack(fill=tk.BOTH, expand=1)
        self.frame.pack_propagate(False)
        self.draw_clusters()
    
    def draw_clusters(self):
        if len(App.clusters_list) == 1:
            fig = App.recon_graph.draw()
        else:
            fig, axs = plt.subplots(len(App.clusters_list), len(App.clusters_list))
            for i in range(len(App.clusters_list)):
                for j in range(len(App.clusters_list[i])):
                    App.clusters_list[i][j].draw_on(axs[i,j])
        
        canvas = FigureCanvasTkAgg(fig, self.frame)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        # The toolbar allows the user to zoom in/out, drag the graph and save the graph
        toolbar = NavigationToolbar2Tk(canvas, self.frame)
        toolbar.update()
        canvas.get_tk_widget().pack(side=tk.TOP)

# View reconciliations 
class ReconciliationsWindow(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master        
        self.frame = tk.Frame(master)
        self.frame.pack(fill=tk.BOTH, expand=1)
        self.frame.pack_propagate(False)
        self.draw_median_recons()
    
    def draw_median_recons(self):
        if len(App.medians) == 1:
            fig = App.medians[0].draw()
        else:
            fig, axs = plt.subplots(1, len(App.medians))
            for i in range(len(App.medians)):
                App.medians[i].draw_on(axs[i])
        canvas = FigureCanvasTkAgg(fig, self.frame)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        # The toolbar allows the user to zoom in/out, drag the graph and save the graph
        toolbar = NavigationToolbar2Tk(canvas, self.frame)
        toolbar.update()
        canvas.get_tk_widget().pack(side=tk.TOP)

# p-value Histogram 
class PValueHistogramWindow(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master        
        self.frame = tk.Frame(master)
        self.frame.pack(fill=tk.BOTH, expand=1)
        self.frame.pack_propagate(False)
        self.draw_p_value_histogram()
    
    def draw_p_value_histogram(self):
        canvas = FigureCanvasTkAgg(App.p_value_histogram, self.frame)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        # The toolbar allows the user to zoom in/out, drag the graph and save the graph
        toolbar = NavigationToolbar2Tk(canvas, self.frame)
        toolbar.update()
        canvas.get_tk_widget().pack(side=tk.TOP)

def on_closing():
    """Kills the matplotlib program and all other tkinter programs when the master window is closed."""
    plt.close("all")
    root.destroy()

root = tk.Tk()
root.geometry("600x600")
root.title("eMPRess GUI Version 1")
App(root)
root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()
root.quit()
