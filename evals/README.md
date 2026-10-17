# evals

一条 eval = 一个真实任务 + 一组「什么算可接受」的检查。

## 写一条新 eval

1. 从 `_template.eval.json` 复制成 `<name>.eval.json`；
2. `from` 填任务开始前的 commit（`git rev-parse <commit>`）；
3. `prompt` 用人真实说过的话；
4. `checks` 测**行为**，不要测写法（变量名变了也要通过）；
5. 跑 `python3 evals/check.py evals/<name>.eval.json /tmp/result.json` 验证检查本身能跑。

## 什么时候加

- 每个生产事故 → 一条 eval（写进复盘模板，最容易断的一环）；
- 每次政策变更 → 一条 eval；
- 每季度清理：不再有区分度的用例删掉，否则套件维护成本会超过收益。

## 本地运行全套

```bash
bash evals/run.sh
```
