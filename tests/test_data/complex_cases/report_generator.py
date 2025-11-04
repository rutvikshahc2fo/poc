def generate_report(data):
    total = 0
    for record in data:
        total += record.get("amount", 0)
    avg = total / len(data) if data else 0
    return {"total": total, "average": avg}


def summarize_numbers(values):
    count = len(values)
    return {"sum": sum(values), "count": count}