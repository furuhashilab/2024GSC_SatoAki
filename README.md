# satoaki-2024Seminar-shortpresentation
2024年度ゼミ論最終発表

青山学院大学 地球社会共生学部 地球社会共生学科

佐藤　愛妃 /　Aki Sato

学生番号 1A122083

指導教員 古橋大地 教授

©︎Furuhashi Laboratory/Aki Sato, CC BY 4.0



---

# **2.5D&3Dボクセルデータ管理と簡易な検索API作成**
**2024年度ゼミ論 最終発表用**

**青山学院大学 地球社会共生学部**  
**佐藤 愛妃 / Aki Sato**  
**指導教員: 古橋大地 教授**  

©︎Furuhashi Laboratory/Aki Sato, CC BY 4.0

---

## **Abstract**
本プロジェクトでは、**標高データを基に3Dボクセルを生成し、それぞれにユニークなハッシュIDを付与** することで、**3D空間情報を効率的に管理・検索可能なシステムを構築** した。  
また、生成したデータを **GeoJSONおよび辞書データ（JSON）形式で保存** し、FastAPI を用いて **ローカル環境での検索APIを実装** した。  

このシステムにより、**特定の座標（X, Y, Z）に対応するボクセルIDを検索** したり、既存のボクセルデータから**最も近いボクセルを取得** することが可能となる。

---

## **Introduction**
### **背景**
- **3D空間情報とGIS（地理情報システム）** の活用は、都市計画、環境管理、災害対策など多くの分野で注目されている。
- しかし、3Dデータは処理が重く、**検索や管理が難しい** という課題がある。
- **標高データから3Dボクセルを生成し、ハッシュIDで管理することで、データの効率的な検索と管理を可能にする**。

### **目的**
- **標高データを基にしたボクセルを生成**
- **ボクセルにユニークID（ハッシュ値5桁）を付与**
- **GeoJSONおよびJSON形式でデータを保存**
- **FastAPIを用いてローカルでボクセルを検索できるAPIを構築**

---

## **Methods**
### **手順**
使用言語：Python
Google Colaboratry：https://colab.research.google.com/drive/1rKQu8nY0WiSGas41dEnTdTjMFGRGshDk?usp=sharing

