import argparse
import os
import numpy as np
import pandas as pd
import rasterio

def parse_arguments():
    parser = argparse.ArgumentParser(description="Generate synthetic laterite drillholes from DEM and Grid.")
    parser.add_argument("--dem", required=True, help="Path to DEM raster file (.tif)")
    parser.add_argument("--grid", required=True, help="Path to fishnet grid CSV file with Hole_ID, X, Y")
    parser.add_argument("--output", required=True, help="Output directory for generated CSVs")
    return parser.parse_args()

def main():
    args = parse_arguments()
    os.makedirs(args.output, exist_ok=True)
    
    print(f"[*] Reading grid file from: {args.grid}")
    grid_df = pd.read_csv(args.grid)
    
    collars, surveys, geology, assays = [], [], [], []
    
    print(f"[*] Processing spatial sampling from DEM and building database...")
    with rasterio.open(args.dem) as dem:
        for _, row_data in grid_df.iterrows():
            # Mengambil data langsung dari kolom CSV hasil QGIS
            hole_id = row_data['Hole_ID']
            x, y = row_data['X'], row_data['Y']
            
            # Ambil Elevasi Z dari Raster DEM
            try:
                row_idx, col_idx = dem.index(x, y)
                z_elevation = float(dem.read(1)[row_idx, col_idx])
            except Exception:
                z_elevation = 100.0 
            
            # Variasi total kedalaman lubang bor berdasarkan elevasi
            base_depth = np.random.uniform(15.0, 25.0) if z_elevation > 120 else np.random.uniform(8.0, 14.0)
            is_anomaly = np.random.random() < 0.15
            total_depth = round(base_depth * 0.6 if is_anomaly else base_depth, 2)
            
            # Sesuai target collar.csv: hole_id, y, x, z, max_depth
            collars.append({
                "hole_id": hole_id, 
                "y": y, 
                "x": x, 
                "z": round(z_elevation, 2), 
                "max_depth": total_depth
            })
            
            # Sesuai target survey.csv: hole_id, depth (disamakan dengan max_depth), dip, azimuth
            surveys.append({
                "hole_id": hole_id, 
                "depth": total_depth, 
                "dip": -90.0, 
                "azimuth": 0.0
            })
            
            # Logika Litologi Nikel Laterit (LIM -> SAP -> BRK)
            current_depth = 0.0
            lim_limit = total_depth * np.random.uniform(0.3, 0.5)
            sap_limit = total_depth * np.random.uniform(0.7, 0.9)
            
            sample_counter = 1
            
            while current_depth < total_depth:
                interval = 1.0 if np.random.random() > 0.25 else 0.5
                next_depth = min(current_depth + interval, total_depth)
                
                # Format penamaan samp_id otomatis (contoh: DH-001/01)
                samp_id = f"{hole_id}/{str(sample_counter).zfill(2)}"
                
                if next_depth <= lim_limit:
                    litho = "LIM"
                    ni = np.random.normal(1.0, 0.2)
                    co = np.random.normal(0.06, 0.01)
                    fe = np.random.normal(45.0, 3.0)
                    mgo = np.random.normal(1.5, 0.5)
                    sio2 = np.random.normal(6.0, 2.0)
                elif next_depth <= sap_limit:
                    litho = "SAP"
                    mean_ni = 1.1 if is_anomaly else 1.8
                    ni = np.random.normal(mean_ni, 0.3)
                    co = np.random.normal(0.02, 0.005)
                    fe = np.random.normal(16.0, 4.0)
                    mgo = np.random.normal(12.0, 3.0)
                    sio2 = np.random.normal(35.0, 5.0)
                else:
                    litho = "BRK"
                    ni = np.random.normal(0.2, 0.05)
                    co = np.random.normal(0.008, 0.002)
                    fe = np.random.normal(7.0, 1.5)
                    mgo = np.random.normal(36.0, 3.0)
                    sio2 = np.random.normal(42.0, 3.0)
                
                # Proteksi agar tidak bernilai minus
                ni = max(0.05, ni)
                co = max(0.001, co)
                fe = max(3.0, fe)
                mgo = max(0.1, mgo)
                sio2 = max(1.0, sio2)
                
                # Sesuai target geology.csv: hole_id, samp_id, depth_from, depth_to, lithology
                geology.append({
                    "hole_id": hole_id, 
                    "samp_id": samp_id,
                    "depth_from": round(current_depth, 1), 
                    "depth_to": round(next_depth, 1), 
                    "lithology": litho
                })
                
                # Sesuai target assay.csv: hole_id, samp_id, depth_from, depth_to, ni, co, fe, mgo, sio2
                assays.append({
                    "hole_id": hole_id, 
                    "samp_id": samp_id,
                    "depth_from": round(current_depth, 1), 
                    "depth_to": round(next_depth, 1), 
                    "ni": round(ni, 2), 
                    "co": round(co, 3), 
                    "fe": round(fe, 1),
                    "mgo": round(mgo, 2),
                    "sio2": round(sio2, 2)
                })
                
                current_depth = next_depth
                sample_counter += 1

    # Ekspor hasil ke format CSV dengan susunan kolom yang sudah diatur ketat
    pd.DataFrame(collars)[["hole_id", "y", "x", "z", "max_depth"]].to_csv(os.path.join(args.output, "collar.csv"), index=False)
    pd.DataFrame(surveys)[["hole_id", "depth", "dip", "azimuth"]].to_csv(os.path.join(args.output, "survey.csv"), index=False)
    pd.DataFrame(geology)[["hole_id", "samp_id", "depth_from", "depth_to", "lithology"]].to_csv(os.path.join(args.output, "geology.csv"), index=False)
    pd.DataFrame(assays)[["hole_id", "samp_id", "depth_from", "depth_to", "ni", "co", "fe", "mgo", "sio2"]].to_csv(os.path.join(args.output, "assay.csv"), index=False)
    
    print(f"[✔] Success! All database tables generated inside: {args.output}")

if __name__ == "__main__":
    main()
