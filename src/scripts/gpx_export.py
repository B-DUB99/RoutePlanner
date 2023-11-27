import gpxpy
import os


class GPX_export:
	# constructor
	def __init__(self, path):
		self.path_string = path
		self.path = []

	def set_path(self, path):
		self.path = path

	def get_path(self):
		return self.path

	def parse_string_to_list(self, input_string):
		# Remove whitespaces and newlines
		clean_string = input_string.replace('\n', '').replace('\t', '').replace(' ', '')

		# Remove square brackets at the beginning and end
		clean_string = clean_string[1:-1]

		# Split the string into individual coordinate strings
		coordinate_strings = clean_string.split('],[')

		# Initialize an empty list to store the result
		result_list = []

		# Iterate through the coordinate strings and convert them to lists of floats
		for coordinate_string in coordinate_strings:
			# Remove square brackets from each coordinate string
			coordinate_string = coordinate_string.replace('[', '').replace(']', '')

			# Split the coordinate string into latitude and longitude
			lat_str, lon_str = coordinate_string.split(',')

			# Convert latitude and longitude to floats and create a list
			coordinate_list = [float(lat_str), float(lon_str)]

			# Append the coordinate list to the result list
			result_list.append(coordinate_list)

		self.path = result_list

	def export(self):
		self.parse_string_to_list(self.path_string)

		# Create a new file:
		f = open("my-gpx.gpx", "w")

		# Create a gpx object:
		gpx = gpxpy.gpx.GPX()

		# Create first track in our GPX:
		gpx_track = gpxpy.gpx.GPXTrack()

		# Create first segment in our GPX track:
		gpx_segment = gpxpy.gpx.GPXTrackSegment()

		# Create points where the path is a list of lists of lat and lng
		for point in self.path:
			gpx_segment.points.append(gpxpy.gpx.GPXTrackPoint(point[0], point[1]))

		# Add the segment to the track:
		gpx_track.segments.append(gpx_segment)

		# name the track
		gpx_track.name = "Route Planner"

		# Add the track to the GPX:
		gpx.tracks.append(gpx_track)

		# Write the GPX file:
		f.write(gpx.to_xml())

		f.close()

		return 'my-gpx.gpx'


# clean up function
def clean_up():
	# delete the file
	os.remove("my-gpx.gpx")


# test function DELETE ME LATER
def test():
	tmp_path = [
		[42.29127852746485, -85.5919075012207],
		[42.30918068099292, -85.6549072265625],
		[42.26790919743789, -85.65319061279297],
		[42.291532494305976, -85.58795928955078]
	]

	# pass the path to the GPX_export class
	gpx = GPX_export(tmp_path)
	# call the export function
	gpx.export()
	# wait for user input to delete the file
	input("Press Enter to continue...")
	# call the clean_up function
	clean_up()


if __name__ == "__main__":
	test()
