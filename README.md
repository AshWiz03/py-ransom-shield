# Ransomware-Proof Backup Tool for Windows

A deduplicating backup tool that **scans files for signs of ransomware encryption before they enter the backup**, so a later restore doesn't bring back encrypted or infected data.

Most backup tools (Restic, Kopia, Borg) back up whatever is on disk. If ransomware has already encrypted your files, the next backup stores the encrypted versions too, and clean copies can be lost as old snapshots rotate out. This tool checks each file first. Files that look maliciously encrypted are moved to quarantine, and everything else is chunked, deduplicated, encrypted and stored.

> B.Tech final-year project, Computer Science & Engineering (Cyber Security), TIFAC-CORE in Cyber Security, Amrita Vishwa Vidyapeetham, Coimbatore (May 2025).

---

## Features

- **Pre-backup ransomware detection** with a different strategy for each kind of file:
  - **Low-entropy files** (`.txt`, `.json`, `.xml`, `.config`, …): Shannon entropy is compared against a per-file-type threshold.
  - **High-entropy files** (`.pdf`, `.docx`, `.xlsx`, `.pptx`, `.jpg`, `.zip`, …): metadata, header and footer validation, because entropy alone causes false positives on formats that are already compressed.
  - **Unknown or ransomware-tagged extensions** go straight to quarantine.
- **Content-defined chunking with [FastCDC](https://www.usenix.org/conference/atc16/technical-sessions/presentation/xia)**: variable-size chunks (64 KB min / 128 KB avg / 256 KB max), so small edits don't invalidate the whole file.
- **Deduplication** with per-chunk reference counting: each unique chunk is stored once.
- **Encryption at rest** with AES-CTR. Chunks use a fixed IV, so identical chunks produce identical ciphertext and still deduplicate. Metadata files use a random IV.
- **BLAKE3 hashing** for chunk addressing and integrity checks.
- **Snapshot retention**: keeps the latest *n* backups and deletes the oldest automatically in a single step, with no separate forget-and-prune.
- **On-demand integrity verification** for any snapshot.
- **Hash-verified restoration**: each restored file is checked against its recorded hash.

---

## How it works

```
               ┌──────────────────────────┐
 Source dirs ─▶│  Scan & classify files   │
               └────────────┬─────────────┘
        ┌───────────────────┼────────────────────┐
        ▼                   ▼                    ▼
  High entropy         Low entropy        Unrecognised type
  (PDF, DOCX, …)       (TXT, JSON, …)     / ransomware ext.
  metadata + header/   entropy vs.               │
  footer validation    type threshold            │
        │  fail ─────────────┼── fail ───────────┴──▶  QUARANTINE
        ▼ pass               ▼ pass
               ┌──────────────────────────┐
               │ FastCDC chunking         │
               │ → AES-CTR encrypt        │
               │ → BLAKE3 hash            │
               │ → dedupe via ref_count   │
               └────────────┬─────────────┘
                            ▼
          backup/<YYYY-MM-DD_HH-MM-SS>/  +  chunks/
                            ▼
           Retention: if snapshots > n, delete the oldest
```

### Backup layout

```
backup/
├── chunks/                     # encrypted chunks, each named by its BLAKE3 hash
├── 2025-04-12_10-30-00/
│   ├── chunkmap.json           # chunk name → hash
│   ├── filemap.json            # file → ordered list of chunks
│   └── ref_count.json          # reference count per chunk
└── 2025-04-13_10-30-00/
    └── ...
quarantine/                     # files flagged as possibly ransomware-encrypted
```

The metadata JSON files are encrypted (AES-CTR, random IV).

---

## Requirements

- Windows 10/11. Development and testing targeted Windows; the Python code itself is mostly portable.
- Python 3.9+

| Purpose | Library |
|---|---|
| Content-defined chunking | `fastcdc` |
| Hashing | `blake3` |
| Encryption | `pycryptodome` |
| PDF metadata | `PyPDF2` |
| Office metadata | `python-docx`, `python-pptx`, `openpyxl` |
| XML well-formedness | `lxml` |
| Progress bars | `tqdm` |

```bash
pip install fastcdc blake3 pycryptodome PyPDF2
