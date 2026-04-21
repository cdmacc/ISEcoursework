# Configuration Performance Tuning Tool for ISE Coursework

## Dataset Description (from lab 3)

The project includes datasets for various configurable systems. Each dataset is stored as a `.csv` file and contains the following structure:

- **Columns 1 to n-1:** Configuration parameters (discrete or continuous values).

- **Column n:** Performance objective (a numeric value to be optimized).

### Included Systems

| System     | Language | Domain            | Performance Metric | #O (Options) | #C (Configurations) | Optimization Type |
| ---------- | -------- | ----------------- | ------------------ | ------------ | ------------------- | ----------------- |
| 7z         | C++      | Compressor        | Runtime & Energy   | 8            | 68640               | Minimization      |
| Brotli     | C        | Compressor        | Runtime & Energy   | 2            | 180                 | Minimization      |
| LLVM       | C        | Compiler          | Runtime & Energy   | 16           | 65536               | Minimization      |
| PostgreSQL | C        | Database          | Runtime & Energy   | 8            | 864                 | Minimization      |
| x264       | C        | Video Encoder     | Runtime & Energy   | 10           | 4608                | Minimization      |
| Apache     | C        | Web Server        | Runtime & Energy   | 8            | 640                 | Minimization      |
| Spear      | C        | SAT Solver        | Runtime            | 14           | 16384               | Minimization      |
| Storm      | Clojure  | Streaming Process | Latency            | 12           | 1557                | Minimization      |

### Notes

- **Optimization Type:** All datasets are minimization problems, where smaller values indicate better results.
- **Performance Objectives:**
  - **Runtime & Energy:** Measures runtime and energy efficiency (Only consider Runtime here).
  - **Latency:** Measures system delay during processing.
