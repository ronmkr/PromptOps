import { test, expect } from '@playwright/test';

test.describe('PromptBook Hydration', () => {
  test('should search and hydrate a prompt', async ({ page }) => {
    // Navigate to the base URL
    await page.goto('./');
    
    // 1. Wait for loading container to be gone
    const loadingContainer = page.locator('.loading-container');
    
    // If it's an error state, fail with the error message
    const errorState = page.locator('.loading-container.error p');
    if (await errorState.isVisible()) {
      const msg = await errorState.textContent();
      throw new Error(`App entered error state: ${msg}`);
    }

    await expect(loadingContainer).not.toBeVisible({ timeout: 15000 });

    // 2. Now check title (Logo text)
    await expect(page.locator('.logo h1')).toHaveText('PromptBook');

    // 3. Search for a prompt
    const searchInput = page.locator('input[type="text"]');
    await searchInput.fill('refactor-agent');

    // 4. Click on the prompt card
    const promptCard = page.locator('.prompt-card h3', { hasText: 'refactor-agent' });
    await promptCard.click();

    // 5. Verify modal is open
    await expect(page.locator('.modal-content h2')).toHaveText('refactor-agent');

    // 6. Enter arguments
    const argsInput = page.locator('.args-input');
    const testArg = 'const x = 1;';
    await argsInput.fill(testArg);

    // 7. Verify hydration in preview
    const preview = page.locator('.prompt-preview pre');
    await expect(preview).toContainText(testArg);

    // 8. Verify "Copy" button works (status change)
    const copyBtn = page.locator('.copy-full-btn');
    await copyBtn.click();
    
    // Check if the icon changed to "Check" (lucide-react icon check)
    await expect(page.locator('.copy-full-btn svg.lucide-check')).toBeVisible();
  });
});
