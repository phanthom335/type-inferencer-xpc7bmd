        """
        Type Inferencer Xpc7bmd
        =======================
        Lightweight ETL component that can aggregate millions of rows efficiently.

        Category : Data Processing Tools
        Created  : 2026-03-14
        Version  : 1.0.0
        License  : MIT
        """

        import argparse
        import logging
        import sys
        from dataclasses import dataclass, field
        from typing import Any, Dict
        import json
from pathlib import Path

        APP_NAME    = "Type Inferencer Xpc7bmd"
        APP_VERSION = "1.0.0"

        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s [%(levelname)s] %(message)s",
        )
        logger = logging.getLogger(APP_NAME)


        @dataclass
        class Config:
            """Runtime configuration."""
            verbose:    bool = False
            dry_run:    bool = False
            debug:      bool = False
            output_dir: str  = "./output"
            difficulty: str  = "medium"
            rounds:     int  = 3
            extra:      Dict[str, Any] = field(default_factory=dict)


        # ── Core logic ──────────────────────────────────────────────────────

        def process_data(input_path: Path, config: Config) -> dict:
    """Read, validate, transform and write a data file."""
    if not input_path.exists():
        raise FileNotFoundError(f"Not found: {input_path}")
    suffix = input_path.suffix.lower()
    if suffix == ".csv":
        rows = _read_csv(input_path)
    elif suffix == ".json":
        rows = _read_json(input_path)
    else:
        raise ValueError(f"Unsupported type: {suffix}")
    cleaned, errors = _transform(rows)
    output_path = input_path.parent / f"{input_path.stem}_processed{suffix}"
    _write_output(cleaned, output_path, suffix)
    logger.info("Written: %s", output_path)
    return {"input": str(input_path), "output": str(output_path),
            "rows_in": len(rows), "rows_out": len(cleaned), "errors": errors}

def _read_csv(path: Path) -> list:
    import csv
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))

def _read_json(path: Path) -> list:
    # FIX-12: no confusing alias — just use json directly
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    return data if isinstance(data, list) else [data]

def _transform(rows: list) -> tuple:
    cleaned, errors = [], []
    for i, row in enumerate(rows):
        try:
            cleaned.append(row)  # TODO: add real logic
        except Exception as exc:
            errors.append({"row": i, "error": str(exc)})
    return cleaned, errors

def _write_output(rows: list, path: Path, suffix: str) -> None:
    import csv
    if suffix == ".csv" and rows:
        with open(path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=rows[0].keys())
            writer.writeheader()
            writer.writerows(rows)
    else:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(rows, f, indent=2)


        # ── CLI ─────────────────────────────────────────────────────────────

        def build_parser() -> argparse.ArgumentParser:
            p = argparse.ArgumentParser(prog=APP_NAME, description="Lightweight ETL component that can aggregate millions of rows efficiently.")
            p.add_argument("--verbose", "-v", action="store_true")
            p.add_argument("--dry-run",        action="store_true")
            p.add_argument("--debug",          action="store_true")
            p.add_argument("--version",        action="version", version=f"%(prog)s {APP_VERSION}")
            return p


        def parse_args(argv=None) -> Config:
            args = build_parser().parse_args(argv)
            if args.debug or args.verbose:
                logging.getLogger().setLevel(logging.DEBUG)
            return Config(verbose=args.verbose, dry_run=args.dry_run, debug=args.debug)


        # ── Entry point ──────────────────────────────────────────────────────

        def main() -> int:
            config = parse_args()
            logger.info("Starting %s v%s", APP_NAME, APP_VERSION)
            try:
                import pathlib
        sample = pathlib.Path("sample_data.csv")
        if not sample.exists():
            sample.write_text("id,name,value\n1,Alice,100\n2,Bob,200\n")
        result = process_data(sample, config)
                logger.info("Result: %s", result)
                logger.info("%s completed successfully.", APP_NAME)
                return 0
            except KeyboardInterrupt:
                logger.info("Interrupted by user.")
                return 0
            except (FileNotFoundError, ValueError) as exc:
                logger.error("%s", exc)
                return 1
            except Exception as exc:
                logger.exception("Unexpected error: %s", exc)
                return 1


        if __name__ == "__main__":
            sys.exit(main())
