/**
 * Chart.js Color Palettes
 * Theme-aware colors for dark and light modes.
 * 
 * Color semantics:
 * - primary/secondary: Main data series (cyan/teal)
 * - tertiary: Warning/temperature (red)
 * - quaternary: Success/positive (green)
 * - quinary: Alert/warning (amber)
 * - senary: Supplementary (purple)
 */

export const chartColors = {
    dark: {
        // Data series colors
        primary: 'rgba(102, 252, 241, 0.7)',      // Neon Cyan
        primaryBorder: '#66fcf1',
        secondary: 'rgba(69, 162, 158, 0.7)',     // Teal  
        secondaryBorder: '#45a29e',
        tertiary: 'rgba(252, 32, 68, 0.7)',       // Neon Red
        tertiaryBorder: '#fc2044',
        quaternary: 'rgba(32, 252, 143, 0.7)',    // Neon Green
        quaternaryBorder: '#20fc8f',
        quinary: 'rgba(224, 168, 0, 0.7)',        // Amber
        quinaryBorder: '#e0a800',
        senary: 'rgba(168, 85, 247, 0.7)',        // Purple
        senaryBorder: '#a855f7',
        // UI colors
        grid: '#30363d',
        text: '#8b949e',
        legendText: '#e6edf3',
        tooltipBg: 'rgba(11, 12, 16, 0.95)',
        tooltipTitle: '#66fcf1',
        tooltipBody: '#c5c6c7',
        tooltipBorder: '#45a29e',
    },
    light: {
        // Data series colors (more saturated for light bg)
        primary: 'rgba(6, 182, 212, 0.75)',       // Cyan-500
        primaryBorder: '#0891b2',
        secondary: 'rgba(20, 184, 166, 0.75)',    // Teal-500
        secondaryBorder: '#0d9488',
        tertiary: 'rgba(239, 68, 68, 0.75)',      // Red-500
        tertiaryBorder: '#dc2626',
        quaternary: 'rgba(34, 197, 94, 0.75)',    // Green-500
        quaternaryBorder: '#16a34a',
        quinary: 'rgba(245, 158, 11, 0.75)',      // Amber-500
        quinaryBorder: '#d97706',
        senary: 'rgba(139, 92, 246, 0.75)',       // Violet-500
        senaryBorder: '#7c3aed',
        // UI colors
        grid: '#e2e8f0',          // Slate-200
        text: '#64748b',          // Slate-500
        legendText: '#0f172a',    // Slate-900
        tooltipBg: 'rgba(255, 255, 255, 0.98)',
        tooltipTitle: '#0f172a',
        tooltipBody: '#475569',
        tooltipBorder: '#e2e8f0',
    }
};

/**
 * Returns an array of chart colors for pie/doughnut charts.
 * @param {Object} colors - The color palette (chartColors.dark or chartColors.light)
 */
export const getChartColorArray = (colors) => [
    colors.primary,
    colors.secondary,
    colors.quaternary,
    colors.tertiary,
    colors.quinary,
    colors.senary,
];

/**
 * Returns border colors matching getChartColorArray order.
 */
export const getChartBorderArray = (colors) => [
    colors.primaryBorder,
    colors.secondaryBorder,
    colors.quaternaryBorder,
    colors.tertiaryBorder,
    colors.quinaryBorder,
    colors.senaryBorder,
];

/**
 * Zoom and Pan plugin configuration.
 * - Scroll wheel to zoom
 * - Ctrl+drag to pan
 */
export const zoomOptions = {
    pan: {
        enabled: true,
        mode: 'xy',
        modifierKey: 'ctrl',
    },
    zoom: {
        wheel: { enabled: true },
        pinch: { enabled: true },
        mode: 'xy',
        onZoomComplete: ({ chart }) => chart.update('none'),
    },
};

/**
 * Creates a themed tooltip configuration.
 * @param {Object} colors - The color palette
 */
export const createTooltipConfig = (colors) => ({
    enabled: true,
    backgroundColor: colors.tooltipBg,
    titleColor: colors.tooltipTitle,
    bodyColor: colors.tooltipBody,
    borderColor: colors.tooltipBorder,
    borderWidth: 1,
    padding: 12,
    cornerRadius: 4,
    titleFont: { size: 14, weight: 'bold', family: "'JetBrains Mono', monospace" },
    bodyFont: { size: 12, family: "'Inter', sans-serif" },
    displayColors: true,
    boxPadding: 4,
});
