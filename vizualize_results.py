import json
import matplotlib.pyplot as plt
from collections import Counter
from pathlib import Path


def load_results(json_path: str):
    """Load the JSON file created by main.py"""
    path = Path(json_path)
    if not path.exists():
        raise FileNotFoundError(f"{json_path} not found.")
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def summarize_duplicates(results):
    """Count duplicate occurrences per file"""
    counter = Counter()
    for r in results:
        counter[r["a_file"]] += 1
        counter[r["b_file"]] += 1
    return counter


def plot_summary(counter):
    """Create a bar chart for duplicate counts"""
    if not counter:
        print("No data to visualize.")
        return

    files = list(counter.keys())
    counts = [counter[f] for f in files]

    plt.figure(figsize=(10, 5))
    bars = plt.barh(files, counts)
    plt.xlabel("Duplicate Occurrences")
    plt.ylabel("File Path")
    plt.title("Duplicate Function Occurrences by File")
    plt.grid(axis="x", linestyle="--", alpha=0.7)

    # Add labels on bars
    for bar, val in zip(bars, counts):
        plt.text(val + 0.1, bar.get_y() + bar.get_height() / 2, str(val), va="center")

    plt.tight_layout()
    plt.show()


def main():
    json_path = "duplicate_results.json"
    results = load_results(json_path)
    counter = summarize_duplicates(results)
    plot_summary(counter)


if __name__ == "__main__":
    main()
