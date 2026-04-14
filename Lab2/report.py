from init_db import connect
import math


def print_table_sizes(c):
    print("\n===== DATASET SIZE =====")

    tables = ["raw_data", "intermediate_data", "features"]

    for table in tables:
        c.execute(f"SELECT COUNT(*) FROM {table}")
        count = c.fetchone()[0]

        print(f"{table}: {count} rows")


# Helper functions
def percentile(sorted_data, p):
    if not sorted_data:
        return None
    k = (len(sorted_data) - 1) * p
    f = int(k)
    c = min(f + 1, len(sorted_data) - 1)
    if f == c:
        return sorted_data[int(k)]
    return sorted_data[f] + (sorted_data[c] - sorted_data[f]) * (k - f)


def mean(data):
    return sum(data) / len(data) if data else None


def std_dev(data, avg):
    if not data or avg is None:
        return None
    return math.sqrt(sum((x - avg) ** 2 for x in data) / len(data))


# Numerical features
def analyze_numerical(c, feature):
    c.execute(f"SELECT {feature} FROM features")
    values = [row[0] for row in c.fetchall()]

    total = len(values)
    clean = [v for v in values if v is not None]

    missing = total - len(clean)
    miss_pct = (missing / total) * 100 if total else 0

    if not clean:
        return None

    clean.sort()

    avg = mean(clean)
    med = percentile(clean, 0.5)
    q1 = percentile(clean, 0.25)
    q3 = percentile(clean, 0.75)
    sd = std_dev(clean, avg)

    return {
        "count": total,
        "miss_pct": miss_pct,
        "cardinality": len(set(clean)),
        "min": clean[0],
        "Q1": q1,
        "mean": avg,
        "median": med,
        "Q3": q3,
        "max": clean[-1],
        "sd": sd
    }


# Categorical features
def analyze_categorical(c, feature):
    c.execute(f"SELECT {feature} FROM features")
    values = [row[0] for row in c.fetchall()]

    total = len(values)
    clean = [v for v in values if v is not None]

    missing = total - len(clean)
    miss_pct = (missing / total) * 100 if total else 0

    if not clean:
        return None

    freq = {}
    for v in clean:
        freq[v] = freq.get(v, 0) + 1

    sorted_freq = sorted(freq.items(), key=lambda x: x[1], reverse=True)

    mode, mode_freq = sorted_freq[0]
    mode_pct = (mode_freq / total) * 100

    if len(sorted_freq) > 1:
        mode2, mode2_freq = sorted_freq[1]
        mode2_pct = (mode2_freq / total) * 100
    else:
        mode2, mode2_freq, mode2_pct = None, 0, 0

    return {
        "count": total,
        "miss_pct": miss_pct,
        "cardinality": len(freq),
        "mode": mode,
        "mode_freq": mode_freq,
        "mode_pct": mode_pct,
        "mode2": mode2,
        "mode2_freq": mode2_freq,
        "mode2_pct": mode2_pct
    }


def report():
    conn = connect("")
    c = conn.cursor()

    print("\n=======================")
    print("     DATA REPORT")
    print("=======================")

    print_table_sizes(c)

    # Dataset size
    c.execute("SELECT COUNT(*) FROM features")
    total = c.fetchone()[0]

    print(f"\nTotal records: {total}")

    print("\n===== NUMERICAL FEATURES =====")
    numerical_features = [
        "lat",
        "lon",
        "distance_to_center",
        "tags_count",
        "description_length"
    ]

    for f in numerical_features:
        stats = analyze_numerical(c, f)
        if not stats:
            continue

        print(f"Feature: {f}")
        for k, v in stats.items():
            print(f"  {k}: {round(v, 3) if isinstance(v, float) else v}")

    print("\n===== CATEGORICAL FEATURES =====")
    categorical_features = [
        "category_encoded",
        "has_website",
        "has_wikipedia",
        "is_tourism_place",
        "has_phone"
    ]

    for f in categorical_features:
        stats = analyze_categorical(c, f)
        if not stats:
            continue

        print(f"Feature: {f}")
        for k, v in stats.items():
            print(f"  {k}: {round(v, 3) if isinstance(v, float) else v}")

    conn.close()


if __name__ == "__main__":
    report()