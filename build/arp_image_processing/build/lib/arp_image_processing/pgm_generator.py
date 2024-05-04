import numpy as np

# Replace with your actual map data
map_data = np.array([
    [0, 0, 0, 0, 0],
    [0, 0, 1, 0, 0],
    [0, 1, 1, 1, 0],
    [0, 0, 1, 0, 0],
    [0, 0, 0, 0, 0]
])

# Convert map data to PGM format
pgm_header = "P6\n" + \
    str(map_data.shape[1]) + " " + str(map_data.shape[0]) + "\n255\n"
pgm_data = pgm_header + \
    "\n".join(" ".join(str(int(cell)) for cell in row) for row in map_data)

# Save the PGM file
with open("my_map.pgm", "wb") as f:
    f.write(pgm_data.encode("ascii"))

print("PGM file 'my_map.pgm' generated successfully.")
