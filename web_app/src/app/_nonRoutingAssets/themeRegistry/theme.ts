import { createTheme } from "@mui/material/styles";
import '@bcgov/bc-sans/css/BC_Sans.css';

// rem  16px base equivalent
// 1.375    20px
// 
// 1        16px


// Custom colors
const colors = {
    primary: '#003366',
    secondary: '#FCBA19',
    error: '#ff1744',
    warning: '#ff9800',
    info: '#fff',
    success: '#4caf50',
    background: {
        default: '#fff',
        paper: '#fff', //  '#f4f5fd',
    },
    text: {
        primary: '#333333',
        secondary: '#555555',
        disabled: '#a6a6a6',
    },
};

const typography = {
    fontFamily: 'BC Sans, Noto Sans, Arial, sans serif',
    h1: {
        fontSize: '1.375rem',
        fontWeight: 500,
    },
    h2: {
        fontSize: '1.125rem',
        fontWeight: 'bold',
    },
    h3: {
        fontSize: '1rem',
        fontWeight: 'bold',
    },
    // More typography settings
};

// Define custom breakpoints if needed
// const breakpoints = {
//     values: {
//         xs: 0,
//         sm: 600,
//         md: 960,
//         lg: 1280,
//         xl: 1920,
//     },
// };

// Overrides for Material-UI components
const components = {
    MuiButton: {
        styleOverrides: {
            root: {
                borderRadius: 4,
                // color: 'white',
                fontStyle: 'bold',
                // borderWidth: '2px',
                textTransform: 'none' as const,
                
                // fontSize: '1rem',
                // fontWeigh: 'bold',
                borderWidth: 2,
                // borderStyle: 'solid',
                '&:hover': {
                    borderWidth: 2,
                },

                // Other button styles
            },
        },
    },
    // Overrides for other components
};

const theme = createTheme({
    palette: {
        primary: { main: colors.primary},
        secondary: { main: colors.secondary },
        error: { main: colors.error },
        warning: { main: colors.warning },
        info: { main: colors.info },
        success: { main: colors.success },
        background: {
            default: colors.background.default,
            paper: colors.background.paper,
        },
        text: {
            primary: colors.text.primary,
            secondary: colors.text.secondary,
            disabled: colors.text.disabled,
        },
    },
    typography,
    components: components,
    // breakpoints,
    // Other global theme overrides or additions
});

export default theme;