# Security Policy

## Supported Versions

We currently support the following versions with security updates:

| Version | Supported          |
| ------- | ------------------ |
| 1.0.x   | :white_check_mark: |
| < 1.0   | :x:                |

## Reporting a Vulnerability

We take the security of JobSpy Docker API seriously. If you believe you've found a security vulnerability, please follow these steps:

1. **Do Not** disclose the vulnerability publicly
2. **Do Not** open a public GitHub issue

Instead, please email us at [security@example.com](mailto:security@example.com) with:

- Description of the vulnerability
- Steps to reproduce
- Potential impact
- Any suggestions for remediation

We will acknowledge receipt of your report within 48 hours and provide an estimated timeline for a fix. We'll keep you informed of our progress.

## Security Measures

- API key authentication (when enabled)
- Rate limiting capabilities
- Regular dependency updates
- Input validation
- Safe error handling

## Security Best Practices for Users

1. **API Keys**: When using API key authentication, follow best practices:
   - Use unique keys for different use cases
   - Rotate keys regularly
   - Only share keys securely

2. **Environment Variables**: Never commit real API keys to version control
   - Use `.env.local` for local development
   - Use secure methods for production deployment

3. **Rate Limiting**: Enable rate limiting in production
   - Adjust limits according to your expected usage

4. **Regular Updates**: Update to the latest version regularly

## Disclosure Policy

When we receive a security bug report, we will:

1. Confirm the vulnerability
2. Determine its impact and severity
3. Develop and test a fix
4. Release a patched version
5. Acknowledge your contribution (unless you prefer to remain anonymous)
