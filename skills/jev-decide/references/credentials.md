# Credential Handling in Jev Decide

This file explains credential handling in this skill so anyone can verify it without reading the entire codebase.

## Where the key comes from

`scripts/jev_decide.py` reads the key from the environment or secure local configuration:

```python
api_key = os.environ.get("TYPESAFE_API_KEY", "").strip()
```

If unset in the active environment, it automatically inspects local `.env` files in the skill directory or the sibling `agent-meter-doctor` directory.

## Where the key does NOT go

* It is never written to a public git file by this skill.
* It is never included in example code, documentation, or public repositories.
* It is never logged. Error messages describe that the key is missing, never its actual characters.
* It is never leaked across network boundaries outside direct HTTPS requests to `https://api.typesafe.ai/v1/systemone`.

## What happens when it is missing

Every public function checks for the key before making network requests. If absent or empty, the function returns immediately with `available=False` and a human readable error, making no network call. Nothing crashes the calling task; callers simply check `.available` and fall back to standard heuristics.

## Setting the key

```bash
export TYPESAFE_API_KEY=your_key_here
```

On Windows PowerShell:

```powershell
$env:TYPESAFE_API_KEY = "your_key_here"
```

A local `.env` file inside `F:\Agent Skills\jev-decide\.env` is also automatically detected and read at runtime, and is ignored by git.
