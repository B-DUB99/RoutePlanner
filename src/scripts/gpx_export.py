import gpxpy
import os


class GPX_export:
	# constructor
	def __init__(self, path):
		self.path = path

	def set_path(self, path):
		self.path = path

	def get_path(self):
		return self.path

	def export(self):
		# Create a new file:
		f = open("mygpx.gpx", "w")

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

		# Add the track to the GPX:
		gpx.tracks.append(gpx_track)

		# Write the GPX file:
		f.write(gpx.to_xml())

		f.close()
		
		return 'mygpx.gpx'

	def clean_up(self):
		# delete the file
		os.remove("mygpx.gpx")


# test function
def main():
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
	gpx.clean_up()


if __name__ == "__main__":
	main()
