import { test, expect } from '@playwright/test';

test.describe('PromptBook Hydration', () => {
  test('should search and hydrate a prompt', async ({ page }) => {
    await page.goto('./');
    
    // Check title
    await expect(page.locator('h1')).toHaveText('PromptBook');

    // Search for a prompt
    const searchInput = page.locator('input[type="text"]');
    await searchInput.fill('refactor-agent');

    // Click on the prompt card
    const promptCard = page.locator('.prompt-card h3', { hasText: 'refactor-agent' });
    await promptCard.click();

    // Verify modal is open
    await expect(page.locator('.modal-content h2')).toHaveText('refactor-agent');

    // Enter arguments
    const argsInput = page.locator('.args-input');
    const testArg = 'const x = 1;';
    await argsInput.fill(testArg);

    // Verify hydration in preview
    const preview = page.locator('.prompt-preview pre');
    await expect(preview).toContainText(testArg);

    // Verify "Copy" button works (status change)
    const copyBtn = page.locator('.copy-full-btn');
    await copyBtn.click();
    
    // Check if the icon changed to "Check" (lucide-react icon check)
    // In our App.tsx, we show <Check /> when copied is true
    await expect(page.locator('.copy-full-btn svg.lucide-check')).toBeVisible();
  });
});
