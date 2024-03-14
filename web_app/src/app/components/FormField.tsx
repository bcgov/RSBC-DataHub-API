import React from 'react';
import HelpIcon from '@mui/icons-material/Help';
import CloseIcon from '@mui/icons-material/Close';
import { Box, IconButton, Typography, Grid, Tooltip } from '@mui/material';

interface FormFieldProps {
    readonly id: string;
    readonly labelText?: string;
    readonly placeholder?: string;
    readonly helperText?: string;
    readonly tooltipTitle?: string;
    readonly tooltipContent?: React.ReactNode;
    readonly children: React.ReactNode;
    readonly error?: boolean;
    readonly errorText?: string;
}

const styles = {
    iconButton: {
        '&:hover': {
            backgroundColor: 'transparent',
        },
    },
    popoverContent: {
        padding: '1px',
        maxWidth: '1200px',
        marginTop: '-10px',
    },
};
export function FormField({
    id,
    labelText,
    placeholder,
    helperText,
    tooltipTitle,
    tooltipContent,
    children,
    error,
    errorText, }: FormFieldProps) {  
   
    const [openTooltip, setOpenTooltip] = React.useState(false);
    const handleTooltipOpen = () => setOpenTooltip(true);
    const handleTooltipClose = () => setOpenTooltip(false);
    return (
        <Box sx={{ display: 'block', alignItems: 'left', flexDirection: 'column', gap: 1, ml: '5px', width: 'auto', mb: '30px' }}>
            {labelText &&
                <Box sx={{ display: 'flex', alignItems: 'left', width: 'auto' }}>
                    <IconButton size="small" onClick={handleTooltipOpen}>
                        <HelpIcon fontSize="small" style={{ color: 'black', height: '16px', width: '16px' }} />
                    </IconButton>
                    <Typography variant='subtitle1' component="label" htmlFor={id + '-field'} sx={{ color: '#313132', fontSize: '16px', fontWeight: '700' }}>
                        {labelText}
                    </Typography>
                </Box>
            }
            <Box sx={{ display: 'inline-flex', alignItems: 'center', width: 'auto',  }}>
                <Tooltip
                    arrow
                    placement="right" 
                    componentsProps={{
                        tooltip: {
                            sx: {
                                bgcolor: "#E6E6E6"
                            }
                        },
                        arrow: {
                            sx: {
                                color: "#E6E6E6"
                            }
                        }
                    }} 
                                       
                    title={
                        <div style={{ color: 'black', width: 'auto', maxWidth: '400px', minWidth: '254px', boxShadow: '0px 2px 2px #00000029 !important', borderRadius: '6px', lineHeight: '20px', overflowWrap:'break-word'}}>
                        <Box sx={{ color: 'black', width:'auto',  padding: '8px 14px', margin:'0px', }} >
                            <Grid container spacing={2}>
                                <Grid item xs={11} sx={{ padding: "1px" }}>
                                    <Typography sx={{ fontWeight: 600 }}>{tooltipTitle}</Typography>
                                </Grid>
                                <Grid item xs={1} sx={{ padding: "1px" }}>
                                    <Box sx={{ display: 'flex', justifyContent: 'flex-end' }}>
                                        <IconButton aria-label="close" onClick={handleTooltipClose} size="small">
                                            <CloseIcon fontSize="small" />
                                        </IconButton>
                                    </Box>
                                </Grid>
                            </Grid>
                           
                        </Box>
                            <Box sx={{ color: 'black', width: 'auto', padding: '9px 14px', margin: '0px', }}>
                                <Typography sx={styles.popoverContent} >{tooltipContent}</Typography>
                            </Box>
                        </div>
                    }
                    open={openTooltip}
                    onClose={handleTooltipClose}
                    disableHoverListener
                    disableFocusListener
                    disableTouchListener
                >
                    <Box sx={{ display: 'table-cell', paddingLeft: '2px', paddingTop:'15px' }}>
                        {children}
                        {error &&
                            <Typography variant="caption" sx={{ color: '#D8292F', fontWeight: '700', padding: '4px 0px 2px 0px', ml: '4px', fontSize: '16px', display: 'block' }}>

                                {errorText}
                            </Typography>
                        }
                    </Box>
                </Tooltip>
            </Box>
            <Typography variant="caption" sx={{ mb: 1, color: '#767676', display: 'block', fontSize: '16px', mt: 0, paddingLeft: '10px', fontFamily: "'BC Sans', 'Noto Sans',  Arial, sans-serif" }}>
                {helperText}
            </Typography>
        </Box>
    );
}

