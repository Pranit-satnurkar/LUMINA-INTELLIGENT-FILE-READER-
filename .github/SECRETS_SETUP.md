# GitHub Secrets Setup Guide

This guide will help you configure the required secrets for GitHub Actions CI/CD workflows.

## Required Secrets

The LUMINA repository requires three secrets to be configured in GitHub:

1. **GROQ_API_KEY** - For backend testing and LLM inference
2. **EXPO_TOKEN** - For mobile app builds (optional for basic CI)
3. **CODECOV_TOKEN** - For code coverage reporting

---

## How to Add Secrets to GitHub

### Step 1: Navigate to Repository Settings

1. Go to your GitHub repository: https://github.com/Pranit-satnurkar/LUMINA-INTELLIGENT-FILE-READER-
2. Click on **Settings** (top menu bar)
3. In the left sidebar, click on **Secrets and variables** → **Actions**

### Step 2: Add Each Secret

Click the **New repository secret** button for each secret below.

---

## 1. GROQ_API_KEY

**Purpose**: Required for backend testing and LLM inference in CI/CD

**How to Get**:
1. Visit https://console.groq.com/
2. Sign up or log in
3. Navigate to **API Keys** section
4. Click **Create API Key**
5. Copy the generated key (starts with `gsk_`)

**Add to GitHub**:
- **Name**: `GROQ_API_KEY`
- **Value**: Your Groq API key (e.g., `gsk_xxxxxxxxxxxxxxxxxxxxx`)

> [!IMPORTANT]
> Never commit this key to your repository or share it publicly!

---

## 2. EXPO_TOKEN

**Purpose**: Required for building mobile app APKs with EAS Build

**How to Get**:
1. Install EAS CLI (if not already installed):
   ```bash
   npm install -g eas-cli
   ```

2. Log in to Expo:
   ```bash
   eas login
   ```

3. Generate a token:
   ```bash
   eas build:configure
   ```
   
   Or create one manually at: https://expo.dev/accounts/[your-username]/settings/access-tokens

4. Copy the generated token

**Add to GitHub**:
- **Name**: `EXPO_TOKEN`
- **Value**: Your Expo access token

> [!NOTE]
> This is optional if you're not building APKs in CI/CD. The mobile-ci workflow will skip build steps if this token is not present.

---

## 3. CODECOV_TOKEN

**Purpose**: Required for uploading code coverage reports to Codecov

**How to Get**:
1. Visit https://codecov.io/
2. Sign up using your GitHub account
3. Click **Add new repository**
4. Select `LUMINA-INTELLIGENT-FILE-READER-`
5. Copy the **Repository Upload Token** shown on the setup page

**Add to GitHub**:
- **Name**: `CODECOV_TOKEN`
- **Value**: Your Codecov repository token

> [!TIP]
> See [CODECOV_SETUP.md](../CODECOV_SETUP.md) for detailed Codecov integration instructions.

---

## Verification

After adding all secrets:

1. Go to **Settings** → **Secrets and variables** → **Actions**
2. You should see three secrets listed:
   - `GROQ_API_KEY`
   - `EXPO_TOKEN`
   - `CODECOV_TOKEN`

3. Trigger a workflow by pushing a commit:
   ```bash
   git commit --allow-empty -m "test: Trigger CI/CD workflows"
   git push
   ```

4. Go to the **Actions** tab to see workflows running
5. Check that workflows complete successfully

---

## Security Best Practices

✅ **DO**:
- Rotate API keys regularly
- Use separate keys for development and production
- Monitor secret usage in Actions logs
- Revoke compromised keys immediately

❌ **DON'T**:
- Commit secrets to the repository
- Share secrets in public channels
- Use production keys in CI/CD (use test keys when possible)
- Print secrets in workflow logs

---

## Troubleshooting

### Workflow fails with "GROQ_API_KEY not found"
- Ensure the secret name is exactly `GROQ_API_KEY` (case-sensitive)
- Check that the secret value is valid and not expired
- Verify the secret is accessible in the workflow (check repository settings)

### Mobile build fails with authentication error
- Ensure `EXPO_TOKEN` is correctly set
- Verify your Expo account has access to the project
- Check that the token hasn't expired

### Coverage upload fails
- Ensure `CODECOV_TOKEN` is correctly set
- Verify the repository is linked in Codecov
- Check Codecov service status

---

## Additional Resources

- [GitHub Secrets Documentation](https://docs.github.com/en/actions/security-guides/encrypted-secrets)
- [Groq API Documentation](https://console.groq.com/docs)
- [Expo EAS Build Documentation](https://docs.expo.dev/build/introduction/)
- [Codecov Documentation](https://docs.codecov.com/docs)

---

<div align="center">
  <p>Need help? Open an issue on GitHub!</p>
</div>
