import requests
import os

image = "backend"

a = requests.get(f"https://registry.proqa.gg.ax/v2/{image}/tags/list")
for tag in a.json()["tags"]:
    print(f"Deleting registry.proqa.gg.ax/{image}:{tag}")
    os.system(f"skopeo delete docker://registry.proqa.gg.ax/{image}:{tag}")
