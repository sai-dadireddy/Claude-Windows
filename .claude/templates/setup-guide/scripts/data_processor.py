#!/usr/bin/env -S uv run --quiet --script
# /// script
# requires-python = ">=3.10"
# dependencies = ["pandas", "numpy"]
# ///
"""
Data Processor - Heavy data operations offloaded from Claude's context

Usage: data_processor.py <operation> <input_file> [options]

Operations:
- stats: Basic statistics (mean, std, min, max, count)
- describe: Full statistical description
- head: First N rows
- tail: Last N rows
- filter: Filter by condition
- aggregate: Group by and aggregate

Output: Compact JSON summary (not full data)
"""

import json
import sys
import os

def load_data(file_path: str):
    """Load data from CSV, JSON, or JSONL"""
    import pandas as pd

    ext = os.path.splitext(file_path)[1].lower()

    if ext == '.csv':
        return pd.read_csv(file_path)
    elif ext == '.json':
        return pd.read_json(file_path)
    elif ext == '.jsonl':
        return pd.read_json(file_path, lines=True)
    else:
        raise ValueError(f"Unsupported file format: {ext}")

def stats(df, column=None):
    """Get basic statistics"""
    import numpy as np

    if column and column in df.columns:
        data = df[column].dropna()
        if data.dtype in ['int64', 'float64']:
            return {
                "column": column,
                "count": int(len(data)),
                "mean": float(np.mean(data)),
                "std": float(np.std(data)),
                "min": float(np.min(data)),
                "max": float(np.max(data)),
                "median": float(np.median(data))
            }
        else:
            return {
                "column": column,
                "count": int(len(data)),
                "unique": int(data.nunique()),
                "top": str(data.mode().iloc[0]) if len(data.mode()) > 0 else None
            }
    else:
        # All numeric columns
        numeric_cols = df.select_dtypes(include=['int64', 'float64']).columns
        return {
            "rows": int(len(df)),
            "columns": int(len(df.columns)),
            "numeric_columns": list(numeric_cols),
            "stats": {col: stats(df, col) for col in numeric_cols[:5]}  # Limit to 5
        }

def describe(df, column=None):
    """Full statistical description"""
    if column and column in df.columns:
        desc = df[column].describe()
    else:
        desc = df.describe()

    return json.loads(desc.to_json())

def head(df, n=5):
    """First N rows as records"""
    return {
        "rows": int(len(df)),
        "showing": min(n, len(df)),
        "data": json.loads(df.head(n).to_json(orient='records'))
    }

def tail(df, n=5):
    """Last N rows as records"""
    return {
        "rows": int(len(df)),
        "showing": min(n, len(df)),
        "data": json.loads(df.tail(n).to_json(orient='records'))
    }

def filter_data(df, condition: str):
    """Filter data by condition (e.g., 'column > 5')"""
    try:
        filtered = df.query(condition)
        return {
            "original_rows": int(len(df)),
            "filtered_rows": int(len(filtered)),
            "condition": condition,
            "sample": json.loads(filtered.head(5).to_json(orient='records'))
        }
    except Exception as e:
        return {"error": str(e), "condition": condition}

def aggregate(df, group_by: str, agg_col: str, agg_func: str = 'mean'):
    """Group by and aggregate"""
    import numpy as np

    agg_funcs = {
        'mean': np.mean,
        'sum': np.sum,
        'count': len,
        'min': np.min,
        'max': np.max,
        'std': np.std
    }

    if agg_func not in agg_funcs:
        return {"error": f"Unknown aggregation: {agg_func}"}

    try:
        result = df.groupby(group_by)[agg_col].agg(agg_funcs[agg_func]).reset_index()
        return {
            "group_by": group_by,
            "aggregation": f"{agg_func}({agg_col})",
            "groups": int(len(result)),
            "data": json.loads(result.to_json(orient='records'))
        }
    except Exception as e:
        return {"error": str(e)}

def main():
    if len(sys.argv) < 3:
        print(json.dumps({
            "error": "Usage: data_processor.py <operation> <file> [options]",
            "operations": ["stats", "describe", "head", "tail", "filter", "aggregate"]
        }))
        sys.exit(1)

    operation = sys.argv[1]
    file_path = sys.argv[2]
    args = sys.argv[3:] if len(sys.argv) > 3 else []

    try:
        df = load_data(file_path)

        if operation == "stats":
            column = args[0] if args else None
            result = stats(df, column)
        elif operation == "describe":
            column = args[0] if args else None
            result = describe(df, column)
        elif operation == "head":
            n = int(args[0]) if args else 5
            result = head(df, n)
        elif operation == "tail":
            n = int(args[0]) if args else 5
            result = tail(df, n)
        elif operation == "filter":
            condition = args[0] if args else ""
            result = filter_data(df, condition)
        elif operation == "aggregate":
            if len(args) < 2:
                result = {"error": "aggregate requires: group_by agg_col [agg_func]"}
            else:
                group_by, agg_col = args[0], args[1]
                agg_func = args[2] if len(args) > 2 else 'mean'
                result = aggregate(df, group_by, agg_col, agg_func)
        else:
            result = {"error": f"Unknown operation: {operation}"}

        print(json.dumps(result, indent=2))

    except Exception as e:
        print(json.dumps({"error": str(e), "file": file_path}))
        sys.exit(1)

if __name__ == "__main__":
    main()
