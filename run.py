import numpy as np
from stl import mesh
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from tkinter import Tk, filedialog, Button, Frame, messagebox, BOTH
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class STLViewer:
    def __init__(self, master):
        self.master = master
        self.stl_mesh = None
        self.createWidgets()
        self.figure = plt.figure()
        self.ax = self.figure.add_subplot(111, projection='3d')
        self.master.bind("<Configure>", self.onResize)

    def createWidgets(self):    # Button functions for handling stl files and resetting 3d view
        self.controlFrame = Frame(self.master)
        self.controlFrame.pack(side='top', fill='x', pady=5)

        self.importButton = Button(self.controlFrame, text="Import STL file", command=self.filePromptWindow)
        self.importButton.pack(side='left', padx=5, expand=True, fill=BOTH)

        self.resetButton = Button(self.controlFrame, text="Reset View", command=self.reset_view)
        self.resetButton.pack(side='left', padx=5, expand=True, fill=BOTH)

    def onResize(self, event):     # dynamic window resizing
        newWidth = self.master.winfo_width() // 20
        newHeight = self.master.winfo_height() // 30
        newFontSize = min(newWidth, newHeight)

        self.importButton.config(font=('Helvetica', newFontSize))
        self.resetButton.config(font=('Helvetica', newFontSize))

    def filePromptWindow(self):     # directs the user to locate the stl file
        stlPath = filedialog.askopenfilename(title="Open STL File", filetypes=[("STL Files", "*.stl")])
        if stlPath:
            self.loadSTL(stlPath)

    def loadSTL(self, file_name):
        try:
            self.stl_mesh = mesh.Mesh.from_file(file_name)
            self.display_model()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load STL file: {e}")

    def display_model(self):
        self.ax.clear()

        """"Extracting vertices and meshes.
        This part is where the program stutters.
        Some (and probably the most) stl 3d models have thousands of connected vertices, 
        resulting a heavy lag in program"""

        vertices = self.stl_mesh.vectors.reshape(-1, 3)
        faces = np.arange(vertices.shape[0]).reshape(-1, 3)

        mesh_poly = Poly3DCollection(vertices[faces], alpha=.25, facecolor='r', edgecolor='k')
        self.ax.add_collection3d(mesh_poly)

        # Scaling the axes
        scale = vertices.flatten()
        self.ax.auto_scale_xyz(scale, scale, scale)

        self.ax.set_xlabel('X')
        self.ax.set_ylabel('Y')
        self.ax.set_zlabel('Z')

        plt.draw()

    def reset_view(self):
        self.ax.view_init(elev=20., azim=-35)
        plt.draw()


if __name__ == "__main__":
    root = Tk()
    root.title("STL Viewer Toolkit")
    viewer = STLViewer(root)

    # Creating the matplotlib canvas
    canvas = FigureCanvasTkAgg(viewer.figure, master=root)
    canvas.get_tk_widget().pack(side='top', fill='both', expand=True)

    viewer.ax.view_init(elev=20., azim=-35)  # Initializing the view

    root.mainloop()