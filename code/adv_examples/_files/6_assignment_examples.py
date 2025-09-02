"""
Educational Examples: Different Ways to Filter Canvas Assignments
This file shows various approaches to filter and categorize assignments for learning purposes.
"""

from dotenv import load_dotenv
from canvasapi import Canvas
import os
from datetime import datetime, timedelta

def get_canvas_instance():
    """Check if .env file exists and has required variables"""
    if not os.path.exists('.env'):
        print("❌ .env file not found!")
        print("   Please copy .env.template to .env and fill in your details")
        return
    
    load_dotenv()
    
    required_vars = ['API_KEY', 'API_URL']
    missing_vars = []
    
    for var in required_vars:
        value = os.getenv(var)
        if not value:
            missing_vars.append(var)
    
    if missing_vars:
        print("❌ Missing or placeholder values in .env file:")
        for var in missing_vars:
            print(f"   - {var}")
        return
    
    return Canvas(
        os.getenv("API_URL"), 
        os.getenv("API_KEY")
    )

# Change this course number to yours
course_number = 62413

def example_1_basic_filtering():
    """
    Example 1: Basic assignment filtering
    Shows how to filter by submission type and publication status
    """
    print("\n📚 EXAMPLE 1: Basic Filtering")
    print("-" * 40)

    canvas = get_canvas_instance()
    course = canvas.get_course(course_number)
    assignments = course.get_assignments()
    
    for assignment in assignments:
        # Filter: Only published assignments with submissions
        if assignment.published and hasattr(assignment, 'submission_types'):
            submission_types = assignment.submission_types
            if submission_types and 'none' not in submission_types:
                print(f"✅ {assignment.name} - {submission_types}")

def example_2_date_filtering():
    """
    Example 2: Filter assignments by due date
    Shows assignments due in the next 7 days
    """
    print("\n📅 EXAMPLE 2: Date-based Filtering")
    print("-" * 40)
    
    canvas = get_canvas_instance()
    course = canvas.get_course(course_number)
    assignments = course.get_assignments()
    
    now = datetime.now()
    next_week = now + timedelta(days=7)
    
    for assignment in assignments:
        if assignment.due_at:
            # Input: "2025-08-20T15:30:00Z"
	        # Converted: "2025-08-20T15:30:00+00:00"
            due_date = datetime.fromisoformat(assignment.due_at.replace('Z', '+00:00'))
            # datetime.datetime(2025, 8, 20, 15, 30, tzinfo=datetime.timezone.utc)
            # Remove timezone info for comparison
            # datetime.datetime(2025, 8, 20, 15, 30)
            due_date = due_date.replace(tzinfo=None)
            
            if now <= due_date <= next_week:
                print(f"⏰ {assignment.name} - Due: {due_date.strftime('%Y-%m-%d %H:%M')}")

def example_3_points_categorization():
    """
    Example 3: Categorize assignments by point value
    Shows how to group assignments by their worth
    """
    print("\n💯 EXAMPLE 3: Points-based Categorization")
    print("-" * 40)
    
    canvas = get_canvas_instance()
    course = canvas.get_course(course_number)
    assignments = course.get_assignments()
    
    major_assignments = []  # > 50 points
    regular_assignments = []  # 10-50 points
    minor_assignments = []  # < 10 points
    
    for assignment in assignments:
        if assignment.published:
            points = assignment.points_possible or 0
            
            if points > 50:
                major_assignments.append((assignment.name, points))
            elif points >= 10:
                regular_assignments.append((assignment.name, points))
            elif points > 0:
                minor_assignments.append((assignment.name, points))
    
    print("🏆 Major Assignments (>50 points):")
    for name, points in major_assignments:
        print(f"   • {name}: {points} points")
    
    print("\n📝 Regular Assignments (10-50 points):")
    for name, points in regular_assignments:
        print(f"   • {name}: {points} points")
    
    print("\n✏️  Minor Assignments (<10 points):")
    for name, points in minor_assignments:
        print(f"   • {name}: {points} points")

def example_4_submission_type_analysis():
    """
    Example 4: Analyze assignments by submission type
    Educational example showing different submission methods
    """
    print("\n📤 EXAMPLE 4: Submission Type Analysis")
    print("-" * 40)
    
    canvas = get_canvas_instance()
    course = canvas.get_course(course_number)
    assignments = course.get_assignments()
    
    submission_counts = {}
    
    for assignment in assignments:
        if assignment.published and hasattr(assignment, 'submission_types'):
            for sub_type in assignment.submission_types:
                if sub_type not in submission_counts:
                    submission_counts[sub_type] = []
                submission_counts[sub_type].append(assignment.name)
    
    for sub_type, assignments_list in submission_counts.items():
        print(f"\n📋 {sub_type.upper()} submissions ({len(assignments_list)}):")
        for assignment_name in assignments_list[:3]:  # Show first 3
            print(f"   • {assignment_name}")
        if len(assignments_list) > 3:
            print(f"   ... and {len(assignments_list) - 3} more")

def example_5_overdue_assignments():
    """
    Example 5: Find overdue assignments
    Useful for tracking late submissions
    """
    print("\n⚠️  EXAMPLE 5: Overdue Assignment Check")
    print("-" * 40)
    
    canvas = get_canvas_instance()
    course = canvas.get_course(course_number)
    assignments = course.get_assignments()
    
    now = datetime.now()
    overdue_count = 0
    
    for assignment in assignments:
        if assignment.due_at and assignment.published:
            due_date = datetime.fromisoformat(assignment.due_at.replace('Z', '+00:00'))
            due_date = due_date.replace(tzinfo=None)
            
            if due_date < now:
                overdue_count += 1
                days_overdue = (now - due_date).days
                print(f"🔴 {assignment.name} - {days_overdue} days overdue")
    
    if overdue_count == 0:
        print("✅ No overdue assignments found!")
    else:
        print(f"\n📊 Total overdue assignments: {overdue_count}")

def main():
    """
    Run all examples to demonstrate different filtering approaches
    """
    print("🎓 Canvas Assignment Filtering Examples")
    print("=" * 50)
    
    try:
        example_1_basic_filtering()
        example_2_date_filtering()
        example_3_points_categorization()
        example_4_submission_type_analysis()
        example_5_overdue_assignments()
        
        print("\n" + "=" * 50)
        print("✅ All examples completed successfully!")
        
    except Exception as e:
        print(f"❌ Error running examples: {e}")

if __name__ == "__main__":
    main()
