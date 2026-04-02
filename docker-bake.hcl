target "delphes" {
  context    = "dependencies/delphes"
  tags       = ["startown/delphes:3.5.0"]
  platforms  = ["linux/amd64", "linux/arm64"]
  attest     = ["type=provenance", "type=sbom"]
  output     = ["type=registry"]
}

target "emela" {
  context    = "dependencies/emela"
  tags       = ["startown/emela:1.0.1"]
  platforms  = ["linux/amd64", "linux/arm64"]
  attest     = ["type=provenance", "type=sbom"]
  output     = ["type=registry"]
}

target "fastjet" {
  context    = "dependencies/fastjet"
  tags       = ["startown/fastjet:3.5.1"]
  platforms  = ["linux/amd64", "linux/arm64"]
  attest     = ["type=provenance", "type=sbom"]
  output     = ["type=registry"]
}

target "hepmc" {
  context    = "dependencies/hepmc"
  tags       = ["startown/hepmc:2.06.09"]
  platforms  = ["linux/amd64", "linux/arm64"]
  attest     = ["type=provenance", "type=sbom"]
  output     = ["type=registry"]
}

target "lhapdf" {
  context    = "dependencies/lhapdf"
  tags       = ["startown/lhapdf:6.5.5"]
  platforms  = ["linux/amd64", "linux/arm64"]
  attest     = ["type=provenance", "type=sbom"]
  output     = ["type=registry"]
}

target "madgraph" {
  context    = "dependencies/madgraph"
  tags       = ["startown/madgraph:3.5.13"]
  platforms  = ["linux/amd64", "linux/arm64"]
  attest     = ["type=provenance", "type=sbom"]
  output     = ["type=registry"]
}

target "madgraph-serverless" {
  tags       = ["startown/madgraph-serverless:0.1.12"]
  platforms  = ["linux/amd64"]
  attest     = ["type=provenance", "type=sbom"]
  output     = ["type=registry"]
}

target "pythia" {
  context    = "dependencies/pythia"
  tags       = ["startown/pythia:8.316"]
  platforms  = ["linux/amd64", "linux/arm64"]
  attest     = ["type=provenance", "type=sbom"]
  output     = ["type=registry"]
}

target "root" {
  context    = "dependencies/root"
  tags       = ["startown/root:6.34.10"]
  platforms  = ["linux/amd64", "linux/arm64"]
  attest     = ["type=provenance", "type=sbom"]
  output     = ["type=registry"]
}

target "zlib" {
  context    = "dependencies/zlib"
  tags       = ["startown/zlib:1.3.1"]
  platforms  = ["linux/amd64", "linux/arm64"]
  attest     = ["type=provenance", "type=sbom"]
  output     = ["type=registry"]
}