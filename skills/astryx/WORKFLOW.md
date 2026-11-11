# Astryx Design System Workflow

Astryx is Meta's design system and UI library for React 19 applications, built with atomic StyleX styling, accessible primitives, and modular themes.

## 1. Quick Start and Installation

Astryx requires React 19 or later. Install the core package, StyleX peer dependency, neutral theme, and the CLI:

```bash
npm install @astryxdesign/core @stylexjs/stylex @astryxdesign/theme-neutral @astryxdesign/cli
```

Initialize agent documentation and project configuration non interactively:

```bash
npx @astryxdesign/cli init --all
```

Install the CLI globally for system wide access across all coding agents:

```bash
npm install -g @astryxdesign/cli
```

## 2. Base Styles and Theming

Import the reset and base styles in your global CSS. Astryx styles use cascade layers: `@layer reset` and `@layer astryx-base`:

```css
@import '@astryxdesign/core/reset.css';
@import '@astryxdesign/core/astryx.css';
```

Discover and add themes using the CLI:

```bash
astryx theme list
astryx theme add neutral
```

Available official themes:
* `neutral`: muted and minimal starting point
* `butter`: warm golden tones with blue accents
* `chocolate`: rich chocolate and caramel tones
* `gothic`: dark only theme with ink and noir influences
* `matcha`: earthy greens and botanical tones
* `stone`: warm neutrals inspired by sandstone
* `y2k`: playful early 2000s pop aesthetic

Wrap your application root with the selected theme:

```tsx
import { Theme } from '@astryxdesign/core/theme';
import { themes, defaultThemeSlug } from './astryx-themes';

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <Theme theme={themes[defaultThemeSlug]}>
      {children}
    </Theme>
  );
}
```

## 3. Component Architecture and StyleX

Import each component directly from its individual entry to minimize bundle sizes:

```tsx
import { Button } from '@astryxdesign/core/Button';
import { VStack } from '@astryxdesign/core/VStack';
import { Text } from '@astryxdesign/core/Text';
import * as stylex from '@stylexjs/stylex';

const styles = stylex.create({
  container: {
    padding: 16,
    borderRadius: 8
  },
  action: {
    alignSelf: 'flex-start',
    marginTop: 8
  }
});

export function WelcomeCard() {
  return (
    <VStack gap={3} xstyle={styles.container}>
      <Text variant="title">Welcome to Astryx</Text>
      <Button label="Get Started" onClick={() => {}} xstyle={styles.action} />
    </VStack>
  );
}
```

## 4. Page Building Workflow

Build pages by scaffolding from vetted templates rather than starting from blank files:

1. Search or evaluate template matches:
   ```bash
   astryx build "<your page idea>"
   ```
2. Scaffold the target template to your designated path:
   ```bash
   astryx template <name> <target-path>
   ```
3. Discover specific blocks or component props:
   ```bash
   astryx template <BlockName>
   astryx component <ComponentName>
   ```
4. Verify design tokens and styling:
   ```bash
   astryx docs tokens
   astryx docs color
   astryx docs spacing
   ```

## 5. Verification Gate

Before completing any task:
1. Re inspect every generated file. Replace unstyled div or span elements with Astryx primitives like Box, VStack, HStack, or Text.
2. Replace hardcoded hex colors or arbitrary pixel margins with Astryx design tokens.
3. Verify that the application builds cleanly with `npm run build` without StyleX compiler errors or CSS layer conflicts.
