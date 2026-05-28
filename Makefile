PROTO_DIR := ./proto-contracts/proto
OUT_DIR := .
PROTO_FILES := $(shell find $(PROTO_DIR) -name "*.proto")

.PHONY: all generate clean update-submodule init-submodule

all: generate

init:
	git submodule update --init --recursive

update:
	git submodule update --remote --merge

generate-contracts:
	@echo "generating grpc contracts ... "
	python -m grpc_tools.protoc \
		-I=$(PROTO_DIR) \
		--python_out=$(OUT_DIR) \
		--grpc_python_out=$(OUT_DIR) \
		$(PROTO_FILES)
	@echo "OK !"

	@find ./contracts -type d -exec touch {}/__init__.py \;

clean-contracts:
	@echo "cleaning contracts ..."
	rm -rf ./contracts
	@echo "OK !"
