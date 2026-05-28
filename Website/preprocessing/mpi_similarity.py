from mpi4py import MPI
import sqlite3
import math

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()
DATABASE = 'database/website.db'
conn = sqlite3.connect(DATABASE)
cursor = conn.cursor()


if rank == 0:
    cursor.execute('''
     SELECT
     place_id,
     feature_vector
     FROM images
    ''')

    rows = cursor.fetchall()

    chunks = [
        rows[i::size]
        for i in range(size)
    ]
else:
    chunks = None

local_rows = comm.scatter(
    chunks,
    root=0
)

local_results = []

for row in local_rows:
    vector = [
        float(x)
        for x in row[1].split(',')
    ]

    local_results.append((
        row[0],
        len(vector)
    ))

gathered = comm.gather(
    local_results,
    root=0
)

if rank == 0:
    total = 0
    for process in gathered:
        total += len(process)

    print('MPI processed:', total)