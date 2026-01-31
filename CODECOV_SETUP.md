# Codecov Integration Setup

This guide will help you set up Codecov for code coverage tracking on the LUMINA repository.

## What is Codecov?

Codecov is a code coverage reporting tool that integrates with your CI/CD pipeline to track test coverage over time, identify untested code, and ensure quality standards.

---

## Setup Steps

### Step 1: Create Codecov Account

1. Visit https://codecov.io/
2. Click **Sign up** (top right)
3. Choose **Sign up with GitHub**
4. Authorize Codecov to access your GitHub account

### Step 2: Add Repository

1. After logging in, click **Add new repository** or go to https://app.codecov.io/gh/Pranit-satnurkar
2. Find `LUMINA-INTELLIGENT-FILE-READER-` in the list
3. Click **Setup repo**

### Step 3: Get Repository Token

1. On the repository setup page, you'll see a **Repository Upload Token**
2. Copy this token (it looks like: `xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx`)
3. Add it to GitHub Secrets as `CODECOV_TOKEN` (see [SECRETS_SETUP.md](SECRETS_SETUP.md))

### Step 4: Configure Codecov (Already Done!)

The repository already includes `.codecov.yml` configuration file. No additional configuration needed!

### Step 5: Trigger First Coverage Report

1. Make a commit and push to trigger CI/CD:
   ```bash
   git commit --allow-empty -m "test: Trigger coverage report"
   git push
   ```

2. Wait for GitHub Actions to complete
3. Check the **Actions** tab to see the workflow running
4. Coverage will be uploaded automatically

### Step 6: View Coverage Reports

1. Go to https://app.codecov.io/gh/Pranit-satnurkar/LUMINA-INTELLIGENT-FILE-READER-
2. You'll see:
   - Overall coverage percentage
   - Coverage trends over time
   - File-by-file coverage breakdown
   - Uncovered lines highlighted

---

## Add Codecov Badge to README

### Step 1: Get Badge Markdown

1. In Codecov, go to your repository
2. Click **Settings** → **Badge**
3. Copy the Markdown code (looks like):
   ```markdown
   [![codecov](https://codecov.io/gh/Pranit-satnurkar/LUMINA-INTELLIGENT-FILE-READER-/branch/main/graph/badge.svg)](https://codecov.io/gh/Pranit-satnurkar/LUMINA-INTELLIGENT-FILE-READER-)
   ```

### Step 2: Add to README

Add the badge to your README.md in the badges section at the top:

```markdown
![Version](https://img.shields.io/badge/Version-1.0.0-blue?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)
[![codecov](https://codecov.io/gh/Pranit-satnurkar/LUMINA-INTELLIGENT-FILE-READER-/branch/main/graph/badge.svg)](https://codecov.io/gh/Pranit-satnurkar/LUMINA-INTELLIGENT-FILE-READER-)
```

---

## Understanding Coverage Reports

### Coverage Metrics

- **Line Coverage**: Percentage of code lines executed during tests
- **Branch Coverage**: Percentage of conditional branches tested
- **Function Coverage**: Percentage of functions called during tests

### Coverage Goals

Current targets (defined in `.codecov.yml`):
- **Target**: 70% overall coverage
- **Threshold**: 60% minimum (builds won't fail below this)
- **Patch**: 50% for new code

### Reading the Report

**Green**: Well-tested code (>80% coverage)
**Yellow**: Moderately tested (50-80% coverage)
**Red**: Poorly tested (<50% coverage)

---

## Codecov Configuration

The repository includes `.codecov.yml` with the following settings:

```yaml
coverage:
  status:
    project:
      default:
        target: 70%
        threshold: 5%
    patch:
      default:
        target: 50%
        
comment:
  layout: "reach, diff, flags, files"
  behavior: default
  
ignore:
  - "tests/"
  - "**/__pycache__/"
  - "**/node_modules/"
  - "mobile-app/**"
```

---

## Troubleshooting

### Coverage not uploading

**Check**:
1. `CODECOV_TOKEN` is set in GitHub Secrets
2. GitHub Actions workflow completed successfully
3. `pytest --cov` ran without errors
4. `coverage.xml` file was generated

**Solution**:
- Check Actions logs for upload errors
- Verify token is correct
- Ensure `codecov/codecov-action@v4` is in workflow

### Coverage shows 0%

**Possible causes**:
1. Tests aren't running
2. Coverage paths are incorrect
3. Source files not found

**Solution**:
- Run tests locally: `pytest --cov=backend`
- Check `pytest.ini` configuration
- Verify file paths in `.codecov.yml`

### Badge not updating

**Solution**:
- Clear browser cache
- Wait 5-10 minutes for Codecov to process
- Check if latest commit has coverage data

---

## Best Practices

### Writing Testable Code

✅ **DO**:
- Write small, focused functions
- Separate business logic from I/O
- Use dependency injection
- Mock external services

❌ **DON'T**:
- Write monolithic functions
- Mix concerns (UI + logic)
- Hardcode dependencies
- Skip edge cases

### Improving Coverage

1. **Identify gaps**: Use Codecov's file view to find untested code
2. **Prioritize**: Focus on critical business logic first
3. **Add tests**: Write tests for uncovered lines
4. **Refactor**: Make code more testable if needed

### Maintaining Coverage

- Set coverage requirements in pull requests
- Review coverage reports before merging
- Don't sacrifice quality for coverage percentage
- Focus on meaningful tests, not just coverage numbers

---

## Additional Resources

- [Codecov Documentation](https://docs.codecov.com/)
- [Coverage.py Documentation](https://coverage.readthedocs.io/)
- [Pytest Coverage Plugin](https://pytest-cov.readthedocs.io/)
- [Jest Coverage](https://jestjs.io/docs/configuration#collectcoverage-boolean)

---

## Support

- **Codecov Support**: support@codecov.io
- **GitHub Issues**: Open an issue in the repository
- **Documentation**: https://docs.codecov.com/docs

---

<div align="center">
  <p><strong>Happy Testing! 🧪</strong></p>
  <p>Remember: Coverage is a tool, not a goal. Write meaningful tests!</p>
</div>
