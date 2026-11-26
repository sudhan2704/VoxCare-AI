
from app.services.local_analysis import analyze_call


sample_transcript = """
Customer called to check the status of a medical appointment.
The agent verified the details and explained the next steps.
The customer thanked the agent for the helpful support.
"""

result = analyze_call(sample_transcript)

print("\nVOXCARE AI - LOCAL ANALYSIS")
print("---------------------------")

for key, value in result.items():
    print(f"{key}: {value}")
