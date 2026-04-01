import os
import tempfile

import pexpect
from fastapi import FastAPI
from fastapi.responses import HTMLResponse, StreamingResponse
from pydantic import BaseModel

app = FastAPI()

INDEX_HTML = """\
<!DOCTYPE html>
<html>
<head><meta charset="utf-8"><title>MG5 Runner</title></head>
<body style="font-family:monospace; max-width:800px; margin:40px auto">
<h2>MG5 Runner</h2>
<textarea id="script" rows="22" cols="80" placeholder="Paste .mg5 commands here…">generate p p > w+ w-, w+ > j j, w- > j j
output pp2ww_w2jj_w2jj
launch

shower=pythia8
detector=delphes
done

set iseed 42
set ebeam 7000
set htjmin 300
set htjmax 400
set nevents 1000
add pythia8_card Random:setSeed = on
add pythia8_card Random:seed = 42
add delphes_card --line_position=0 set RandomSeed 42
done

!rm py.py</textarea>
<br><button onclick="run()">Run</button>
<pre id="output" style="background:#111;color:#0f0;padding:16px;height:400px;overflow:auto"></pre>
<script>
async function run() {
  const out = document.getElementById("output");
  out.textContent = "";
  const text = document.getElementById("script").value;
  const commands = text.split("\\n");
  const res = await fetch("/run", {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify({commands}),
  });
  const reader = res.body.getReader();
  const decoder = new TextDecoder();
  while (true) {
    const { done, value } = await reader.read();
    if (done) break;
    out.textContent += decoder.decode(value);
    out.scrollTop = out.scrollHeight;
  }
}
</script>
</body>
</html>"""


class RunRequest(BaseModel):
    commands: list[str]


ALLOWED_SHELL_COMMANDS = {"!rm py.py"}


def run_mg5(commands: list[str]):
    sanitized = []
    warnings = []
    for command in commands:
        if command.startswith("!") and command not in ALLOWED_SHELL_COMMANDS:
            warnings.append(f"WARNING: shell command not allowed, skipping: {command}\n")
            continue
        sanitized.append(command)

    yield from warnings

    with tempfile.NamedTemporaryFile(mode="w", suffix=".mg5", delete=False) as f:
        f.write("\n".join(sanitized) + "\n")
        script_path = f.name

    child = pexpect.spawn(f"mg5_aMC {script_path}", encoding="utf-8", timeout=None)

    while True:
        try:
            child.expect("\n")
            yield (child.before or "") + "\n"
        except pexpect.EOF:
            remaining = child.before or ""
            if remaining:
                yield remaining + "\n"
            break

    child.close()
    os.unlink(script_path)


@app.get("/")
async def index():
    return HTMLResponse(INDEX_HTML)


@app.post("/run")
def run(request: RunRequest):
    return StreamingResponse(
        run_mg5(request.commands),
        media_type="text/plain",
        headers={"X-Content-Type-Options": "nosniff"},
    )
