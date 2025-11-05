import argparse
from agent.duplicate_detector import DuplicateDetector
from pathlib import Path
import json


def main():
    parser = argparse.ArgumentParser(description="Simple code duplication detector")
    parser.add_argument("--path", required=True, help="Path to scan for .py files")
    parser.add_argument("--threshold", type=float, default=0.9, help="Similarity threshold (0-1)")
    parser.add_argument("--topk", type=int, default=5, help="Top-k neighbors to check for each snippet")
    parser.add_argument("--output", default="duplicate_results.json", help="Path to save JSON output")
    args = parser.parse_args()

    detector = DuplicateDetector(threshold=args.threshold, top_k=args.topk)
    results = detector.run(args.path)

    if results:
        print("\nDetected duplicates:\n")
        for r in results:
            print(f"Score: {r['score']:.4f} | {r['a_file']}:{r['a_name']} <=> {r['b_file']}:{r['b_name']}")

        # Save results to JSON
        output_path = Path(args.output)
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(results, f, indent=4, ensure_ascii=False)
        print(f"\n✅ Results saved to {output_path.resolve()}\n")

    else:
        print("No duplicates found.")


if __name__ == "__main__":
    main()
