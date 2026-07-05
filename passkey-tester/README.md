# Passkey Tester

This folder contains a single-page HTML artifact for testing browser password managers and platform/cross-platform authenticators with WebAuthn passkey registration and authentication ceremonies.

Open the demo locally or via GitHub Pages:

https://rdslw.github.io/risercz/passkey-tester/demo.html

## Files

- `demo.html` — the Passkey Tester web artifact.
- `notes.md` — working notes captured during implementation.

## What it tests

- Passkey registration (`navigator.credentials.create`) with configurable authenticator requirements.
- Passkey authentication (`navigator.credentials.get`) with selectable registered credential IDs.
- Client-side storage of credential metadata in `localStorage`.
- Inspection of attestation objects, authenticator data flags, AAGUID, credential ID, sign count, transports, and client extension results.
- Basic client-side consistency checks for challenge, origin, type, RP ID hash, and user presence / verification flags.

## Important limitation

The browser never exposes passkey private keys to JavaScript. This artifact stores only metadata and public registration/authentication outputs in `localStorage`; the actual passkeys remain in the browser password manager, platform authenticator, security key, or synced passkey provider.

Attestation trust-chain validation is intentionally presented as an inspection/checklist workflow. Production attestation verification requires a server-side verifier, trusted metadata roots, replay protection, and policy decisions about acceptable authenticators.
