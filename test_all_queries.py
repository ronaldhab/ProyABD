import warnings
warnings.filterwarnings('ignore', category=UserWarning)

from app.queries.r01_tablas_indices import get_tablas_y_indices
from app.queries.r02_conteo import get_conteo_tablas_indices
from app.queries.r03_restricciones import get_restricciones
from app.queries.r04_detalle_indices import get_detalle_indices
from app.queries.r05_triggers import get_triggers
from app.queries.r06_tamano_tablas import get_tamano_tablas
from app.queries.r07_tamano_registro import get_tamano_registro_por_tabla
from app.queries.r08_tamano_columnas import get_tamano_columnas
from app.queries.r09_factor_bloqueo import get_factor_bloqueo
from app.queries.r10_costo_consulta import get_tables_and_columns, estimate_query_cost

def run_test():
    print("--- TESTING ALL QUERY FUNCTIONS ---")
    try:
        df_tablas, df_indices = get_tablas_y_indices()
        print(f"R1: Tablas={df_tablas.shape}, Indices={df_indices.shape}")
        
        total, df_c = get_conteo_tablas_indices()
        print(f"R2: Total={total}, Conteo={df_c.shape}")
        
        df_r = get_restricciones()
        print(f"R3: Restricciones={df_r.shape}")
        
        df_d = get_detalle_indices()
        print(f"R4: Detalles={df_d.shape}")
        
        df_t = get_triggers()
        print(f"R5: Triggers={df_t.shape}")
        
        df_sz = get_tamano_tablas()
        print(f"R6: Tamaños={df_sz.shape}")
        
        df_reg = get_tamano_registro_por_tabla()
        print(f"R7: Registros={df_reg.shape}")
        
        df_col = get_tamano_columnas()
        print(f"R8: Columnas={df_col.shape}")
        
        df_t_fb, df_i_fb = get_factor_bloqueo()
        print(f"R9: TableFB={df_t_fb.shape}, IndexFB={df_i_fb.shape}")
        
        mapa = get_tables_and_columns()
        print(f"R10: Mapa tables={len(mapa)}")
        cost = estimate_query_cost('serie', 'cod_serie')
        print(f"R10: Cost seek={cost['costo_seek']}")
        
    except Exception as e:
        print("ERROR ENCONTRADO:")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    run_test()
