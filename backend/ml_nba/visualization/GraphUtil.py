# File: my_library/utils/graph_util.py

import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Rectangle, Arc

class GraphUtil:

    @staticmethod
    def draw_court(ax=None, color="gray", lw=1, zorder=0):
        """
        Draw basketball court lines on a Matplotlib Axes.

        Args:
            ax (matplotlib.axes.Axes, optional): The Axes to draw on. If None, the current Axes will be used.
            color (str, optional): Line color. Default is "gray".
            lw (float, optional): Line width. Default is 1.
            zorder (int, optional): Z-order for rendering. Default is 0.

        Returns:
            matplotlib.axes.Axes: The updated Axes.
        """
        if ax is None:	
            ax = plt.gca()	

        # Creates the out of bounds lines around the court	
        outer = Rectangle((0,-50), width=94, height=50, color=color,	
                          zorder=zorder, fill=False, lw=lw)	

        # The left and right basketball hoops	
        l_hoop = Circle((5.35,-25), radius=.75, lw=lw, fill=False, 	
                        color=color, zorder=zorder)	
        r_hoop = Circle((88.65,-25), radius=.75, lw=lw, fill=False,	
                        color=color, zorder=zorder)	

        # Left and right backboards	
        l_backboard = Rectangle((4,-28), 0, 6, lw=lw, color=color,	
                                zorder=zorder)	
        r_backboard = Rectangle((90, -28), 0, 6, lw=lw,color=color,	
                                zorder=zorder)	

        # Left and right paint areas	
        l_outer_box = Rectangle((0, -33), 19, 16, lw=lw, fill=False,	
                                color=color, zorder=zorder)    	
        l_inner_box = Rectangle((0, -31), 19, 12, lw=lw, fill=False,	
                                color=color, zorder=zorder)	
        r_outer_box = Rectangle((75, -33), 19, 16, lw=lw, fill=False,	
                                color=color, zorder=zorder)	

        r_inner_box = Rectangle((75, -31), 19, 12, lw=lw, fill=False,	
                                color=color, zorder=zorder)	

        # Left and right free throw circles	
        l_free_throw = Circle((19,-25), radius=6, lw=lw, fill=False,	
                              color=color, zorder=zorder)	
        r_free_throw = Circle((75, -25), radius=6, lw=lw, fill=False,	
                              color=color, zorder=zorder)	

        # Left and right corner 3-PT lines	
        # a represents the top lines	
        # b represents the bottom lines	
        l_corner_a = Rectangle((0,-3), 14, 0, lw=lw, color=color,	
                               zorder=zorder)	
        l_corner_b = Rectangle((0,-47), 14, 0, lw=lw, color=color,	
                               zorder=zorder)	
        r_corner_a = Rectangle((80, -3), 14, 0, lw=lw, color=color,	
                               zorder=zorder)	
        r_corner_b = Rectangle((80, -47), 14, 0, lw=lw, color=color,	
                               zorder=zorder)	

        # Left and right 3-PT line arcs	
        l_arc = Arc((5,-25), 47.5, 47.5, theta1=292, theta2=68, lw=lw,	
                    color=color, zorder=zorder)	
        r_arc = Arc((89, -25), 47.5, 47.5, theta1=112, theta2=248, lw=lw,	
                    color=color, zorder=zorder)	

        # half_court	
        # ax.axvline(470)	
        half_court = Rectangle((47,-50), 0, 50, lw=lw, color=color,	
                               zorder=zorder)	

        hc_big_circle = Circle((47, -25), radius=6, lw=lw, fill=False,	
                               color=color, zorder=zorder)	
        hc_sm_circle = Circle((47, -25), radius=2, lw=lw, fill=False,	
                              color=color, zorder=zorder)	

        court_elements = [l_hoop, l_backboard, l_outer_box, outer,	
                          l_inner_box, l_free_throw, l_corner_a,	
                          l_corner_b, l_arc, r_hoop, r_backboard, 	
                          r_outer_box, r_inner_box, r_free_throw,	
                          r_corner_a, r_corner_b, r_arc, half_court,	
                          hc_big_circle, hc_sm_circle]	

        # Add the court elements onto the axes	
        for element in court_elements:	
            ax.add_patch(element)

        # Remove the axix ticks
        ax.xaxis.set_visible(False)
        ax.yaxis.set_visible(False)

        return ax

    @staticmethod
    def plot_player_movement(player_data):
        """
        Plot a single player's movements on the basketball court.

        Args:
            player_data (pandas.DataFrame): Player's movement data.

        Returns:
            None
        """
        # read in the court png file	
        court = plt.imread(r"C:\Users\Stephanos\Documents\Dev\NBAThesis\NBA_Thesis\static\backend\imgs\fullcourt.png")	

        plt.figure(figsize=(15, 11.5))	

        # Plot the movemnts as scatter plot	
        # using a colormap to show change in game clock	
        plt.scatter(player_data.x_loc, -player_data.y_loc, c=player_data.game_clock,	
                    cmap=plt.cm.Blues, s=1000, zorder=1, edgecolors='k')	
        # Darker colors represent moments earlier on in the game	
        cbar = plt.colorbar(orientation="horizontal")	
        cbar.ax.invert_xaxis()	

        GraphUtil.draw_court()	

        plt.xlim(-7,101)	
        plt.ylim(-50, 0)	

        plt.show() 

    @staticmethod
    def display_full_court():
        """
        Display a full basketball court.

        Returns:
            None
        """
        plt.xlim(0, 94)
        plt.ylim(-50, 0)
        plt.show()

    @staticmethod
    def display_half_court():
        """
        Display a half basketball court.

        Returns:
            None
        """
        plt.xlim(0, 47)
        plt.ylim(-50, 0)
        plt.show()

    @staticmethod
    def save_half_court(filepath):
        """
        Save a half basketball court diagram to a file.

        Args:
            filepath (str): Path to the output file.

        Returns:
            None
        """
        plt.xlim(0, 47)
        plt.ylim(-50, 0)
        plt.savefig(filepath)
        plt.clf()