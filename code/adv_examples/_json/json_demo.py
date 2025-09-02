import json
from datetime import datetime
from canvasapi.requester import Requester

def demonstrate_json_dumps():
    """
    Demonstrates what json.dumps() can and cannot serialize
    """
    
    print("=== WHAT CAN BE SERIALIZED ===")
    
    # Basic data types that work
    examples = [
        ("String", "Hello World"),
        ("Integer", 42),
        ("Float", 3.14),
        ("Boolean", True),
        ("None", None),
        ("List", [1, 2, 3, "four"]),
        ("Dictionary", {"name": "John", "age": 30}),
        ("Nested", {"course": {"id": 123, "students": ["Alice", "Bob"]}})
    ]
    
    for name, value in examples:
        try:
            json_string = json.dumps(value)
            print(f"✅ {name}: {value} → {json_string}")
        except Exception as e:
            print(f"❌ {name}: Failed - {e}")
    
    print("\n=== WHAT CANNOT BE SERIALIZED ===")
    
    # Things that fail
    problematic_examples = [
        ("Function", print),
        ("Lambda", lambda x: x + 1),
        ("Datetime", datetime.now()),
        ("Set", {1, 2, 3}),
        ("Complex number", 3 + 4j),
        ("Class instance", Requester("http://example.com", "token"))
    ]
    
    for name, value in problematic_examples:
        try:
            json_string = json.dumps(value)
            print(f"✅ {name}: {value} → {json_string}")
        except Exception as e:
            print(f"❌ {name}: Failed - {type(e).__name__}: {e}")

if __name__ == "__main__":
    demonstrate_json_dumps()
