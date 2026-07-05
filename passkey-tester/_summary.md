Passkey Tester is a single-page web tool for evaluating browser password managers and authenticators using WebAuthn passkey registration and authentication flows. Users can test how different platforms handle passkey ceremonies, inspect attestation details, and review metadata stored client-side, without access to private keys. The tool supports configurable authentication requirements and exposes credential data for educational and debugging purposes, but emphasizes that robust attestation validation must occur server-side. For hands-on testing and inspection, the artifact is available at the [GitHub demo](https://rdslw.github.io/risercz/passkey-tester/demo.html).

**Key Features:**
- Tests `navigator.credentials.create` and `navigator.credentials.get` WebAuthn flows.
- Metadata and attestation details are viewable via localStorage—only public outputs are accessible.
- Designed to help developers explore authenticator properties; not intended for production security validation.
