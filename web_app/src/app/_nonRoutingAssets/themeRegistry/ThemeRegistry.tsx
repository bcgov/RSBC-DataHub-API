'use client';
import * as React from 'react';
import { ThemeProvider } from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';
import NextAppDirEmotionCacheProvider from './EmotionCache';
import theme from './theme';
import { Global } from '@emotion/react';
import { globalStyles } from './globalStyles';

export default function ThemeRegistry({
    children,
  }: {
    children: React.ReactNode
  }) {
  return (
    <NextAppDirEmotionCacheProvider options={{ key: 'mui' }}>
      <ThemeProvider theme={theme}>
        {/* CssBaseline kickstart an elegant, consistent, and simple baseline to build upon. */}
        <CssBaseline />
        <Global styles={globalStyles(theme)} />
        {children}
      </ThemeProvider>
    </NextAppDirEmotionCacheProvider>
  );
}