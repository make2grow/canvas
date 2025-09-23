## 13. Example Script

This example shows how to create weekly assignments automatically.

```python
#!/usr/bin/env python3
from canvasapi import Canvas
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta

def setup_course():
    load_dotenv()
    canvas = Canvas(os.getenv("CANVAS_API_URL"), os.getenv("CANVAS_API_TOKEN"))
    course = canvas.get_course(os.getenv("COURSE_ID"))
    
    # Create weekly assignments
    for week in range(1, 13):
        due_date = datetime.now() + timedelta(weeks=week)
        create_homework(
            course=course,
            title=f"Week {week} Assignment",
            description=f"<p>Complete Week {week} exercises</p>",
            due_date=due_date.strftime("%Y-%m-%dT23:59:59Z"),
            points=100
        )
    
    print("✅ Course setup complete!")
```

---

---

## 15. Useful Resources

### 📚 Documentation

- [Canvas API Documentation](https://canvas.instructure.com/doc/api/)
- [canvasapi Python Library](https://canvasapi.readthedocs.io/)

### 🛠️ Tools

- **Postman** for API testing
- **Canvas API Explorer** (in Canvas settings)
- **Jupyter Notebooks** for experimentation

---

### 💡 Ideas for Advanced Use

- Grade analytics and visualization
- Automated feedback generation
- Integration with external grading tools
- Student progress tracking dashboards

---

## Questions & Discussion

### What would you like to automate in your courses?

- Bulk assignment creation?
- Automated grading workflows?
- Student progress tracking?
- Content management?

**Let's explore specific use cases together!**