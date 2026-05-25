from mpi4py import MPI
import sqlite3
import math

comm = MPI.COMM_WORLD

rank = comm.Get_rank()
size = comm.Get_size()

DATABASE = 'database/website.db'

conn = sqlite3.connect(DATABASE)
cursor = conn.cursor()

# ------------------------------------------------
# MASTER LOADS DATA
# ------------------------------------------------

if rank == 0:

    cursor.execute('''
    SELECT
        place_id,
        feature_vector
    FROM images
    ''')

    rows = cursor.fetchall()

    dataset = []

    for row in rows:

        vector = [
            float(x)
            for x in row[1].split(',')
        ]

        dataset.append({
            'place_id': row[0],
            'vector': vector
        })

    chunks = [
        dataset[i::size]
        for i in range(size)
    ]

else:
    chunks = None

local_data = comm.scatter(
    chunks,
    root=0
)

# ------------------------------------------------
# DISTANCE
# ------------------------------------------------

def euclidean(a, b):

    total = 0

    for i in range(len(a)):
        total += (a[i] - b[i]) ** 2

    return math.sqrt(total)

# ------------------------------------------------
# LOCAL SIMILARITIES
# ------------------------------------------------

local_results = []

for item in local_data:

    source_id = item['place_id']

    distances = []

    for other in local_data:

        if source_id == other['place_id']:
            continue

        d = euclidean(
            item['vector'],
            other['vector']
        )

        distances.append((other['place_id'], d))

    distances.sort(key=lambda x: x[1])

    top_k = distances[:5]

    local_results.append({
        'source': source_id,
        'recommendations': top_k
    })

# ------------------------------------------------
# GATHER
# ------------------------------------------------

gathered = comm.gather(
    local_results,
    root=0
)

if rank == 0:

    print('MPI preprocessing completed.')

    total = 0

    for process in gathered:
        total += len(process)

    print('Processed:', total)