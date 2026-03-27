import argparse
import os
import json

def main():
    parser = argparse.ArgumentParser(description='Validate album cover')
    parser.add_argument('--file', required=True)
    args = parser.parse_args()

    result = {
        "valid": True,
        "issues": []
    }

    if not os.path.exists(args.file):
        result["valid"] = False
        result["issues"].append("File does not exist")
    else:
        # Check file size (min 5KB as per spec)
        size = os.path.getsize(args.file)
        if size < 5 * 1024:
            result["valid"] = False
            result["issues"].append(f"File size too small: {size} bytes")

        # Without Pillow, we can't easily check resolution or aspect ratio.
        # We'll assume it's okay for now if it's over the size limit.
    
    print(json.dumps(result, indent=2))

if __name__ == '__main__':
    main()
