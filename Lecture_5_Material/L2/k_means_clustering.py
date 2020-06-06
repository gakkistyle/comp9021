# COMP9021 Term 3 2019


from collections import defaultdict
import tkinter as tk
import tkinter.messagebox


class KMeansClustering(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.title('k-means clustering')
        menubar = tk.Menu()
        help_menu = tk.Menu(menubar)
        menubar.add_cascade(label='k-means Clustering Help', menu=help_menu)
        help_menu.add_command(label='Principle', command=self.principle_help)
        help_menu.add_command(label='Clearing', command=self.clearing_help)
        help_menu.add_command(
                    label='Creating points and initial centroids',
                    command=self.creating_points_and_initial_centroids_help
                             )
        self.config(menu=menubar)

        self.space = Space()
        buttons = tk.Frame(bd=20)
        self.configure_space_or_cluster_button =\
                tk.Button(buttons, text='Cluster', width=5,
                          command=self.configure_space_or_cluster
                         )
        self.configure_space_or_cluster_button.pack(padx=30, side=tk.LEFT)
        self.clear_or_iterate_button = tk.Button(buttons, text='Clear',
                                                 width=5,
                                                 command=self.clear_or_iterate
                                                )
        self.clear_or_iterate_button.pack(padx=30)
        buttons.pack()
        self.space.pack()
        self.clustering = False

    def principle_help(self):
        tkinter.messagebox.showinfo(
                'Principle',
                'k, a positive integer which here can only be at most '
                'equal to 6, represents the number of clusters to be '
                'created.\n\nAfter the user has created a number of '
                '(round) points, the button displaying "Cluster" can '
                'be clicked, and then the user can create k (square) '
                'points, or "centroids", displayed in different '
                'colors.\nClicking the button displaying "Iterate" '
                'gives each point the colour of the closest centroid, '
                'making that point a member of the cluster associated '
                'with that colour.\n\nThe centre of gravity of each '
                'cluster then becomes the new centroid. The same '
                'computation can be done again by clicking the button '
                'displaying "Iterate", until the clusters do not '
                'change any more, in which case the button labels '
                'change and the user is in a position to run another '
                'experiment.\n\nThe user can also click the button '
                'displaying "Stop" to get back to that position, and '
                'change her mind by clicking again on the button '
                'displaying "Cluster".'
                                    )

    def clearing_help(self):
        tkinter.messagebox.showinfo(
                'Clearing',
                'In case centroids are displayed, clicking the "Clear" '
                'button deletes the centroids, and if the points are '
                'coloured because they have been clustered, then they '
                'lose their colour.\n\nIn case no centroid is '
                'displayed, possibly because the "Clear" button has '
                'just been clicked, then clicking the "Clear" button '
                'deletes all points.'
                                    )

    def creating_points_and_initial_centroids_help(self):
        tkinter.messagebox.showinfo(
                'Creating points and initial centroids',
                'Points and initial centroids are created simply by '
                'clicking in the grey area.\nClicking on an existing '
                'point or initial centroid deletes it.\nNo point or '
                'centroid is created when it is too close to an '
                'existing point or centroid, respectively.\n\nThere '
                'can be at most 6 centroids. Trying to create more '
                'will have no effect.'
                                    )

    def configure_space_or_cluster(self):
        if self.clustering:
            self.configure_space_or_cluster_button.config(text='Cluster')
            self.clear_or_iterate_button.config(text='Clear')
            self.clustering = False
            self.space.clustering = False
            self.space.nb_of_clusters = 0
        else:
            self.configure_space_or_cluster_button.config(text='Stop')
            self.clear_or_iterate_button.config(text='Iterate')
            self.clustering = True
            self.space.clustering = True

    def clear_or_iterate(self):
        if self.clustering:
            if not self.space.iterate():
                self.configure_space_or_cluster()
        else:
            self.space.clear()


class Space(tk.Frame):
    space_dim = 600
    space_colour = '#F5F5F5'
    point_colour = '#808080'

    def __init__(self):
        tk.Frame.__init__(self, padx=20, pady=20)
        self.space = tk.Canvas(self, width=self.space_dim,
                               height=self.space_dim, bg=self.space_colour
                              )
        self.space.bind('<1>', self.act_on_click)
        self.space.pack()
        self.points = {}
        self.centroids = {}
        self.colours = 'red', 'green', 'blue', 'cyan', 'black', 'magenta'
        self.available_colours = list(self.colours)
        self.clustering = False

    def clear(self):
        if self.centroids:
            for centroid_coordinates in self.centroids:
                self.space.itemconfig(
                        self.centroids[centroid_coordinates].drawn_point,
                        fill='', outline=''
                                     )
            self.centroids.clear()
            for point_coordinates in self.points:
                self.points[point_coordinates].colour = self.point_colour
                self.space.itemconfig(
                        self.points[point_coordinates].drawn_point,
                        fill=self.point_colour, outline=self.point_colour
                                     )
            self.available_colours = list(self.colours)
        else:
            for point_coordinates in self.points:
                self.space.itemconfig(
                        self.points[point_coordinates].drawn_point, fill='',
                        outline=''
                                     )
            self.points.clear()

    def act_on_click(self, event):
        x = self.space.canvasx(event.x)
        y = self.space.canvasx(event.y)
        if x < 10 or x > self.space_dim - 5 or y < 10\
           or y > self.space_dim - 5:
            return
        coordinates = x, y
        if self.clustering:
            if self.request_point_otherwise_delete_or_ignore(
                                            coordinates, self.centroids, 8
                                                            )\
               and self.available_colours:
                colour = self.available_colours.pop()
                self.centroids[coordinates] =\
                        Point(self.draw_centroid(x, y, colour), colour)
        else:
            if self.request_point_otherwise_delete_or_ignore(coordinates,
                                                             self.points, 25
                                                            ):
                self.points[coordinates] = Point(self.space.create_oval(
                                                    x - 2, y - 2, x + 2, y + 2,
                                                    fill=self.point_colour,
                                                    outline=self.point_colour),
                                                    self.point_colour
                                                )

    def request_point_otherwise_delete_or_ignore(self, coordinates, points,
                                                 size
                                                ):
        for point_coordinates in points:
            if self.square_of_distance(coordinates, point_coordinates) < size:
                self.space.itemconfig(points[point_coordinates].drawn_point,
                                      fill='', outline=''
                                     )
                colour = points[point_coordinates].colour
                if colour != self.point_colour:
                    self.available_colours.append(colour)
                del points[point_coordinates]
                return False
        if any(self.square_of_distance(coordinates,
                                       point_coordinates
                                      ) < 4 * size
                    for point_coordinates in points
              ):
                return False
        return True

    def square_of_distance(self, coordinates_1, coordinates_2):
        return (coordinates_1[0] - coordinates_2[0]) ** 2\
               + (coordinates_1[1] - coordinates_2[1]) ** 2

    def iterate(self):
        if not self.centroids:
            return
        clusters = defaultdict(set)
        different_clustering = False
        for point_coordinates in self.points:
            min_square_of_distance = float('inf')
            for centroid_coordinates in self.centroids:
                square_of_distance =\
                        self.square_of_distance(point_coordinates,
                                                centroid_coordinates
                                               )
                if square_of_distance < min_square_of_distance:
                    min_square_of_distance = square_of_distance
                    closest_centroid_coordinates = centroid_coordinates
            colour = self.centroids[closest_centroid_coordinates].colour
            if self.points[point_coordinates].colour != colour:
                self.points[point_coordinates].colour = colour
                self.space.itemconfig(
                        self.points[point_coordinates].drawn_point,
                        fill=colour, outline=colour
                                     )
                different_clustering = True
            clusters[closest_centroid_coordinates].add(point_coordinates)
        for centroid_coordinates in clusters:
            nb_of_points = len(clusters[centroid_coordinates])
            x, y = [sum(c) for c in zip(*clusters[centroid_coordinates])]
            clusters[centroid_coordinates] = x / nb_of_points, y / nb_of_points
        for centroid_coordinates in self.centroids:
            self.space.itemconfig(
                    self.centroids[centroid_coordinates].drawn_point, fill='',
                    outline=''
                                 )
        updated_centroids = {}
        for centroid_coordinates in clusters:
            colour = self.centroids[centroid_coordinates].colour
            x, y = clusters[centroid_coordinates]
            updated_centroids[(x, y)] = Point(self.draw_centroid(x, y, colour),
                                              colour
                                             )
        self.centroids = updated_centroids
        return different_clustering

    def draw_centroid(self, x, y, colour):
        return self.space.create_rectangle(x - 1, y - 1, x + 1, y + 1,
                                           fill=colour, outline=colour
                                          )


class Point:
    def __init__(self, drawn_point, colour):
        self.drawn_point = drawn_point
        self.colour = colour


if __name__ == '__main__':
    KMeansClustering().mainloop()