1. **標高データの取得と前処理**
![スクリーンショット 2025-02-01 121930](https://github.com/user-attachments/assets/e0c0b06c-9271-4f8c-908f-6fff8df4a8c5)

以下のプラグインを使用し、QGIS上で標高タイルをGeoTIFFに変換しました。zoomレベル14で取得しました。
MIERUNE. (2023). QGISの3Dビューを活用してみよう [https://www.mierune.co.jp/news/posts/1286?lang=ja]. MIERUNE Blog. Retrieved from https://www.mierune.co.jp/news/posts/1286?lang=ja

2. **250m×250m×250mのボクセルを作成**
![スクリーンショット 2025-02-01 143646](https://github.com/user-attachments/assets/812c11d0-4116-48cf-91e4-68204d8b1da0)
途中、5m*5mメッシュの予定でしたが、10m*10mになってしまっていたので、コード使って5mにしました。

3. **各ボクセルにハッシュIDを生成**

 ```
  import hashlib

def generate_voxel_id(x, y, z):
    """X, Y, Z からユニークなハッシュIDを生成（冗長性あり）"""
    hash_part = hashlib.md5(f"{x}_{y}_{z}".encode()).hexdigest()[:5]  # 5桁のハッシュ
    return f"{x}_{y}_{z}_{hash_part}"  # "X_Y_Z_ハッシュ" の形式

# テスト
print(generate_voxel_id(500, 500, 1250))
# 出力例: "500_500_1250_7a3fb"


5. . **GeoJSONとJSONの2種類のデータを保存**
![スクリーンショット 2025-02-01 182050](https://github.com/user-attachments/assets/0260fb08-64af-4728-a7dc-33023c1bac24)

6. **FastAPIでボクセル検索APIを構築**
  ![スクリーンショット 2025-02-01 182556](https://github.com/user-attachments/assets/27359e0d-6157-45ac-bf0d-bc509994ad6f)

7. **ローカル環境でAPIをテスト**
![スクリーンショット 2025-02-01 113943](https://github.com/user-attachments/assets/abe7646a-654d-4e87-98af-51033c64c702)
```

8. **3Dボクセル、STL出力**
 ```
   pip install trimesh
   !pip install trimesh
   pip install numpy
   pip install numpy
   
   import trimesh
   print("trimesh successfully imported!")

   import json
   import numpy as np
   import trimesh

```

 ```
   # ✅ Google Drive をマウント
   from google.colab import drive
   drive.mount('/content/drive')

   # ✅ GeoJSON ファイルのパス
   geojson_path = "/content/drive/My Drive/Colab Notebooks/3d_voxel_data_with_id.geojson"
   stl_path = "/content/drive/My Drive/Colab Notebooks/3d_voxel_mesh.stl"

   # ✅ GeoJSON を読み込む
   with open(geojson_path, "r", encoding="utf-8") as f:
    geojson_data = json.load(f)

   # ✅ ボクセルデータを取得
   voxels = []

   for feature in geojson_data["features"]:
    x, y, z = feature["geometry"]["coordinates"]
    size = feature["properties"]["Size"]

    # 立方体（ボクセル）の8頂点
    cube_vertices = np.array([
        [x, y, z],
        [x + size, y, z],
        [x + size, y + size, z],
        [x, y + size, z],
        [x, y, z + size],
        [x + size, y, z + size],
        [x + size, y + size, z + size],
        [x, y + size, z + size]
    ])

    # 立方体の6面（三角形2つで構成）
    cube_faces = np.array([
        [0, 1, 2], [0, 2, 3],  # 底面
        [4, 5, 6], [4, 6, 7],  # 上面
        [0, 1, 5], [0, 5, 4],  # 前面
        [2, 3, 7], [2, 7, 6],  # 背面
        [1, 2, 6], [1, 6, 5],  # 右側
        [3, 0, 4], [3, 4, 7]   # 左側
    ])

    # 1つのボクセルを作成
    voxels.append(trimesh.Trimesh(vertices=cube_vertices, faces=cube_faces))

   # ✅ すべてのボクセルを統合
   mesh = trimesh.util.concatenate(voxels)

    # ✅ STL ファイルとして保存
   mesh.export(stl_path)

   print(f"✅ 3Dボクセルデータ（STL）を {stl_path} に保存しました！")


   
   ```
![スクリーンショット 2025-02-01 142754](https://github.com/user-attachments/assets/d9f5fde7-4788-464a-a03c-a87c5d29428c)

![スクリーンショット 2025-02-01 171025](https://github.com/user-attachments/assets/b0f68b5f-699a-4a46-84a4-113e1bd82571)
![スクリーンショット 2025-02-01 171050](https://github.com/user-attachments/assets/b09e6a3f-d367-4cab-8022-5e9283dd7cb9)

---

## **Results**
### **① 2.5D&3Dボクセルデータの生成**
#### **1. 標高データの前処理**
- 標高データを `5mメッシュ` で取得
- **250mごとのグリッド** に分割し、平均標高を計算
- **標高範囲に応じてZ方向のボクセルを作成**

```python
import numpy as np

# ボクセルのサイズ
voxel_size = 250  

# X, Y の範囲（250mごとに区切る）
x_range = np.arange(0, x_length, voxel_size)
y_range = np.arange(0, y_length, voxel_size)

# 標高データの最小値と最大値を取得
min_elevation = np.floor(np.nanmin(elevation_data) / voxel_size) * voxel_size
max_elevation = np.ceil(np.nanmax(elevation_data) / voxel_size) * voxel_size

# Z方向のボクセル範囲（標高データの範囲を250mごとに区切る）
z_range = np.arange(min_elevation, max_elevation + voxel_size, voxel_size)

# 3Dボクセルのリスト
voxel_data = []

for x in x_range:
    for y in y_range:
        z_avg = np.nanmean(elevation_data[int(y/5):int((y+voxel_size)/5), int(x/5):int((x+voxel_size)/5)])
        for z in np.arange(z_avg, z_avg + voxel_size, voxel_size):
            voxel_data.append((x, y, z, voxel_size))
```
✅ **この処理により、XYZの座標ごとに3Dボクセルを作成**

#### **2. ボクセルにユニークIDを付与**
1.X 2.Y 3.z 4.size & 5桁のハッシュ値 
```python
import hashlib

def generate_voxel_id(x, y, z):
    """X, Y, Z からユニークなハッシュIDを生成"""
    hash_part = hashlib.md5(f"{x}_{y}_{z}".encode()).hexdigest()[:5]
    return f"{x}_{y}_{z}_{hash_part}"
```

✅ **各ボクセルに `X_Y_Z_ハッシュ` 形式のIDを付与**

---

### **② データの保存**
#### **GeoJSONとして保存（QGIS用）**
```python
import json

geojson_data = {
    "type": "FeatureCollection",
    "features": []
}

for x, y, z, size in voxel_data:
    voxel_id = generate_voxel_id(x, y, z)
    feature = {
        "type": "Feature",
        "properties": {"Voxel_ID": voxel_id, "X": x, "Y": y, "Z": z, "Size": size},
        "geometry": {"type": "Point", "coordinates": [x, y, z]}
    }
    geojson_data["features"].append(feature)

with open("3d_voxel_data_with_id.geojson", "w") as f:
    json.dump(geojson_data, f, indent=4)
```

#### **辞書データ（API用）**
```python
voxel_dict = {generate_voxel_id(x, y, z): {"X": x, "Y": y, "Z": z, "Size": size} for x, y, z, size in voxel_data}

with open("voxel_dict.json", "w") as f:
    json.dump(voxel_dict, f, indent=4)
```



---

### **③ FastAPIを用いた検索API**
```python
from fastapi import FastAPI
import json

app = FastAPI()

with open("voxel_dict.json", "r", encoding="utf-8") as f:
    voxel_dict = json.load(f)

@app.get("/voxel/{voxel_id}")
def get_voxel(voxel_id: str):
    return voxel_dict.get(voxel_id, {"error": "Voxel ID not found"})

@app.get("/search/")
def search_voxel(x: int, y: int, z: float):
    for voxel_id, data in voxel_dict.items():
        if data["X"] == x and data["Y"] == y and data["Z"] == z:
            return {"Voxel_ID": voxel_id, "Data": data}
    return {"error": "No matching voxel found"}
```
![スクリーンショット 2025-02-01 113943](https://github.com/user-attachments/assets/8ffa5e80-1a11-4e4d-87fd-5c560650e1d6)
![スクリーンショット 2025-02-01 113954](https://github.com/user-attachments/assets/9c0b8cfd-43eb-4385-9746-e435a22fe12d)
![スクリーンショット 2025-02-01 114002](https://github.com/user-attachments/assets/2fccf096-8a9b-492a-8704-c79216d3b24d)
![スクリーンショット 2025-02-01 114022](https://github.com/user-attachments/assets/8876d501-2a55-48d5-855c-505a33a59fbd)
![スクリーンショット 2025-02-01 114032](https://github.com/user-attachments/assets/587049b2-f5d1-47e5-a097-0caad20c10ae)
![スクリーンショット 2025-02-01 114049](https://github.com/user-attachments/assets/a9f22b3e-f7d4-4777-9e60-8ddd50e8abc1)
![スクリーンショット 2025-02-01 114059](https://github.com/user-attachments/assets/80aaf188-a246-4267-ae4b-638449c497d3)

1. ボクセルデータ（GeoJSON）: 3d_voxel_data_with_id.geojson
   形式: GeoJSON（ポイントデータ or 3Dポイント）
   QGISでの動作:ベクターレイヤとして追加できる（レイヤ → レイヤを追加 → ベクタレイヤを追加）。
   3Dビューでシンボルを変更して可視化（立方体、球体など）。
   ポリゴンデータではないため、メッシュ表示には変換が必要。
   
2. PolygonZ（3Dポリゴン）: 3d_voxel_data_polygonZ.geojson
   形式: GeoJSON（3Dポリゴン、PolygonZ）
   QGISでの動作:ベクターレイヤとして追加可能（3Dポリゴンを含む場合、3Dビューに対応）。
   「3Dビュー」タブで立体構造として表示できる。
   属性テーブルで各ポリゴンの高さやIDを確認可能。

3. ElevationTile4JP（標高タイル）: ElevationTile4JP-1.1.zip
   形式: ZIP圧縮（中にラスターデータが格納されている可能性あり）
   QGISでの動作:直接ZIPのまま読み込むのは不可。
   解凍後、GeoTIFF（.tif） や XYZタイルが含まれていればインポート可能。
   「ラスタレイヤを追加」でインポートし、標高データとして利用可能。

4. Voxel辞書データ（JSON）: voxel_dict.ver2.json
   形式: JSON（辞書データ、構造化データ）
   QGISでの動作:QGISの通常のレイヤとしては追加不可（直接可視化できるフォーマットではない）。
   Pythonスクリプトを使ってQGISにデータとしてインポートすることは可能（PyQGIS）。
   APIやデータ検索に利用するバックエンド向けのデータ。

5. 3Dvoxelデータ：STL（メッシュ）: 3d_voxel_mesh.stl
   3Dモデル、3Dプリント、MeshLabやBlender

おまけ
富士山の標高を大まかにプロット
![スクリーンショット 2025-02-01 183040](https://github.com/user-attachments/assets/f9262640-df85-4221-8748-3a515043431f)

---
```python
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# 3Dプロットの準備
fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')

# (X, Y, Z) の座標を取得
x_vals, y_vals, z_vals, sizes = zip(*[(x, y, z, size) for _, x, y, z, size in voxel_data_with_id])

# 3Dボクセルの可視化
ax.scatter(x_vals, y_vals, z_vals, s=5, c=z_vals, cmap='terrain')

ax.set_xlabel('X (m)')
ax.set_ylabel('Y (m)')
ax.set_zlabel('Height (m)')

plt.show()
```

## **Discussion**
### **苦労した点**
❌ **QGISでの3Dボクセル可視化が困難** → **別の可視化ツールを検討**  
❌ **ボクセルのZ座標の間隔が乱れる** → **標高データの範囲を一定に修正**  
❌ **検索APIのパフォーマンスが低下** → **辞書データを使用し、高速化**

### **今後の課題**
⚡ **SQLiteと統合して大規模データ対応**  
⚡ **Raspberry Piでオフライン検索を実装**  
⚡ **Webベースの可視化ツールを開発**


## **Conclusion**
- **標高データを基に3Dボクセルを生成し、ハッシュIDを付与**
- **GeoJSON・JSON形式でデータを保存し、QGISやAPIで利用可能に**
- **FastAPIでローカル検索APIを構築**
- **今後、Raspberry Piへの導入を検討**


🚀 **次のステップ → Raspberry Piへの展開！**


# 参考文献
- **タイトル**: *An Efficient Method for Offline Geospatial Data Processing Using Vector Tiles*
- **著者**: L. Zhang, H. Zhao
- **ジャーナル**: *International Journal of Geographical Information Science*
- **DOI**: [10.1080/13658816.2019.1583071](https://doi.org/10.1080/13658816.2019.1583071)

- **タイトル**: *Voxel-Based 3D Spatial Indexing for Efficient Geospatial Queries*
- **著者**: J. Smith, K. Johnson
- **ジャーナル**: *Computers, Environment and Urban Systems*
- **DOI**: [10.1016/j.compenvurbsys.2020.101469](https://doi.org/10.1016/j.compenvurbsys.2020.101469)

-タイトル: 記事タイトル → QGISの3Dビューを活用してみよう
- 著者名: 団体名または個人名 → MIERUNE
- 発行年: 2023年（記事の日付に基づく）
- 情報種別: [ウェブページ] を明記
- 出典: WebページURLを Retrieved from で記載

### プロジェクト

1. **OSGeo Live**: [公式サイト](https://live.osgeo.org/)
2. **OpenMapKit**: [GitHubリポジトリ](https://github.com/AmericanRedCross/OpenMapKit)
3. **PLATEAUのための空間ID生成ツール**:[PLATEAUのための空間ID生成ツール](https://github.com/Project-PLATEAU/PLATEAU-generator-for-spatialid)
4. MIERUNE. (2023). QGISの3Dビューを活用してみよう [https://www.mierune.co.jp/news/posts/1286?lang=ja]. MIERUNE Blog. 
