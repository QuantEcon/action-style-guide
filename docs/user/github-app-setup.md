---
title: GitHub App Setup
---

# GitHub App Setup

For production use, we recommend using a GitHub App instead of personal access tokens for better security, rate limits, and permissions management.

## Why Use a GitHub App?

- **Better Rate Limits**: 5,000 requests/hour per repository (vs 1,000 for PAT)
- **Fine-grained Permissions**: Only grant what's needed
- **Better Security**: Scoped to specific repositories
- **Audit Trail**: Track all app activities
- **No User Association**: Operates independently

## Creating the App

### 1. Create the App

1. Go to your organization settings: `https://github.com/organizations/QuantEcon/settings/apps`
2. Click "New GitHub App"
3. Fill in the details:
   - **Name**: `quantecon-style-guide-bot`
   - **Homepage URL**: `https://github.com/QuantEcon/action-style-guide`
   - **Webhook**: Uncheck "Active" (we don't need webhooks)

### 2. Set Permissions

#### Repository Permissions

- **Contents**: Read & Write (for creating branches and committing)
- **Issues**: Read (for reading issue comments)
- **Pull Requests**: Read & Write (for creating PRs and comments)
- **Metadata**: Read (automatically granted)

#### Where can this GitHub App be installed?

Select "Only on this account" (for QuantEcon organization).

### 3. Generate Private Key

1. After creating the app, scroll down to "Private keys"
2. Click "Generate a private key"
3. Save the downloaded `.pem` file securely

### 4. Install the App

1. Go to "Install App" in the left sidebar
2. Click "Install" next to your organization
3. Select repositories:
   - Choose "Only select repositories"
   - Select your lecture repositories (e.g., `lecture-python-programming.myst`)
4. Click "Install"

### 5. Get App Credentials

You'll need:

- **App ID**: Found in app settings (e.g., `123456`)
- **Installation ID**: Found in installation URL (e.g., `https://github.com/settings/installations/98765`)
- **Private Key**: The `.pem` file you downloaded

## Using the App in Workflows

### Recommended: `actions/create-github-app-token`

```yaml
name: Style Guide Check
on:
  issue_comment:
    types: [created]

jobs:
  review:
    runs-on: ubuntu-latest
    steps:
      - name: Generate token
        id: generate-token
        uses: actions/create-github-app-token@v1
        with:
          app-id: ${{ secrets.APP_ID }}
          private-key: ${{ secrets.APP_PRIVATE_KEY }}

      - name: Run style guide checker
        uses: QuantEcon/action-style-guide@v0.7
        with:
          mode: 'single'
          github-token: ${{ steps.generate-token.outputs.token }}
          anthropic-api-key: ${{ secrets.ANTHROPIC_API_KEY }}
          comment-body: ${{ github.event.comment.body }}
```

### Manual Token Generation

For more control, generate the token manually:

```yaml
- name: Generate App Token
  id: app-token
  run: |
    TOKEN=$(curl -X POST \
      -H "Authorization: Bearer $(ruby -e "require 'jwt'; puts JWT.encode({iat: Time.now.to_i, exp: Time.now.to_i + 60, iss: '${{ secrets.APP_ID }}'}, OpenSSL::PKey::RSA.new('${{ secrets.APP_PRIVATE_KEY }}'), 'RS256')")" \
      -H "Accept: application/vnd.github+json" \
      https://api.github.com/app/installations/${{ secrets.INSTALLATION_ID }}/access_tokens | jq -r .token)
    echo "::add-mask::$TOKEN"
    echo "token=$TOKEN" >> $GITHUB_OUTPUT

- name: Use token
  uses: QuantEcon/action-style-guide@v0.7
  with:
    github-token: ${{ steps.app-token.outputs.token }}
```

## Setting Up Secrets

1. Go to **Settings → Secrets and variables → Actions**
2. Add repository secrets:
   - `APP_ID` — Your GitHub App ID
   - `APP_PRIVATE_KEY` — Contents of the `.pem` file
   - `INSTALLATION_ID` — Installation ID (optional, usually auto-detected)

## Testing the Setup

1. Create a test issue in your repository
2. Comment: `@quantecon-style-guide test-lecture`
3. Verify:
   - The workflow triggers
   - A branch is created
   - A PR is opened
   - Labels applied correctly

## Troubleshooting

### "Resource not accessible by integration"

- **Cause**: Missing repository permission
- **Fix**: Go to app settings → Permissions → Grant required permission

### "Bad credentials"

- **Cause**: Invalid or expired token
- **Fix**: Regenerate private key, update secret

### "Not Found"

- **Cause**: App not installed on repository
- **Fix**: Go to app → Install App → Select repository

## Rate Limits

| Token type | Limit |
|------------|-------|
| GitHub App | 5,000 requests/hour per repo |
| User access token | 15,000 requests/hour |

Check current rate limit:

```bash
curl -H "Authorization: Bearer $TOKEN" https://api.github.com/rate_limit
```

## Security Best Practices

1. **Rotate Keys Regularly** — Generate new private keys periodically
2. **Minimum Permissions** — Only grant necessary permissions
3. **Scope Installation** — Install only on required repositories
4. **Monitor Activity** — Review app activity logs regularly
5. **Secure Storage** — Store private key in GitHub Secrets, never commit
