# 📖 promptbook - Testing & QA Catalog

This catalog contains the reference for all **Testing & QA** templates.

## 📑 Table of Contents
- [common-testing](#common-testing)
- [e2e-runner](#e2e-runner)
- [e2e-testing](#e2e-testing)
- [generate-e2e-tests](#generate-e2e-tests)
- [generate-unit-tests](#generate-unit-tests)
- [mock-data-gen](#mock-data-gen)
- [research](#research)
- [review](#review)
- [review-test-coverage](#review-test-coverage)
- [tdd-guide](#tdd-guide)
- [tdd-workflow](#tdd-workflow)
- [test-edge-cases](#test-edge-cases)
- [testing](#testing)
- [testing-specialist](#testing-specialist)

---

### common-testing

> **Description**: Testing requirements: 80% coverage, TDD workflow, test types.
> **Input Needed**: `Context or Source Code`
> **Version**: `1.0.0` | **Last Updated**: `2026-03-22`
> **Tags**: `testing`

<details>
<summary>🔍 View Full Template: common-testing</summary>

````markdown


# Testing Requirements

## Minimum Test Coverage: 80%

Test Types (ALL required):
1. **Unit Tests** - Individual functions, utilities, components
2. **Integration Tests** - API endpoints, database operations
3. **E2E Tests** - Critical user flows (framework chosen per language)

## Test-Driven Development

MANDATORY workflow:
1. Write test first (RED)
2. Run test - it should FAIL
3. Write minimal implementation (GREEN)
4. Run test - it should PASS
5. Refactor (IMPROVE)
6. Verify coverage (80%+)

## Troubleshooting Test Failures

1. Use **tdd-guide** agent
2. Check test isolation
3. Verify mocks are correct
4. Fix implementation, not tests (unless tests are wrong)

## Agent Support

- **tdd-guide** - Use PROACTIVELY for new features, enforces write-tests-first

# Context/Input
{{args}}



````
</details>

---

### e2e-runner

> **Description**: End-to-end testing specialist using Vercel Agent Browser and Playwright for creating and maintaining reliable browser-based test suites.
> **Input Needed**: `Context or Source Code`
> **Version**: `1.0.0` | **Last Updated**: `2026-03-22`
> **Tags**: `testing`

<details>
<summary>🔍 View Full Template: e2e-runner</summary>

````markdown


# E2E Test Runner

You are an expert end-to-end testing specialist. Your mission is to ensure critical user journeys work correctly by creating, maintaining, and executing comprehensive E2E tests with proper artifact management and flaky test handling.

## Core Responsibilities

1. **Test Journey Creation** — Write tests for user flows (prefer Agent Browser, fallback to Playwright)
2. **Test Maintenance** — Keep tests up to date with UI changes
3. **Flaky Test Management** — Identify and quarantine unstable tests
4. **Artifact Management** — Capture screenshots, videos, traces
5. **CI/CD Integration** — Ensure tests run reliably in pipelines
6. **Test Reporting** — Generate HTML reports and JUnit XML

## Primary Tool: Agent Browser

**Prefer Agent Browser over raw Playwright** — Semantic selectors, AI-optimized, auto-waiting, built on Playwright.

```bash
# Setup
npm install -g agent-browser && agent-browser install

# Core workflow
agent-browser open https://example.com
agent-browser snapshot -i          # Get elements with refs [ref=e1]
agent-browser click @e1            # Click by ref
agent-browser fill @e2 "text"      # Fill input by ref
agent-browser wait visible @e5     # Wait for element
agent-browser screenshot result.png
```

## Fallback: Playwright

When Agent Browser isn't available, use Playwright directly.

```bash
npx playwright test                        # Run all E2E tests
npx playwright test tests/auth.spec.ts     # Run specific file
npx playwright test --headed               # See browser
npx playwright test --debug                # Debug with inspector
npx playwright test --trace on             # Run with trace
npx playwright show-report                 # View HTML report
```

## Workflow

### 1. Plan
- Identify critical user journeys (auth, core features, payments, CRUD)
- Define scenarios: happy path, edge cases, error cases
- Prioritize by risk: HIGH (financial, auth), MEDIUM (search, nav), LOW (UI polish)

### 2. Create
- Use Page Object Model (POM) pattern
- Prefer `data-testid` locators over CSS/XPath
- Add assertions at key steps
- Capture screenshots at critical points
- Use proper waits (never `waitForTimeout`)

### 3. Execute
- Run locally 3-5 times to check for flakiness
- Quarantine flaky tests with `test.fixme()` or `test.skip()`
- Upload artifacts to CI

## Key Principles

- **Use semantic locators**: `[data-testid="..."]` > CSS selectors > XPath
- **Wait for conditions, not time**: `waitForResponse()` > `waitForTimeout()`
- **Auto-wait built in**: `page.locator().click()` auto-waits; raw `page.click()` doesn't
- **Isolate tests**: Each test should be independent; no shared state
- **Fail fast**: Use `expect()` assertions at every key step
- **Trace on retry**: Configure `trace: 'on-first-retry'` for debugging failures

## Flaky Test Handling

```typescript
// Quarantine
test('flaky: market search', async ({ page }) => {
  test.fixme(true, 'Flaky - Issue #123')
})

// Identify flakiness
// npx playwright test --repeat-each=10
```

Common causes: race conditions (use auto-wait locators), network timing (wait for response), animation timing (wait for `networkidle`).

## Success Metrics

- All critical journeys passing (100%)
- Overall pass rate > 95%
- Flaky rate < 5%
- Test duration < 10 minutes
- Artifacts uploaded and accessible

## Reference

For detailed Playwright patterns, Page Object Model examples, configuration templates, CI/CD workflows, and artifact management strategies, see skill: `e2e-testing`.

---

**Remember**: E2E tests are your last line of defense before production. They catch integration issues that unit tests miss. Invest in stability, speed, and coverage.

# Context/Input
{{args}}



````
</details>

---

### e2e-testing

> **Description**: Playwright E2E testing patterns, Page Object Model, configuration, CI/CD integration, artifact management, and flaky test strategies.
> **Input Needed**: `Context or Source Code`
> **Version**: `1.0.0` | **Last Updated**: `2026-03-22`
> **Tags**: `testing`

<details>
<summary>🔍 View Full Template: e2e-testing</summary>

````markdown


# E2E Testing Patterns

Comprehensive Playwright patterns for building stable, fast, and maintainable E2E test suites.

## Test File Organization

```
tests/
├── e2e/
│   ├── auth/
│   │   ├── login.spec.ts
│   │   ├── logout.spec.ts
│   │   └── register.spec.ts
│   ├── features/
│   │   ├── browse.spec.ts
│   │   ├── search.spec.ts
│   │   └── create.spec.ts
│   └── api/
│       └── endpoints.spec.ts
├── fixtures/
│   ├── auth.ts
│   └── data.ts
└── playwright.config.ts
```

## Page Object Model (POM)

```typescript
import { Page, Locator } from '@playwright/test'

export class ItemsPage {
  readonly page: Page
  readonly searchInput: Locator
  readonly itemCards: Locator
  readonly createButton: Locator

  constructor(page: Page) {
    this.page = page
    this.searchInput = page.locator('[data-testid="search-input"]')
    this.itemCards = page.locator('[data-testid="item-card"]')
    this.createButton = page.locator('[data-testid="create-btn"]')
  }

  async goto() {
    await this.page.goto('/items')
    await this.page.waitForLoadState('networkidle')
  }

  async search(query: string) {
    await this.searchInput.fill(query)
    await this.page.waitForResponse(resp => resp.url().includes('/api/search'))
    await this.page.waitForLoadState('networkidle')
  }

  async getItemCount() {
    return await this.itemCards.count()
  }
}
```

## Test Structure

```typescript
import { test, expect } from '@playwright/test'
import { ItemsPage } from '../../pages/ItemsPage'

test.describe('Item Search', () => {
  let itemsPage: ItemsPage

  test.beforeEach(async ({ page }) => {
    itemsPage = new ItemsPage(page)
    await itemsPage.goto()
  })

  test('should search by keyword', async ({ page }) => {
    await itemsPage.search('test')

    const count = await itemsPage.getItemCount()
    expect(count).toBeGreaterThan(0)

    await expect(itemsPage.itemCards.first()).toContainText(/test/i)
    await page.screenshot({ path: 'artifacts/search-results.png' })
  })

  test('should handle no results', async ({ page }) => {
    await itemsPage.search('xyznonexistent123')

    await expect(page.locator('[data-testid="no-results"]')).toBeVisible()
    expect(await itemsPage.getItemCount()).toBe(0)
  })
})
```

## Playwright Configuration

```typescript
import { defineConfig, devices } from '@playwright/test'

export default defineConfig({
  testDir: './tests/e2e',
  fullyParallel: true,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 2 : 0,
  workers: process.env.CI ? 1 : undefined,
  reporter: [
    ['html', { outputFolder: 'playwright-report' }],
    ['junit', { outputFile: 'playwright-results.xml' }],
    ['json', { outputFile: 'playwright-results.json' }]
  ],
  use: {
    baseURL: process.env.BASE_URL || 'http://localhost:3000',
    trace: 'on-first-retry',
    screenshot: 'only-on-failure',
    video: 'retain-on-failure',
    actionTimeout: 10000,
    navigationTimeout: 30000,
  },
  projects: [
    { name: 'chromium', use: { ...devices['Desktop Chrome'] } },
    { name: 'firefox', use: { ...devices['Desktop Firefox'] } },
    { name: 'webkit', use: { ...devices['Desktop Safari'] } },
    { name: 'mobile-chrome', use: { ...devices['Pixel 5'] } },
  ],
  webServer: {
    command: 'npm run dev',
    url: 'http://localhost:3000',
    reuseExistingServer: !process.env.CI,
    timeout: 120000,
  },
})
```

## Flaky Test Patterns

### Quarantine

```typescript
test('flaky: complex search', async ({ page }) => {
  test.fixme(true, 'Flaky - Issue #123')
  // test code...
})

test('conditional skip', async ({ page }) => {
  test.skip(process.env.CI, 'Flaky in CI - Issue #123')
  // test code...
})
```

### Identify Flakiness

```bash
npx playwright test tests/search.spec.ts --repeat-each=10
npx playwright test tests/search.spec.ts --retries=3
```

### Common Causes & Fixes

**Race conditions:**
```typescript
// Bad: assumes element is ready
await page.click('[data-testid="button"]')

// Good: auto-wait locator
await page.locator('[data-testid="button"]').click()
```

**Network timing:**
```typescript
// Bad: arbitrary timeout
await page.waitForTimeout(5000)

// Good: wait for specific condition
await page.waitForResponse(resp => resp.url().includes('/api/data'))
```

**Animation timing:**
```typescript
// Bad: click during animation
await page.click('[data-testid="menu-item"]')

// Good: wait for stability
await page.locator('[data-testid="menu-item"]').waitFor({ state: 'visible' })
await page.waitForLoadState('networkidle')
await page.locator('[data-testid="menu-item"]').click()
```

## Artifact Management

### Screenshots

```typescript
await page.screenshot({ path: 'artifacts/after-login.png' })
await page.screenshot({ path: 'artifacts/full-page.png', fullPage: true })
await page.locator('[data-testid="chart"]').screenshot({ path: 'artifacts/chart.png' })
```

### Traces

```typescript
await browser.startTracing(page, {
  path: 'artifacts/trace.json',
  screenshots: true,
  snapshots: true,
})
// ... test actions ...
await browser.stopTracing()
```

### Video

```typescript
// In playwright.config.ts
use: {
  video: 'retain-on-failure',
  videosPath: 'artifacts/videos/'
}
```

## CI/CD Integration

```yaml
# .github/workflows/e2e.yml
name: E2E Tests
on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: 20
      - run: npm ci
      - run: npx playwright install --with-deps
      - run: npx playwright test
        env:
          BASE_URL: ${{ vars.STAGING_URL }}
      - uses: actions/upload-artifact@v4
        if: always()
        with:
          name: playwright-report
          path: playwright-report/
          retention-days: 30
```

## Test Report Template

```markdown
# E2E Test Report

**Date:** YYYY-MM-DD HH:MM
**Duration:** Xm Ys
**Status:** PASSING / FAILING

## Summary
- Total: X | Passed: Y (Z%) | Failed: A | Flaky: B | Skipped: C

## Failed Tests

### test-name
**File:** `tests/e2e/feature.spec.ts:45`
**Error:** Expected element to be visible
**Screenshot:** artifacts/failed.png
**Recommended Fix:** [description]

## Artifacts
- HTML Report: playwright-report/index.html
- Screenshots: artifacts/*.png
- Videos: artifacts/videos/*.webm
- Traces: artifacts/*.zip
```

## Wallet / Web3 Testing

```typescript
test('wallet connection', async ({ page, context }) => {
  // Mock wallet provider
  await context.addInitScript(() => {
    window.ethereum = {
      isMetaMask: true,
      request: async ({ method }) => {
        if (method === 'eth_requestAccounts')
          return ['0x1234567890123456789012345678901234567890']
        if (method === 'eth_chainId') return '0x1'
      }
    }
  })

  await page.goto('/')
  await page.locator('[data-testid="connect-wallet"]').click()
  await expect(page.locator('[data-testid="wallet-address"]')).toContainText('0x1234')
})
```

## Financial / Critical Flow Testing

```typescript
test('trade execution', async ({ page }) => {
  // Skip on production — real money
  test.skip(process.env.NODE_ENV === 'production', 'Skip on production')

  await page.goto('/markets/test-market')
  await page.locator('[data-testid="position-yes"]').click()
  await page.locator('[data-testid="trade-amount"]').fill('1.0')

  // Verify preview
  const preview = page.locator('[data-testid="trade-preview"]')
  await expect(preview).toContainText('1.0')

  // Confirm and wait for blockchain
  await page.locator('[data-testid="confirm-trade"]').click()
  await page.waitForResponse(
    resp => resp.url().includes('/api/trade') && resp.status() === 200,
    { timeout: 30000 }
  )

  await expect(page.locator('[data-testid="trade-success"]')).toBeVisible()
})
```

# Context/Input
{{args}}



````
</details>

---

### generate-e2e-tests

> **Description**: Create end-to-end tests.
> **Input Needed**: `Code to Test`
> **Version**: `1.0.0` | **Last Updated**: `2026-03-22`
> **Tags**: `testing`

<details>
<summary>🔍 View Full Template: generate-e2e-tests</summary>

````markdown


# Generate End-to-End Tests

Please create comprehensive end-to-end tests for the following application/feature:

{{args}}

  ## Test Framework Considerations

Choose appropriate E2E testing framework:
- Web: Playwright, Cypress, Selenium
- Mobile: Appium, Detox
- API: Supertest, REST Assured
- Desktop: TestComplete, WinAppDriver

  ## E2E Test Structure

  ### 1. User Journey Tests

Test complete user workflows from start to finish:
```javascript
test('User can complete signup and login flow', async ({ page }) => {
  // Navigate to signup
  await page.goto('/signup');

  // Fill signup form
  await page.fill('[name="email"]', 'user@example.com');
  await page.fill('[name="password"]', 'SecurePass123');
  await page.click('button[type="submit"]');

  // Verify redirect to dashboard
  await expect(page).toHaveURL('/dashboard');

  // Verify welcome message
  await expect(page.locator('.welcome')).toContainText('Welcome');
});
```

  ### 2. Test Categories

  #### Critical User Paths
- User registration and authentication
- Core business workflows
- Payment/checkout processes
- Data submission and retrieval

  #### Cross-Browser/Platform
- Test on major browsers (Chrome, Firefox, Safari, Edge)
- Test on different devices (desktop, tablet, mobile)
- Test on different OS (Windows, macOS, Linux)

  #### Integration Points
- Third-party service integrations
- API interactions
- Database operations
- External system communications

  ### 3. Test Patterns

  #### Page Object Model
```javascript
class LoginPage {
  constructor(page) {
    this.page = page;
    this.emailInput = page.locator('[name="email"]');
    this.passwordInput = page.locator('[name="password"]');
    this.submitButton = page.locator('button[type="submit"]');
  }

  async login(email, password) {
    await this.emailInput.fill(email);
    await this.passwordInput.fill(password);
    await this.submitButton.click();
  }
}

test('user can login', async ({ page }) => {
  const loginPage = new LoginPage(page);
  await page.goto('/login');
  await loginPage.login('user@example.com', 'password');
  await expect(page).toHaveURL('/dashboard');
});
```

  #### Setup and Teardown
```javascript
test.beforeEach(async ({ page }) => {
  // Clear cookies and local storage
  await page.context().clearCookies();
  await page.evaluate(() => localStorage.clear());

  // Navigate to starting point
  await page.goto('/');
});

test.afterEach(async ({ page }, testInfo) => {
  // Screenshot on failure
  if (testInfo.status !== 'passed') {
    await page.screenshot({
      path: `test-results/${testInfo.title}-failure.png`
    });
  }
});
```

  ### 4. Test Scenarios to Cover

  #### Authentication & Authorization
- User registration with valid/invalid data
- Login with correct/incorrect credentials
- Logout functionality
- Password reset flow
- Session management
- Access control (authorized vs unauthorized users)

  #### CRUD Operations
- Create new records
- Read/view records
- Update existing records
- Delete records
- List/search records
- Pagination

  #### Forms & Validation
- Submit valid forms
- Submit invalid forms
- Field validation messages
- Required field enforcement
- Format validation (email, phone, etc.)
- File uploads

  #### Navigation
- Menu navigation
- Breadcrumb navigation
- Back/forward browser buttons
- Deep linking
- Redirects

  #### Search & Filters
- Search with various queries
- Apply filters
- Sort results
- Pagination of results
- Empty results handling

  #### Error Handling
- Network errors
- Server errors (500, 503)
- Not found (404)
- Validation errors
- Timeout scenarios

  ### 5. Waiting Strategies

```javascript
// Wait for element
await page.waitForSelector('.data-loaded');

// Wait for navigation
await page.waitForNavigation();

// Wait for API response
await page.waitForResponse(response =>
  response.url().includes('/api/data')
);

// Wait for condition
await page.waitForFunction(() =>
  document.querySelector('.loading') === null
);

// Custom timeout
await page.waitForSelector('.slow-element', { timeout: 10000 });
```

  ### 6. Data Management

  #### Test Data Setup
```javascript
test.beforeEach(async ({ request }) => {
  // Create test user via API
  await request.post('/api/users', {
    data: {
      email: 'test@example.com',
      name: 'Test User'
    }
  });
});
```

  #### Test Data Cleanup
```javascript
test.afterEach(async ({ request }) => {
  // Delete test data
  await request.delete('/api/users/test@example.com');
});
```

  ### 7. Assertions

```javascript
// Element visibility
await expect(page.locator('.success-message')).toBeVisible();

// Text content
await expect(page.locator('h1')).toHaveText('Dashboard');

// URL
await expect(page).toHaveURL('/dashboard');

// Element count
await expect(page.locator('.item')).toHaveCount(5);

// Attribute
await expect(page.locator('button')).toHaveAttribute('disabled');

// Screenshot comparison
await expect(page).toHaveScreenshot('homepage.png');
```

  ### 8. API Testing in E2E

```javascript
test('should create user via API and verify in UI', async ({ request, page }) => {
  // Create via API
  const response = await request.post('/api/users', {
    data: { name: 'John Doe', email: 'john@example.com' }
  });
  expect(response.ok()).toBeTruthy();

  const user = await response.json();

  // Verify in UI
  await page.goto(`/users/${user.id}`);
  await expect(page.locator('.user-name')).toHaveText('John Doe');
});
```

  ### 9. Mobile/Responsive Testing

```javascript
test('should work on mobile', async ({ page }) => {
  // Set viewport to mobile
  await page.setViewportSize({ width: 375, height: 667 });

  await page.goto('/');

  // Open mobile menu
  await page.click('.mobile-menu-toggle');
  await expect(page.locator('.mobile-menu')).toBeVisible();
});
```

  ### 10. Performance Checks

```javascript
test('page should load within 3 seconds', async ({ page }) => {
  const start = Date.now();
  await page.goto('/');
  await page.waitForLoadState('networkidle');
  const loadTime = Date.now() - start;

  expect(loadTime).toBeLessThan(3000);
});
```

  ## Best Practices

1. **Stability**: Use reliable selectors (data-testid preferred)
2. **Independence**: Tests should not depend on each other
3. **Cleanup**: Always clean up test data
4. **Waits**: Use explicit waits, avoid arbitrary sleeps
5. **Retries**: Configure retries for flaky tests
6. **Parallelization**: Run tests in parallel when possible
7. **Screenshots**: Capture screenshots on failure
8. **Videos**: Record videos for debugging
9. **Logs**: Capture console logs
10. **Reports**: Generate comprehensive test reports

  ## Output Format

Provide:
1. Complete E2E test suite
2. Page Object Models (if applicable)
3. Setup and teardown code
4. Test data factories/fixtures
5. Configuration suggestions
6. Clear test descriptions
7. Comments for complex interactions

Generate a complete, production-ready E2E test suite following these best practices.



````
</details>

---

### generate-unit-tests

> **Description**: Create unit tests for code.
> **Input Needed**: `Code to Test`
> **Version**: `1.0.0` | **Last Updated**: `2026-03-22`
> **Tags**: `testing`

<details>
<summary>🔍 View Full Template: generate-unit-tests</summary>

````markdown


# Generate Unit Tests

Please create comprehensive unit tests for the following code:

{{args}}

  ## Test Framework Considerations

Adapt to the appropriate testing framework:
- JavaScript/TypeScript: Jest, Vitest, Mocha
- Python: pytest, unittest
- Java: JUnit
- C#: xUnit, NUnit
- Go: testing package
- Ruby: RSpec
- PHP: PHPUnit

  ## Test Structure

  ### 1. Test Organization

```
describe('FunctionName' or 'ClassName', () => {
  describe('methodName', () => {
    it('should handle normal case', () => {});
    it('should handle edge case', () => {});
    it('should throw error for invalid input', () => {});
  });
});
```

  ### 2. Test Coverage Areas

  #### Happy Path Tests
Test normal, expected behavior:
- Valid inputs with expected outputs
- Common use cases
- Typical workflows

  #### Edge Cases
Test boundary conditions:
- Empty inputs (null, undefined, empty string, empty array)
- Zero values
- Negative numbers
- Very large numbers
- Maximum/minimum values
- Single element collections

  #### Error Cases
Test error handling:
- Invalid inputs
- Type mismatches
- Out of range values
- Missing required parameters
- Malformed data

  #### Boundary Conditions
- First and last elements
- Off-by-one scenarios
- Limits and thresholds

  ### 3. Test Patterns

  #### Arrange-Act-Assert (AAA)
```javascript
it('should calculate total with discount', () => {
  // Arrange
  const price = 100;
  const discount = 0.2;

  // Act
  const result = calculateTotal(price, discount);

  // Assert
  expect(result).toBe(80);
});
```

  #### Given-When-Then (BDD style)
```javascript
it('should calculate total with discount', () => {
  // Given
  const price = 100;
  const discount = 0.2;

  // When
  const result = calculateTotal(price, discount);

  // Then
  expect(result).toBe(80);
});
```

  ### 4. Test Types to Include

  #### Basic Functionality Tests
```javascript
it('should return correct value for valid input', () => {
  expect(add(2, 3)).toBe(5);
});
```

  #### Parameterized Tests
```javascript
it.each([
  [2, 3, 5],
  [0, 0, 0],
  [-1, 1, 0],
  [100, 200, 300]
])('should add %i and %i to equal %i', (a, b, expected) => {
  expect(add(a, b)).toBe(expected);
});
```

  #### Async Tests
```javascript
it('should fetch user data', async () => {
  const user = await fetchUser(1);
  expect(user.id).toBe(1);
});
```

  #### Mock/Stub Tests
```javascript
it('should call API with correct parameters', () => {
  const mockApi = jest.fn();
  service.setApi(mockApi);
  service.fetchData(123);
  expect(mockApi).toHaveBeenCalledWith(123);
});
```

  #### State Tests
```javascript
it('should update state correctly', () => {
  const obj = new MyClass();
  obj.setValue(10);
  expect(obj.getValue()).toBe(10);
});
```

  ### 5. Setup and Teardown

```javascript
describe('Database operations', () => {
  beforeAll(() => {
    // Setup before all tests
  });

  beforeEach(() => {
    // Setup before each test
  });

  afterEach(() => {
    // Cleanup after each test
  });

  afterAll(() => {
    // Cleanup after all tests
  });
});
```

  ### 6. Test Naming

Use descriptive names that explain:
- What is being tested
- Under what conditions
- What the expected result is

**Good names**:
- `should return empty array when no items match filter`
- `should throw error when input is negative`
- `should call callback with correct parameters`

**Bad names**:
- `test1`
- `it works`
- `should work correctly`

  ## Test Quality Guidelines

1. **Independence**: Tests should not depend on each other
2. **Repeatability**: Tests should produce same results every time
3. **Fast**: Unit tests should run quickly
4. **Isolated**: Use mocks/stubs for external dependencies
5. **Clear**: Test intent should be obvious
6. **Comprehensive**: Cover all code paths
7. **Maintainable**: Easy to update when code changes

  ## Coverage Goals

Aim to test:
- All public methods/functions
- All branches (if/else)
- All error paths
- All edge cases
- All important combinations

  ## Output Format

Provide:
1. Complete test suite with all necessary imports
2. Setup/teardown if needed
3. Mock configurations
4. Clear test descriptions
5. Comments explaining complex test scenarios
6. Assertion explanations where helpful

Generate a complete, production-ready test suite following these best practices.



````
</details>

---

### mock-data-gen

> **Description**: Create realistic JSON/CSV mock data schemas for testing.
> **Input Needed**: `Context or Source Code`
> **Version**: `1.0.0` | **Last Updated**: `2026-03-22`
> **Tags**: `testing`

<details>
<summary>🔍 View Full Template: mock-data-gen</summary>

````markdown


# Mock Data Generator

Please generate realistic, diverse mock data for testing purposes based on the following schema or requirements:

```
{{args}}
```

Please follow these guidelines:

  ## 1. Realism
- Do not use generic placeholders like "test1", "test2". Use realistic names, addresses, dates, and text strings.
- Ensure logical consistency (e.g., if a user is from the UK, their phone number should match UK formats).

  ## 2. Edge Cases
Include at least a few records that contain:
- Null or missing optional fields.
- Extremely long strings.
- Special characters / Unicode (e.g., accents, emojis).
- Boundary values for numbers and dates.

  ## 3. Format
Provide the output in valid, well-formatted JSON (an array of objects) unless CSV is explicitly requested.



````
</details>

---

### research

> **Description**: Research Context.
> **Input Needed**: `Context or Source Code`
> **Version**: `1.0.0` | **Last Updated**: `2026-03-22`
> **Tags**: `testing`

<details>
<summary>🔍 View Full Template: research</summary>

````markdown


# Research Context

Mode: Exploration, investigation, learning
Focus: Understanding before acting

## Behavior
- Read widely before concluding
- Ask clarifying questions
- Document findings as you go
- Don't write code until understanding is clear

## Research Process
1. Understand the question
2. Explore relevant code/docs
3. Form hypothesis
4. Verify with evidence
5. Summarize findings

## Tools to favor
- Read for understanding code
- Grep, Glob for finding patterns
- WebSearch, WebFetch for external docs
- Task with Explore agent for codebase questions

## Output
Findings first, recommendations second

# Context/Input
{{args}}



````
</details>

---

### review

> **Description**: Code Review Context.
> **Input Needed**: `Context or Source Code`
> **Version**: `1.0.0` | **Last Updated**: `2026-03-22`
> **Tags**: `testing`

<details>
<summary>🔍 View Full Template: review</summary>

````markdown


# Code Review Context

Mode: PR review, code analysis
Focus: Quality, security, maintainability

## Behavior
- Read thoroughly before commenting
- Prioritize issues by severity (critical > high > medium > low)
- Suggest fixes, don't just point out problems
- Check for security vulnerabilities

## Review Checklist
- [ ] Logic errors
- [ ] Edge cases
- [ ] Error handling
- [ ] Security (injection, auth, secrets)
- [ ] Performance
- [ ] Readability
- [ ] Test coverage

## Output Format
Group findings by file, severity first

# Context/Input
{{args}}



````
</details>

---

### review-test-coverage

> **Description**: Analyze test coverage gaps.
> **Input Needed**: `Code to Test`
> **Version**: `1.0.0` | **Last Updated**: `2026-03-22`
> **Tags**: `testing`

<details>
<summary>🔍 View Full Template: review-test-coverage</summary>

````markdown


# Test Coverage Analysis

Please analyze test coverage for the following code and identify gaps:

{{args}}

  ## Analysis Areas

  ### 1. Code Coverage Metrics

  #### Line Coverage
- Percentage of lines executed
- Uncovered lines identification
- Critical uncovered lines

  #### Branch Coverage
- Percentage of branches tested
- Uncovered if/else branches
- Uncovered switch cases
- Uncovered ternary operators
- Short-circuit evaluations

  #### Function Coverage
- Percentage of functions tested
- Untested functions
- Partially tested functions

  #### Statement Coverage
- Individual statement execution
- Dead code identification

  ### 2. Coverage by Category

  #### Happy Path Coverage
✓ **Covered:**
- Normal operation scenarios
- Expected inputs
- Standard workflows

✗ **Missing:**
- Additional common use cases
- Variations in normal flow

  #### Error Path Coverage
✓ **Covered:**
- Handled exceptions
- Validation errors

✗ **Missing:**
- Unhandled exceptions
- Edge case errors
- System errors
- Network failures

  #### Edge Case Coverage
✓ **Covered:**
- Empty inputs
- Null/undefined
- Basic boundaries

✗ **Missing:**
- Extreme values
- Resource limits
- Concurrent access
- State combinations

  ### 3. Detailed Gap Analysis

For each uncovered area, provide:

  #### Gap Description
What functionality is not tested

  #### Risk Level
- **Critical**: Could cause data loss, security issues, or system failure
- **High**: Could cause incorrect behavior or crashes
- **Medium**: Could cause user-facing issues
- **Low**: Minor issues or unlikely scenarios

  #### Impact Assessment
What could go wrong if this remains untested

  #### Test Recommendation
Specific tests that should be added

  ### 4. Coverage Report Structure

```markdown
## Current Coverage Summary

| Metric | Percentage | Status |
|--------|------------|--------|
| Lines | 75% | 🟡 Fair |
| Branches | 60% | 🔴 Poor |
| Functions | 85% | 🟢 Good |
| Statements | 73% | 🟡 Fair |

### Coverage Goals
- Lines: 80%+ (current: 75%)
- Branches: 75%+ (current: 60%)
- Functions: 90%+ (current: 85%)
- Statements: 80%+ (current: 73%)

## Detailed Gap Analysis

### 1. Uncovered Functions (15%)

#### `handleError(error)` - Lines 45-60
**Risk**: High
**Issue**: Error handling logic is completely untested
**Tests Needed**:
- Test with different error types
- Test error logging
- Test error recovery
- Test error propagation

#### `parseDate(dateString)` - Lines 120-135
**Risk**: Medium
**Issue**: Date parsing edge cases not tested
**Tests Needed**:
- Invalid date formats
- Null/undefined inputs
- Future dates
- Leap year dates

### 2. Uncovered Branches (40%)

#### File: `user.js`, Lines 78-82
```javascript
if (user.age > 18) {
  // ✓ Tested
} else {
  // ✗ Not tested
}
```
**Risk**: Medium
**Tests Needed**: Add test for users under 18

#### File: `payment.js`, Lines 145-152
```javascript
switch (paymentMethod) {
  case 'credit': // ✓ Tested
    break;
  case 'debit': // ✗ Not tested
    break;
  case 'paypal': // ✗ Not tested
    break;
  default: // ✗ Not tested
}
```
**Risk**: Critical
**Tests Needed**: Test all payment methods

### 3. Untested Edge Cases

#### Empty Array Handling
**Location**: Lines 200-210
**Risk**: Medium
**Current**: Only non-empty arrays tested
**Add**: Tests for empty arrays

#### Null/Undefined Inputs
**Location**: Throughout
**Risk**: High
**Current**: Assumes valid inputs
**Add**: Null safety tests for all public functions

### 4. Missing Integration Tests

#### Database Operations
**Coverage**: 0%
**Risk**: High
**Needed**:
- Connection failure handling
- Transaction rollback
- Query timeout
- Concurrent access

#### API Integrations
**Coverage**: 30%
**Risk**: High
**Needed**:
- Error response handling
- Timeout scenarios
- Rate limiting
- Retry logic

### 5. Missing Scenario Tests

#### Concurrent Operations
**Coverage**: 0%
**Risk**: Critical
**Needed**: Race condition tests

#### Resource Exhaustion
**Coverage**: 0%
**Risk**: High
**Needed**: Memory/connection limit tests

#### State Transitions
**Coverage**: 40%
**Risk**: Medium
**Needed**: Invalid state transition tests

## Recommendations

### Priority 1 (Critical) - Implement Immediately
1. Test error handling in `handleError()` function
2. Test all payment method branches
3. Add concurrent operation tests
4. Test database failure scenarios

### Priority 2 (High) - Implement This Sprint
1. Test `parseDate()` edge cases
2. Add null/undefined checks for all public APIs
3. Test API integration error paths
4. Add resource exhaustion tests

### Priority 3 (Medium) - Next Sprint
1. Test else branches in user age validation
2. Test empty array handling
3. Test state transition edge cases
4. Improve boundary value testing

### Priority 4 (Low) - Backlog
1. Test default cases in switches
2. Add performance benchmarks
3. Test obscure edge cases

## Test Code Examples

### Example 1: Error Handling Test
```javascript
describe('handleError', () => {
  it('should log error with correct severity', () => {
    const error = new Error('Test error');
    handleError(error);
    expect(logger.error).toHaveBeenCalledWith(error);
  });

  it('should handle null error gracefully', () => {
    expect(() => handleError(null)).not.toThrow();
  });
});
```

### Example 2: Branch Coverage Test
```javascript
describe('payment processing', () => {
  it('should handle debit card payment', () => {
    const result = processPayment('debit', 100);
    expect(result.method).toBe('debit');
  });

  it('should handle paypal payment', () => {
    const result = processPayment('paypal', 100);
    expect(result.method).toBe('paypal');
  });

  it('should reject invalid payment method', () => {
    expect(() => processPayment('invalid', 100)).toThrow();
  });
});
```

## Coverage Improvement Plan

### Phase 1 (Week 1)
- Add critical missing tests
- Bring branch coverage to 70%
- Test all error paths

### Phase 2 (Week 2)
- Add high-priority tests
- Bring line coverage to 80%
- Add integration tests

### Phase 3 (Week 3)
- Add medium-priority tests
- Achieve 85% total coverage
- Add scenario tests

### Phase 4 (Ongoing)
- Maintain coverage as code evolves
- Add tests for new features
- Refine existing tests

## Metrics Tracking

Track these metrics over time:
- Coverage percentage by type
- Number of uncovered critical paths
- Test execution time
- Test flakiness rate
- Code churn vs test churn
```

Generate a detailed coverage analysis following this structure.



````
</details>

---

### tdd-guide

> **Description**: TDD specialist enforcing the write-tests-first methodology for new features, bug fixes, and refactoring with high coverage standards.
> **Input Needed**: `Context or Source Code`
> **Version**: `1.0.0` | **Last Updated**: `2026-03-22`
> **Tags**: `testing`

<details>
<summary>🔍 View Full Template: tdd-guide</summary>

````markdown


You are a Test-Driven Development (TDD) specialist who ensures all code is developed test-first with comprehensive coverage.

## Your Role

- Enforce tests-before-code methodology
- Guide through Red-Green-Refactor cycle
- Ensure 80%+ test coverage
- Write comprehensive test suites (unit, integration, E2E)
- Catch edge cases before implementation

## TDD Workflow

### 1. Write Test First (RED)
Write a failing test that describes the expected behavior.

### 2. Run Test -- Verify it FAILS
```bash
npm test
```

### 3. Write Minimal Implementation (GREEN)
Only enough code to make the test pass.

### 4. Run Test -- Verify it PASSES

### 5. Refactor (IMPROVE)
Remove duplication, improve names, optimize -- tests must stay green.

### 6. Verify Coverage
```bash
npm run test:coverage
# Required: 80%+ branches, functions, lines, statements
```

## Test Types Required

| Type | What to Test | When |
|------|-------------|------|
| **Unit** | Individual functions in isolation | Always |
| **Integration** | API endpoints, database operations | Always |
| **E2E** | Critical user flows (Playwright) | Critical paths |

## Edge Cases You MUST Test

1. **Null/Undefined** input
2. **Empty** arrays/strings
3. **Invalid types** passed
4. **Boundary values** (min/max)
5. **Error paths** (network failures, DB errors)
6. **Race conditions** (concurrent operations)
7. **Large data** (performance with 10k+ items)
8. **Special characters** (Unicode, emojis, SQL chars)

## Test Anti-Patterns to Avoid

- Testing implementation details (internal state) instead of behavior
- Tests depending on each other (shared state)
- Asserting too little (passing tests that don't verify anything)
- Not mocking external dependencies (Supabase, Redis, OpenAI, etc.)

## Quality Checklist

- [ ] All public functions have unit tests
- [ ] All API endpoints have integration tests
- [ ] Critical user flows have E2E tests
- [ ] Edge cases covered (null, empty, invalid)
- [ ] Error paths tested (not just happy path)
- [ ] Mocks used for external dependencies
- [ ] Tests are independent (no shared state)
- [ ] Assertions are specific and meaningful
- [ ] Coverage is 80%+

For detailed mocking patterns and framework-specific examples, see `skill: tdd-workflow`.

## v1.8 Eval-Driven TDD Addendum

Integrate eval-driven development into TDD flow:

1. Define capability + regression evals before implementation.
2. Run baseline and capture failure signatures.
3. Implement minimum passing change.
4. Re-run tests and evals; report pass@1 and pass@3.

Release-critical paths should target pass^3 stability before merge.

# Context/Input
{{args}}



````
</details>

---

### tdd-workflow

> **Description**: Enforces TDD with 80%+ coverage for unit, integration, and E2E tests during feature development, bug fixes, and refactors.
> **Input Needed**: `Context or Source Code`
> **Version**: `1.0.0` | **Last Updated**: `2026-03-22`
> **Tags**: `testing`

<details>
<summary>🔍 View Full Template: tdd-workflow</summary>

````markdown


# Test-Driven Development Workflow

This skill ensures all code development follows TDD principles with comprehensive test coverage.

## When to Activate

- Writing new features or functionality
- Fixing bugs or issues
- Refactoring existing code
- Adding API endpoints
- Creating new components

## Core Principles

### 1. Tests BEFORE Code
ALWAYS write tests first, then implement code to make tests pass.

### 2. Coverage Requirements
- Minimum 80% coverage (unit + integration + E2E)
- All edge cases covered
- Error scenarios tested
- Boundary conditions verified

### 3. Test Types

#### Unit Tests
- Individual functions and utilities
- Component logic
- Pure functions
- Helpers and utilities

#### Integration Tests
- API endpoints
- Database operations
- Service interactions
- External API calls

#### E2E Tests (Playwright)
- Critical user flows
- Complete workflows
- Browser automation
- UI interactions

## TDD Workflow Steps

### Step 1: Write User Journeys
```
As a [role], I want to [action], so that [benefit]

Example:
As a user, I want to search for markets semantically,
so that I can find relevant markets even without exact keywords.
```

### Step 2: Generate Test Cases
For each user journey, create comprehensive test cases:

```typescript
describe('Semantic Search', () => {
  it('returns relevant markets for query', async () => {
    // Test implementation
  })

  it('handles empty query gracefully', async () => {
    // Test edge case
  })

  it('falls back to substring search when Redis unavailable', async () => {
    // Test fallback behavior
  })

  it('sorts results by similarity score', async () => {
    // Test sorting logic
  })
})
```

### Step 3: Run Tests (They Should Fail)
```bash
npm test
# Tests should fail - we haven't implemented yet
```

### Step 4: Implement Code
Write minimal code to make tests pass:

```typescript
// Implementation guided by tests
export async function searchMarkets(query: string) {
  // Implementation here
}
```

### Step 5: Run Tests Again
```bash
npm test
# Tests should now pass
```

### Step 6: Refactor
Improve code quality while keeping tests green:
- Remove duplication
- Improve naming
- Optimize performance
- Enhance readability

### Step 7: Verify Coverage
```bash
npm run test:coverage
# Verify 80%+ coverage achieved
```

## Testing Patterns

### Unit Test Pattern (Jest/Vitest)
```typescript
import { render, screen, fireEvent } from '@testing-library/react'
import { Button } from './Button'

describe('Button Component', () => {
  it('renders with correct text', () => {
    render(<Button>Click me</Button>)
    expect(screen.getByText('Click me')).toBeInTheDocument()
  })

  it('calls onClick when clicked', () => {
    const handleClick = jest.fn()
    render(<Button onClick={handleClick}>Click</Button>)

    fireEvent.click(screen.getByRole('button'))

    expect(handleClick).toHaveBeenCalledTimes(1)
  })

  it('is disabled when disabled prop is true', () => {
    render(<Button disabled>Click</Button>)
    expect(screen.getByRole('button')).toBeDisabled()
  })
})
```

### API Integration Test Pattern
```typescript
import { NextRequest } from 'next/server'
import { GET } from './route'

describe('GET /api/markets', () => {
  it('returns markets successfully', async () => {
    const request = new NextRequest('http://localhost/api/markets')
    const response = await GET(request)
    const data = await response.json()

    expect(response.status).toBe(200)
    expect(data.success).toBe(true)
    expect(Array.isArray(data.data)).toBe(true)
  })

  it('validates query parameters', async () => {
    const request = new NextRequest('http://localhost/api/markets?limit=invalid')
    const response = await GET(request)

    expect(response.status).toBe(400)
  })

  it('handles database errors gracefully', async () => {
    // Mock database failure
    const request = new NextRequest('http://localhost/api/markets')
    // Test error handling
  })
})
```

### E2E Test Pattern (Playwright)
```typescript
import { test, expect } from '@playwright/test'

test('user can search and filter markets', async ({ page }) => {
  // Navigate to markets page
  await page.goto('/')
  await page.click('a[href="/markets"]')

  // Verify page loaded
  await expect(page.locator('h1')).toContainText('Markets')

  // Search for markets
  await page.fill('input[placeholder="Search markets"]', 'election')

  // Wait for debounce and results
  await page.waitForTimeout(600)

  // Verify search results displayed
  const results = page.locator('[data-testid="market-card"]')
  await expect(results).toHaveCount(5, { timeout: 5000 })

  // Verify results contain search term
  const firstResult = results.first()
  await expect(firstResult).toContainText('election', { ignoreCase: true })

  // Filter by status
  await page.click('button:has-text("Active")')

  // Verify filtered results
  await expect(results).toHaveCount(3)
})

test('user can create a new market', async ({ page }) => {
  // Login first
  await page.goto('/creator-dashboard')

  // Fill market creation form
  await page.fill('input[name="name"]', 'Test Market')
  await page.fill('textarea[name="description"]', 'Test description')
  await page.fill('input[name="endDate"]', '2025-12-31')

  // Submit form
  await page.click('button[type="submit"]')

  // Verify success message
  await expect(page.locator('text=Market created successfully')).toBeVisible()

  // Verify redirect to market page
  await expect(page).toHaveURL(/\/markets\/test-market/)
})
```

## Test File Organization

```
src/
├── components/
│   ├── Button/
│   │   ├── Button.tsx
│   │   ├── Button.test.tsx          # Unit tests
│   │   └── Button.stories.tsx       # Storybook
│   └── MarketCard/
│       ├── MarketCard.tsx
│       └── MarketCard.test.tsx
├── app/
│   └── api/
│       └── markets/
│           ├── route.ts
│           └── route.test.ts         # Integration tests
└── e2e/
    ├── markets.spec.ts               # E2E tests
    ├── trading.spec.ts
    └── auth.spec.ts
```

## Mocking External Services

### Supabase Mock
```typescript
jest.mock('@/lib/supabase', () => ({
  supabase: {
    from: jest.fn(() => ({
      select: jest.fn(() => ({
        eq: jest.fn(() => Promise.resolve({
          data: [{ id: 1, name: 'Test Market' }],
          error: null
        }))
      }))
    }))
  }
}))
```

### Redis Mock
```typescript
jest.mock('@/lib/redis', () => ({
  searchMarketsByVector: jest.fn(() => Promise.resolve([
    { slug: 'test-market', similarity_score: 0.95 }
  ])),
  checkRedisHealth: jest.fn(() => Promise.resolve({ connected: true }))
}))
```

### OpenAI Mock
```typescript
jest.mock('@/lib/openai', () => ({
  generateEmbedding: jest.fn(() => Promise.resolve(
    new Array(1536).fill(0.1) // Mock 1536-dim embedding
  ))
}))
```

## Test Coverage Verification

### Run Coverage Report
```bash
npm run test:coverage
```

### Coverage Thresholds
```json
{
  "jest": {
    "coverageThresholds": {
      "global": {
        "branches": 80,
        "functions": 80,
        "lines": 80,
        "statements": 80
      }
    }
  }
}
```

## Common Testing Mistakes to Avoid

### ❌ WRONG: Testing Implementation Details
```typescript
// Don't test internal state
expect(component.state.count).toBe(5)
```

### ✅ CORRECT: Test User-Visible Behavior
```typescript
// Test what users see
expect(screen.getByText('Count: 5')).toBeInTheDocument()
```

### ❌ WRONG: Brittle Selectors
```typescript
// Breaks easily
await page.click('.css-class-xyz')
```

### ✅ CORRECT: Semantic Selectors
```typescript
// Resilient to changes
await page.click('button:has-text("Submit")')
await page.click('[data-testid="submit-button"]')
```

### ❌ WRONG: No Test Isolation
```typescript
// Tests depend on each other
test('creates user', () => { /* ... */ })
test('updates same user', () => { /* depends on previous test */ })
```

### ✅ CORRECT: Independent Tests
```typescript
// Each test sets up its own data
test('creates user', () => {
  const user = createTestUser()
  // Test logic
})

test('updates user', () => {
  const user = createTestUser()
  // Update logic
})
```

## Continuous Testing

### Watch Mode During Development
```bash
npm test -- --watch
# Tests run automatically on file changes
```

### Pre-Commit Hook
```bash
# Runs before every commit
npm test && npm run lint
```

### CI/CD Integration
```yaml
# GitHub Actions
- name: Run Tests
  run: npm test -- --coverage
- name: Upload Coverage
  uses: codecov/codecov-action@v3
```

## Best Practices

1. **Write Tests First** - Always TDD
2. **One Assert Per Test** - Focus on single behavior
3. **Descriptive Test Names** - Explain what's tested
4. **Arrange-Act-Assert** - Clear test structure
5. **Mock External Dependencies** - Isolate unit tests
6. **Test Edge Cases** - Null, undefined, empty, large
7. **Test Error Paths** - Not just happy paths
8. **Keep Tests Fast** - Unit tests < 50ms each
9. **Clean Up After Tests** - No side effects
10. **Review Coverage Reports** - Identify gaps

## Success Metrics

- 80%+ code coverage achieved
- All tests passing (green)
- No skipped or disabled tests
- Fast test execution (< 30s for unit tests)
- E2E tests cover critical user flows
- Tests catch bugs before production

---

**Remember**: Tests are not optional. They are the safety net that enables confident refactoring, rapid development, and production reliability.

# Context/Input
{{args}}



````
</details>

---

### test-edge-cases

> **Description**: Identify and test edge cases.
> **Input Needed**: `Code to Test`
> **Version**: `1.0.0` | **Last Updated**: `2026-03-22`
> **Tags**: `testing`

<details>
<summary>🔍 View Full Template: test-edge-cases</summary>

````markdown


# Identify Edge Cases

Please identify comprehensive edge cases for the following code or feature:

{{args}}

  ## Edge Case Categories

  ### 1. Boundary Values

  #### Numeric Boundaries
- Zero (0)
- Negative numbers (-1, -100)
- Positive numbers (1, 100)
- Maximum values (Integer.MAX_VALUE, Number.MAX_SAFE_INTEGER)
- Minimum values (Integer.MIN_VALUE, Number.MIN_SAFE_INTEGER)
- Infinity and -Infinity
- NaN (Not a Number)
- Floating point precision issues (0.1 + 0.2)
- Very large numbers
- Very small numbers (near zero)

  #### String Boundaries
- Empty string ("")
- Single character
- Very long strings (1MB+)
- Strings with special characters
- Unicode characters and emojis
- Null bytes (\0)
- Strings with only whitespace
- Leading/trailing whitespace

  #### Collection Boundaries
- Empty array/list ([])
- Single element array
- Very large arrays (millions of elements)
- Null or undefined collections
- Nested empty collections

  #### Date/Time Boundaries
- Epoch time (1970-01-01)
- Very old dates (1900-01-01)
- Future dates (2100-01-01)
- Leap years
- End of year/month
- Daylight saving time transitions
- Different time zones
- Invalid dates (February 30)

  ### 2. Input Validation

  #### Type Mismatches
- Passing string when number expected
- Passing null when object expected
- Passing undefined
- Passing array when string expected
- Mixed types in collections

  #### Format Issues
- Invalid email formats
- Invalid phone numbers
- Invalid URLs
- Invalid JSON
- Invalid XML
- Malformed data structures

  #### Missing Data
- Required fields missing
- Null values
- Undefined values
- Empty objects
- Partial data

  ### 3. State-Related Edge Cases

  #### Order Dependencies
- Operations in different order
- Concurrent operations
- Race conditions
- First-time vs subsequent operations

  #### Lifecycle Edge Cases
- Before initialization
- During initialization
- After cleanup/disposal
- Repeated initialization
- Multiple cleanups

  #### State Combinations
- Combinations of flags/settings
- Conflicting states
- Invalid state transitions

  ### 4. Concurrency Edge Cases

  #### Threading Issues
- Multiple simultaneous requests
- Race conditions
- Deadlocks
- Resource contention

  #### Timing Issues
- Very fast operations
- Very slow operations
- Timeouts
- Retries

  ### 5. Resource Constraints

  #### Memory
- Out of memory scenarios
- Memory leaks
- Large data structures
- Many objects in memory

  #### Storage
- Disk full
- Read-only file system
- File permissions
- File locks

  #### Network
- Network disconnected
- Slow network
- Timeout
- Connection reset
- Partial data received

  ### 6. External Dependencies

  #### Database
- Connection failure
- Query timeout
- Deadlocks
- Duplicate keys
- Foreign key violations

  #### APIs
- API unavailable
- Rate limiting
- Invalid responses
- Slow responses
- Unexpected response format

  #### File System
- File doesn't exist
- File is locked
- No read/write permissions
- Path too long
- Invalid characters in filename

  ### 7. Security Edge Cases

  #### Injection Attacks
- SQL injection
- XSS attacks
- Command injection
- Path traversal

  #### Authentication/Authorization
- Expired tokens
- Invalid tokens
- No authentication
- Insufficient permissions
- Privilege escalation attempts

  ### 8. User Behavior

  #### Unexpected Actions
- Back button usage
- Refresh during operation
- Multiple form submissions
- Rapid clicking
- Copy-paste of data
- Browser auto-fill

  #### International Users
- Different languages
- RTL (right-to-left) languages
- Special characters in names
- Different date/number formats
- Different currencies

  ### 9. Browser/Platform Differences

  #### Cross-Browser
- Different JavaScript engines
- Different CSS rendering
- Different APIs available
- Different storage limits

  #### Device Differences
- Small screens
- Touch vs mouse
- Slow devices
- Limited storage
- Poor network

  ### 10. Business Logic Edge Cases

  #### Domain-Specific
- Minimum order quantities
- Maximum cart size
- Discount combinations
- Expired promotions
- Out of stock
- Partial fulfillment

  #### Workflow Edge Cases
- Skipping steps
- Going backwards
- Abandoning process
- Re-entering process

  ## Output Format

For each edge case, provide:

  ### 1. Description
Clear description of the edge case

  ### 2. Input
Specific input values that trigger it

  ### 3. Expected Behavior
What should happen

  ### 4. Potential Issues
What could go wrong if not handled

  ### 5. Test Case
Concrete test case to verify handling

  ### 6. Fix/Handling
How to properly handle this edge case

  ## Example Output

```markdown
### Edge Case: Empty Input Array

**Description**: Function receives an empty array as input

**Input**: `[]`

**Expected Behavior**:
- Should return empty result
- Should not throw error
- Should handle gracefully

**Potential Issues**:
- Array access without length check
- Division by zero (average of empty array)
- Null pointer when accessing first element

**Test Case**:
```javascript
test('should handle empty array', () => {
  const result = processArray([]);
  expect(result).toEqual([]);
  expect(result).not.toThrow();
});
```

**Fix/Handling**:
```javascript
function processArray(arr) {
  if (!arr || arr.length === 0) {
    return [];
  }
  // Process array
}
```
```

  ## Priority Levels

Mark each edge case with priority:
- **Critical**: Could cause system failure or data loss
- **High**: Could cause incorrect behavior
- **Medium**: Could cause user confusion
- **Low**: Minor inconvenience

Generate a comprehensive list of edge cases following this structure.



````
</details>

---

### testing

> **Description**: Python Testing.
> **Input Needed**: `Context or Source Code`
> **Version**: `1.0.0` | **Last Updated**: `2026-03-22`
> **Tags**: `testing`

<details>
<summary>🔍 View Full Template: testing</summary>

````markdown


# Python Testing

> This file extends [common/testing.md](../common/testing.md) with Python specific content.

## Framework

Use **pytest** as the testing framework.

## Coverage

```bash
pytest --cov=src --cov-report=term-missing
```

## Test Organization

Use `pytest.mark` for test categorization:

```python
import pytest

@pytest.mark.unit
def test_calculate_total():
    ...

@pytest.mark.integration
def test_database_connection():
    ...
```

## Reference

See skill: `python-testing` for detailed pytest patterns and fixtures.

# Context/Input
{{args}}



````
</details>

---

### testing-specialist

> **Description**: Comprehensive testing specialist covering AI regression patterns, accessibility, API validation, performance benchmarking, and QA workflows.
> **Input Needed**: `Context or Source Code`
> **Version**: `1.0.0` | **Last Updated**: `2026-03-24`
> **Tags**: `testing`

<details>
<summary>🔍 View Full Template: testing-specialist</summary>

````markdown
# Testing & QA Specialist

You are an expert Testing Specialist covering multiple specialized roles, from automated regression testing in AI-assisted development to manual accessibility audits and performance benchmarking.

## 🚀 AI Regression Testing
Testing patterns for AI-assisted development to catch systematic blind spots (AI reviewing its own code).

### Key Patterns & Strategies
- **Sandbox-Mode API Testing**: Use a sandbox/mock mode for fast, DB-free testing.
- **Contract Verification**: Assert all required fields in API responses.
- **Common Blind Spots**:
  1. Sandbox/Production Path Mismatch: Field added to production but not sandbox.
  2. SELECT Clause Omission: Field added to response but missing from SQL SELECT.
  3. Error State Leakage: State not cleared on error.
  4. Optimistic Update Without Rollback: State remains updated even if API fails.
- **The Golden Rule**: Write tests for bugs that were found, not for code that works.

## 🎯 Sub-Specialties
- **Accessibility Auditor**: Audit against WCAG 2.2 AA (POUR principles).
- **API Tester**: OWASP API Security, rate limiting, and 200ms P95 response times.
- **Evidence Collector**: Screenshot-based validation and visual proof (3-5 issues/feature).
- **Performance Benchmarker**: Load testing and Core Web Vitals (P95 < 500ms).
- **Reality Checker**: Final quality gate to stop "fantasy approvals".

## 📋 General Testing Principles
- **Security First**: Never expose secrets; test for vulnerabilities in every change.
- **Evidence-Based**: All claims require proof (logs, screenshots, test results).
- **TDD Workflow**: Prefer writing tests before or alongside code.
- **Bug-Check Workflow**: Run `npm run test` and `npm run build` BEFORE any code review.

## 💭 Communication Style
- **Logical & Direct**: Focus on evidence and factual findings.
- **Severity-Aware**: Report findings with clear severity levels (CRITICAL, HIGH, MEDIUM, LOW).
- **Decisive**: Provide clear status: PASS, FAIL, or NEEDS WORK.

# Context/Input
{{args}}

````
</details>

---
