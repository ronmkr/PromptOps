# promptbook Makefile (Wrapper for cargo-make)

.PHONY: help test validate docs all clean tui cli lint fmt build release-binary setup

help:
	@cargo make --no-workspace help

all:
	@cargo make --no-workspace all

build:
	@cargo make --no-workspace build

test:
	@cargo make --no-workspace test

lint:
	@cargo make --no-workspace lint

fmt:
	@cargo make --no-workspace fmt

validate:
	@cargo make --no-workspace validate

docs:
	@cargo make --no-workspace docs

tui:
	@cargo make --no-workspace tui

cli:
	@cargo make --no-workspace cli

mcp:
	@cargo build -p promptbook-mcp

clean:
	@cargo make --no-workspace clean

release-binary:
	@cargo make --no-workspace release-binary

setup:
	@cargo make --no-workspace setup
