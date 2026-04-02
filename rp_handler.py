import os
import sys
import tarfile

import pexpect
import runpod
import s3fs

S3_ENDPOINT = os.getenv("ENDPOINT")
S3_ACCESS_KEY_ID = os.getenv("ACCESS_KEY_ID")
S3_SECRET_ACCESS_KEY = os.getenv("SECRET_ACCESS_KEY")
S3_BUCKET = os.getenv("BUCKET")


def handler(event: dict):
    job_input = event["input"]

    commands = job_input.get("commands")
    if not commands:
        return {"error": "No commands provided"}

    sanitized_commands = []
    for command in commands:
        command = " ".join(command.split())
        if not command or command.startswith("!"):
            continue
        sanitized_commands.append(command)

    output_path = None
    for sanitized_command in sanitized_commands:
        if sanitized_command.startswith("output"):
            output_path = sanitized_command.split(" ")[1]
            break
    if not output_path:
        return {"error": "No output path provided"}

    script_path = "commands.mg5"
    with open(script_path, "w") as f:
        f.write("\n".join(sanitized_commands))

    child = None
    try:
        child = pexpect.spawn(
            f"mg5_aMC {script_path}",
            encoding="utf-8",
            timeout=None,
        )
        child.logfile = sys.stdout
        child.expect(pexpect.EOF)
    except Exception as e:
        return {"error": str(e)}
    finally:
        if child is not None:
            child.close()

    if not os.path.exists(output_path):
        return {"error": f"Output path '{output_path}' not found after execution"}

    archive_path = f"{output_path}.tar.gz"
    print(f"Compressing {output_path} to {archive_path}")
    with tarfile.open(archive_path, "w:gz") as tar:
        tar.add(output_path, arcname=output_path)

    if not all([S3_ENDPOINT, S3_ACCESS_KEY_ID, S3_SECRET_ACCESS_KEY, S3_BUCKET]):
        print("S3 credentials not configured, skipping upload")
        return {"output_path": archive_path}

    s3_path = f"{S3_BUCKET}/{archive_path}"
    print(f"Uploading {archive_path} to {s3_path}")
    try:
        s3 = s3fs.S3FileSystem(
            endpoint_url=S3_ENDPOINT,
            key=S3_ACCESS_KEY_ID,
            secret=S3_SECRET_ACCESS_KEY,
        )
        s3.put(archive_path, s3_path, ContentType="application/gzip")
    except Exception as e:
        return {"error": f"Failed to upload to S3: {str(e)}"}

    return {"output_path": s3_path}


if __name__ == "__main__":
    runpod.serverless.start({"handler": handler})
