import lib
import params
import os
import numpy as np

def objective_manual(control_points, name):
    # ステップごとの出力ファイル名 (例: ./optimization_steps/step_000.xdmf)
    filename = os.path.join(params.output_dir, f"{name}.xdmf")

    try:
        # 1. メッシュ生成
        domain, cell_tags, facet_tags = lib.rho_fields_from_controls(
            control_points=control_points,
            lc_domain=2.0,
            lc_wall=0.5,
        )

        # 2. ヘルムホルツ解析 ＆ XDMFファイル出力
        J = lib.solve_helmholtz_and_evaluate_perceptual_rms(
            domain=domain,
            facet_tags=facet_tags,
            cell_tags=cell_tags,
            freq=params.test_freqs[0],
            source_pos=(0.0, 1.0),
            amplitude_db=params.test_amplitude,
            output_filename=filename,  # 連番出力
        )

        print(f"J(dBA): {J:.4f}")
        return J

    except Exception as e:
        print(f"Failed: {e}")
        return 1e6

objective_manual(
    lib.right_side_cp_to_whole(
        np.array([
            [1.0, 11.5],  # 左端の高さ
            [5.0, 11.0],  # 左側の山
            [8.5, 5.0],   # 中央の谷
            [12.0, 11.0], # 右側の山
            [15.0, 2.0]   # 右端（固定）
        ])
    ), 
    "initial"
)
