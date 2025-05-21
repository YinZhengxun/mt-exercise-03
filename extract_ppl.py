import re
import sys

def parse_log(path):
    step_pattern = re.compile(r"Step:\s*(\d+)")
    ppl_pattern  = re.compile(r"ppl:\s*([\d.]+)")

    current_step = None
    records = []

    with open(path, encoding="utf-8") as f:
        for line in f:
            step_match = step_pattern.search(line)
            if step_match:
                current_step = int(step_match.group(1))

            ppl_match = ppl_pattern.search(line)
            if ppl_match and current_step is not None:
                ppl = float(ppl_match.group(1))
                records.append((current_step, ppl))
                current_step = None  # 避免重复
    return records

def print_table(*logs):
    all_data = [dict(parse_log(path)) for path in logs]
    all_steps = sorted(set().union(*[data.keys() for data in all_data]))

    # 打印表头
    print("Step\tBaseline\tPrenorm\t\tPostnorm")
    for step in all_steps:
        row = [str(step)]
        for data in all_data:
            row.append(f"{data.get(step, '-'):>8}")
        print("\t".join(row))

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("用法: python extract_ppl.py baseline.log prenorm.log postnorm.log")
        sys.exit(1)
    print_table(sys.argv[1], sys.argv[2], sys.argv[3])
