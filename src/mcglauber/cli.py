from __future__ import annotations
import argparse
from .config import load_config
from .simulation import run_simulation
from .observables import summarize_results
from .io_utils import ensure_dir, save_dataframe, save_histogram, save_event_geometries_jsonl

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Monte Carlo Glauber simulation")
    parser.add_argument("-c", "--config", type=str, required=True, help="Ruta al archivo YAML de configuración")
    return parser

def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    cfg = load_config(args.config)
    outdir = ensure_dir(cfg.output.outdir)
    df_events, geometry_records, sigma_inel_nn_mb = run_simulation(cfg)
    summary = summarize_results(df_events)
    print(f"sqrt(s_NN) = {cfg.beam.sqrts_gev:.3f} GeV")
    print(f"sigma_inel_nn = {sigma_inel_nn_mb:.3f} mb")
    print(summary.to_string(index=False))
    if cfg.output.save_summary_csv:
        save_dataframe(df_events, outdir / "events_summary.csv")
        save_dataframe(summary, outdir / "summary.csv")
    if cfg.output.save_histograms:
        save_histogram(df_events["b_fm"], xlabel="b [fm]", path=outdir / "hist_b.png")
        save_histogram(df_events["n_part"], xlabel="Npart", path=outdir / "hist_npart.png")
        save_histogram(df_events["n_coll"], xlabel="Ncoll", path=outdir / "hist_ncoll.png")
    if cfg.output.save_event_geometries and cfg.output.event_geometry_format == "jsonl":
        save_event_geometries_jsonl(geometry_records, outdir / "event_geometries.jsonl.gz")

if __name__ == "__main__":
    main()
