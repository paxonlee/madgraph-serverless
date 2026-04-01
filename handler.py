import os
import sys

import pexpect
import runpod


def handler(event: dict):
    job_input = event["input"]
    job_id = event.get("id", "runpod_local_test")

    commands = job_input.get("commands", [])
    if len(commands) == 0:
        return {"error": "No commands provided"}

    script_path = f"{job_id}.mg5"
    with open(script_path, "w") as f:
        f.write("\n".join(commands))

    try:
        child = pexpect.spawn(
            f"mg5_aMC {script_path}",
            encoding="utf-8",
            timeout=None,
        )
        child.logfile = sys.stdout
        child.expect(pexpect.EOF)
    except Exception as e:
        return {"status": "failed", "error": str(e)}

    child.close()

    directory_contents = os.listdir(".")

    return {
        "status": "success",
        "job_id": job_id,
        "commands": commands,
        "pwd": os.getcwd(),
        "directory_contents": directory_contents,
    }


if __name__ == "__main__":
    runpod.serverless.start({"handler": handler})
