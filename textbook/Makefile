# 《我们如何知道？》一键构建与校验
#
# 常用命令：
#   make            # 全量构建 PDF（含索引两遍流程），输出到 $(BUILD_DIR)/main.pdf
#   make check      # 源稿一致性校验（练习/提示配对、文献引用、include 完整性）
#   make clean      # 删除构建临时目录
#
# 构建产物一律写入项目外目录，源码树保持只有可编辑稿件。

BUILD_DIR ?= /tmp/epistemology-build
LATEXMK   := latexmk -norc -xelatex -interaction=nonstopmode -halt-on-error
PYTHON    ?= python3

.PHONY: all pdf index check clean

all: pdf

pdf:
	@mkdir -p $(BUILD_DIR)
	@# 全新目录下目录/索引/文献交叉引用可能需要额外一轮才收敛，失败则重试。
	@ok=0; for i in 1 2 3; do \
	  if $(LATEXMK) -outdir=$(BUILD_DIR) main.tex; then ok=1; break; fi; \
	  echo "== 第 $$i 轮未收敛，自动重试 =="; \
	done; \
	if [ $$ok -ne 1 ]; then echo "!! 构建失败：请查看 $(BUILD_DIR)/main.log"; exit 1; fi
	$(MAKE) --no-print-directory index
	$(LATEXMK) -outdir=$(BUILD_DIR) main.tex
	@echo "== 完成：$(BUILD_DIR)/main.pdf"

# 索引必须在正文 idx 记录生成后单独执行，再重编译一次才能进入版面。
# 注意：在构建目录内运行，否则 TeX 的 openout_any 安全策略会拒绝写入绝对路径。
index:
	cd $(BUILD_DIR) && makeindex -o main.ind main.idx

check:
	$(PYTHON) tools/check_consistency.py .

clean:
	rm -rf $(BUILD_DIR)
