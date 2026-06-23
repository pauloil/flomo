#!/usr/bin/env python3
import os
import json
from mcp.server.fastmcp import FastMCP
from . import Flomo, Parser

mcp = FastMCP("flo-cli")


def _client() -> Flomo:
    token = os.environ.get("FLOMO_AUTHORIZATION", "")
    if not token:
        raise RuntimeError("FLOMO_AUTHORIZATION environment variable not set")
    if not token.startswith("Bearer "):
        token = f"Bearer {token}"
    return Flomo(token)


@mcp.tool()
def create_memo(content: str) -> str:
    """Create a new flomo memo. Supports plain text or HTML. Use #tag for tags."""
    memo = _client().create(content)
    return f"Created memo: {memo['slug']}"


@mcp.tool()
def list_memos(limit: int = 10) -> str:
    """List recent flomo memos."""
    memos = _client().get_all_memos()[:limit]
    results = []
    for m in memos:
        p = Parser(m)
        results.append(f"[{m['slug']}] {m.get('updated_at', '')}\n{p.text.strip()[:100]}")
    return "\n---\n".join(results) if results else "No memos found"


@mcp.tool()
def search_memos(keyword: str, limit: int = 10) -> str:
    """Search flomo memos by keyword."""
    memos = _client().get_all_memos()
    hits = [m for m in memos if keyword.lower() in m.get("content", "").lower()][:limit]
    if not hits:
        return f"No memos found matching '{keyword}'"
    results = []
    for m in hits:
        p = Parser(m)
        results.append(f"[{m['slug']}] {m.get('updated_at', '')}\n{p.text.strip()[:100]}")
    return "\n---\n".join(results)


@mcp.tool()
def update_memo(slug: str, content: str) -> str:
    """Update an existing flomo memo by its slug."""
    memo = _client().update(slug, content)
    return f"Updated memo: {memo['slug']}"


@mcp.tool()
def delete_memo(slug: str) -> str:
    """Delete a flomo memo by its slug."""
    return _client().delete(slug)


def main():
    mcp.run()


if __name__ == "__main__":
    main()
