#!/usr/bin/env python3
"""控制带检测：读 30 天小时读数（JSON 数组，旧→新），输出最新读数命中的层级。

用法：
  python3 scripts/detect_band.py < readings.json
  python3 scripts/detect_band.py --self-test
"""
import json
import statistics
import sys

MIN_SIGMA = 0.01  # 指标自身的单位；防止平坦基线把每个小波动判成越界


def above(readings, line, need, out_of):
    return sum(r > line for r in readings[-out_of:]) >= need


def tier(readings):
    baseline = readings[:-1]
    if len(baseline) < 24:
        sys.exit("至少需要 24 个基线读数（推荐 30 天小时级）")
    mean = statistics.mean(baseline)
    sigma = max(statistics.stdev(baseline), MIN_SIGMA)
    rules = [
        ("3sigma", "reading above 3 sigma", above(readings, mean + 3 * sigma, 1, 1)),
        ("2sigma", "reading above 2 sigma", above(readings, mean + 2 * sigma, 1, 1)),
        ("2sigma", "drift: 4 of 5 above 1 sigma", above(readings, mean + sigma, 4, 5)),
        ("2sigma", "drift: 8 in a row above mean", above(readings, mean, 8, 8)),
        ("1sigma", "reading above 1 sigma", above(readings, mean + sigma, 1, 1)),
    ]
    for name, rule, tripped in rules:
        if tripped:
            return {"tier": name, "rule": rule, "reading": readings[-1],
                    "mean": round(mean, 4), "sigma": round(sigma, 4)}
    return {"tier": "none", "reading": readings[-1],
            "mean": round(mean, 4), "sigma": round(sigma, 4)}


def self_test():
    import random
    random.seed(7)
    base = [round(random.gauss(0.2, 0.02), 4) for _ in range(30 * 24)]
    normal = tier(base + [0.21])
    spike = tier(base + [1.9])
    assert normal["tier"] in ("none", "1sigma"), normal
    assert spike["tier"] == "3sigma", spike
    print("self-test ok:", json.dumps(normal), json.dumps(spike))


if __name__ == "__main__":
    if "--self-test" in sys.argv:
        self_test()
    else:
        print(json.dumps(tier(json.load(sys.stdin))))
