from fastapi import FastAPI
import json

# FastAPI アプリケーションの作成
app = FastAPI()

# Voxelデータの読み込み
json_path = "voxel_dict.ver2.json"  # voxel_dict.ver2.json のパスを確認
with open(json_path, "r", encoding="utf-8") as f:
    voxel_dict = json.load(f)

# Voxel ID で検索
@app.get("/voxel/{voxel_id}")
def get_voxel(voxel_id: str):
    return voxel_dict.get(voxel_id, {"error": "Voxel ID not found"})

# X, Y, Z で検索（完全一致）
@app.get("/search/")
def search_voxel(x: int, y: int, z: float):
    for voxel_id, data in voxel_dict.items():
        if data["X"] == x and data["Y"] == y and data["Z"] == z:
            return {"Voxel_ID": voxel_id, "Data": data}
    return {"error": "No matching voxel found"}

# X, Y, Z に最も近い Voxel を検索
@app.get("/nearest/")
def find_nearest_voxel(x: int, y: int, z: float, tolerance=250):
    closest_voxel = None
    min_distance = float("inf")

    for voxel_id, data in voxel_dict.items():
        dist = abs(data["X"] - x) + abs(data["Y"] - y) + abs(data["Z"] - z)
        if dist < min_distance and dist <= tolerance:
            min_distance = dist
            closest_voxel = voxel_id

    return {"Voxel_ID": closest_voxel} if closest_voxel else {"error": "No nearby voxel found"}
