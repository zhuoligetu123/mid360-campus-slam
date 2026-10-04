#!/usr/bin/env python3
"""After building and sourcing install/setup.bash, verify maps cannot be erased."""
import os
from pathlib import Path
import resource
import subprocess
import tempfile


root = Path(__file__).resolve().parents[1]
resource.setrlimit(resource.RLIMIT_CORE, (0, 0))
with tempfile.TemporaryDirectory(prefix="mid360-map-guard-") as directory:
    sentinel = Path(directory) / "keep.txt"
    sentinel.write_text("preserve-existing-map")
    executable = root / "install/sc_liorf_localization/lib/sc_liorf_localization/sc_liorf_localization_sc_mapOptmization"
    result = subprocess.run(
        [str(executable), "--ros-args", "--params-file",
         str(root / "src/sc_liorf_localization/config/lio_sam_mid360_mapping.yaml"),
         "-p", "savePCDDirectory:=" + directory + "/"],
        env=dict(os.environ, ROS_DOMAIN_ID="217", ROS_LOCALHOST_ONLY="1"),
        stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, timeout=15)
    assert result.returncode != 0, result.stdout
    assert "Mapping requires a new or empty map_dir" in result.stdout, result.stdout
    assert sentinel.read_text() == "preserve-existing-map"
print("PASS: existing map preserved; nonempty mapping directory rejected")
