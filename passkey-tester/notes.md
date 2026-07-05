# Notes

- Created `passkey-tester/` for the HTML artifact.
- Goal: single-page WebAuthn/passkey tester for registration and authentication ceremonies.
- Important constraint: real passkey private keys are never available to JavaScript and cannot be stored in localStorage. The page can store credential metadata, credential IDs, public keys, attestation/authenticator data, and test results in localStorage while the authenticator/password manager stores the passkey itself.
- Implementing registration with configurable authenticatorSelection, residentKey, userVerification, attestation, timeout, and publicKeyCredParams.
- Implementing authentication with allowCredentials selection, userVerification, timeout, and challenge generation.
- Adding client-side parsing of authenticator data and attestation object for technical inspection. Full trust-chain attestation verification generally requires server-side policy and metadata roots, so the artifact reports parsed attestation and client-side consistency checks rather than pretending to provide production-grade attestation trust.
- Added initial README with GitHub Pages link and limitations.
- Next: write `demo.html` with no external dependencies so it works from static hosting.
- Wrote `demo.html` as a dependency-free static page with registration and authentication flows.
- Added localStorage metadata management, credential enable/disable, export, and checklist output.
- Added lightweight CBOR parsing sufficient to inspect attestation format, attStmt keys, and authenticator data.
- Reviewing implementation for static-page constraints and committing only the new project folder.
