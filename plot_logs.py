#!/usr/bin/env python3
import re
import sys
import matplotlib.pyplot as plt

def parse_log(path):
    """
    从日志中提取 step 和 ppl 对。
    每次遇到一行 Step: XXXX 时记录 step，接下来的 Evaluation 行提取 ppl。
    """
    step_pattern = re.compile(r"Step:\s*(\d+)")
    ppl_pattern  = re.compile(r"ppl:\s*([\d\.]+)")
    current_step = None
    steps = []
    ppls = []

    with open(path, encoding="utf-8") as f:
        for line in f:
            m_step = step_pattern.search(line)
            if m_step:
                current_step = int(m_step.group(1))
            m_ppl = ppl_pattern.search(line)
            if m_ppl and current_step is not None:
                ppl = float(m_ppl.group(1))
                steps.append(current_step)
                ppls.append(ppl)
                current_step = None  # 避免重复匹配
    return steps, ppls

def main():
    if len(sys.argv) != 4:
        print("用法: python plot_logs.py <baseline.log> <prenorm/train.log> <postnorm/train.log>")
        sys.exit(1)

    baseline_log = sys.argv[1]
    prenorm_log  = sys.argv[2]
    postnorm_log = sys.argv[3]

    steps_base, ppls_base = parse_log(baseline_log)
    steps_pre,  ppls_pre  = parse_log(prenorm_log)
    steps_post, ppls_post = parse_log(postnorm_log)

    plt.figure(figsize=(9, 6))
    plt.plot(steps_base, ppls_base, label="Baseline", marker="o")
    plt.plot(steps_pre,  ppls_pre,  label="Prenorm", marker="s")
    plt.plot(steps_post, ppls_post, label="Postnorm", marker="^")
    plt.xlabel("Training Step")
    plt.ylabel("Validation PPL")
    plt.title("Validation Perplexity: Baseline vs. Prenorm vs. Postnorm")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()
