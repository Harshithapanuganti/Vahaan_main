import subprocess
import yaml
from datetime import datetime
import subprocess


CONFIG_FILE = "config.yaml"


def load_config():
    with open(CONFIG_FILE, "r") as f:
        return yaml.safe_load(f)


def get_options(script):
    """
    Runs: --list-options and extracts Y-axis & X-axis
    """
    result = subprocess.run(
        ["python", script, "--list-options"],
        capture_output=True,
        text=True
    )

    output = result.stdout

    yaxis = []
    xaxis = []

    for line in output.splitlines():
        if "Y-Axis options" in line:
            yaxis = line.split(":")[1].split(",")

        if "X-Axis options" in line:
            xaxis = line.split(":")[1].split(",")

    return [y.strip() for y in yaxis], [x.strip() for x in xaxis]


def build_base_cmd(cfg):
    script = cfg["job"]["script"]
    params = cfg["parameters"]

    cmd = ["python", script]

    if params.get("state"):
        cmd += ["--state", params["state"]]

    if params.get("all_rtos"):
        cmd.append("--all-rtos")

    return cmd


def run():
    cfg = load_config()
    script = cfg["job"]["script"]

    # ✅ get all axis options
    yaxis_list, xaxis_list = get_options(script)

    print("Y-axis:", yaxis_list)
    print("X-axis:", xaxis_list)

    # ✅ dynamic year
    start_year = cfg["parameters"].get("start_year") or 1900
    end_year = cfg["parameters"].get("end_year") or datetime.now().year

    base_cmd = build_base_cmd(cfg)

    # ✅ LOOP ALL COMBINATIONS
    for y in yaxis_list:
        for x in xaxis_list:

            print(f"\nRunning → Y: {y}, X: {x}")

            cmd = base_cmd + [
                "--yaxis", y,
                "--xaxis", x,
                "--start-year", str(start_year),
                "--end-year", str(end_year)
            ]

            subprocess.run(cmd)


if __name__ == "__main__":
    run()
