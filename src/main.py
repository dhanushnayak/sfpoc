from datetime import datetime, timedelta

# Get the current time
current_time = datetime.now()

# Add 15 minutes to the current time
new_time = current_time + timedelta(minutes=15)

# Format the new time as a string (optional)
formatted_time = new_time.strftime("%Y-%m-%d %H:%M:%S")

print(f"Current Time: {current_time}")
print(f"New Time (After adding 15 minutes): {formatted_time}")
