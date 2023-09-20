class Pathfinder:
    def __init__(self, start, end):
        self.start = start
        self.end = end

        # ------------------ #
        # list of lat and lng #
        self.lat_lng = [[]]

    def find_path(self):            # returns a list of coordinates in the order of the path
        # finds the path from start to end calls the other functions
        print(f'Start:  {self.start}')
        print(f'End:    {self.end}')
        # extract the lat and lng from the start and end dictionaries
        self.lat_lng[0] = [self.start['lat'], self.start['lng']]
        self.lat_lng.append([self.end['lat'], self.end['lng']])
        

        print(f'Path:   {self.lat_lng}')

        pass



    def return_path(self):          # returns a list of coordinates in the order of the path
        # returns the path
        return self.lat_lng


    # retrieve the lat and lng from website ( user ) ( start and end )
    # start node lat lng goes to dataretriever, get_closest_node
    # retrieve is a list of nodes ( node_id, lat, lng )
    # decide what node to go to next (closest node to end node)
        # send new node to the dataretriever, get_node_neighbors to get the next node (node_id)
        # retrieve the neighbors of the node ( node_id, lat, lng )
        # compare the neighbors to the end node (lat, lng)
        # if the neighbor is the end node or within 100 m, then we are done
        # if the neighbor is not the end node, then we need to find the next node to go to


