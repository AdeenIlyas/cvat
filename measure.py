import requests
import time
import sys

# Replace with the actual URL and credentials once server is up
URL = "http://localhost:8080/api/tasks/3/annotation_counts"
SESSION_URL = "http://localhost:8080/api/auth/login"

def measure():
    s = requests.Session()
    # Login
    res = s.post(SESSION_URL, json={"username": "admin", "password": "admin"})
    if res.status_code != 200:
        print("Login failed!", res.text)
        return

    times = []
    for i in range(5):
        start = time.time()
        r = s.get(URL)
        end = time.time()
        if r.status_code == 200:
            duration = (end - start) * 1000
            times.append(duration)
            print(f"Run {i+1}: {duration:.2f} ms")
        else:
            print(f"Run {i+1}: Failed with status {r.status_code}")
            times.append(0)
    
    with open('docs/MO-1_results.md', 'w') as f:
        f.write("# MO-1 Measurement Results\n\n")
        f.write("Target: < 200ms\n\n")
        if any(times):
            avg = sum(t for t in times if t > 0) / len([t for t in times if t > 0])
            for i, t in enumerate(times):
                f.write(f"- Run {i+1}: {t:.2f} ms\n")
            f.write(f"\n**Average**: {avg:.2f} ms\n")
            f.write("\n**Conclusion**: " + ("Target met." if avg < 200 else "Target missed. Needs optimization.") + "\n")
            print(f"\nAverage: {avg:.2f} ms")
        else:
            f.write("All requests failed.\n")

if __name__ == "__main__":
    measure()
