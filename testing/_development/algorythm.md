<h1> Path Finding Algorythm</h1>

![DB_Schema_2.0.jpeg](..%2F..%2Fpaperwork%2FDB_schema%2FDB_Schema_2.0.jpeg)


## TODO - ISH 

- Set up connector nodes
    between Database and Actual Python Algorythm

- Pull all node ways for Path Finding intpo Python
    depending on the start and end node

- Get a line to follow the path


CLass Algorythm:
    def __init__(self, start, end):
        self.start = start
        self.end = end

    def get_path(self):
        # find path between start and end node from database
        # return path as list of nodes

    def build_box_around_start_and_end_node:
        # any ideas on how to build that box? to get specific nodes?
        # maybe we can use the box to get all nodes in the box and then filter them by distance to start and end node?
        