import subprocess

result = subprocess.run(
    "cut -f1 -d, sample.csv | head -n5", shell=True, capture_output=True, text=True
)

print(result.stdout)
